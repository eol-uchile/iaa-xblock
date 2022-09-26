from django.db import models


class IAAActivity(models.Model):

    id_course = models.TextField()
    activity_name = models.TextField()


class IAAStage(models.Model):

    activity = models.ForeignKey(
        IAAActivity,
        on_delete=models.CASCADE
    )
    stage_label = models.TextField()
    stage_number = models.IntegerField()


class IAASubmission(models.Model):

    stage = models.ForeignKey(
        IAAStage,
        on_delete=models.CASCADE
    )
    id_student = models.TextField()
    submission = models.TextField()
    submission_time = models.DateField()


class IAAFeedback(models.Model):

    stage = models.ForeignKey(
        IAAStage,
        on_delete=models.CASCADE
    )
    id_student = models.TextField()
    id_instructor = models.TextField()
    feedback = models.TextField()
    feedback_time = models.DateField()


