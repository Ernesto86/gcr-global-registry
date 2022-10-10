from rest_framework import serializers

from .models import SysCountries

class SysCountriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = SysCountries
        fields = [
            "id",
            "code",
            "name",
            "created_at"
        ]