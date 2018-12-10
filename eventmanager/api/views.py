from api.serializers import EventSerializer
from api.serializers import CategorySerializer, CommentsSerializer, InvitationsSerializer

from django.core.serializers import serialize
from django.shortcuts import render

from events.models import Event, Comment, Invite
from categories.models import Category

from rest_framework import filters
from rest_framework import viewsets
from rest_framework.response import Response


class EventViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for listing or retrieving news.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class CategoriesViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for listing or retrieving news.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CommentsViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for listing or retrieving news.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer

class InvitationsViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for listing or retrieving news.
    """
    queryset = Invite.objects.all()
    serializer_class = InvitationsSerializer