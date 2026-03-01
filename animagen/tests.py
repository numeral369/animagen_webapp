from django.test import TestCase
from django.contrib.auth.models import User
from .models import Session, Message, SessionHTML
from .Animagen_Utils import AnimationGenerator
import os


class SessionHTMLModelTest(TestCase):
    def test_session_html_creation(self):
        session = Session.objects.create(title="Test Session")
        html_content = "<html><body>Test animation</body></html>"
        session_html = SessionHTML.objects.create(
            session=session,
            html_content=html_content
        )
        self.assertEqual(session_html.session, session)
        self.assertEqual(session_html.html_content, html_content)
        self.assertIsNotNone(session_html.created_at)
        self.assertIsNotNone(session_html.updated_at)


class AnimationGeneratorTest(TestCase):
    def setUp(self):
        self.api_key = os.environ.get("MISTRAL_API_KEY")
        if not self.api_key:
            self.skipTest("MISTRAL_API_KEY environment variable not set")

    def test_animation_generator_initialization(self):
        generator = AnimationGenerator(api_key=self.api_key)
        self.assertIsNotNone(generator.api_key)
        self.assertEqual(generator.model, "devstral-medium-latest")

    def test_html_extraction(self):
        generator = AnimationGenerator(api_key=self.api_key)
        
        test_cases = [
            "```html\n<html><body>test</body></html>\n```",
            "<html><body>test</body></html>",
            "```\n<html><body>test</body></html>\n```"
        ]
        
        for test_case in test_cases:
            html = generator._extract_html_code(test_case)
            self.assertIn("<html", html.lower())
            self.assertIn("</html>", html.lower())

    def test_html_validation(self):
        generator = AnimationGenerator(api_key=self.api_key)
        
        valid_html = "<!DOCTYPE html><html><head></head><body></body></html>"
        self.assertTrue(generator.validate_html(valid_html))
        
        invalid_html = "Not a valid HTML"
        self.assertFalse(generator.validate_html(invalid_html))

    def test_html_sanitization(self):
        generator = AnimationGenerator(api_key=self.api_key)
        
        dangerous_html = '<script src="javascript:alert(1)"></script><html><body>safe</body></html>'
        sanitized = generator.sanitize_html(dangerous_html)
        self.assertNotIn("javascript:alert", sanitized)
        self.assertIn("safe", sanitized)


class MessageAnimationIntegrationTest(TestCase):
    def setUp(self):
        self.session = Session.objects.create(title="Test Session")
        self.message = Message.objects.create(
            session=self.session,
            content="Create an animation of a bouncing ball",
            isPending=False
        )

    def test_message_creation(self):
        self.assertEqual(self.message.session, self.session)
        self.assertFalse(self.message.isPending)
        self.assertIn("animation", self.message.content.lower())

    def test_session_html_relationship(self):
        html_content = "<!DOCTYPE html><html><head><style>ball { animation: bounce 2s; }</style></head><body><div class='ball'></div></body></html>"
        session_html = SessionHTML.objects.create(
            session=self.session,
            html_content=html_content
        )
        
        self.assertEqual(session_html.session, self.session)
        self.assertEqual(self.session.html_content, session_html)
