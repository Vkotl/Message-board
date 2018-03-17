from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth import login
from django.views import generic
from django.utils import timezone
from django.http import HttpResponseRedirect
from .forms import MessageForm, LoginForm, RegisterForm


def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Form returned from clean() is returned already authenticated.
            user = User.objects.get(username=form.cleaned_data['username'])
            # Avoid the need to authenticate, due to the fact authentication is done in the form.
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return HttpResponseRedirect(r'/chat/')
        # Error in username or password entered.
        return render(request, r'registration/login.html', {'form': LoginForm(), 'error': form.non_field_errors})
    # If the request wasn't made with post method.
    return render(request, r'registration/login.html', {'form': LoginForm()})


def registerView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Form returned from clean() is returned already authenticated.
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Form verifies username is not already used and passwords were entered correctly.
            user = User(username=username)
            user.set_password(password)
            user.save()
            return HttpResponseRedirect(r'/chat/login/')
        return render(request, r'registration/register.html', {'form': RegisterForm(), 'error': form.non_field_errors})
    else:
        form = RegisterForm()
    return render(request, r'registration/register.html', {'form': form})


class IndexView(generic.ListView):
    template_name = 'chat/index.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        return User.objects.all()

@login_required(redirect_field_name=None)
def chat_room(request, user_id):
    contact = get_object_or_404(User, id=user_id)
    context = {}
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = Message(sender=request.user, mess_receiver=contact,
                                  content=form.cleaned_data['content'], pub_date=timezone.now())
            new_message.save()
        else:
            context.update({'error': form.non_field_errors})

    message_list = Message.objects.filter((Q(sender=contact) & Q(mess_receiver=request.user))
                                          | (Q(mess_receiver=contact) & Q(sender=request.user))).order_by('pub_date')
    if message_list is not None:
        date = 0
        msg_list=[]
        for (i,message) in enumerate(message_list):
            if message.pub_date.date() != date:
                if message.pub_date.date() == timezone.now().date():
                    msg_list += ['\n\n<div class="Date">Today</div>']
                else:
                    msg_list += ['\n\n<div class="Date">' + '{}.{}.{}'.format(message.pub_date.day, message.pub_date.month,
                                                                              message.pub_date.year) + "</div>"]
                msg_list[i] += message.__str__().replace(request.user.username.__str__(), 'You', 1)
                date = message.pub_date.date()
            else:
                msg_list += ['\n\n' + message.__str__().replace(request.user.username.__str__(), 'You', 1)]

        # To replace the username of the current user with the word 'You' when chat displayed.
        message_list = msg_list
    context.update({'message_list': message_list, 'other': contact, 'form': MessageForm()})
    return render(request, r'chat/room.html', context)