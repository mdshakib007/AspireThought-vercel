from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.views import (
    BlogViewSet, CreatePostAPIView, EditPostAPIView, DeletePostAPIView, 
    LikeBlogView, CommentCreateView, CommentListView, BlogViewIncrease,
    CreateStoryAPIView, DeleteStoryAPIView, StoryDetailAPIView,
    CreateChapterAPIView, EditChapterAPIView, DeleteChapterAPIView, 
    ListChaptersAPIView, StoryListViewSet
)

# Existing blog router
router = DefaultRouter()
router.register('list', BlogViewSet)

urlpatterns = [
    # ----- Blog Endpoints -----
    path('', include(router.urls)),
    path('create/', CreatePostAPIView.as_view(), name='create_post'),
    path('edit/', EditPostAPIView.as_view(), name='edit_post'),
    path('delete/', DeletePostAPIView.as_view(), name='delete_post'),
    path('<slug:slug>/like/', LikeBlogView.as_view(), name='like_post'),
    path('<slug:slug>/view/', BlogViewIncrease.as_view(), name='view_post'),
    path('<slug:blog_slug>/comments/', CommentListView.as_view({'get': 'list'}), name='list_comments'),
    path('<slug:blog_slug>/comments/add/', CommentCreateView.as_view(), name='create_comment'),

    # ----- Story Endpoints -----
    # story list
    path('stories/', StoryListViewSet.as_view({'get': 'list'}), name='story_list'),
    # Create a new story
    path('stories/create/', CreateStoryAPIView.as_view(), name='create_story'),
    # Retrieve a story detail (including its nested chapters)
    path('stories/<slug:slug>/', StoryDetailAPIView.as_view(), name='story_detail'),
    # Delete a story (by its author)
    path('stories/<slug:slug>/delete/', DeleteStoryAPIView.as_view(), name='delete_story'),

    # Chapter endpoints for a specific story:
    # List chapters with pagination (one chapter per page)
    path('stories/<slug:story_slug>/chapters/', ListChaptersAPIView.as_view(), name='list_chapters'),
    # Create a new chapter for a story
    path('stories/<slug:story_slug>/chapters/create/', CreateChapterAPIView.as_view(), name='create_chapter'),
    # Edit a specific chapter
    path('stories/chapters/<slug:chapter_slug>/edit/', EditChapterAPIView.as_view(), name='edit_chapter'),
    # Delete a specific chapter
    path('stories/chapters/<slug:chapter_slug>/delete/', DeleteChapterAPIView.as_view(), name='delete_chapter'),
]
