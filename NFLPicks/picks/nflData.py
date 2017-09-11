import requests
import datetime
import json
from .models import Week, Game, Team

def getData():
    url = "http://www.nfl.com/liveupdate/scorestrip/scorestrip.json"
    response = requests.request("GET", url)
    json_response = response.text
    json_response = ','.join(x or '-1' for x in json_response.split(','))
    json_response = json.loads(json_response)
    return json_response

def updateGames():
    json_response = getData()
    games = json_response.get("ss")
    if len(games) > 0:
        games_start = getDate(games[0])
        games_end = getDate(games[-1])
        year = games[0][13]
        week = games[0][12]
        if Week.objects.filter(year=year, week=week).exists():
            game_week = Week.objects.get(year=year, week=week)
            created = False
        else:
            game_week, created = Week.objects.get_or_create(year=year, week=week, starts=games_start, ends=games_end)

        # Creates inital games:
        game_objects = []
        if created:
            for game in games:
                home = getTeam(game[6])
                away = getTeam(game[4])
                spread = 0
                week = game_week
                start_time = getDate(game)
                game_objects.append(Game(week=week, start_time=start_time, home=home, away=away, spread=spread))
            Game.objects.bulk_create(game_objects)

        # Update scores
        for game in games:
            home = getTeam(game[6])
            home_score = int(game[7])
            away = getTeam(game[4])
            away_score = int(game[5])
            status = game[2]
            week = game_week
            game_object = Game.objects.get(week=week, home=home, away=away)
            if status == "Final":
                game_object.home_score = home_score
                game_object.away_score = away_score
                spread = game_object.spread

                if((home_score + spread) > away_score):
                    winner = home
                else:
                    winner = away
                game_object.winner = winner

                game_object.save()

def getCurrentWeekYear():
    data = getData()
    game = data.get("ss")[0]
    year = game[13]
    week = game[12]
    return week, year

def getTeam(team_abbrev):
    if Team.objects.filter(team_abbrev=team_abbrev).exists():
        return Team.objects.get(team_abbrev=team_abbrev)
    else:
        print("******TEAM DOESN'T EXIST*********** | " + team_abbrev)
        return Team.objects.get(pk=1)

def getDate(game):
    time_code = {"Thu":3, "Fri":4, "Sat":5, "Sun":6, "Mon":7}
    date = game[0]
    print(date)

    today = datetime.date.today()
    days_added = datetime.timedelta( days=(time_code[date]-today.weekday()) )
    day = today + days_added
    print(today, days_added)
    print(day)

    time_input = (game[1]).split(":") #19:00:00
    time = datetime.time(int(time_input[0]), int(time_input[1]), int(time_input[2]))

    return datetime.datetime.combine(day, time)

