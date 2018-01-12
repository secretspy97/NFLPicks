from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .models import Week, Game, Team, PlayerPick, MondayTieBreaker
from .nflData import updateGames, getCurrentWeekYear
from django.utils import timezone
import math

def mainPage(request):
    return render(request, 'base.html')


@login_required
def getPicks(request):
    week, year = getCurrentWeekYear()
    week = Week.objects.get(week=week, year=year)
    games = Game.objects.filter(week=week)

    # Time to view data?
    if timezone.now() > week.starts:
        return render(request, 'base.html',
                      context={"message": "Picks are closed for the week. Next weeks picks will become available on Tuesday"})

    return render(request, 'picks/choosePicks.html', context={"matches": games})


@login_required
def submitPicks(request):
    for key in request.POST:
        if key.isdigit():
            team_pick = request.POST.get(key)
        else:
            team_pick = None

        # If the team pick is not None
        if team_pick:
            team = Team.objects.get(team_abbrev=team_pick)
            game = Game.objects.get(pk=int(key))
            playerPick, create = PlayerPick.objects.get_or_create(user=request.user, game=game)
            playerPick.pick = team
            playerPick.save()

    # Tiebreaker
    tiebreaker = request.POST.get("tiebreaker")
    if playerPick:
        week = playerPick.game.week
        monday_tie, created = MondayTieBreaker.objects.get_or_create(user=request.user, week=week)
        monday_tie.totalScore=tiebreaker
        monday_tie.save()

    return HttpResponseRedirect('/viewPicks/')


@login_required
def getResults(request):
    updateGames()
    week, year = getCurrentWeekYear()
    week = Week.objects.get(week=week, year=year)
    return getPreviousResults(request, week.pk)


@login_required
def getPreviousResults(request, week):
    if Week.objects.filter(pk=week).exists():
        week = Week.objects.get(pk=week)
    else:
        return getResults(request)

    # Time to view data?
    if timezone.now() < week.starts:

        return render(request, 'picks/results.html',
                      context={"message": "Picks are still open. Results will appear after kickoff", "week": week.week, "week_id": week.pk})

    users = User.objects.all()

    table = createTable(week=week, users=users)

    return render(request, 'picks/results.html', context={"week": week.week, "week_id": week.pk, "table": table})


@login_required
def getUserPicks(request):
    week, year = getCurrentWeekYear()
    week = Week.objects.get(week=week, year=year)

    table = createTable(week=week, users=[request.user])

    return render(request, 'picks/results.html', context={"week": week.week, "table": table})


def createTable(week, users):
    games = Game.objects.filter(week=week)

    table = []

    # Creates headers
    headers = [{"val": "Game", "header": True}]
    scores = [{"val": "Score","header": True}]
    fav = [{"val": "Favorite", "header": True}]
    spread = [{"val": "Spread", "header": True}]
    under_dog = [{"val": "Underdog", "header": True}]
    for game in games:
        headers.append({"val": game.__str__(), "header": True})

        # Fav
        # Spread
        # Underdog
        spread.append({"val": abs(game.spread), "header": True})

        if game.favorite:
            fav.append({"val": game.favorite.team_abbrev, "header": True})
            if game.favorite == game.home:
                under_dog.append({"val": game.away.team_abbrev, "header": True})
            else:
                under_dog.append({"val": game.home.team_abbrev, "header": True})
        else:
            under_dog.append({"val": "--", "header": True})
            fav.append({"val": "--", "header": True})

        # Score
        home_score = game.home_score
        away_score = game.away_score
        if home_score != None and away_score != None:
            score = str(away_score) + " | " + str(home_score)
        else:
            score = (game.start_time - timezone.timedelta(hours=4)).strftime('%a')

        scores.append({"val": score, "header": True})

    # Tie Breaker
    headers.append({"val": "Monday Tiebreaker", "header": True})
    spread.append({"val": "", "header": True})
    fav.append({"val": "", "header": True})
    scores.append({"val": "", "header": True})
    under_dog.append({"val": "", "header": True})

    table.append(headers)
    table.append(fav)
    table.append(spread)
    table.append(under_dog)
    table.append(scores)

    # Creates Played results
    for user in users:
        row = [{"val": user.first_name[0] + " " + user.last_name}]
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

        # Monday Tiebreaker

        if MondayTieBreaker.objects.filter(user=user, week=week).exists():
            tiebreaker = MondayTieBreaker.objects.get(user=user, week=week)
            row.append({"val": tiebreaker.totalScore})
        else:
            row.append({"val": ""})

        table.append(row)

    table = sorted(table, key=correct_guess)
    return table


def correct_guess(week):
    wrong = 0
    for game in week:
        if game.get("header"):
            return -1
        if game.get("won") == False or game.get('val') == "":
            wrong += 1

    return wrong


@login_required
def getSpread(request):
    user = request.user
    if user.groups.filter(name='modifySpread').exists():
        week, year = getCurrentWeekYear()
        week = Week.objects.get(week=week, year=year)
        games = Game.objects.filter(week=week)

        return render(request, 'picks/setSpread.html', context={"matches": games})
    else:
        return render(request, 'base.html', context={"message": "Unauthorized"})

@login_required
def setSpread(request):
    user = request.user
    if user.groups.filter(name='modifySpread').exists():
        for key in request.POST:
            if key.isdigit():
                spread = request.POST.get(key)
            else:
                spread = None

            # If the team pick is not None
            if spread:
                game = Game.objects.get(pk=int(key))

                fav_abbrev = request.POST.get(key + "_fav")
                fav_team = Team.objects.get(team_abbrev=fav_abbrev)
                game.favorite = fav_team

                if fav_team == game.home:
                    spread = -float(spread)
                game.spread = spread

                game.save()

        return render(request, 'base.html', context={"message": "The spread has been updated"})
    else:
        return render(request, 'base.html', context={"message": "Unauthorized"})
