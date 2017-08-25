from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Week, Game, Team, PlayerPick

def mainPage(request):
    return render(request, 'base.html')

@login_required
def getPicks(request):
    week = Week.objects.get(year=2016, week=1)
    games = Game.objects.filter(week=week)

    return render(request, 'picks/choosePicks.html', context={"matches": games})

@login_required
def submitPicks(request):
    picks = []
    print(request.POST)
    for i in range(1, 15):
        team_pick = request.POST.get(str(i))
        print(team_pick)

        # If the team pick is not None
        if team_pick:
            team = Team.objects.get(team_abbrev=team_pick)
            game = Game.objects.get(pk=i)
            picks.append(PlayerPick(user=request.user, game=game, pick=team))
        else:
            break
    PlayerPick.objects.bulk_create(picks)
    return render(request, 'base.html', context={"message": "Your picks have been saved!"})

