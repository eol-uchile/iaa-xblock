from django.db import models
from django.core.exceptions import ValidationError


class IAAActivity(models.Model):

    id_course = models.TextField()
    activity_name = models.TextField()


class IAAStage(models.Model):

    id_activity = models.ForeignKey(
        IAAActivity,
        on_delete=models.CASCADE,
        related_name="iaa_activity"
    )
    stage_label = models.TextField()
    stage_number = models.IntegerField()


class IAASubmission(models.Model):

    id_stage = models.ForeignKey(
        IAAStage,
        on_delete=models.CASCADE,
        related_name="iaa_stage"
    )
    id_student = models.TextField()
    submission = models.TextField()
    submission_time = models.DateField()


class IAAFeedback(models.Model):

    id_stage = models.ForeignKey(
        IAAStage,
        on_delete=models.CASCADE,
        related_name="iaa_stage"
    )
    id_student = models.TextField()
    id_instructor = models.TextField()
    feedback = models.TextField()
    feedback_time = models.DateField()


