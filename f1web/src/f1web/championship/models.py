from django.db import models

class Championship(models.Model):
    year = models.IntegerField(primary_key=True)
    
    def __unicode__(self):
        return str(self.year)

class Race(models.Model):
    championship = models.ForeignKey(Championship)
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    date = models.DateField()
    
    def __unicode__(self):
        return str(self.championship) + " - " + self.code + " - " +self.name
    
    def get_drivers(self):
        return Driver.objects.filter(
                        driverteamassignment__assigned_from__lte=self.date, 
                        driverteamassignment__assigned_to__gte=self.date)

class Team(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.code + " - " + self.name

class Driver(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=100)
    teams = models.ManyToManyField(Team, through = 'DriverTeamAssignment')
    
    def __unicode__(self):
        return self.code + " - " + self.name
    
    def team_for_race(self, race):
        return self.driverteamassignment_set.get(assigned_from__lte=race.date,assigned_to__gte=race.date).team

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
    
    def list_display_race_championship(self):
        return self.race.championship
    def list_display_race_code(self):
        return self.race.code
    def list_display_race_name(self):
        return self.race.name
    def list_display_race_date(self):
        return self.race.date

class RaceResultPosition(models.Model):
    race_result = models.ForeignKey(RaceResult)
    position = models.IntegerField(choices=zip(range(1,11), range(1,11)))
    driver = models.ForeignKey(Driver)
