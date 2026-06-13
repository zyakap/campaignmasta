import logging

from django.core.management.base import BaseCommand

from campaigns.models import Candidate
from campaigns.services import check_and_escalate_coordinator_alerts

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Check all active candidates for quiet coordinators and create escalation alerts"

    def handle(self, *args, **options):
        candidates = Candidate.objects.filter(status__in=["TRIAL", "ACTIVE"])
        total = 0
        for candidate in candidates:
            try:
                check_and_escalate_coordinator_alerts(candidate)
                total += 1
            except Exception as exc:
                logger.exception("Error checking alerts for candidate %s: %s", candidate.id, exc)
                self.stderr.write(f"Error for {candidate.name}: {exc}")
        self.stdout.write(self.style.SUCCESS(f"Checked {total} candidates for coordinator alerts."))
