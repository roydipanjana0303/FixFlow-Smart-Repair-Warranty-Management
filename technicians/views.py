
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Q
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from repairs.models import RepairTicket, RepairUpdate
from .forms import RepairProgressForm
from .models import Technician


def get_current_technician(request):
    if request.user.is_staff:
        return None

    return Technician.objects.filter(
        user=request.user,
        user__is_active=True,
    ).first()


@login_required
def technician_dashboard(request):
    technician = get_current_technician(request)

    if technician is None:
        return HttpResponseForbidden(
            "This page is available only to registered technicians."
        )

    tickets = RepairTicket.objects.filter(
        assigned_technician=technician
    ).select_related(
        "customer",
        "product",
    ).order_by("-created_at")

    counts = tickets.aggregate(
        total=Count("id"),
        assigned=Count(
            "id",
            filter=Q(status="assigned"),
        ),
        in_progress=Count(
            "id",
            filter=Q(status="in_progress"),
        ),
        completed=Count(
            "id",
            filter=Q(status="completed"),
        ),
    )

    active_count = counts["assigned"] + counts["in_progress"]

    context = {
        "technician": technician,
        "tickets": tickets,
        "counts": counts,
        "active_count": active_count,
        "remaining_capacity": max(
            technician.max_active_tickets - active_count,
            0,
        ),
    }

    return render(
        request,
        "technicians/dashboard.html",
        context,
    )


@login_required
@require_http_methods(["GET", "POST"])
def technician_ticket_detail(request, pk):
    technician = get_current_technician(request)

    if technician is None:
        return HttpResponseForbidden(
            "This page is available only to registered technicians."
        )

    ticket = get_object_or_404(
        RepairTicket.objects.select_related(
            "customer",
            "product",
            "assigned_technician",
        ),
        pk=pk,
        assigned_technician=technician,
    )

    form = RepairProgressForm(
        request.POST or None,
        initial={"status": ticket.status},
    )

    if request.method == "POST":
        if ticket.status == "completed":
            messages.error(
                request,
                "Completed repairs cannot be modified.",
            )
            return redirect(
                "technicians:ticket_detail",
                pk=ticket.pk,
            )

        if form.is_valid():
            new_status = form.cleaned_data["status"]
            note = form.cleaned_data["message"]

            allowed_transitions = {
                "assigned": {"in_progress"},
                "in_progress": {"completed"},
            }

            with transaction.atomic():
                locked_ticket = get_object_or_404(
                    RepairTicket.objects.select_for_update(),
                    pk=ticket.pk,
                    assigned_technician=technician,
                )

                allowed = allowed_transitions.get(
                    locked_ticket.status,
                    set(),
                )

                if new_status not in allowed:
                    messages.error(
                        request,
                        "Invalid status transition. Start the "
                        "repair before marking it completed.",
                    )
                    return redirect(
                        "technicians:ticket_detail",
                        pk=ticket.pk,
                    )

                locked_ticket.status = new_status
                locked_ticket.save(
                    update_fields=["status", "updated_at"]
                )

                RepairUpdate.objects.create(
                    ticket=locked_ticket,
                    updated_by=request.user,
                    message=note,
                )

            messages.success(
                request,
                "Repair status updated successfully.",
            )

            return redirect(
                "technicians:ticket_detail",
                pk=ticket.pk,
            )

    updates = RepairUpdate.objects.filter(
        ticket=ticket
    ).select_related("updated_by").order_by("created_at")

    context = {
        "technician": technician,
        "ticket": ticket,
        "updates": updates,
        "form": form,
    }

    return render(
        request,
        "technicians/ticket_detail.html",
        context,
    )
