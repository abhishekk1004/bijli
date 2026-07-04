import logging

from django.db import transaction

from apps.contact.tasks import send_contact_notification

logger = logging.getLogger(__name__)


def notify_new_contact(contact) -> None:
    """Queue the admin notification after commit; a dead broker must never fail the submission."""
    def enqueue():
        try:
            send_contact_notification.delay(str(contact.pk))
        except Exception:
            logger.exception('Failed to queue contact notification for %s', contact.pk)

    transaction.on_commit(enqueue)
