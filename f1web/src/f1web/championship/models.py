from django.db import models

class Championship(models.Model):
    year = models.IntegerField(primary_key=True)
    
    def __str__(self):
        return str(self.year)

class Race(models.Model):
    championship = models.ForeignKey(Championship)
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    date = models.DateField()
    
    def __str__(self):
        return str(self.championship) + " - " + self.code + " - " +self.name

class Team(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.code + " - " + self.name

class Driver(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=100)
    teams = models.ManyToManyField(Team, through = 'DriverTeamAssignment')
    
    def __str__(self):
        return self.code + " - " + self.name

class DriverTeamAssignment(models.Model):
    team = models.ForeignKey(Team)
    driver = models.ForeignKey(Driver)
    assigned_from = models.DateField()
    assigned_to = models.DateField()

class RaceResult(models.Model):
    race = models.OneToOneField(Race)
    pole_position = models.ForeignKey(Driver, related_name='poles')
    fastest_lap = models.ForeignKey(Driver, related_name='fastest_laps')
    top_ten = models.ManyToManyField(Driver, through='RaceResultPosition')

class RaceResultPosition(models.Model):
    race_result = models.ForeignKey(RaceResult)
    position = models.IntegerField(choices=zip(range(1,11), range(1,11)))
    driver = models.ForeignKey(Driver)
