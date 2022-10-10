
import django_filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, generics
from .pagination import Pagination
from .serializers import SysCountriesSerializer

from .models import SysCountries


class SysCountriesFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(
        field_name="name", lookup_expr="icontains"
    )

    code = django_filters.CharFilter(
        field_name="code", lookup_expr="icontains"
    )

    class Meta:
        model = SysCountries
        fields = ["name", "code"]


class ListSysCountriesAPIView(generics.ListAPIView):
    serializer_class = SysCountriesSerializer
    pagination_class = Pagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = SysCountriesFilter
    search_fields = ["code", "name"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        return SysCountries.objects.filter(deleted=False).order_by("-created_at")