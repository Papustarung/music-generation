from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from core.models.entities.creator import Creator

@dataclass
class AuthResult:
	success: bool
	creator: Optional[Creator] = None
	error: Optional[str] = None

class AuthStrategy(ABC):
	@abstractmethod
	def authenticate(self, **credentials) -> AuthResult:
		...

	@abstractmethod
	def register(self, **data) -> AuthResult:
		...