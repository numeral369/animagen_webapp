from django.test import TestCase
from django.contrib.auth.models import User
from .models import Session, Message, SessionHTML
from unittest.mock import Mock, patch
import os


class AnimationTaskTest(TestCase):
    def setUp(self):
        self.session = Session.objects.create(title="Test Session")
        self.user_message = Message.objects.create(
            session=self.session,
            content="Create an animation of a bouncing ball",
            isPending=True
        )

    @patch('animagen.tasks.AnimationGenerator')
    def test_generate_animation_creates_assistant_message_success(self, MockGenerator):
        mock_generator_instance = Mock()
        mock_generator_instance.generate_animation.return_value = {
            "status": "success",
            "html_content": "<html><body>Animation</body></html>",
            "model_used": "devstral-medium-latest"
        }
        MockGenerator.return_value = mock_generator_instance

        from animagen.tasks import generate_animation_task

        result = generate_animation_task(
            str(self.session.sessionGUID),
            str(self.user_message.id)
        )

        self.assertEqual(result["status"], "success")
        self.user_message.refresh_from_db()
        self.assertFalse(self.user_message.isPending)

        assistant_messages = Message.objects.filter(
            session=self.session,
            role="assistant"
        )
        self.assertEqual(assistant_messages.count(), 1)
        assistant_message = assistant_messages.first()
        self.assertIn("Animation generated successfully", assistant_message.content)
        self.assertIn("assistant_message_id", result)

    @patch('animagen.tasks.AnimationGenerator')
    def test_generate_animation_creates_assistant_message_error(self, MockGenerator):
        mock_generator_instance = Mock()
        mock_generator_instance.generate_animation.return_value = {
            "status": "error",
            "error": "API error",
            "html_content": ""
        }
        MockGenerator.return_value = mock_generator_instance

        from animagen.tasks import generate_animation_task

        result = generate_animation_task(
            str(self.session.sessionGUID),
            str(self.user_message.id)
        )

        self.assertEqual(result["status"], "error")
        self.user_message.refresh_from_db()
        self.assertFalse(self.user_message.isPending)

        assistant_messages = Message.objects.filter(
            session=self.session,
            role="assistant"
        )
        self.assertEqual(assistant_messages.count(), 1)
        assistant_message = assistant_messages.first()
        self.assertIn("Failed to generate animation", assistant_message.content)
        self.assertIn("API error", assistant_message.content)

    @patch('animagen.tasks.AnimationGenerator')
    def test_generate_animation_exception_creates_assistant_message(self, MockGenerator):
        mock_generator_instance = Mock()
        mock_generator_instance.generate_animation.side_effect = Exception("Unexpected error")
        MockGenerator.return_value = mock_generator_instance

        from animagen.tasks import generate_animation_task

        result = generate_animation_task(
            str(self.session.sessionGUID),
            str(self.user_message.id)
        )

        self.assertEqual(result["status"], "error")
        self.user_message.refresh_from_db()
        self.assertFalse(self.user_message.isPending)

        assistant_messages = Message.objects.filter(
            session=self.session,
            role="assistant"
        )
        self.assertEqual(assistant_messages.count(), 1)
        assistant_message = assistant_messages.first()
        self.assertIn("Error during animation generation", assistant_message.content)
        self.assertIn("Unexpected error", assistant_message.content)

    @patch('animagen.tasks.AnimationGenerator')
    def test_generate_animation_creates_session_html(self, MockGenerator):
        mock_generator_instance = Mock()
        test_html = "<html><body>Test Animation</body></html>"
        mock_generator_instance.generate_animation.return_value = {
            "status": "success",
            "html_content": test_html,
            "model_used": "devstral-medium-latest"
        }
        MockGenerator.return_value = mock_generator_instance

        from animagen.tasks import generate_animation_task

        result = generate_animation_task(
            str(self.session.sessionGUID),
            str(self.user_message.id)
        )

        session_html = SessionHTML.objects.get(session=self.session)
        self.assertEqual(session_html.html_content, test_html)
        self.assertEqual(result["session_html_id"], session_html.id)
