class PredictionCalculation():
    """
    Points will be awarded as follows:

    For drivers:
    - 1 point for each correct name among top 10
    - 1 point for each correct name among top 3
    - extra point for each correct finishing position
    - extra point for correct winner
    - 2 points for correct driver with fastest lap
    - 2 points for correct pole position prediction (the actual driver on
    pole at the start of the race)
    
    Teams:
    - 1 point for each correct team among point finishers.
    """
    def __init__(self, prediction):
        self.prediction = prediction
    
    def race_result(self):
        return self.prediction.race.raceresult
    
    def correct_name_among_top_10(self):
        return len(
            set([prediction_position.driver for prediction_position in self.prediction.predictionposition_set.all()]) & 
            set([race_result_position.driver for race_result_position in self.race_result().raceresultposition_set.all()]))
        
    def correct_name_among_top_3(self):
        return len(
            set([prediction_position.driver for prediction_position in self.prediction.predictionposition_set.filter(position__lte=3)]) & 
            set([race_result_position.driver for race_result_position in self.race_result().raceresultposition_set.filter(position__lte=3)]))
    
    def correct_finishing_position(self):
        return sum([ 1 for pos in range(1,11) if self.prediction.predictionposition_set.get(position=pos).driver == self.race_result().raceresultposition_set.get(position=pos).driver])
    
    def correct_winner(self):
        return 1 if self.prediction.predictionposition_set.get(position=1).driver == self.race_result().raceresultposition_set.get(position=1).driver else 0
    
    def correct_fastest_lap(self):
        return 2 if self.prediction.fastest_lap == self.race_result().fastest_lap else 0
    
    def correct_pole_position(self):
        return 2 if self.prediction.pole_position == self.race_result().pole_position else 0
    
    def correct_team(self):
        return 0
    
    def total(self):
        return (
            self.correct_name_among_top_10() +
            self.correct_name_among_top_3() +
            self.correct_finishing_position() +
            self.correct_winner() +
            self.correct_fastest_lap() +
            self.correct_pole_position() +
            self.correct_team())

def calculate(prediction):
    return PredictionCalculation(prediction)
