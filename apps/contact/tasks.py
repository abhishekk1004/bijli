from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_contact_notification(contact_id: str) -> None:
    from apps.contact.models import Contact

    recipient = settings.ADMIN_NOTIFICATION_EMAIL
    contact = Contact.objects.filter(pk=contact_id).first()
    if not recipient or contact is None:
        return

    send_mail(
        subject=f'New inquiry: {contact.subject}',
        message=(
            f'From: {contact.name} <{contact.email}>\n'
            f'Phone: {contact.phone}\n'
            f'Service interest: {contact.service_interest or "-"}\n'
            f'Product interest: {contact.product_interest or "-"}\n\n'
            f'{contact.message}'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient],
    )
