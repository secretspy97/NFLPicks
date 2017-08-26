from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Week, Game, Team, PlayerPick

def mainPage(request):
    return render(request, 'base.html')

@login_required
def getPicks(request):
    week = Week.objects.get(year=2017, week=-2)
    games = Game.objects.filter(week=week)

    return render(request, 'picks/choosePicks.html', context={"matches": games})

@login_required
def submitPicks(request):
    picks = []
    print(request.POST)
    for i in range(1, 20):
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

@login_required
def getResults(request):
    week = Week.objects.get(year=2017, week=-2)
    games = Game.objects.filter(week=week)
    users = User.objects.all()

    table = []

    # Creates headers
    row = [""]
    for game in games:
        row.append({"val": game.__str__()})
    table.append(row)

    # Creates Played results
    for user in users:
        row=[{"val": user.get_full_name()}]
        for game in games:
            pick = PlayerPick.objects.get(user=user, game=game)
            if game.winner:
                row.append({"val": pick.pick.team_abbrev, "won":(pick.pick == game.winner)})
            else:
                row.append({"val": pick.pick.team_abbrev})

        table.append(row)

    print(table)
    return render(request, 'picks/results.html', context={"table": table})