from django.urls import path
from . import views

urlpatterns=[
    path('reply_look/',views.reply_look),
    path('reply_generate/',views.reply_generate),
    path('send_text_and_reply_generate/',views.send_text_and_reply_generate),
]   