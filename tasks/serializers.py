from rest_framework import serializers
from .models import Task, STATUS_VALUES, PRIORITY_VALUES

class TaskSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=STATUS_VALUES,
                                     error_messages={'invalid_choice': 'Status must be one of: BACKLOG, IN_PROGRESS, DONE.'})
    priority = serializers.ChoiceField(choices=PRIORITY_VALUES,
                                       error_messages={'invalid_choice': 'Priority must be one of: LOW, MEDIUM, HIGH.'})
    title = serializers.CharField(required=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'due_date', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise serializers.ValidationError('Title is required and must not be blank or whitespace-only.')
        return value
