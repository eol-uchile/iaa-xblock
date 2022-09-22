import json
import pkg_resources
from xblock.core import XBlock
from django.template.context import Context
from xblock.fields import Integer, String, Scope
from xblockutils.resources import ResourceLoader
from xblock.fragment import Fragment
import datetime


loader = ResourceLoader(__name__)

@XBlock.needs('i18n')
class IterativeAssessedActivityXBlock(XBlock):
    """
    This XBlock allows to create open response activities with multiples steps, with the possibility for instructors
    to provide feedback to each submission.
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
        from .models import IAAActivity, IAAStage, IAASubmission, IAAFeedback
        from django.contrib.auth.models import User

        # Staff
        if getattr(self.runtime, 'user_is_staff', False):

            id_course = self.id_course
            id_instructor = self.scope_ids.user_id
            current_activity = IAAActivity.objects.get(id_course=id_course, activity_name=self.activity_name)

            if self.block_type == "none":
                context.update(
                    {
                        "block_type": self.block_type
                    }
                )

            elif self.block_type == "full":
                enrolled = User.objects.filter(courseenrollment__course_id=self.course_id,courseenrollment__is_active=1).order_by('id').values('id' ,'first_name', 'last_name', 'email')
                students = []
                student_names = [x["email"] for x in enrolled]
                student_ids = [x["id"] for x in enrolled]
                current_stage = IAAStage.objects.get(iaa_activity=current_activity, stage_number=self.activity_stage)
                for i in range(len(student_names)):
                    submission = IAASubmission.objects.filter(iaa_stage_submission=current_stage, id_student=student_ids[i]).values('id_student', 'submission', 'submission_time')
                    feedback = IAAFeedback.objects.filter(iaa_stage_feedback=current_stage, id_student=student_ids[i], id_instructor=id_instructor).values('id_student', 'feedback', 'feedback_time')
                    if len(submission) == 0:
                        this_submission = ""
                        this_submission_time = ""
                    else:
                        this_submission = submission[0]["submission"]
                        this_submission_time = str(submission[0]["submission_time"])
                    if len(feedback) == 0:
                        this_feedback = ""
                        this_feedback_time = ""
                    else:
                        this_feedback = feedback[0]["feedback"]
                        this_feedback_time = str(feedback[0]["feedback_time"])
                    students.append((student_ids[i], student_names[i], this_submission, this_submission_time, this_feedback, this_feedback_time))
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
                'public/html/iaaxblock_instructor.html',
                context=Context(context),
                i18n_service=self.runtime.service(self, 'i18n'),
            )
            frag = self.build_fragment(
                template,
                initialize_js_func='IterativeAssessedActivityInstructor',
                additional_css=[
                    'public/css/iaaxblock.css',
                ],
                additional_js=[
                    'public/js/iaaxblock_instructor.js',
                ],
            )
            return frag

        
        
        # Student
        else:
            if self.block_type == "none":
                context.update(
                    {
                        "block_type": self.block_type
                    }
                )
            else:
                id_student = self.scope_ids.user_id
                id_course = self.id_course
                current_activity = IAAActivity.objects.get(id_course=id_course, activity_name=self.activity_name)

                if self.block_type == "full":
                    current_activity_previous = IAAActivity.objects.get(id_course=id_course, activity_name=self.activity_name_previous)
                    current_stage_previous = IAAStage.objects.get(iaa_activity=current_activity_previous, stage_number=self.activity_stage_previous)
                    current_submission_previous = IAASubmission.objects.filter(iaa_stage_submission=current_stage_previous, id_student=id_student).values("submission", "submission_time")
                    if len(current_submission_previous) == 0:
                        this_submission_previous = ""
                        this_submission_time_previous = ""
                    else:
                        this_submission_previous = current_submission_previous[0]["submission"]
                        this_submission_time_previous = current_submission_previous[0]["submission_time"]
                    current_stage = IAAStage.objects.get(iaa_activity=current_activity, stage_number=self.activity_stage)
                    feedbacks = [(x["id_instructor"], x["feedback"], x["feedback_time"]) for x in IAAFeedback.objects.filter(iaa_stage_feedback=current_stage, id_student=id_student).values('id_instructor', 'feedback', 'feedback_time')]
                    context.update(
                        {
                            "title": self.title,
                            "block_type": self.block_type,
                            "activity_name_previous": self.activity_name_previous,
                            "activity_stage_previous": self.activity_stage_previous,
                            "submission_previous": this_submission_previous,
                            "submission_previous_time": this_submission_time_previous,
                            "display_title": self.display_title,
                            "activity_name": self.activity_name,
                            "activity_stage": self.activity_stage,
                            "submission": self.submission,
                            "submission_time": self.submission_time,
                            "stage_label": self.stage_label,
                            "question": self.question,
                            "feedbacks": feedbacks
                        }
                    )

                elif self.block_type == "display":
                    current_activity_previous = IAAActivity.objects.get(id_course=id_course, activity_name=self.activity_name_previous)
                    current_stage_previous = IAAStage.objects.get(iaa_activity=current_activity_previous, stage_number=self.activity_stage_previous)
                    current_submission_previous = IAASubmission.objects.filter(iaa_stage_submission=current_stage_previous, id_student=id_student).values("submission", "submission_time")
                    if len(current_submission_previous) == 0:
                        this_submission_previous = ""
                        this_submission_time_previous = ""
                    else:
                        this_submission_previous = current_submission_previous[0]["submission"]
                        this_submission_time_previous = current_submission_previous[0]["submission_time"]
                    context.update(
                        {
                            "title": self.title,
                            "block_type": self.block_type,
                            "activity_name_previous": self.activity_name_previous,
                            "activity_stage_previous": self.activity_stage_previous,
                            "submission_previous": this_submission_previous,
                            "submission_previous_time": this_submission_time_previous,
                            "display_title": self.display_title,
                        }
                    )

                else:
                    summary = []
                    stages_list = IAAStage.objects.filter(iaa_activity=current_activity).order_by("stage_number").all()

                    for stage in stages_list:
                        submission = IAASubmission.objects.filter(iaa_stage_submission=stage, id_student=id_student).values("submission", "submission_time")
                        if len(submission) == 0:
                            this_summary_submission = ""
                            this_summary_submission_time = ""
                        else:
                            this_summary_submission = submission[0]["submission"]
                            this_summary_submission_time = submission[0]["submission_time"]
                        summary.append((stage.stage_label, this_summary_submission, this_summary_submission_time))
                    
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
        from .models import IAAActivity, IAAStage
        id_course = self.id_course
        activities_no_stage = [x for x in IAAActivity.objects.filter(id_course=id_course).values("id", "activity_name")]
        activities = []
        for i in range(len(activities_no_stage)):
            activity = activities_no_stage[i]
            stages_list = [str(x[0]) for x in IAAStage.objects.filter(iaa_activity=activity).order_by("stage_number").values("stage_number")]
            if len(stages_list) != 0:
                stages = stages_list.join(",")
            activities.append([activity[0], activity[1], stages])
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
        Vista de autor
        """

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
        from .models import IAAActivity, IAAStage, IAASubmission, IAAFeedback

        id_course = self.id_course
        previous_block_type = self.block_type
        previous_activity_stage = self.activity_stage
        previous_stage_label = self.stage_label
        self.title = data.get('title')
        self.block_type = data.get('block_type')
        if self.block_type == "full":
            self.activity_name = data.get('activity_name')
            self.activity_stage = int(data.get('activity_stage'))
            self.stage_label = data.get('stage_label')
            self.question = data.get('question')
            self.activity_name_previous = data.get('activity_name_previous')
            self.activity_stage_previous = int(data.get('activity_stage_previous'))
            self.display_title = data.get('display_title')
        elif self.block_type == "display":
            self.activity_name_previous = data.get('activity_name_previous')
            self.activity_stage_previous = int(data.get('activity_stage_previous'))
            self.display_title = data.get('display_title')
        else:
            self.activity_name = data.get('activity_name')
            self.summary_text = data.get('summary_text')

        if previous_block_type == "none" and self.block_type == "full":
            new_activity = IAAActivity(id_course=id_course, activity_name=self.activity_name)
            new_activity.save()
            new_stage = IAAStage(iaa_activity=new_activity, stage_label=self.stage_label, stage_number=self.activity_stage)
            new_stage.save()
        
        else:
            if previous_activity_stage != self.activity_stage:
                new_stage = IAAStage(iaa_activity=new_activity, stage_label=self.stage_label, stage_number=self.activity_stage)
                new_stage.save()
                current_submissions = IAASubmission.objects.filter().all()
                for submission in current_submissions:
                    submission.stage = new_stage
                    submission.save()
                current_feedbacks = IAAFeedback.objects.filter().all()
                for feedback in current_feedbacks:
                    feedback.stage = new_stage
                    feedback.save()
                current_activity = IAAActivity.objects.get(id_course=id_course, activity_name=self.activity_name)
                IAAStage.objects.get(iaa_activity=current_activity, stage_number=previous_activity_stage).delete()
            
            else:
                if previous_stage_label != self.stage_label:
                    current_activity = IAAActivity.objects.get(id_course=id_course, activity_name=self.activity_name)
                    current_stage = IAAStage.objects.get(iaa_activity=current_activity, stage_number=self.activity_stage)
                    current_stage.stage_label = self.stage_label
                    current_stage.save()

        return {'result': 'success'}


    @XBlock.json_handler
    def student_submit(self, data, suffix=''):
        """
        """
        from .models import IAAActivity, IAAStage, IAASubmission

        id_course = self.id_course
        id_student = self.scope_ids.user_id
        current_activity = IAAActivity.objects.get(id_course=id_course, activity_name=self.activity_name)
        current_stage = IAAStage.objects.get(iaa_activity=current_activity)
        new_submission_time = datetime.datetime.now()
        new_submission = IAASubmission(iaa_stage_submission=current_stage, id_student=id_student, submission=data["submission"], submission_time=new_submission_time)
        new_submission.save()
        self.submission = data["submission"]
        self.submission_time = str(new_submission_time)
        return {"result": 'success'}

    
    @XBlock.json_handler
    def instructor_submit(self, data, suffix=''):
        """
        """
        from .models import IAAActivity, IAAStage, IAAFeedback
        id_course = self.id_course
        id_instructor = self.scope_ids.user_id
        current_activity = IAAActivity.objects.get(id_course=id_course, activity_name=self.activity_name)
        current_stage = IAAStage.objects.get(iaa_activity=current_activity)
        for student in data["feedbacks"]:
            if student["feedback"] != "":
                existing_feedback = IAAFeedback.objects.filter(iaa_stage_feedback=current_stage, id_instructor=id_instructor, id_student=student["id_stundent"]).all()
                new_feedback_time = datetime.datetime.now()
                if len(existing_feedback) == 0:
                    new_feedback = IAAFeedback(iaa_stage_feedback=current_stage, id_instructor=id_instructor, id_student=student["id_student"], feedback=student["feedback"], feedback_time=new_feedback_time)
                    new_feedback.save()
                else:
                    existing_feedback.feedback = student["feedback"]
                    existing_feedback.feedback_time = str(new_feedback_time)
                    existing_feedback.save()
        return {"result": "success"}


    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("IterativeAssessedActivityXBlock",
             """<iaaxblock/>
             """)
        ]

