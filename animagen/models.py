import uuid
from django.db import models
from django.core.validators import FileExtensionValidator


class Session(models.Model):
    sessionGUID = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=255, default="New Session")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-createdAt"]

    def __str__(self):
        return f"{self.title} ({self.sessionGUID})"


class Message(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    session = models.ForeignKey(Session, related_name="messages", on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    isPending = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.content[:50]}..."


class Attachment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    message = models.ForeignKey(Message, related_name="attachments", on_delete=models.CASCADE)
    file = models.FileField(
        upload_to="attachments/%Y/%m/%d/",
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"])
        ]
    )
    name = models.CharField(max_length=255)
    size = models.BigIntegerField()
    uploadedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploadedAt"]

    def __str__(self):
        return self.name


class SessionHTML(models.Model):
    session = models.OneToOneField(Session, related_name="html_content", on_delete=models.CASCADE)
    html_content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Session HTML"
        verbose_name_plural = "Session HTMLs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"HTML for {self.session.title}"
