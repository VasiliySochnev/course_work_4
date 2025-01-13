from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse

from auth_users.models import User


@login_required
def block_user(self, pk):
    user = User.objects.get(pk=pk)
    user.is_active = {user.is_active: False, not user.is_active: True}[True]
    user.save()
    return redirect(reverse("users:user_list"))