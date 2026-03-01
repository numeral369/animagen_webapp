import logging
import threading
from django.shortcuts import get_object_or_404
from animagen.models import Session, Message, SessionHTML
from animagen.Animagen_Utils import AnimationGenerator

logger = logging.getLogger(__name__)


def generate_animation_task(session_guid: str, message_id: str) -> dict:
    try:
        session = get_object_or_404(Session, sessionGUID=session_guid)
        message = get_object_or_404(Message, id=message_id)
        print("Message content: ", message.content)
        generator = AnimationGenerator()
        result = generator.generate_animation(message.content)
        
        if result["status"] == "success":
            html_content = result["html_content"]
            
            session_html, created = SessionHTML.objects.update_or_create(
                session=session,
                defaults={"html_content": html_content}
            )
            
            message.isPending = False
            message.save()
            
            logger.info(f"Animation generated successfully for session {session_guid}")
            return {
                "status": "success",
                "session_html_id": session_html.id,
                "message_id": str(message.id),
            }
        else:
            message.isPending = False
            message.save()
            
            logger.error(f"Animation generation failed for session {session_guid}: {result['error']}")
            return {
                "status": "error",
                "error": result["error"],
            }
            
    except Exception as e:
        logger.exception(f"Exception in generate_animation_task for session {session_guid}: {str(e)}")
        
        try:
            message = get_object_or_404(Message, id=message_id)
            message.isPending = False
            message.save()
            
        except Exception:
            pass
        
        return {
            "status": "error",
            "error": str(e)
        }


def start_animation_generation(session_guid: str, user_message: str) -> str:

    session = get_object_or_404(Session, sessionGUID=session_guid)
    message = Message.objects.create(
        session=session,
        content=user_message,
        isPending=True
    )
    thread = threading.Thread(
        target=generate_animation_task,
        args=(session_guid, message.id),
        daemon=True
    )
    thread.start()
    thread_id = f"thread-{session_guid}-{message.id}"
    logger.info(f"Started animation generation thread {thread_id} for session {session_guid}")
    return message.id
