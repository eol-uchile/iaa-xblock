from django.contrib import admin

from .models import IAAActivity, IAASubmission, IAAFeedback

admin.site.register(IAAActivity)
admin.site.register(IAASubmission)
admin.site.register(IAAFeedback)