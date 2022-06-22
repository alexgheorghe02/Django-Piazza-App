from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .models import WallPost, WallComment, WallLike, WallDislike
from .serializers import WallPostSerializer, WallCommentSerializer, WallLikeSerializer, WallDislikeSerializer



class WallPostViewSet(viewsets.ModelViewSet):
    queryset = WallPost.objects.all()
    serializer_class = WallPostSerializer
    filterset_fields = ('owner', 'topic', 'status')


class WallCommentViewSet(viewsets.ModelViewSet):
    queryset = WallComment.objects.all()
    serializer_class = WallCommentSerializer
   

class WallLikeViewSet(viewsets.ModelViewSet):
    queryset = WallLike.objects.all()
    serializer_class = WallLikeSerializer
    

class WallDislikeViewSet(viewsets.ModelViewSet):
    queryset = WallDislike.objects.all()
    serializer_class = WallDislikeSerializer