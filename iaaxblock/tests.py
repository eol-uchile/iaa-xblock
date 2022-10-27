"""
Module To Test IAA XBlock
"""
import json
import pytest
from django.test import TransactionTestCase

from mock import MagicMock, Mock

from xblock.field_data import DictFieldData

from .iaaxblock import IterativeAssessedActivityXBlock
from .models import IAAActivity, IAAStage, IAAFeedback, IAASubmission

COURSE_ID = "some_course_id"


class TestRequest(object):
    # pylint: disable=too-few-public-methods
    """
    Module helper for @json_handler
    """
    method = None
    body = None
    success = None


@pytest.mark.django_db
class IAATestCase(TransactionTestCase):
    # pylint: disable=too-many-instance-attributes, too-many-public-methods
    """
    A complete suite of unit tests for the IAA XBlock
    """

    @classmethod
    def make_an_xblock(cls, **kw):
        """
        Helper method that creates an IAA XBlock
        """
        runtime = Mock(
            service=Mock(
                return_value=Mock(_catalog={}),
            ),
        )
        scope_ids = MagicMock()
        field_data = DictFieldData(kw)
        xblock = IterativeAssessedActivityXBlock(runtime, field_data, scope_ids)
        xblock.course_id = COURSE_ID
        return xblock


    def setUp(self):
        """
        Creates some XBlocks
        """
        self.xblock1 = IAATestCase.make_an_xblock()
        self.xblock2 = IAATestCase.make_an_xblock()
        self.xblock3 = IAATestCase.make_an_xblock()


    def tearDown(self):
        """
        Cleans the database.
        """
        self.xblock1.iaa_delete()
        self.xblock2.iaa_delete()
        self.xblock3.iaa_delete()


    def test_validate_field_data(self):
        """
        Checks if XBlock was created successfully.
        """
        self.assertEqual(self.xblock1.title, "Iterative Assessed Activity")
        self.assertEqual(self.xblock1.block_type, "none")
        self.assertEqual(self.xblock1.activity_name, "")
        self.assertEqual(self.xblock1.activity_stage, 0)
        self.assertEqual(self.xblock1.stage_label, "")
        self.assertEqual(self.xblock1.activity_previous, False)
        self.assertEqual(self.xblock1.activity_name_previous, "")
        self.assertEqual(self.xblock1.activity_stage_previous, 0)
        self.assertEqual(self.xblock1.display_title, "")
        self.assertEqual(self.xblock1.question, "")
        self.assertEqual(self.xblock1.submission, "")
        self.assertEqual(self.xblock1.submission_time, "")
        self.assertEqual(self.xblock1.summary_text, "")



    def test_create_full(self):
        """
        Checks if a 'full' type XBlock was created successfully.
        """
        request = TestRequest()
        request.method = 'POST'
        data = json.dumps({
            "block_type": "full",
            "activity_name": "TestActivity",
            "activity_stage": "1",
            "stage_label": "TestStageLabel1",
            "question": "TestQuestion1",
            "activity_previous": "no",
        })
        request.body = data.encode('utf-8')
        response = self.xblock1.studio_submit(request)
        self.assertEqual(response.json_body["result"], "success")
        self.assertEqual(self.xblock1.block_type, "full")
        self.assertEqual(self.xblock1.activity_name, "TestActivity")
        self.assertEqual(self.xblock1.activity_stage, 1)
        self.assertEqual(self.xblock1.stage_label, "TestStageLabel1")
        self.assertEqual(self.xblock1.question, "TestQuestion1")
        self.assertEqual(self.xblock1.activity_previous, False)
        activity = IAAActivity.objects.get(id_course=COURSE_ID, activity_name=self.xblock1.activity_name)
        self.assertEqual(activity.activity_name, "TestActivity")
        self.assertEqual(activity.id_course, COURSE_ID)
        stage = IAAStage.objects.filter(activity=activity, stage_number=self.xblock1.activity_stage).values("stage_number", "stage_label")
        self.assertEqual(len(stage), 1)
        self.assertEqual(stage[0]["stage_number"], 1)
        self.assertEqual(stage[0]["stage_label"], "TestStageLabel1")



    def test_create_display(self):
        """
        Checks if a 'display' type XBlock was created successfully.
        """
        request = TestRequest()
        request.method = 'POST'
        data = json.dumps({
            "block_type": "full",
            "activity_name": "TestActivity",
            "activity_stage": "1",
            "stage_label": "TestStageLabel1",
            "question": "TestQuestion1",
            "activity_previous": "no",
        })
        request.body = data.encode('utf-8')
        response = self.xblock1.studio_submit(request)
        self.assertEqual(response.json_body["result"], "success")
        request2 = TestRequest()
        request2.method = 'POST'
        data2 = json.dumps({
            "block_type": "display",
            "activity_name_previous": "TestActivity",
            "activity_stage_previous": "1",
            "display_title": "TestDisplayTitle"
        })
        request2.body = data2.encode('utf-8')
        response2 = self.xblock2.studio_submit(request2)
        self.assertEqual(response2.json_body["result"], "success")
        self.assertEqual(self.xblock2.block_type, "display")
        self.assertEqual(self.xblock2.activity_name_previous, "TestActivity")
        self.assertEqual(self.xblock2.activity_stage_previous, 1)
        self.assertEqual(self.xblock2.display_title, "TestDisplayTitle")


    def test_create_summary(self):
        """
        Checks if a 'summary' type XBlock was created successfully.
        """
        request = TestRequest()
        request.method = 'POST'
        data = json.dumps({
            "block_type": "full",
            "activity_name": "TestActivity",
            "activity_stage": "1",
            "stage_label": "TestStageLabel1",
            "question": "TestQuestion1",
            "activity_previous": "no",
        })
        request.body = data.encode('utf-8')
        response = self.xblock1.studio_submit(request)
        self.assertEqual(response.json_body["result"], "success")
        request2 = TestRequest()
        request2.method = 'POST'
        data2 = json.dumps({
            "block_type": "summary",
            "activity_name": "TestActivity",
            "summary_text": "TestSummaryText"
        })
        request2.body = data2.encode('utf-8')
        response2 = self.xblock2.studio_submit(request2)
        self.assertEqual(response2.json_body["result"], "success")
        self.assertEqual(self.xblock2.block_type, "summary")
        self.assertEqual(self.xblock2.activity_name, "TestActivity")
        self.assertEqual(self.xblock2.summary_text, "TestSummaryText")


    def test_create_full_with_display(self):
        """
        Checks if a 'full' type XBlock, with a previous displayed answer, was created successfully.
        """
        request = TestRequest()
        request.method = 'POST'
        data = json.dumps({
            "block_type": "full",
            "activity_name": "TestActivity",
            "activity_stage": "1",
            "stage_label": "TestStageLabel1",
            "question": "TestQuestion1",
            "activity_previous": "no",
        })
        request.body = data.encode('utf-8')
        response = self.xblock1.studio_submit(request)
        self.assertEqual(response.json_body["result"], "success")
        request2 = TestRequest()
        request2.method = 'POST'
        data2 = json.dumps({
            "block_type": "full",
            "activity_name": "TestActivity",
            "activity_stage": "2",
            "stage_label": "TestStageLabel2",
            "question": "TestQuestion2",
            "activity_previous": "yes",
            "activity_name_previous": "TestActivity",
            "activity_stage_previous": "1",
            "display_title": "TestDisplayTitle"
        })
        request2.body = data2.encode('utf-8')
        response2 = self.xblock2.studio_submit(request2)
        self.assertEqual(response2.json_body["result"], "success")
        self.assertEqual(self.xblock2.block_type, "full")
        self.assertEqual(self.xblock2.activity_name_previous, "TestActivity")
        self.assertEqual(self.xblock2.activity_stage_previous, 1)
        self.assertEqual(self.xblock2.display_title, "TestDisplayTitle")


    # def test_make_submission(self):
    #     """
    #     Checks if a submission is sent correctly.
    #     """
    #     request = TestRequest()
    #     request.method = 'POST'
    #     data = json.dumps({
    #         "block_type": "full",
    #         "activity_name": "TestActivity",
    #         "activity_stage": "1",
    #         "stage_label": "TestStageLabel1",
    #         "question": "TestQuestion1",
    #         "activity_previous": "no",
    #     })
    #     request.body = data.encode('utf-8')
    #     response = self.xblock1.studio_submit(request)
    #     self.assertEqual(response.json_body["result"], "success")
    #     request2 = TestRequest()
    #     request2.method = 'POST'
    #     data2 = json.dumps({
    #         "submission": "TestSubmission"
    #     })
    #     request2.body = data2.encode('utf-8')
    #     response2 = self.xblock1.student_submit(request2)
    #     self.assertEqual(response2.json_body["result"], "success")
    #     activity = IAAActivity.objects.get(id_course=COURSE_ID, activity_name=self.xblock1.activity_name)
    #     stage = IAAStage.objects.get(activity=activity, stage_number=self.xblock1.activity_stage)
    #     submissions = IAASubmission.objects.filter(stage=stage).values("submission")
    #     self.assertEqual(len(submissions), 1)
    #     self.assertEqual(submissions[0]["submission"], "TestSubmission")







