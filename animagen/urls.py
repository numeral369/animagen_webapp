from django.urls import path
from . import views

urlpatterns = [
    path("sessions/<uuid:session_guid>/", views.get_session, name="get_session"),
    path("sessions/<uuid:session_guid>/messages/", views.create_message, name="create_message"),
    path("sessions/<uuid:session_guid>/messages/<uuid:message_id>/", views.get_message, name="get_message"),
    path("sessions/<uuid:session_guid>/messages/<uuid:message_id>/generate-animation/", views.generate_animation, name="generate_animation"),
    path("sessions/<uuid:session_guid>/animation/", views.get_animation_html, name="get_animation_html"),
    path("sessions/", views.create_session, name="create_session"),
]
