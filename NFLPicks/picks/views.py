from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Week, Game, Team, PlayerPick
from .nflData import updateGames, getCurrentWeekYear
from django.utils import timezone


def mainPage(request):
    return render(request, 'base.html')


@login_required
def getPicks(request):
    week, year = getCurrentWeekYear()
    week = Week.objects.get(week=week, year=year)
    games = Game.objects.filter(week=week)

    # Time to view data?
    # if timezone.now() > week.starts:
    #     return render(request, 'base.html',
    #                   context={"message": "Picks are closed for the week. Next weeks picks will become available on Monday"})

    return render(request, 'picks/choosePicks.html', context={"matches": games})


@login_required
def submitPicks(request):
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
    return HttpResponseRedirect('/viewPicks/')


@login_required
def getResults(request):
    week, year = getCurrentWeekYear()
    week = Week.objects.get(week=week, year=year)

    # Time to view data?
    if timezone.now() < week.starts:
        return render(request, 'picks/results.html',
                      context={"message": "Picks are still open. Results will appear after kickoff on Thursday"})

    updateGames()
    games = Game.objects.filter(week=week)
    users = User.objects.all()

    table = createTable(games=games, users=users)

    return render(request, 'picks/results.html', context={"table": table})

@login_required
def getUserPicks(request):
    week, year = getCurrentWeekYear()
    week = Week.objects.get(week=week, year=year)

    updateGames()
    games = Game.objects.filter(week=week)
    users = User.objects.all()
    table = createTable(games=games, users=[request.user])

    return render(request, 'picks/results.html', context={"table": table})

def createTable(games, users):
    table = []

    # Creates headers
    headers = [{"val": "Game", "header": True}]
    scores = [{"val": "Score","header": True}]
    spread = [{"val": "Spread", "header":True}]
    for game in games:
        headers.append({"val": game.__str__(), "header": True})

        # Spread
        spread_val = game.home.team_abbrev + ": " + str(game.spread)
        spread.append({"val": spread_val, "header": True})

        # Score
        home_score = game.home_score
        away_score = game.away_score
        if home_score != None and away_score != None:
            score = str(away_score) + " | " + str(home_score)
        else:
            try: #Server
                score = game.start_time.strftime("%a %-Ipm")
            except: #Windows
                score = game.start_time.strftime("%a %#Ipm")
        scores.append({"val": score, "header": True})

    table.append(headers)
    table.append(spread)
    table.append(scores)

    # Creates Played results
    for user in users:
        row = [{"val": user.get_full_name()}]
        for game in games:
            if PlayerPick.objects.filter(user=user, game=game).exists():
                pick = PlayerPick.objects.get(user=user, game=game)
                if game.winner:
                    row.append({"val": pick.pick.team_abbrev, "won": (pick.pick == game.winner)})
                else:
                    row.append({"val": pick.pick.team_abbrev})

            #Coould't find pick
            else:
                row.append({"val": ""})

        table.append(row)

    table = sorted(table, key=correct_guess)
    return table

def correct_guess(week):
    print(week)
    wrong = 0
    for game in week:
        if game.get("header"):
            return -1
        if game.get("won") == False or game.get('val') == "":
            wrong += 1

    return wrong
