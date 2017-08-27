from picks.nflData import updateGames, getCurrentWeekYear
from picks.models import Week

def update_games(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        week, year = getCurrentWeekYear()
        if not Week.objects.filter(week=week, year=year).exists():
            updateGames()

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware