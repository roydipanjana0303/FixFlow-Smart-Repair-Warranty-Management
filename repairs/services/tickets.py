
from django.db import transaction

from repairs.models import RepairTicket, RepairUpdate
from .assignment import find_available_technician


@transaction.atomic
def create_repair_ticket(
    *,
    customer,
    product,
    issue_description,
    priority,
):
    if product.customer_id != customer.pk:
        raise ValueError(
            "This product does not belong to the customer."
        )

    # Date-based warranty check.
    warranty_status = (
        "eligible"
        if product.is_under_warranty
        else "expired"
    )

    technician = find_available_technician(
        product.category
    )

    ticket = RepairTicket.objects.create(
        customer=customer,
        product=product,
        issue_description=issue_description,
        priority=priority,
        warranty_status=warranty_status,
        assigned_technician=technician,
        status=(
            "assigned"
            if technician
            else "pending"
        ),
    )

    RepairUpdate.objects.create(
        ticket=ticket,
        updated_by=None,
        message=(
            "Repair request submitted successfully. "
            "Warranty period checked automatically."
        ),
    )

    if technician:
        RepairUpdate.objects.create(
            ticket=ticket,
            updated_by=None,
            message=(
                "A technician has been assigned "
                "to this repair request."
            ),
        )
    else:
        RepairUpdate.objects.create(
            ticket=ticket,
            updated_by=None,
            message=(
                "Your request is waiting for "
                "an available technician."
            ),
        )

    return ticket
