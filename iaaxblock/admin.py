from django.contrib import admin

from .models import IAAActivity, IAAStage, IAASubmission, IAAFeedback

admin.site.register(IAAActivity)
admin.site.register(IAAStage)
admin.site.register(IAASubmission)
admin.site.register(IAAFeedback)
