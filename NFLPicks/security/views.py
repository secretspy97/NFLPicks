from django.http import JsonResponse
from django.core.management import call_command
from django.views.decorators.csrf import csrf_exempt
import json as jsonFile
from accounts.mail import send_message

FILE_NAME = 'static/db-backup.json'

# Create your views here.
def save_request(request=None, password=None):
    if password:
        security = password
    else:
        security = request.GET.get("password") or request.POST.get("password")

    if security == "a12b3c4e5d":

        with open(FILE_NAME,'w') as file: # Point stdout at a file for dumping data to.
            call_command('dumpdata', 'picks', 'auth.user', format='json',indent=3,stdout=file)
            file.close()

        with open(FILE_NAME,'r') as file:
            send_message("Database Backup", "Backup", ('db-backup.json', file.read(), 'application/json'))
            file.close();

        return JsonResponse({"Success": True})
    return JsonResponse({"Success": False, "Message": "Password Invalid"})