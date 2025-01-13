from datetime import timezone

from django.core.mail import send_mail
from django.core.management import BaseCommand

from config.settings import EMAIL_HOST_USER
from mailing_service.models import AttemptMailing, Mailing


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Функция запуска рассылки по требованию"""

        mailings = Mailing.objects.filter(status__in=Mailing.LAUNCHED)
        for mailing in mailings:
            mailing.status = Mailing.LAUNCHED
            mailing.save()

            for recipient in mailing.client.all():
                try:
                    mailing.status = Mailing.LAUNCHED
                    send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.content,
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[recipient.mail],
                        fail_silently=False,
                    )
                    AttemptMailing.objects.create(
                        date_attempt=timezone.now(),
                        status=AttemptMailing.STATUS_OK,
                        server_response="Email отправлен",
                        mailing=mailing,
                    )
                except Exception as e:
                    print(f"Ошибка при отправке письма для {recipient.mail}: {str(e)}")
                    AttemptMailing.objects.create(
                        date_attempt=timezone.now(),
                        status=AttemptMailing.STATUS_NOK,
                        server_response=str(e),
                        mailing=mailing,
                    )
            if mailing.end_sending and mailing.end_sending <= timezone.now():

                mailing.status = Mailing.COMPLETED
            mailing.save()
        self.stdout.write(self.style.SUCCESS("Рассылка завершена."))
