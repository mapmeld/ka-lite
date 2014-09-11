"""
These use a web-browser, along selenium, to simulate user actions.
"""
import time
import glob
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from django.conf import settings
logging = settings.LOG
from django.core.urlresolvers import reverse
from django.utils import unittest

from .base import KALiteDistributedBrowserTestCase, KALiteDistributedWithFacilityBrowserTestCase


PLAYLIST_ID = "g3_p1"

class QuizTest(KALiteDistributedWithFacilityBrowserTestCase):

    """
    Test tests.
    """
    student_username = 'test_student'
    student_password = 'socrates'

    def setUp(self):
        """
        Create a student, log the student in, and go to the playlist page.
        """
        super(QuizTest, self).setUp()
        self.student = self.create_student(facility_name=self.facility_name)
        self.browser_login_student(
            self.student_username,
            self.student_password,
            facility_name=self.facility_name,
        )

        self.browse_to(
            self.live_server_url +
            reverse("view_playlist", kwargs={"playlist_id": PLAYLIST_ID}))
        self.browser_check_django_message(num_messages=0)

    def test_quiz_first_answer_correct_not_registered(self):
        """
        Log an answer as correct on a new QuizDataLog Model and check
        that it produces the right values on its total_correct and response_log
        fields.
        """

        self.browser.execute_script("quizlog = new QuizLogModel();")
        self.browser.execute_script("quizlog.add_response_log_item({correct: true});")
        self.assertEqual(self.browser.execute_script("return quizlog.get('total_correct')"), 1)
        self.assertEqual(self.browser.execute_script("return quizlog._response_log_cache[0]"), 1)
