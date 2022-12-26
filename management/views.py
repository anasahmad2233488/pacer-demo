from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404
from django.shortcuts import redirect

from django.contrib.auth.models import User
from score.models import Score

def IndexView(request):
    template = loader.get_template('index.html')
    context = {
        'form': AuthenticationForm
    }
    return HttpResponse(template.render(context, request))

@login_required
def DashboardView(request):
    template = loader.get_template('dashboard.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required
def UserView(request):
    users = list(User.objects.all())
    template = loader.get_template('users.html')
    context = {
        'users': users,
    }
    return HttpResponse(template.render(context, request))

@login_required
def UserEditView(request, pk):    
    users = list(User.objects.filter(id=pk))

    if len(users) == 0:
        raise Http404
    else:
        user = users[0]

    if request.method == 'GET':
        template = loader.get_template('user-edit.html')
        context = {
            'user': user,
        }
        return HttpResponse(template.render(context, request))
    
    elif request.method == 'POST':
        data = request.POST

        is_superuser = False
        is_staff = False
        is_active = False

        if 'is_superuser' in data.keys():
            is_superuser = True

        if 'is_staff' in data.keys():
            is_staff = True

        if 'is_active' in data.keys():
            is_active = True

        user.username = data['username']
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['email']

        user.is_superuser = is_superuser
        user.is_staff = is_staff
        user.is_active = is_active

        user.save()
        return redirect('user-edit', pk=pk)

@login_required
def ScoresView(request):
    scores = list(Score.objects.all())
    template = loader.get_template('scores.html')
    context = {
        'scores': scores,
    }
    return HttpResponse(template.render(context, request))

@login_required
def ScoresEditView(request, pk):
    scores = list(Score.objects.filter(id=pk))

    if len(scores) == 0:
        raise Http404
    else:
        score = scores[0]

    if request.method == 'GET':
        template = loader.get_template('score-edit.html')
        context = {
            'score': score,
        }
        return HttpResponse(template.render(context, request))
    
    elif request.method == 'POST':
        data = request.POST

        score.score_a = data['score_a']
        score.score_b = data['score_b']
        score.score_c = data['score_c']
        
        score.save()
        return redirect('score-edit', pk=pk)