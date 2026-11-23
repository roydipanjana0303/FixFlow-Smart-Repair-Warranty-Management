
from django.db.models import Count, Q

from technicians.models import Technician


# Repair statuses considered active
ACTIVE_STATUSES = [
    "assigned",
    "in_progress",
]


def find_available_technician(category):
    """
    Find the best available technician based on:
    1. Product category / specialization
    2. Technician availability
    3. Active repair workload
    4. Technician experience
    """

    technicians = (
        Technician.objects.filter(
            specialization__iexact=category,
            is_available=True,
            user__is_active=True,
        )
        .annotate(
            active_count=Count(
                "assigned_tickets",
                filter=Q(
                    assigned_tickets__status__in=ACTIVE_STATUSES
                ),
                distinct=True,
            )
        )
        .order_by(
            "active_count",
            "-experience_years",
            "pk",
        )
    )

    for technician in technicians:
        if (
            technician.max_active_tickets > 0
            and technician.active_count
            < technician.max_active_tickets
        ):
            return technician

    return None
