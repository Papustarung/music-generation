from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class GenerationRequest:
    title: str
    story: str
    genre: str
    vocal_style: str
    occasion: str
    lyrics: Optional[str] = None
    job_id: Optional[int] = None


@dataclass
class GenerationResult:
    success: bool
    completed: bool = False
    task_id: Optional[str] = None
    audio_url: Optional[str] = None
    lyrics: Optional[str] = None
    error: Optional[str] = None


class SongGeneratorStrategy(ABC):
    @abstractmethod
    def generate(self, request: GenerationRequest) -> GenerationResult:
        """
        Start song generation.
        - Sync strategies (Mock): return completed=True immediately.
        - Async strategies (Suno): return completed=False with a task_id for polling.
        """
        ...

    @abstractmethod
    def poll(self, task_id: str) -> GenerationResult:
        """
        Check the status of an in-progress generation.
        Returns GenerationResult with completed=True when done, or completed=False
        if still in progress.
        """
        ...
