from django.urls import path
from django.views.decorators.cache import cache_page

from mailing_service.apps import MailingServiceConfig
from mailing_service.services import block_mailing, run_mail
from mailing_service.views import (Contacts, MailingAttemptCreateView,
                                   MailingAttemptListView, MailingCreateView,
                                   MailingDeleteView, MailingDetailView,
                                   MailingListView, MailingUpdateView,
                                   MessageCreateView, MessageDeleteView,
                                   MessageDetailView, MessageListView,
                                   MessageUpdateView, ReceiveMailCreateView,
                                   ReceiveMailDetailView,
                                   ReceiveMailingDeleteView,
                                   ReceiveMailListView, ReceiveMailUpdateView,
                                   homeView)

app_name = MailingServiceConfig.name

urlpatterns = [
    path("home/", homeView.as_view(), name="home"),
    path("contacts/", cache_page(60)(Contacts.as_view()), name="contacts"),
    path("message/", MessageListView.as_view(), name="message"),
    path("mailing/", MailingListView.as_view(), name="mailing_list"),
    path("mailing/<int:pk>/run_mail/", run_mail, name="run_mail"),
    path(
        "mailing/<int:pk>/detail/", MailingDetailView.as_view(), name="mailing_detail"
    ),
    path(
        "message/<int:pk>/detail/", MessageDetailView.as_view(), name="message_detail"
    ),
    path(
        "message/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"
    ),
    path("message/<int:pk>/edit/", MessageUpdateView.as_view(), name="message_update"),
    path("mailing/new/", MailingCreateView.as_view(), name="mailing_create"),
    path("message/new/", MessageCreateView.as_view(), name="message_create"),
    path("mailing/<int:pk>/edit/", MailingUpdateView.as_view(), name="mailing_update"),
    path(
        "mailing/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"
    ),
    path("receivemail/", ReceiveMailListView.as_view(), name="receivemail_list"),
    path(
        "receivemail/<int:pk>/detail/",
        cache_page(60)(ReceiveMailDetailView.as_view()),
        name="receivemail_detail",
    ),
    path(
        "receivemail/create/", ReceiveMailCreateView.as_view(), name="receivemail_form"
    ),
    path(
        "receivemail/<int:pk>/edit/",
        ReceiveMailUpdateView.as_view(),
        name="receivemail_update",
    ),
    path(
        "receivemail/<int:pk>/delete/",
        ReceiveMailingDeleteView.as_view(),
        name="receivemail_delete",
    ),
    path("send/", MailingAttemptListView.as_view(), name="send_list"),
    path("send/create/", MailingAttemptCreateView.as_view(), name="send_create"),
    path("attempt/", MailingAttemptListView.as_view(), name="attempt"),
    path("block_mailing/<int:pk>", block_mailing, name="block_mailing"),
]
