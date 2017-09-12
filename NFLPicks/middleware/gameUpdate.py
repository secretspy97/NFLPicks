from picks.nflData import updateGames, getCurrentWeekYear
from picks.models import Week
from security.views import save_request
from django.utils import timezone


def update_games(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        week, year = getCurrentWeekYear()

        if not Week.objects.filter(week=week, year=year).exists():
            updateGames()

        week_obj = Week.objects.get(week=week, year=year)
        if week_obj.starts < timezone.now() < week_obj.ends and not week_obj.saveBackup:
            save_request(password="a12b3c4e5d")
            week_obj.saveBackup = True
            week_obj.save()
        if timezone.now() >= week_obj.ends and week_obj.saveBackup:
            save_request(password="a12b3c4e5d")
            week_obj.saveBackup = False
            week_obj.save()

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware