from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.db import connection
from .models import Message
import datetime

from app.forms.SignUpForm import SignUpForm


def homePageView(request):
	user = request.user
	 
	return render(request, 'home.html')

def userPage(request, username):
	if request.method == 'POST':
		u = User.objects.get(username=username)
		u.set_password(request.POST.get('newPassword'))
		u.save()
		login(request, u)
		return redirect('./'+username)

	if request.method == 'GET':
		if (request.user.username == username):
			return render(request, 'user.html', {'user': request.user})


def registerView(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('home')
	else:
		form = SignUpForm()

	return render(request, 'register.html', {'form': form})


@login_required
def messageView(request, username):
	if request.method == 'POST':
		target = User.objects.get(username=request.POST.get('to'))
		Message.objects.create(source=request.user, target=target, content=request.POST.get('content'))
		return redirect('./messages')

	if request.method == 'GET':
		messages = Message.objects.filter(
			Q(source=request.user) | Q(target=request.user))
		users = User.objects.exclude(pk=request.user.id)
		return render(request, 'messages.html', {'messages': messages, 'users': users})
