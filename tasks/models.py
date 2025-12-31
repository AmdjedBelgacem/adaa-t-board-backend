from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q

# values used for database-level constraints
STATUS_VALUES = ['BACKLOG', 'IN_PROGRESS', 'DONE']
PRIORITY_VALUES = ['LOW', 'MEDIUM', 'HIGH']

# choices for Django model fields
STATUS_CHOICES = [
    ('BACKLOG', 'Backlog'),
    ('IN_PROGRESS', 'In Progress'),
    ('DONE', 'Done'),
]

PRIORITY_CHOICES = [
    ('LOW', 'Low'),
    ('MEDIUM', 'Medium'),
    ('HIGH', 'High'),
]


def validate_non_blank(value):
    if not isinstance(value, str) or not value.strip():
        raise ValidationError('This field cannot be blank.')


class Task(models.Model):
    title = models.CharField(max_length=255, validators=[validate_non_blank])
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} [{self.status}]"

    class Meta:
        constraints = [
            models.CheckConstraint(condition=Q(status__in=STATUS_VALUES), name='task_status_valid'),
            models.CheckConstraint(condition=Q(priority__in=PRIORITY_VALUES), name='task_priority_valid'),
            models.CheckConstraint(condition=~Q(title=''), name='task_title_not_empty'),
        ]