from django.conf import settings

from .strategies.base import SongGeneratorStrategy
from .strategies.mock_strategy import MockSongGeneratorStrategy
from .strategies.suno_strategy import SunoSongGeneratorStrategy


class SongGeneratorFactory:
    """
    GRASP Creator — centralised strategy selection.
    Reads GENERATOR_STRATEGY from settings (sourced from .env).
    Valid values: 'mock' | 'suno'
    """

    _registry: dict[str, type[SongGeneratorStrategy]] = {
        'mock': MockSongGeneratorStrategy,
        'suno': SunoSongGeneratorStrategy,
    }

    @classmethod
    def get_strategy(cls) -> SongGeneratorStrategy:
        name = getattr(settings, 'GENERATOR_STRATEGY', 'mock').lower().strip()
        strategy_class = cls._registry.get(name)
        if strategy_class is None:
            raise ValueError(
                f"Unknown GENERATOR_STRATEGY '{name}'. "
                f"Valid options: {list(cls._registry.keys())}"
            )
        return strategy_class()
