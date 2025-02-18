from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.filters import BaseFilterBackend
from blog.models import Blog, Like, Comment, Story
from blog.serializers import BlogSerializer, LikeSerializer, CommentSerializer, StorySerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.validators import ValidationError


class BlogPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class BlogViewSet(ReadOnlyModelViewSet):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Blog.objects.filter(is_story=False).order_by('-created_at')
    pagination_class = BlogPagination
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get all filter parameters
        post_slug = self.request.query_params.get('post_slug')
        author_id = self.request.query_params.get('author_id')
        tag_slugs = self.request.query_params.get('tag_slug')  # Example: "lifestyle,productivity"
        title = self.request.query_params.get('title')

        if post_slug:
            queryset = queryset.filter(slug=post_slug)
        if author_id:
            queryset = queryset.filter(author=author_id)
        if tag_slugs:
            tag_slug_list = tag_slugs.split(',')  # Convert string to list
            queryset = queryset.filter(tags__slug__in=tag_slug_list).distinct()  # Use `__in` to filter
        if title:
            queryset = queryset.filter(title__icontains=title)

        return queryset


class BlogViewIncrease(APIView):
    permission_classes = [AllowAny]

    def post(self, request, slug):
        try:
            blog = Blog.objects.get(slug=slug)
        except Blog.DoesNotExist:
            return Response({"error": "Blog not found"})

        blog.views += 1
        blog.save()
        return Response({"success": "Blog viewed!"})


class CreatePostAPIView(APIView):
    serializer_class = BlogSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            blog = serializer.save(author=user)
            return Response({"success" : "Blog created successfully!"})
        
        return Response(serializer.errors)


class DeletePostAPIView(APIView):
    def post(self, request):
        user = request.user
        post_slug = request.data.get('post_slug')

        try:
            post = Blog.objects.get(slug=post_slug, author=user)
        except Blog.DoesNotExist:
            return ValidationError({"error" : "Post does not found"})

        post.delete()
        return Response({"success" : "Post deleted successfully"})


class EditPostAPIView(APIView):
    def post(self, request):
        user = request.user
        post_slug = request.data.get('slug')

        try:
            post = Blog.objects.get(slug=post_slug, author=user)
        except Blog.DoesNotExist:
            return ValidationError({"error" : "Post does not found"})

        serializer = BlogSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success" : "Post updated successfully"})
        return Response(serializer.errors)


class LikeBlogView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        try:
            blog = Blog.objects.get(slug=slug)
        except Blog.DoesNotExist:
            return Response({"error": "Blog not found"})

        like, created = Like.objects.get_or_create(user=request.user, blog=blog)

        if not created:
            like.delete()
            return Response({"success": "Blog unliked"})

        return Response({"success": "Blog liked"})

class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, blog_slug):
        try:
            blog = Blog.objects.get(slug=blog_slug)
        except Blog.DoesNotExist:
            return Response({"error": "Blog not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, blog=blog)
            data = {"success": "Comment added!", "comment": serializer.data}
            return Response(data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CommentListView(ReadOnlyModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Get the blog_slug from URL keyword arguments.
        blog_slug = self.kwargs.get('blog_slug')
        # Filter comments for the specific blog.
        return Comment.objects.filter(blog__slug=blog_slug).order_by('-created_at')



class CreateStoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StorySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({"success": "Story created successfully", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteStoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, slug):
        try:
            story = Story.objects.get(slug=slug, author=request.user)
        except Story.DoesNotExist:
            return Response({"error": "Story not found or you're not authorized"},
                            status=status.HTTP_404_NOT_FOUND)
        story.delete()
        return Response({"success": "Story deleted successfully"}, status=status.HTTP_200_OK)


class StoryDetailAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = StorySerializer

    def get(self, request, slug):
        try:
            story = Story.objects.get(slug=slug)
        except Story.DoesNotExist:
            return Response({"error": "Story not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(story, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)



class StoryListPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class StoryListViewSet(ReadOnlyModelViewSet):
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Story.objects.all().order_by('-created_at')
    pagination_class = StoryListPagination
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()

        story_slug = self.request.query_params.get('story_slug')
        author_id = self.request.query_params.get('author_id')
        tag_slugs = self.request.query_params.get('tag_slug')
        name = self.request.query_params.get('name')

        if story_slug:
            queryset = queryset.filter(slug=story_slug)
        if author_id:
            queryset = queryset.filter(author=author_id)
        if tag_slugs:
            tag_slug_list = tag_slugs.split(',')
            queryset = queryset.filter(tags__slug__in=tag_slug_list).distinct() 
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class CreateChapterAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer

    def post(self, request, story_slug):
        try:
            story = Story.objects.get(slug=story_slug)
        except Story.DoesNotExist:
            return Response({"error": "Story not found"}, status=status.HTTP_404_NOT_FOUND)

        if story.author != request.user:
            return Response({"error": "You are not authorized to add chapters to this story."},
                            status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data['story'] = story.slug 
        data['is_story'] = True

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({"success": "Chapter added successfully", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditChapterAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer

    def put(self, request, chapter_slug):
        try:
            chapter = Blog.objects.get(slug=chapter_slug, author=request.user, is_story=True)
        except Blog.DoesNotExist:
            return Response({"error": "Chapter not found or you're not authorized"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(chapter, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Chapter updated successfully", "data": serializer.data},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteChapterAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, chapter_slug):
        try:
            chapter = Blog.objects.get(slug=chapter_slug, author=request.user, is_story=True)
        except Blog.DoesNotExist:
            return Response({"error": "Chapter not found or you're not authorized"},
                            status=status.HTTP_404_NOT_FOUND)
        chapter.delete()
        return Response({"success": "Chapter deleted successfully"}, status=status.HTTP_200_OK)


class ChapterPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1 

class ListChaptersAPIView(ListAPIView):
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]
    pagination_class = ChapterPagination

    def get_queryset(self):
        story_slug = self.kwargs.get('story_slug')
        return Blog.objects.filter(story__slug=story_slug, is_story=True).order_by('created_at')