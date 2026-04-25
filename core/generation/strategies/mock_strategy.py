import logging

from .base import SongGeneratorStrategy, GenerationRequest, GenerationResult

logger = logging.getLogger(__name__)

# Static path served by Django's staticfiles at /static/core/audio/mock_song.mp3
MOCK_AUDIO_URL = '/static/core/audio/mock_song.mp3'


class MockSongGeneratorStrategy(SongGeneratorStrategy):
    """
    Strategy A — Mock generator.
    No network calls; returns predictable output immediately.
    Use for development and testing (GENERATOR_STRATEGY=mock).
    """

    TASK_ID = 'mock-task-001'

    def generate(self, request: GenerationRequest) -> GenerationResult:
        logger.info(
            "Mock generate: title='%s' genre=%s vocal=%s occasion=%s",
            request.title, request.genre, request.vocal_style, request.occasion,
        )
        result = GenerationResult(
            success=True,
            completed=True,
            task_id=self.TASK_ID,
            audio_url=MOCK_AUDIO_URL,
            lyrics=request.lyrics,
        )
        logger.info("Mock generate: returning taskId=%s audio_url=%s", result.task_id, result.audio_url)
        return result

    def poll(self, task_id: str) -> GenerationResult:
        # Mock is always synchronous — poll is never reached in normal flow.
        logger.info("Mock poll: taskId=%s (no-op)", task_id)
        return GenerationResult(
            success=True,
            completed=True,
            task_id=task_id,
            audio_url=MOCK_AUDIO_URL,
            lyrics='',
        )
