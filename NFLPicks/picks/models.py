from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User

class Team(models.Model):
    team_name = models.CharField(max_length=30)
    team_abbrev = models.CharField(max_length=3)

    def __str__(self):
        return self.team_abbrev

class Week(models.Model):
    year = models.IntegerField()
    week = models.IntegerField()
    starts = models.DateField()
    ends = models.DateField()

# Create your models here.
class Game(models.Model):
    home = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home')
    away = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away')
    spread = models.IntegerField()
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name='winner')

    def __str__(self):
        return self.away.team_abbrev + " @ " + self.home.team_abbrev

class PlayerPick(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game')
    pick = models.ForeignKey(Team, on_delete=models.CASCADE)