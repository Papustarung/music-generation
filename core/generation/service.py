import logging
import time
import uuid
import urllib.request
from pathlib import Path

from django.conf import settings

from core.generation.factory import SongGeneratorFactory
from core.generation.strategies.base import GenerationRequest, GenerationResult

logger = logging.getLogger(__name__)

POLL_INTERVAL_SECONDS = 5
MAX_POLL_ATTEMPTS = 120  # 5s × 120 = 10 minutes max (FR-09 timeout)


class GenerationService:
    """
    GRASP Controller — owns the full GenerationJob lifecycle.
    Views are thin HTTP adapters; all business logic lives here.

    Usage:
        service = GenerationService()
        service.run(job)   # called from a background thread
    """

    def __init__(self):
        self.strategy = SongGeneratorFactory.get_strategy()

    def run(self, job) -> None:
        """
        Full blocking execution intended for a background thread (FR-09).
        Transitions: QUEUED → GENERATING → SAVING → COMPLETED | FAILED
        """
        # ── 1. Mark as GENERATING ──────────────────────────────────────────
        self._set_status(job, 'GENERATING')

        request = GenerationRequest(
            title=job.title,
            story=job.story,
            genre=job.genre,
            vocal_style=job.vocal_style,
            occasion=job.occasion,
            lyrics=job.lyrics or None,
            job_id=job.pk,
        )

        # ── 2. Start generation ────────────────────────────────────────────
        try:
            result = self.strategy.generate(request)
        except Exception:
            logger.exception("Unexpected error in strategy.generate() for job %s", job.pk)
            self._set_status(job, 'FAILED')
            return

        if not result.success:
            logger.warning("Generation failed for job %s: %s", job.pk, result.error)
            self._set_status(job, 'FAILED')
            return

        # Persist task_id so it survives across requests (Suno async)
        if result.task_id:
            job.task_id = result.task_id
            job.save(update_fields=['task_id'])

        # ── 3. Poll if async (Suno returns completed=False) ───────────────
        if not result.completed:
            result = self._poll_until_done(job, result.task_id)
            # Re-fetch from DB — webhook may have completed the job while polling
            job.refresh_from_db()
            if job.status == 'COMPLETED':
                logger.info("Job %s already completed by webhook, skipping polling save", job.pk)
                return
            if result is None or not result.success:
                self._set_status(job, 'FAILED')
                return

        # ── 4. Save generated song (SAVING state) ─────────────────────────
        job.refresh_from_db()
        if job.status == 'COMPLETED':
            logger.info("Job %s already completed by webhook, skipping polling save", job.pk)
            return

        self._set_status(job, 'SAVING')

        try:
            self._save_song(job, result)
        except Exception:
            logger.exception("Error saving generated song for job %s", job.pk)
            self._set_status(job, 'FAILED')
            return

        # ── 5. Done ────────────────────────────────────────────────────────
        self._set_status(job, 'COMPLETED')
        job.save(update_fields=['song'])

    # ── Private helpers ────────────────────────────────────────────────────

    def _set_status(self, job, status: str) -> None:
        job.status = status
        job.save(update_fields=['status'])

    def _poll_until_done(self, job, task_id: str) -> GenerationResult | None:
        for attempt in range(1, MAX_POLL_ATTEMPTS + 1):
            time.sleep(POLL_INTERVAL_SECONDS)
            try:
                result = self.strategy.poll(task_id)
            except Exception:
                logger.exception("Error polling strategy for job %s (attempt %s)", job.pk, attempt)
                return None

            if not result.success:
                logger.warning(
                    "Poll returned failure for job %s: %s", job.pk, result.error
                )
                return result

            if result.completed:
                return result

        logger.warning("Generation timed out after %s attempts for job %s", MAX_POLL_ATTEMPTS, job.pk)
        return None

    def _save_song(self, job, result: GenerationResult) -> None:
        from core.models.entities.song import Song

        audio_location = self._download_audio(result.audio_url)

        library = job.creator.library
        song = Song.objects.create(
            library=library,
            title=job.title,
            story=job.story,
            genre=job.genre,
            vocal_style=job.vocal_style,
            occasion=job.occasion,
            lyrics=result.lyrics or job.lyrics or '',
            audio_location=audio_location,
        )
        job.song = song

    def _download_audio(self, url: str | None) -> str:
        """
        Download audio from a remote URL into MEDIA_ROOT/songs/ and return
        the relative URL path (e.g. /media/songs/<uuid>.mp3).
        Falls back to the original URL if download fails or URL is already local.
        """
        if not url or url.startswith('/'):
            return url or ''

        try:
            songs_dir = Path(settings.MEDIA_ROOT) / 'songs'
            songs_dir.mkdir(parents=True, exist_ok=True)

            filename = f"{uuid.uuid4().hex}.mp3"
            dest = songs_dir / filename

            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=60) as response:
                dest.write_bytes(response.read())

            return f"{settings.MEDIA_URL}songs/{filename}"
        except Exception:
            logger.warning("Could not download audio from %s, storing URL directly", url)
            return url
