# Django Import
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from gameapp.models import Player, Result

# Python Import
import random
import logging
log = logging.getLogger(__name__)
# Create your views here.

def home(request):
    '''
    homepage and start game logic
    '''
    if request.method=='POST':
        playername = request.POST.get('name')
        if User.objects.filter(username__iexact=playername):
            messages.warning(request, 'This name already exists, please try another one.')
            return HttpResponseRedirect(request.path_info)
        create_user = User.objects.create(first_name=playername, username=playername)
        create_player = Player.objects.create(name=playername, user=create_user)
        return redirect('start_game')

    return render(request, 'index.html')


def game(request):
    '''
    Rock, paper and scissor logic
    '''
    gamelist = ['rock', 'paper', 'scissors']
    bot_action = random.choice(gamelist)
    user = Player.objects.all().last()
    result_status = None

    if request.method == 'POST':
        user_answer = request.POST.get('name')

        if user_answer == bot_action:
            messages.warning(request, f"Both players selected. It's a tie!")
            result_status = 'tie'
        elif user_answer == "rock":
            if bot_action == "scissors":
                messages.success(request, "Rock smashes scissors! You win!")
                result_status = 'win'
            else:
                messages.info(request, "Paper covers rock! You lose.")
                result_status = 'lose'
        elif user_answer == "paper":
            if bot_action == "rock":
                messages.success(request, "Paper covers rock! You win!")
                result_status = 'win'
            else:
                messages.info(request, "Scissors cuts paper! You lose.")
                result_status = 'lose'
        elif user_answer == "scissors":
            if bot_action == "paper":
                messages.success(request, "Scissors cuts paper! You win!")
                result_status = 'win'
            else:
                messages.info(request, "Rock smashes scissors! You lose.")
                result_status = 'lose'

        result = Result.objects.create(player=user, bot_move=bot_action, user_move=user_answer, status=result_status)

    return render(request, 'game.html', {'user':user, 'result_status':result_status})


def result(request):
    '''
    All users results
    '''
    res = Result.objects.all().order_by('-id')
    context = {'res':res}
    return render(request, 'result.html', context)