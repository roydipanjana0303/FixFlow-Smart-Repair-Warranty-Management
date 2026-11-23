
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product
from repairs.models import RepairTicket
from technicians.models import Technician

from .permissions import IsCustomer, IsTechnician
from .serializers import (
    ProductSerializer,
    RepairTicketSerializer,
)


class ProductListAPI(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return Product.objects.filter(
            customer=self.request.user
        ).order_by("-id")


class RepairTicketListAPI(generics.ListAPIView):
    serializer_class = RepairTicketSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return RepairTicket.objects.filter(
            customer=self.request.user
        ).select_related(
            "product",
            "assigned_technician__user",
        ).order_by("-created_at")


class TechnicianTicketsAPI(generics.ListAPIView):
    serializer_class = RepairTicketSerializer
    permission_classes = [IsTechnician]

    def get_queryset(self):
        technician = get_object_or_404(
            Technician,
            user=self.request.user,
        )

        return RepairTicket.objects.filter(
            assigned_technician=technician
        ).select_related(
            "product",
            "assigned_technician__user",
        ).order_by("-created_at")


class AdminAnalyticsAPI(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        tickets = RepairTicket.objects.all()

        statistics = tickets.aggregate(
            total=Count("id"),
            pending=Count(
                "id",
                filter=Q(status="pending"),
            ),
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

        return Response({
            "total_products": Product.objects.count(),
            "total_technicians": Technician.objects.count(),
            "repair_statistics": statistics,
        })
