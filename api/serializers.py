
from rest_framework import serializers

from products.models import Product
from repairs.models import RepairTicket, RepairUpdate


# ---------------------------------------------
# PRODUCT SERIALIZER
# ---------------------------------------------

class ProductSerializer(serializers.ModelSerializer):

    warranty_expiry = serializers.SerializerMethodField()
    is_under_warranty = serializers.SerializerMethodField()

    class Meta:
        model = Product

        fields = [
            "id",
            "product_name",
            "brand",
            "category",
            "serial_number",
            "purchase_date",
            "warranty_months",
            "warranty_expiry",
            "is_under_warranty",
        ]

        read_only_fields = [
            "id",
            "warranty_expiry",
            "is_under_warranty",
        ]

    def get_warranty_expiry(self, obj):
        return obj.warranty_expiry

    def get_is_under_warranty(self, obj):
        return obj.is_under_warranty


# ---------------------------------------------
# REPAIR UPDATE SERIALIZER
# ---------------------------------------------

class RepairUpdateSerializer(serializers.ModelSerializer):

    updated_by = serializers.CharField(
        source="updated_by.username",
        read_only=True,
    )

    class Meta:
        model = RepairUpdate

        fields = [
            "id",
            "updated_by",
            "message",
            "created_at",
        ]

        read_only_fields = fields


# ---------------------------------------------
# REPAIR TICKET SERIALIZER
# ---------------------------------------------

class RepairTicketSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source="product.product_name",
        read_only=True,
    )

    technician_name = serializers.SerializerMethodField()

    class Meta:
        model = RepairTicket

        fields = [
            "id",
            "product",
            "product_name",
            "issue_description",
            "priority",
            "status",
            "warranty_status",
            "technician_name",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "status",
            "warranty_status",
            "technician_name",
            "created_at",
            "updated_at",
        ]

    def get_technician_name(self, obj):
        if obj.assigned_technician:
            return obj.assigned_technician.user.username

        return None
