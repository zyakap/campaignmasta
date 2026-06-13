import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from campaigns.models import Message
from campaigns.services import dispatch_message

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Send all scheduled messages whose send time has passed"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="List messages that would be sent without sending them",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        now = timezone.now()
        pending = Message.objects.filter(
            status="SCHEDULED",
            scheduled_send_date__lte=now,
        ).select_related("candidate")

        if not pending.exists():
            self.stdout.write("No scheduled messages due.")
            return

        self.stdout.write(f"Found {pending.count()} scheduled message(s) due.")

        sent = 0
        failed = 0
        for message in pending:
            if dry_run:
                self.stdout.write(f"  [DRY RUN] Would send '{message.subject}' (candidate: {message.candidate.name})")
                continue
            try:
                count = dispatch_message(message)
                self.stdout.write(self.style.SUCCESS(f"  Sent '{message.subject}' to {count} recipients"))
                logger.info("Scheduled message sent: id=%s subject=%s recipients=%s", message.id, message.subject, count)
                sent += 1
            except ValueError as exc:
                self.stderr.write(f"  Insufficient credit for '{message.subject}': {exc}")
                logger.warning("Scheduled message blocked (no credit): id=%s error=%s", message.id, exc)
                failed += 1
            except Exception as exc:
                self.stderr.write(f"  Failed '{message.subject}': {exc}")
                logger.exception("Scheduled message error: id=%s", message.id)
                failed += 1

        if not dry_run:
            self.stdout.write(self.style.SUCCESS(f"Done: {sent} sent, {failed} failed"))
