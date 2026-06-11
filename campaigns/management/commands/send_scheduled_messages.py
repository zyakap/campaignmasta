from django.core.management.base import BaseCommand
from django.utils import timezone

from campaigns.models import Message
from campaigns.services import dispatch_message


class Command(BaseCommand):
    help = "Send all scheduled messages whose send time has passed"

    def handle(self, *args, **options):
        now = timezone.now()
        pending = Message.objects.filter(
            status="SCHEDULED",
            scheduled_send_date__lte=now,
        ).select_related("candidate")

        if not pending.exists():
            self.stdout.write("No scheduled messages due.")
            return

        sent = 0
        failed = 0
        for message in pending:
            try:
                count = dispatch_message(message)
                self.stdout.write(f"  Sent '{message.subject}' to {count} recipients")
                sent += 1
            except Exception as exc:
                self.stderr.write(f"  Failed '{message.subject}': {exc}")
                failed += 1

        self.stdout.write(self.style.SUCCESS(f"Done: {sent} sent, {failed} failed"))
