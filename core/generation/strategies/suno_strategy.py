import requests as http_requests
from django.conf import settings

from .base import SongGeneratorStrategy, GenerationRequest, GenerationResult

GENERATE_URL = 'https://api.sunoapi.org/api/v1/generate'
RECORD_URL = 'https://api.sunoapi.org/api/v1/generate/record-info'

COMPLETE_STATUSES = {'SUCCESS', 'FIRST_SUCCESS'}
PENDING_STATUSES = {'PENDING', 'TEXT_SUCCESS', 'GENERATING'}
FAILED_STATUSES = {'FAILED', 'ERROR'}


class SunoSongGeneratorStrategy(SongGeneratorStrategy):
    """
    Strategy B — Suno API generator.
    Calls https://api.sunoapi.org to create a generation task, then polls
    the record-info endpoint until the task completes.
    Requires SUNO_API_KEY in settings / .env.
    """

    def _headers(self) -> dict:
        return {'Authorization': f'Bearer {settings.SUNO_API_KEY}'}

    def generate(self, request: GenerationRequest) -> GenerationResult:
        """
        POST /api/v1/generate — start generation task.
        Returns GenerationResult with task_id and completed=False (async).
        """
        callback_url = getattr(settings, 'SUNO_CALLBACK_URL', '')
        if callback_url and request.job_id:
            sep = '&' if '?' in callback_url else '?'
            callback_url = f'{callback_url}{sep}job={request.job_id}'
        vocal = request.vocal_style.upper()
        is_instrumental = vocal == 'INSTRUMENTAL'
        genre = request.genre.lower()

        # Build style tag — duet needs explicit descriptors, not just the word "duet"
        if is_instrumental:
            style_tag = genre
        elif vocal == 'DUET':
            style_tag = (
                f'{genre}, male and female duet, alternating verses, harmonized chorus, '
                f'both male and female vocals, male baritone and female soprano'
            )
        else:
            style_tag = f'{genre} {request.vocal_style.lower()}'

        # Build prompt — prepend genre so Suno doesn't infer style from story content
        prompt = f"[{request.genre.capitalize()} style] {request.story}"

        # Duet: global pre-song declaration (guide's gold standard technique)
        if vocal == 'DUET':
            prompt = (
                f"[This song is a male-female duet, one male vocalist and one female vocalist] ===\n"
                f"{prompt}"
            )
        elif vocal == 'RAP':
            prompt = f"[rap] {prompt}"

        if request.lyrics:
            prompt += f"\n\nLyric ideas: {request.lyrics}"

        # vocalGender API field only supports m / f
        VOCAL_GENDER_MAP = {'MALE': 'm', 'FEMALE': 'f'}
        vocal_gender = VOCAL_GENDER_MAP.get(vocal)

        payload = {
            'title': request.title,
            'prompt': prompt,
            'style': style_tag,
            'customMode': False,
            'instrumental': is_instrumental,
            'callBackUrl': callback_url,
            'model': getattr(settings, 'SUNO_MODEL', 'V4_5'),
        }
        if vocal_gender:
            payload['vocalGender'] = vocal_gender

        try:
            resp = http_requests.post(
                GENERATE_URL,
                json=payload,
                headers=self._headers(),
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
        except http_requests.RequestException as exc:
            return GenerationResult(success=False, completed=False, error=str(exc))

        if not isinstance(data, dict):
            return GenerationResult(
                success=False,
                completed=False,
                error=f'Unexpected Suno response body: {resp.text[:200]}',
            )

        # Extract taskId — SunoAPI wraps response in a 'data' key
        # Use `or {}` so an explicit null data field is treated as missing
        task_id = (
            (data.get('data') or {}).get('taskId')
            or data.get('taskId')
        )
        if not task_id:
            return GenerationResult(
                success=False,
                completed=False,
                error=f'No taskId in Suno response: {data}',
            )

        return GenerationResult(success=True, completed=False, task_id=task_id)

    def poll(self, task_id: str) -> GenerationResult:
        """
        GET /api/v1/generate/record-info?taskId=... — check generation status.
        Maps Suno statuses:
          PENDING / TEXT_SUCCESS / GENERATING → in-progress (completed=False)
          FIRST_SUCCESS / SUCCESS             → done (completed=True)
          FAILED / ERROR                      → failure
        """
        try:
            resp = http_requests.get(
                RECORD_URL,
                params={'taskId': task_id},
                headers=self._headers(),
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
        except http_requests.RequestException as exc:
            return GenerationResult(
                success=False, completed=False, task_id=task_id, error=str(exc)
            )

        if not isinstance(data, dict):
            return GenerationResult(
                success=False,
                completed=False,
                task_id=task_id,
                error=f'Unexpected Suno poll response body: {resp.text[:200]}',
            )

        record = data.get('data') or {}
        status = record.get('status', '').upper()
        clips = record.get('clips', {})

        if status in FAILED_STATUSES:
            return GenerationResult(
                success=False,
                completed=False,
                task_id=task_id,
                error=f'Suno generation failed with status: {status}',
            )

        if status in COMPLETE_STATUSES:
            first_clip: dict = (
                next(iter(clips.values()), {})
                if isinstance(clips, dict)
                else (clips[0] if clips else {})
            )
            audio_url = first_clip.get('audio_url', '')
            # Audio not ready yet despite complete status — keep polling
            if not audio_url:
                return GenerationResult(success=True, completed=False, task_id=task_id)
            return GenerationResult(
                success=True,
                completed=True,
                task_id=task_id,
                audio_url=audio_url,
                lyrics=first_clip.get('lyric', '') or first_clip.get('prompt', ''),
            )

        # Still pending / generating
        return GenerationResult(success=True, completed=False, task_id=task_id)
