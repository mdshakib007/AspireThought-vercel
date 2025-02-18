from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from tag.models import Tag
from tag.serializers import TagSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.filters import BaseFilterBackend



class AddTagAPIView(APIView):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            tag = serializer.save()
            return Response({"success" : "Tag Added!", "slug" : tag.slug, "name" : tag.name})
        return Response(serializer.errors)


class TagViewSet(ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Tag.objects.all()
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.request.query_params.get('slug')
        tag_name = self.request.query_params.get('tag')

        if slug:
            queryset = queryset.filter(slug=slug)
        if tag_name:
            queryset = queryset.filter(name__iexact=tag_name)

        return queryset
