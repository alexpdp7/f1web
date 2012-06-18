create or replace view v_predictions_predictionresult as 
with j_predictions_predictionposition as (
	select predictions_predictionposition.*, predictions_prediction.race_id
	from   predictions_predictionposition
	join   predictions_prediction on predictions_predictionposition.prediction_id = predictions_prediction.id),
	
	correct_names_among_top_10 as (
	select   j_predictions_predictionposition.prediction_id, count(championship_raceresultposition.id) as correct_names_among_top_10
	from      j_predictions_predictionposition
	join      championship_raceresult using (race_id)
	left join championship_raceresultposition on  championship_raceresult.id = championship_raceresultposition.race_result_id 
	                                          and j_predictions_predictionposition.driver_id = championship_raceresultposition.driver_id
	group by j_predictions_predictionposition.prediction_id),
	
	correct_names_among_top_3 as (
	select    j_predictions_predictionposition.prediction_id, count(championship_raceresultposition.id) as correct_names_among_top_3
	from      j_predictions_predictionposition
	join      championship_raceresult using (race_id)
	left join championship_raceresultposition on  championship_raceresult.id = championship_raceresultposition.race_result_id 
	                                          and j_predictions_predictionposition.driver_id = championship_raceresultposition.driver_id
	and       j_predictions_predictionposition.position between 1 and 3
	and       championship_raceresultposition.position between 1 and 3
	group by  j_predictions_predictionposition.prediction_id),
	
	correct_finishing_position as (
	select    j_predictions_predictionposition.prediction_id, count(championship_raceresultposition.id) as correct_finishing_position
	from      j_predictions_predictionposition
	join      championship_raceresult using (race_id)
	left join championship_raceresultposition on  championship_raceresult.id = championship_raceresultposition.race_result_id 
	                                          and j_predictions_predictionposition.driver_id = championship_raceresultposition.driver_id 
	                                          and j_predictions_predictionposition.position = championship_raceresultposition.position
	group by  j_predictions_predictionposition.prediction_id),
	
	correct_winner as (
	select    j_predictions_predictionposition.prediction_id, count(championship_raceresultposition.id) as correct_winner
	from      j_predictions_predictionposition
	join      championship_raceresult using (race_id)
	left join championship_raceresultposition on  championship_raceresult.id = championship_raceresultposition.race_result_id 
	                                          and j_predictions_predictionposition.driver_id = championship_raceresultposition.driver_id 
	                                          and j_predictions_predictionposition.position = championship_raceresultposition.position
	                                          and championship_raceresultposition.position = 1
	group by  j_predictions_predictionposition.prediction_id),
	
	race_general as (
	select predictions_prediction.id as prediction_id, 
	       case when predictions_prediction.pole_position_id = championship_raceresult.pole_position_id then 2 else 0 end as correct_pole,
	       case when predictions_prediction.fastest_lap_id = championship_raceresult.fastest_lap_id then 2 else 0 end as correct_fastest_lap
	from predictions_prediction
	join championship_raceresult using (race_id)),

	correct_teams as (
	with j_predictions_predictionposition as (
		select predictions_predictionposition.*, predictions_prediction.race_id
		from   predictions_predictionposition
		join   predictions_prediction on predictions_predictionposition.prediction_id = predictions_prediction.id),
		
		j_predictions_teams as (
		select    j_predictions_predictionposition.prediction_id, race_id, team_id, count(*) as top_tens
		from      j_predictions_predictionposition
		join      championship_race on j_predictions_predictionposition.race_id = championship_race.id
		join      championship_driverteamassignment on  j_predictions_predictionposition.driver_id = championship_driverteamassignment.driver_id 
		                                            and championship_race.date between championship_driverteamassignment.assigned_from and championship_driverteamassignment.assigned_to
		group  by j_predictions_predictionposition.prediction_id, race_id, team_id),
	
		results_teams as (
		select   race_id, team_id, count(*) as top_tens
		from     championship_raceresultposition
		join     championship_raceresult on championship_raceresultposition.race_result_id = championship_raceresult.id
		join     championship_race on championship_raceresult.race_id = championship_race.id
		join     championship_driverteamassignment on  championship_raceresultposition.driver_id = championship_driverteamassignment.driver_id 
		                                           and championship_race.date between championship_driverteamassignment.assigned_from and championship_driverteamassignment.assigned_to
		group by race_id, team_id),
		
		prediction_by_team as (
		select    race_id, prediction_id, least(results_teams.top_tens, coalesce(j_predictions_teams.top_tens, 0)) as points_team
		from      results_teams
		join      j_predictions_teams using (race_id, team_id))
	
	select    prediction_id, coalesce(sum(points_team), 0) correct_teams
	from      predictions_prediction
	left join prediction_by_team on predictions_prediction.id = prediction_by_team.prediction_id
	group by  prediction_id)
	
select race_general.*, 
       correct_names_among_top_10.correct_names_among_top_10, 
       correct_names_among_top_3.correct_names_among_top_3, 
       correct_finishing_position.correct_finishing_position, 
       correct_teams.correct_teams,
       correct_winner.correct_winner,
       correct_names_among_top_10 + 
       correct_names_among_top_3 + 
       correct_finishing_position + 
       correct_teams.correct_teams + 
       race_general.correct_pole + 
       correct_winner.correct_winner as total
from   correct_names_among_top_10
join   correct_names_among_top_3 using (prediction_id)
join   correct_finishing_position using (prediction_id)
join   correct_winner using (prediction_id)
join   correct_teams using (prediction_id)
join   race_general using (prediction_id);

