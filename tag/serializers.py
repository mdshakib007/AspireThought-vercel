from rest_framework import serializers
from tag.models import Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'slug', 'followers']
        read_only_fields = ['slug', 'followers']
