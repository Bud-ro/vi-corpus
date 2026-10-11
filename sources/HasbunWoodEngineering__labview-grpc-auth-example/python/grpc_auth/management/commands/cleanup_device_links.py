from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from grpc_auth.models import AccessToken, DeviceLinkSession


class Command(BaseCommand):
    help = "Delete expired or used device link sessions."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show how many sessions would be deleted without deleting them.",
        )
        parser.add_argument(
            "--keep-days",
            type=int,
            default=10,
            help="Keep revoked tokens newer than this many days (default: 10).",
        )

    def handle(self, *args, **options):
        now = timezone.now()
        sessions_qs = DeviceLinkSession.objects.filter(
            Q(used=True) | Q(expires_at__lt=now)
        )
        keep_days = max(0, int(options["keep_days"]))
        cutoff = now - timezone.timedelta(days=keep_days)
        tokens_qs = AccessToken.objects.filter(
            revoked_at__isnull=False,
            revoked_at__lt=cutoff,
        )
        sessions_count = sessions_qs.count()
        tokens_count = tokens_qs.count()

        if options["dry_run"]:
            self.stdout.write(
                "Would delete "
                f"{sessions_count} device link session(s) and "
                f"{tokens_count} revoked token(s) older than {keep_days} day(s)."
            )
            return

        sessions_deleted, _ = sessions_qs.delete()
        tokens_deleted, _ = tokens_qs.delete()
        self.stdout.write(
            "Deleted "
            f"{sessions_deleted} device link session(s) and "
            f"{tokens_deleted} revoked token(s) older than {keep_days} day(s)."
        )
