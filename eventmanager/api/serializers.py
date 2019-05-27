from accounts.models import AccountDetails

from categories.models import Category
from categories.models import SuggestedCategory

from events.models import Comment
from events.models import Event
from events.models import Invite

from tasks.models import Task

from rest_framework import serializers


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "title",
            "description",
            "category",
            "attendees",
            "team_members",
            "cover_image",
            "added_by",
            "starts_at",
            "ends_at",
            "is_active",
            "created_at",
            "updated_at"
        )
        read_only_fields = (
            "pk",
            "attendees",
            "team_members",
            "added_by",
            "starts_at",
            "ends_at",
            "is_active",
            "created_at",
            "updated_at"
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "name",
            "description",
            "is_active",
            "created_at",
            "updated_at"
        )

        read_only_fields = (
            "name",
            "description",
            "is_active",
            "created_at",
            "updated_at"
        )


class SuggestedCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestedCategory
        fields = (
            "name",
            "description",
            'added_by',
        )
        read_only_fields = (
            "added_by",
        )


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "title",
            "author",
            "content",
            "event",
        )

        read_only_fields = (
            "author",
        )


class InvitationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = (
            "id",
            "invited_user",
            "invited_by",
            "event",
            "is_accepted",

        )
        read_only_fields = (
            "invited_by",
            "is_accepted",
        )


class AccountDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountDetails
        fields = (
            "user",
            "profile_picture",
            "friends",
            "birth_date",
            "description",
        )
        read_only_fields = (
            "friends",
            "user",
        )


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "slug",
            "description",
            "status",
            "is_active",
            "created_at",
            "updated_at",
            'added_by',
            'assignee',
            'event'
        )
        read_only_fields = (
            "id",
            "is_active",
            "created_at",
            "updated_at",
            'added_by',
        )
