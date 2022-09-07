"""TO-DO: Write a description of what this XBlock is."""

import json
import pkg_resources
from xblock.core import XBlock
from django.db import IntegrityError
from django.template.context import Context
from xblock.fields import Integer, String, Dict, Scope, Float, Boolean
from xblockutils.resources import ResourceLoader
from xblock.fragment import Fragment
import datetime

from .db_queries import *
#from .models import IAAActivity, IAASubmission, IAAFeedback


loader = ResourceLoader(__name__)

@XBlock.needs('i18n')
class IterativeAssessedActivityXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    title = String(
        default="Iterative Assessed Activity",
        scope=Scope.settings,
        help="Title of this activity."
    )

    activity_name = String(
        default="",
        scope=Scope.settings,
        help="Unique name of this activity within this course."
    )

    block_type = String(
        default="none",
        values=["display", "full", "summary", "none"],
        scope=Scope.settings,
        help="Variant of this block."
    )

    activity_stage = Integer(
        default=0,
        scope=Scope.settings,
        help="Stage of this activity."
    )

    stage_label = String(
        default="",
        scope=Scope.settings,
        help="Label of this stage, shown after the title."
    )

    question = String(
        default="",
        scope=Scope.settings,
        help="Question shown before the text input."
    )

    activity_name_previous = String(
        default="",
        scope=Scope.settings,
        help="Activity of the shown submission."
    )

    activity_stage_previous = Integer(
        default=0,
        scope=Scope.settings,
        help="Stage of the shown submission."
    )

    display_title = String(
        default="",
        scope=Scope.settings,
        help="Title shown before the shown submission."
    )

    submission = String(
        default="",
        scope=Scope.user_state,
        help="The user submission to this block."
    )

    submission_time = String(
        default="",
        scope=Scope.user_state,
        help="Datetime of this student's submission."
    )

    feedback = Dict(
        default={},
        scope=Scope.user_state,
        help="Feedback given by staff to the student, with respective instructors and datetimes."
    )

    summary_text = String(
        default="",
        scope=Scope.settings,
        help="Text shown before the summary."
    )

    has_author_view = True

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def build_fragment(
        self,
        rendered_template,
        initialize_js_func,
        additional_css=[],
        additional_js=[],
    ):
        #  pylint: disable=dangerous-default-value, too-many-arguments
        """
        Creates a fragment for display.
        """
        fragment = Fragment(rendered_template)
        for item in additional_css:
            url = self.runtime.local_resource_url(self, item)
            fragment.add_css_url(url)
        for item in additional_js:
            url = self.runtime.local_resource_url(self, item)
            fragment.add_javascript_url(url)
        settings = {
            'image_path': self.runtime.local_resource_url(self, 'public/images/'),
        }
        fragment.initialize_js(initialize_js_func, json_args=settings)
        return fragment

    def student_view(self, context={}):
        """
        Vista estudiante
        """

        if self.block_type == "none":
            context.update(
                {
                    "block_type": self.block_type
                }
            )

        else:

            # provisorio
            id_student = "ID_student1"
            #id_student = self.runtime.anonymous_student_id
            id_course = "ID_course"
            #id_course = self.id_course
            id_activity = get_id_activity(id_course, self.activity_name)["result"]

            if self.block_type == "full":
                id_activity_previous = get_id_activity(id_course, self.activity_name_previous)["result"]
                submission_previous, submission_previous_time = get_submission(id_activity_previous, id_student, self.activity_stage_previous)["result"]
                context.update(
                    {
                        "title": self.title,
                        "block_type": self.block_type,
                        "activity_name_previous": self.activity_name_previous,
                        "activity_stage_previous": self.activity_stage_previous,
                        "submission_previous": submission_previous,
                        "submission_previous_time": submission_previous_time,
                        "display_title": self.display_title,
                        "activity_name": self.activity_name,
                        "activity_stage": self.activity_stage,
                        "submission": self.submission,
                        "submission_time": self.submission_time,
                        "stage_label": self.stage_label,
                        "question": self.question,
                        "submission": self.submission,
                    }
                )

            elif self.block_type == "display":
                id_activity_previous = get_id_activity(id_course, self.activity_name_previous)["result"]
                submission_previous, submission_previous_time = get_submission(id_activity_previous, id_student, self.activity_stage_previous)["result"]
                context.update(
                    {
                        "title": self.title,
                        "block_type": self.block_type,
                        "activity_name_previous": self.activity_name_previous,
                        "activity_stage_previous": self.activity_stage_previous,
                        "submission_previous": submission_previous,
                        "submission_previous_time": submission_previous_time,
                        "display_title": self.display_title,
                    }
                )

            else:
                summary = get_summary(id_activity, id_student)["result"]
                context.update(
                    {
                        "title": self.title,
                        "block_type": self.block_type,
                        "activity_name": self.activity_name,
                        "summary": summary
                    }
                )

        template = loader.render_django_template(
            'public/html/iaaxblock_student.html',
            context=Context(context),
            i18n_service=self.runtime.service(self, 'i18n'),
        )
        frag = self.build_fragment(
            template,
            initialize_js_func='IterativeAssessedActivityStudent',
            additional_css=[
                'public/css/iaaxblock.css',
            ],
            additional_js=[
                'public/js/iaaxblock_student.js',
            ],
        )
        return frag

    def studio_view(self, context):
        """
        Create a fragment used to display the edit view in the Studio.
        """

        # provisorio
        id_course = "ID_course"
        #id_course = self.id_course

        #activities = IAAActivity.objects.all().values()
        activities = get_activities(id_course)['result']
        js_context = {
            "title": self.title,
            "activity_name": self.activity_name,
            "block_type": self.block_type,
            "activity_stage": str(self.activity_stage),
            "stage_label": self.stage_label,
            "question": self.question,
            "activity_name_previous": self.activity_name_previous,
            "activity_stage_previous": str(self.activity_stage_previous),
            "summary_text": self.summary_text,
            "activities": json.dumps(activities)
        }
        context.update(
            {
                "context": json.dumps(js_context)
            }
        )
        template = loader.render_django_template(
            'public/html/iaaxblock_studio.html',
            context=Context(context),
            i18n_service=self.runtime.service(self, 'i18n'),
        )
        frag = self.build_fragment(
            template,
            initialize_js_func='IterativeAssessedActivityStudio',
            additional_js=[
                'public/js/iaaxblock_studio.js',
            ],
        )    
        return frag


    def author_view(self, context={}):
        """
        Vista instructor
        """
        
        id_course = "ID_course"
        id_instructor = "1"
        #id_course = self.id_course

        #activities = IAAActivity.objects.all().values()
        activities = get_activities(id_course)['result']
        id_activity = get_id_activity(id_course, self.activity_name)["result"]

        if self.block_type == "none":
            context.update(
                {
                    "block_type": self.block_type
                }
            )

        elif self.block_type == "full":
            
            students = get_students_data(id_activity, id_course, self.activity_stage)
            # students = nombre, time, subms, feedback
            context.update(
                {
                    "block_type": self.block_type,
                    "activity_name": self.activity_name,
                    "activity_stage": self.activity_stage,
                    "students": students
                }
            )

        elif self.block_type == "display":

            context.update(
                {
                }
            )

        elif self.block_type == "summary":

            context.update(
                {
                }
            )
        
        template = loader.render_django_template(
            'public/html/iaaxblock_author.html',
            context=Context(context),
            i18n_service=self.runtime.service(self, 'i18n'),
        )
        frag = self.build_fragment(
            template,
            initialize_js_func='IterativeAssessedActivityAuthor',
            additional_css=[
                'public/css/iaaxblock.css',
            ],
            additional_js=[
                'public/js/iaaxblock_author.js',
            ],
        )
        return frag

    

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        """
        Called when submitting the form in Studio.
        """

        self.title = data.get('title')
        self.block_type = data.get('block_type')
        if self.block_type == "full":
            self.activity_name = data.get('activity_name')
            self.activity_stage = int(data.get('activity_stage'))
            self.stage_label = data.get('stage_label')
            self.question = data.get('question')
            self.activity_name_previous = data.get('activity_name_previous')
            self.activity_stage_previous = int(data.get('activity_stage_previous'))
        elif self.block_type == "display":
            self.activity_name_previous = data.get('activity_name_previous')
            self.activity_stage_previous = int(data.get('activity_stage_previous'))
            self.display_title = data.get('display_title')
        else:
            self.activity_name = data.get('activity_name')
            self.summary_text = data.get('summary_text')
        return {'result': 'success'}


    @XBlock.json_handler
    def student_submit(self, data, suffix=''):
        """
        """

        id_course = "ID_course"
        #id_course = self.id_course
        id_student = "ID_student1"
        #id_student = self.runtime.anonymous_student_id
        activities = get_activities(id_course)["result"]
        for activity in activities:
            if activity["activity_name"] == self.activity_name_previous:
                activity_id = activity["id"]
        out = add_submission(activity_id, id_student, self.activity_stage, data["submission"])
        self.submission = data["submission"]
        return {"result": out}

    

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("IterativeAssessedActivityXBlock",
             """<iaaxblock/>
             """)
        ]
