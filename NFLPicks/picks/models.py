from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User

class Team(models.Model):
    team_name = models.CharField(max_length=30)
    team_abbrev = models.CharField(max_length=3)

    def __str__(self):
        return self.team_name

    def get_abv(self):
        return self.team_abbrev

    class Meta:
        ordering = ['team_name']

class Week(models.Model):
    year = models.IntegerField()
    week = models.CharField(max_length=4)
    starts = models.DateTimeField()
    ends = models.DateTimeField()

# Create your models here.
class Game(models.Model):
    home = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home')
    away = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away')
    spread = models.IntegerField()
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='winner')

    def __str__(self):
        return self.away.team_abbrev + " @ " + self.home.team_abbrev

    class Meta:
        ordering = ['start_time', 'home']

class PlayerPick(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game')
    pick = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)