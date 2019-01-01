from api.serializers import EventSerializer
from api.serializers import CategorySerializer
from api.serializers import CommentsSerializer
from api.serializers import InvitationsSerializer
from api.serializers import AccountDetailsSerializer
from api.serializers import TasksSerializer

from django.core.serializers import serialize
from django.shortcuts import render

from events.models import Event
from events.models import Comment
from events.models import Invite
from categories.models import Category
from accounts.models import AccountDetails
from tasks.models import Task

from rest_framework import filters
from rest_framework import viewsets
from rest_framework.response import Response


class EventViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for listing or retrieving events.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for listing or retrieving categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CommentsViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for listing or retrieving comments.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer


class InvitationsViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for listing or retrieving invitations.
    """
    queryset = Invite.objects.all()
    serializer_class = InvitationsSerializer


class AccountDetailsViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for listing or retrieving account details.
    """
    queryset = AccountDetails.objects.all()
    serializer_class = AccountDetailsSerializer


class TasksViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for listing or retrieving tasks.
    """
    queryset = Task.objects.all()
    serializer_class = TasksSerializer
