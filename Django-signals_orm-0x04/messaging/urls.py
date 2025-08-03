from django.urls import path
from .views import delete_user, ThreadedMessagesView, UnreadMessagesView

urlpatterns = [
    path('delete-account/', delete_user, name='delete_user'),
    path('messages/threads/', ThreadedMessagesView.as_view(), name='threaded_messages'),
    path('messages/unread/', UnreadMessagesView.as_view(), name='unread_messages'),
]
