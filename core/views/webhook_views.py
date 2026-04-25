import json
import logging
import threading

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)

# Suno callback payload structure:
# {
#   "code": 200,
#   "data": {
#     "callbackType": "text" | "first" | "complete",
#     "data": [{ "id": "...", "audio_url": "...", "prompt": "...", ... }]
#   }
# }


@csrf_exempt
@require_POST
def suno_webhook(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        logger.warning("Suno webhook: invalid JSON body")
        return HttpResponse(status=400)

    inner = data.get('data') or {}
    callback_type = inner.get('callbackType', '')
    clips = inner.get('data', [])

    logger.info("Suno webhook: callbackType=%s job=%s", callback_type, request.GET.get('job'))

    # Only act when audio is ready
    if callback_type not in ('first', 'complete'):
        return HttpResponse(status=200)

    job_id = request.GET.get('job')
    if not job_id:
        logger.warning("Suno webhook: missing ?job= query param")
        return HttpResponse(status=200)

    first_clip = clips[0] if isinstance(clips, list) and clips else {}
    audio_url = first_clip.get('audio_url', '')
    lyrics = first_clip.get('prompt', '') or first_clip.get('lyric', '')

    logger.info("Suno webhook: job=%s audio_url=%s", job_id, audio_url[:80] if audio_url else '(empty)')

    if not audio_url:
        return HttpResponse(status=200)

    thread = threading.Thread(
        target=_handle_webhook_completion,
        args=(job_id, audio_url, lyrics),
        daemon=False,
    )
    thread.start()

    return HttpResponse(status=200)


def _handle_webhook_completion(job_id: str, audio_url: str, lyrics: str) -> None:
    from django.db import connection
    from core.models import GenerationJob
    from core.generation.service import GenerationService
    from core.generation.strategies.base import GenerationResult

    try:
        job = GenerationJob.objects.filter(pk=job_id).first()
        if not job:
            logger.warning("Suno webhook: job %s not found", job_id)
            return

        # Job already completed by polling but with no audio — patch the song
        if job.status == 'COMPLETED':
            if job.song and not job.song.audio_location:
                service = GenerationService()
                job.song.audio_location = service._download_audio(audio_url)
                job.song.save(update_fields=['audio_location'])
                logger.info("Suno webhook: patched audio for job %s song %s", job_id, job.song.pk)
            return

        result = GenerationResult(
            success=True,
            completed=True,
            audio_url=audio_url,
            lyrics=lyrics,
        )

        from core.notifications import notify
        from core.models.entities.notification import Notification

        service = GenerationService()
        job.status = 'SAVING'
        job.save(update_fields=['status'])
        service._save_song(job, result)
        job.status = 'COMPLETED'
        job.save(update_fields=['status', 'song'])
        notify(job.creator, f'"{job.title}" has been generated and saved to your library.', Notification.Level.SUCCESS)
        logger.info("Suno webhook: job %s completed successfully", job_id)
    except Exception:
        logger.exception("Error handling Suno webhook completion for job %s", job_id)
        from core.models import GenerationJob, Notification
        job_qs = GenerationJob.objects.filter(pk=job_id)
        job_qs.update(status='FAILED')
        failed_job = job_qs.select_related('creator').first()
        if failed_job:
            from core.notifications import notify
            notify(failed_job.creator, f'"{failed_job.title}" could not be generated. Please try again.', Notification.Level.ERROR)
    finally:
        connection.close()
