SELECT round
FROM s002_silver.t006_matches
LIMIT 10;

SELECT *
FROM s002_silver.t004_seasons
LIMIT 10;

SELECT DISTINCT season_year
FROM s002_silver.t004_seasons
LIMIT 10;

CREATE VIEW s003_gold.table_per_round AS
SELECT 
    t006.unique_tournament_id as tournament_id,
    t003.tournament_name,
    t006.season_id,
    t004.season_year as season_year,
    t006.round,
    t006.slug,
    t006.team_id,
    t006.team_name,
    CASE
        WHEN t006.goals_for > t006.goals_against THEN 'win'
        WHEN t006.goals_for < t006.goals_against THEN 'lose'
        ELSE 'draw'
    END AS match_result,
    CASE
        WHEN t006.goals_for > t006.goals_against THEN 3
        WHEN t006.goals_for < t006.goals_against THEN 0
        ELSE 1
    END AS match_points,
    t006.home_or_away,
    t006.opponent_id,
    t006.opponent_name,
    t006.goals_for,
    t006.goals_against,
    t006.goals_for - t006.goals_against AS goal_difference,
    -- Cálculo dos pontos acumulados
    SUM(
        CASE
            WHEN t006.goals_for > t006.goals_against THEN 3
            WHEN t006.goals_for < t006.goals_against THEN 0
            ELSE 1
        END
    ) OVER (
        PARTITION BY t006.team_id, t006.unique_tournament_id, t006.season_id 
        ORDER BY t006.round
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_points,
    -- Número total de partidas jogadas
    COUNT(*) OVER (PARTITION BY t006.team_id, t006.unique_tournament_id, t006.season_id) AS total_matches,
    -- Número total de vitórias
    SUM(CASE WHEN t006.goals_for > t006.goals_against THEN 1 ELSE 0 END) OVER (
        PARTITION BY t006.team_id, t006.unique_tournament_id, t006.season_id
        ORDER BY t006.round
    ) AS total_wins,
    -- Número total de empates
    SUM(CASE WHEN t006.goals_for = t006.goals_against THEN 1 ELSE 0 END) OVER (
        PARTITION BY t006.team_id, t006.unique_tournament_id, t006.season_id
        ORDER BY t006.round
    ) AS total_draws,
    -- Número total de derrotas
    SUM(CASE WHEN t006.goals_for < t006.goals_against THEN 1 ELSE 0 END) OVER (
        PARTITION BY t006.team_id, t006.unique_tournament_id, t006.season_id
        ORDER BY t006.round
    ) AS total_losses,
    -- Gols pró acumulados
    SUM(t006.goals_for) OVER (
        PARTITION BY t006.team_id, t006.unique_tournament_id, t006.season_id
        ORDER BY t006.round
    ) AS cumulative_goals_for,
    -- Gols contra acumulados
    SUM(t006.goals_against) OVER (
        PARTITION BY t006.team_id, t006.unique_tournament_id, t006.season_id
        ORDER BY t006.round
    ) AS cumulative_goals_against,
    -- Saldo de gols acumulado
    SUM(t006.goals_for - t006.goals_against) OVER (
        PARTITION BY t006.team_id, t006.unique_tournament_id, t006.season_id
        ORDER BY t006.round
    ) AS cumulative_goal_difference
FROM (
    SELECT 
        unique_tournament_id,
        season_id,
        round,
        slug,
        home_team_id AS team_id,
        home_team_name AS team_name,
        'home' AS home_or_away,
        away_team_id AS opponent_id,
        away_team_name AS opponent_name,
        CAST(home_score AS INTEGER) AS goals_for,
        CAST(away_score AS INTEGER) AS goals_against
    FROM s002_silver.t006_matches
    WHERE home_score IS NOT NULL
    
    UNION
    
    SELECT 
        unique_tournament_id,
        season_id,
        round,
        slug,
        away_team_id AS team_id,
        away_team_name AS team_name,
        'away' AS home_or_away,
        home_team_id AS opponent_id,
        home_team_name AS opponent_name,
        CAST(away_score AS INTEGER) AS goals_for,
        CAST(home_score AS INTEGER) AS goals_against
    FROM s002_silver.t006_matches
    WHERE away_score IS NOT NULL
) AS t006
LEFT JOIN s002_silver.t003_tournaments t003
    ON t006.unique_tournament_id = t003.tournament_id
LEFT JOIN s002_silver.t004_seasons t004
    ON t006.season_id = t004.season_id
GROUP BY 
    t006.unique_tournament_id,
    t003.tournament_name,
    t006.season_id, 
    t004.season_year,
    t006.round,
    t006.slug,
    t006.team_id, 
    t006.team_name,
    match_result,
    match_points,
    t006.home_or_away,
    t006.opponent_id,
    t006.opponent_name,
    t006.goals_for,
    t006.goals_against,
    goal_difference
ORDER BY
    tournament_name DESC,
    season_year DESC,
    round DESC,
    slug DESC,
    cumulative_points DESC,
    team_name ASC;

