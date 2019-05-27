from api.serializers import AccountDetailsSerializer
from api.serializers import CategorySerializer
from api.serializers import CommentsSerializer
from api.serializers import EventSerializer
from api.serializers import InvitationsSerializer
from api.serializers import TasksSerializer
from api.serializers import SuggestedCategorySerializer

from django.core.serializers import serialize

from django.shortcuts import render

from accounts.models import AccountDetails

from categories.models import Category
from categories.models import SuggestedCategory

from events.models import Comment
from events.models import Event
from events.models import Invite

from tasks.models import Task

from rest_framework import filters
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import mixins
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class EventViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for events, logged in users only.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for getting categories.
    """
    http_method_names = ['get']
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SuggestedCategoriesViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for suggested categories.
    """
    added_by = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    queryset = SuggestedCategory.objects.all()
    serializer_class = SuggestedCategorySerializer

    def perform_create(self, serializer):
        user = self.request.user or NULL
        serializer.save(added_by=user)


class CommentsViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for comments.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    author = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    def perform_create(self, serializer):
        user = self.request.user or NULL
        serializer.save(author=user)


class InvitationsViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for invitations.
    """
    queryset = Invite.objects.all()
    serializer_class = InvitationsSerializer
    invited_by = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    def perform_create(self, serializer):
        user = self.request.user or NULL
        serializer.save(invited_by=user)

    def get_queryset(self):
        try:
            queryset = self.queryset
            query_set = queryset.filter(invited_user=self.request.user)
            return query_set
        except BaseException:
            return


class AccountDetailsViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for account details.
    """
    serializer_class = AccountDetailsSerializer
    queryset = AccountDetails.objects.all()
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    def perform_create(self, serializer):
        user = self.request.user or NULL
        serializer.save(user=user)

    def get_queryset(self):
        try:
            queryset = self.queryset
            query_set = queryset.filter(user=self.request.user)
            return query_set
        except BaseException:
            return


class TasksViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for tasks.
    """
    queryset = Task.objects.all()
    serializer_class = TasksSerializer
    added_by = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    def perform_create(self, serializer):
        user = self.request.user or NULL
        serializer.save(added_by=user)
