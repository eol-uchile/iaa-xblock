from django.db import models
from django.core.exceptions import ValidationError


class IAAActivity(models.Model):

    id_course = models.TextField()
    activity_name = models.TextField()
    stages = models.TextField()


class IAASubmission(models.Model):

    id_activity = models.ForeignKey(
        IAAActivity,
        on_delete=models.CASCADE,
        related_name="iaa_submission"
    )
    id_student = models.TextField()
    stage = models.IntegerField()
    submission = models.TextField()
    submission_time = models.DateField()


class IAAFeedback(models.Model):

    id_activity = models.ForeignKey(
        IAAActivity,
        on_delete=models.CASCADE,
        related_name="iaa_feedback"
    )
    id_student = models.TextField()
    id_instructor = models.TextField()
    stage = models.IntegerField()
    feedback = models.TextField()
    feedback_time = models.DateField()


