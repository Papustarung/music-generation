import logging
from .models.entities.notification import Notification

logger = logging.getLogger(__name__)


def notify(creator, message: str, level: str = Notification.Level.INFO) -> None:
    try:
        Notification.objects.create(creator=creator, message=message, level=level)
    except Exception:
        logger.exception("Failed to create notification for creator %s", creator.pk)
