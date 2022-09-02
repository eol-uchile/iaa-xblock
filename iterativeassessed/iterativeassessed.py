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


loader = ResourceLoader(__name__)

@XBlock.needs('i18n')
class IterativeAssessedActivityXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    activity_name = String(
        default="",
        scope=Scope.settings,
        help="Unique name of this activity within this course."
    )

    block_type = String(
        default="full",
        values=["display", "full", "summary"],
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

        context.update(
            {
            }
        )
        template = loader.render_django_template(
            'public/html/iterativeassessed_student.html',
            context=Context(context),
            i18n_service=self.runtime.service(self, 'i18n'),
        )
        frag = self.build_fragment(
            template,
            initialize_js_func='IterativeAssessedActivityStudent',
            additional_css=[
                'public/css/iterativeassessed.css',
            ],
            additional_js=[
                'public/js/iterativeassessed_student.js',
            ],
        )
        return frag

    def studio_view(self, context):
        """
        Create a fragment used to display the edit view in the Studio.
        """

        id_course = "ID_course"
        activities = get_activities(id_course)['result']
        js_context = {
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
            'public/html/iterativeassessed_studio.html',
            context=Context(context),
            i18n_service=self.runtime.service(self, 'i18n'),
        )
        frag = self.build_fragment(
            template,
            initialize_js_func='IterativeAssessedActivityStudio',
            additional_js=[
                'public/js/iterativeassessed_studio.js',
            ],
        )    
        return frag


    def author_view(self, context={}):
        """
        Vista estudiante
        """


        context.update(
            {
            }
        )
        template = loader.render_django_template(
            'public/html/iterativeassessed_author.html',
            context=Context(context),
            i18n_service=self.runtime.service(self, 'i18n'),
        )
        frag = self.build_fragment(
            template,
            initialize_js_func='IterativeAssessedActivityAuthor',
            additional_css=[
                'public/css/iterativeassessed.css',
            ],
            additional_js=[
                'public/js/iterativeassessed_author.js',
            ],
        )
        return frag

    

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        """
        Called when submitting the form in Studio.
        """
        
        self.activity_name = data.get('activity_name')
        self.block_type = data.get('block_type')
        self.activity_stage = int(data.get('activity_stage'))
        self.stage_label = data.get('stage_label')
        self.question = data.get('question')
        self.activity_name_previous = data.get('activity_name_previous')
        self.activity_stage_previous = int(data.get('activity_stage_previous'))
        self.summary_text = data.get('summary_text')
        return {'result': 'success'}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("IterativeAssessedActivityXBlock",
             """<iterativeassessed/>
             """)
        ]
