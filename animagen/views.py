import os
import re
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Session, Message, Attachment
from .serializers import SessionSerializer, MessageSerializer, AttachmentSerializer
from django.conf import settings
from .tasks import start_animation_generation

MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]
ANIMATION_KEYWORDS = ["animation", "animate", "show me", "create", "generate", "make", "visualize", "demonstrate", "illustrate"]


@api_view(["GET"])
@permission_classes([AllowAny])
def get_session(request, session_guid):
    try:
        session = get_object_or_404(Session, sessionGUID=session_guid)
        serializer = SessionSerializer(session)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def create_message(request, session_guid):
    try:
        session = get_object_or_404(Session, sessionGUID=session_guid)
        
        content = request.POST.get("content", "").strip()
        files = request.FILES.getlist("files")
        
        if not content and not files:
            return Response(
                {"error": "Message must contain content or files"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        for file in files:
            file_ext = file.name.split(".")[-1].lower()
            if file_ext not in ALLOWED_EXTENSIONS:
                return Response(
                    {"error": f"Invalid file type: {file.name}. Only JPG, PNG, and WEBP are allowed"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if file.size > MAX_FILE_SIZE:
                return Response(
                    {"error": f"File too large: {file.name}. Maximum size is 10MB"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Attachment.objects.create(
            #     message=message,
            #     file=file,
            #     name=file.name,
            #     size=file.size
            # )
        
        try:
            message_id = start_animation_generation(str(session.sessionGUID), str(content))
            httpStatus = status.HTTP_201_CREATED
        except Exception as e:
            logger = __import__('logging').getLogger(__name__)
            logger.error(f"Failed to start animation generation: {str(e)}")
            httpStatus = status.HTTP_500_INTERNAL_SERVER_ERROR
            
        #return the message as response
        userMessage = Message.objects.get(id=message_id)

        return Response(
            {"message": {"id": userMessage.id, 
                        "content": userMessage.content, 
                        "timestamp": userMessage.timestamp}},
            status=httpStatus
        )
        
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def create_session(request):
    try:
        title = request.data.get("title", "New Session")
        session = Session.objects.create(title=title)
        serializer = SessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def generate_animation(request, session_guid):
    try:
        session = get_object_or_404(Session, sessionGUID=session_guid)

        user_message = request.data.get("content", "").strip()
        print("User message: ", user_message)
        
        if not user_message:
            return Response(
                {"error": "Message content is required for animation generation"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            #message_id will be used by the frontend to poll for the animation status
            message_id = start_animation_generation(str(session.sessionGUID), str(user_message))
            
            return Response(
                {
                    "status": "started",
                    "message_id": message_id,
                    "message": "Animation generation started"
                },
                status=status.HTTP_202_ACCEPTED
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to start animation generation: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_message(request, session_guid, message_id):
    try:
        session = get_object_or_404(Session, sessionGUID=session_guid)
        message = get_object_or_404(Message, id=message_id, session=session)
        
        serializer = MessageSerializer(message)
        
        html_content = None
        if not message.isPending:
            try:
                session_html = session.html_content
                html_content = session_html.html_content if session_html else None
            except Exception:
                html_content = None
        
        return Response(
            {
                "message": serializer.data,
                "isPending": message.isPending,
                "htmlContent": html_content
            },
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_animation_html(request, session_guid):
    try:
        session = get_object_or_404(Session, sessionGUID=session_guid)
        
        try:
            session_html = session.html_content
            html_content = session_html.html_content
            
            if not html_content:
                return Response(
                    {"error": "No animation HTML content found for this session"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            return Response(
                {"html_content": html_content},
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {"error": "No animation HTML content found for this session"},
                status=status.HTTP_404_NOT_FOUND
            )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
