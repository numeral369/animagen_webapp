from rest_framework import serializers
from .models import Session, Message, Attachment, SessionHTML


class AttachmentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = ["id", "name", "type", "url", "size"]

    def get_url(self, obj):
        if obj.file:
            return obj.file.url
        return ""


class MessageSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    attachments = AttachmentSerializer(many=True, read_only=True)
    isPending = serializers.BooleanField(source="is_pending", read_only=True)

    class Meta:
        model = Message
        fields = ["id", "content", "attachments", "timestamp", "isPending"]

    def get_id(self, obj):
        return str(obj.id)


class SessionSerializer(serializers.ModelSerializer):
    sessionGUID = serializers.UUIDField(read_only=True)
    createdAt = serializers.DateTimeField(read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    htmlContent = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = ["sessionGUID", "title", "createdAt", "messages", "htmlContent"]

    def get_htmlContent(self, obj):
        try:
            html_obj = obj.html_content
            return html_obj.html_content if html_obj else ""
        except SessionHTML.DoesNotExist:
            return ""


class SessionHTMLSerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = SessionHTML
        fields = ["id", "html_content", "createdAt", "updatedAt"]
