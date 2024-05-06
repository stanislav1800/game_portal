from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from bulletin_board.models import Profile
from .models import BaseRegisterForm
from django.contrib.auth.decorators import login_required


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

@login_required
def upgrade_me(request):
    user = request.user
    # authors_group = Group.objects.get(name='authors')
    # if not request.user.groups.filter(name='authors').exists():
    #     authors_group.user_set.add(user)
    # author= Profile.objects.filter(user=user)
    # if not author:
    Profile.objects.create(user=user)
    return redirect('/')