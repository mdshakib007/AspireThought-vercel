from rest_framework import serializers
from blog.models import Story, Blog, Like, Comment



class BlogSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'title', 'slug', 'author', 'story', 'image', 'body',
            'tags', 'created_at', 'updated_at', 'views', 'is_story',
            'like_count', 'comment_count'
        ]
        read_only_fields = [
            'slug', 'author', 'created_at', 'updated_at',
            'views', 'like_count', 'comment_count'
        ]

    def get_like_count(self, obj):
        return obj.like_count()

    def get_comment_count(self, obj):
        return obj.comment_count()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.story is not None:
            representation.pop('image', None)
            representation.pop('tags', None)
        return representation


class StorySerializer(serializers.ModelSerializer):
    # Nest chapters; since chapters are Blog entries, we'll use the BlogSerializer
    chapters = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = [
            'name', 'slug', 'author', 'cover', 'summary',
            'tags', 'reads', 'created_at', 'chapters'
        ]
        read_only_fields = [
            'slug', 'author', 'reads', 'created_at', 'chapters'
        ]

    def get_chapters(self, obj):
        chapters = obj.chapters.all().order_by('created_at')
        return BlogSerializer(chapters, many=True, context=self.context).data


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'blog', 'created_at']
        read_only_fields = ['created_at']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'blog', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'blog', 'created_at']
