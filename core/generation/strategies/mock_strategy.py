from .base import SongGeneratorStrategy, GenerationRequest, GenerationResult

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
        return GenerationResult(
            success=True,
            completed=True,
            task_id=self.TASK_ID,
            audio_url=MOCK_AUDIO_URL,
            lyrics=request.lyrics,  # pass through user's input; None if they left it blank
        )

    def poll(self, task_id: str) -> GenerationResult:
        # Mock is always synchronous — poll is a no-op.
        return GenerationResult(
            success=True,
            completed=True,
            task_id=task_id,
            audio_url='',
            lyrics='Placeholder lyrics.',
        )
