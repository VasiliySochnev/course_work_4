from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from mailing_service.models import (AttemptMailing, Mailing, Message,
                                    ReceiveMail)

from .forms import (MailingForm, MailingModeratorForm, MessageForm,
                    ReceiveMailForm, ReceiveMailModeratorForm)


def base(request):

    return render(request, "base.html")


class homeView(TemplateView):
    template_name = "mailing_service/mailing/home.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = "Главная"
        context_data["count_mailing"] = len(Mailing.objects.all())
        active_mailings_count = Mailing.objects.filter(status="Создано").count()
        context_data["active_mailings_count"] = active_mailings_count
        unique_clients_count = ReceiveMail.objects.distinct().count()
        context_data["unique_clients_count"] = unique_clients_count
        return context_data


class Contacts(TemplateView):

    template_name = "mailing_service/mailing/contacts.html"

    def contacts(request):
        if request.method == "POST":
            name = request.POST.get("name")
            message = request.POST.get("message")
            return HttpResponse(f"Спасибо, {name}! {message} Сообщение получено.")
        return render(request, "mailing_service/mailing/contacts.html")


class Messages(TemplateView):

    template_name = "mailing_service/mailing/message_list.html"


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailing_service/mailing/mailing_list.html"

    def get_queryset(self, *args, **kwargs):
        if (
            self.request.user.is_superuser
            or self.request.user.groups.filter(name="Менеджеры").exists()
        ):
            return super().get_queryset()
        elif self.request.user.groups.filter(name="Пользователи").exists():
            return super().get_queryset().filter(owner=self.request.user)
        raise PermissionDenied


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing_service/mailing/mailing_form.html"
    success_url = reverse_lazy("mailing_service:mailing_list")

    def form_valid(self, form):
        recipient = form.save()
        recipient.owner = self.request.user
        recipient.save()
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing_service/mailing/mailing_detail.html"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if (
            self.request.user.groups.filter(name="Менеджеры")
            or self.request.user.is_superuser
        ):
            return self.object
        if (
            self.object.owner != self.request.user
            and not self.request.user.is_superuser
        ):
            raise PermissionDenied
        return self.object


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing_service/mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_form_class(self):
        user = self.request.user
        if user.has_perm("mailing.set_is_active"):
            return MailingModeratorForm
        return MailingForm


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailing_service/mailing/mailing_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")


class ReceiveMailListView(ListView):
    model = ReceiveMail
    template_name = "mailing_service/mailing/receivemail_list.html"


class ReceiveMailDetailView(LoginRequiredMixin, DetailView):
    model = ReceiveMail
    form_class = ReceiveMailModeratorForm
    template_name = "mailing_service/mailing/mailing_detail.html"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser:
            return self.object
        if (
            self.object.owner != self.request.user
            and not self.request.user.is_superuser
        ):
            raise PermissionDenied
        return self.object


class ReceiveMailCreateView(LoginRequiredMixin, CreateView):
    model = ReceiveMail
    form_class = ReceiveMailForm
    template_name = "mailing_service/mailing/receivemail_form.html"
    success_url = reverse_lazy("mailing:receivemail_list")

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()

        return super().form_valid(form)


class ReceiveMailUpdateView(LoginRequiredMixin, UpdateView):
    model = ReceiveMail
    form_class = ReceiveMailForm
    template_name = "mailing_service/mailing/receivemail_form.html"
    success_url = reverse_lazy("mailing:receivemail_list")

    def get_form_class(self):
        user = self.request.user
        if user.has_perm("mailing.can_blocking_client"):
            return ReceiveMailModeratorForm
        return ReceiveMailForm


class ReceiveMailingDeleteView(LoginRequiredMixin, DeleteView):
    model = ReceiveMail
    template_name = "mailing_service/mailing/receivemail_delete.html"
    success_url = reverse_lazy("mailing:receivemail_list")


class MessageListView(ListView):
    model = Message
    form_class = MessageForm
    template_name = "mailing_service/mailing/message_list.html"

    def get_queryset(self, *args, **kwargs):

        queryset = super().get_queryset()
        return queryset


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    form_class = MessageForm
    template_name = "mailing_service/mailing/message_detail.html"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.request.user == self.object.owner:
            raise PermissionDenied
        return self.object


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing_service/mailing/message_form.html"
    success_url = reverse_lazy("mailing:message")

    def form_valid(self, form):
        recipient = form.save()
        recipient.owner = self.request.user
        recipient.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message")
    template_name = "mailing_service/mailing/message_form.html"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.request.user == self.object.owner:
            raise PermissionDenied
        return self.object


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:message")
    template_name = "mailing_service/mailing/message_delete.html"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.request.user == self.object.owner:
            raise PermissionDenied
        return self.object


class MailingAttemptCreateView(LoginRequiredMixin, CreateView):
    model = AttemptMailing

    def form_valid(self, form):
        recipient = form.save()
        recipient.owner = self.request.user
        recipient.save()
        return super().form_valid(form)


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = AttemptMailing
    template_name = "mailing_service/mailing/attemptmailing_list.html"

    def get_queryset(self, *args, **kwargs):
        if self.request.user:
            return super().get_queryset()
        elif self.request.user.groups.filter(name="Пользователи").exists():
            return super().get_queryset().filter(owner=self.request.user)
        raise PermissionDenied
