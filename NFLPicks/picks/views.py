from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Week, Game, Team, PlayerPick
from .nflData import updateGames, getCurrentWeekYear

def mainPage(request):
    updateGames()
    return render(request, 'base.html')

@login_required
def getPicks(request):
    week, year = getCurrentWeekYear()
    week = Week.objects.get(week=week, year=year)
    games = Game.objects.filter(week=week)

    return render(request, 'picks/choosePicks.html', context={"matches": games})

@login_required
def submitPicks(request):
    print(request.POST)
    for key in request.POST:
        if key.isdigit():
            team_pick = request.POST.get(key)
        else:
            team_pick = None
        print(team_pick)

        # If the team pick is not None
        if team_pick:
            team = Team.objects.get(team_abbrev=team_pick)
            game = Game.objects.get(pk=int(key))
            playerPick, create = PlayerPick.objects.get_or_create(user=request.user, game=game)
            playerPick.pick = team
            playerPick.save()
    return render(request, 'base.html', context={"message": "Your picks have been saved!"})

@login_required
def getResults(request):
    week, year = getCurrentWeekYear()
    week = Week.objects.get(week=week, year=year)
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
            if PlayerPick.objects.filter(user=user, game=game).exists():
                pick = PlayerPick.objects.get(user=user, game=game)
                if game.winner:
                    row.append({"val": pick.pick.team_abbrev, "won":(pick.pick == game.winner)})
                else:
                    row.append({"val": pick.pick.team_abbrev})

        #     Coulnd't find pick
            else:
                row.append({"val": ""})

        table.append(row)

    table = sorted(table, key=correct_guess)
    print(table)
    return render(request, 'picks/results.html', context={"table": table})

def correct_guess(week):
    print(week)
    wrong = 0
    for game in week:
        if isinstance(game, str):
            return -1
        if game.get("won") == False or game.get('val') == "":
            wrong += 1

    return wrong