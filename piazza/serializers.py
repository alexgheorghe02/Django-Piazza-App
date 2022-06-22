from rest_framework import serializers
from .models import WallPost, WallComment, WallLike, WallDislike
class WallPostSerializer(serializers.ModelSerializer):
   number_of_likes = serializers.ReadOnlyField()
   number_of_dislikes = serializers.ReadOnlyField()
   number_of_comments = serializers.ReadOnlyField()
   comments = serializers.ReadOnlyField()
   written_by = serializers.ReadOnlyField()
   this_id = serializers.ReadOnlyField()
   class Meta:
      model = WallPost
      fields = ('owner', 'title', 'topic', 'body', 'post_time', 'expiry_time', 'status', 'number_of_likes', 'number_of_dislikes', 'number_of_comments', 'comments', 'written_by', 'this_id')

class WallCommentSerializer(serializers.ModelSerializer):
   class Meta:
      model = WallComment
      written_by = serializers.ReadOnlyField()
      fields = ('blogpost', 'author', 'comment', 'date_posted', 'written_by')

class WallLikeSerializer(serializers.ModelSerializer):
   class Meta:
      model = WallLike
      liked_by = serializers.ReadOnlyField()
      fields = ('blogpost', 'author', 'date_posted', 'liked_by')

class WallDislikeSerializer(serializers.ModelSerializer):
   class Meta:
      model = WallDislike
      disliked_by = serializers.ReadOnlyField()
      fields = ('blogpost', 'author', 'date_posted', 'disliked_by')
