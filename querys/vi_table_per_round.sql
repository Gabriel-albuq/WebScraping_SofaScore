CREATE OR REPLACE VIEW s003_gold.vi_table_per_round AS
WITH ranked_data AS (
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
        COUNT(*) OVER (PARTITION BY t006.team_id, t006.unique_tournament_id, t006.season_id) AS total_matches,
        SUM(CASE WHEN t006.goals_for > t006.goals_against THEN 1 ELSE 0 END) OVER (
            PARTITION BY t006.team_id, t006.unique_tournament_id, t006.season_id
            ORDER BY t006.round
        ) AS total_wins,
        SUM(CASE WHEN t006.goals_for = t006.goals_against THEN 1 ELSE 0 END) OVER (
            PARTITION BY t006.team_id, t006.unique_tournament_id, t006.season_id
            ORDER BY t006.round
        ) AS total_draws,
        SUM(CASE WHEN t006.goals_for < t006.goals_against THEN 1 ELSE 0 END) OVER (
            PARTITION BY t006.team_id, t006.unique_tournament_id, t006.season_id
            ORDER BY t006.round
        ) AS total_losses,
        SUM(t006.goals_for) OVER (
            PARTITION BY t006.team_id, t006.unique_tournament_id, t006.season_id
            ORDER BY t006.round
        ) AS cumulative_goals_for,
        SUM(t006.goals_against) OVER (
            PARTITION BY t006.team_id, t006.unique_tournament_id, t006.season_id
            ORDER BY t006.round
        ) AS cumulative_goals_against,
        SUM(t006.goals_for - t006.goals_against) OVER (
            PARTITION BY t006.team_id, t006.unique_tournament_id, t006.season_id
            ORDER BY t006.round
        ) AS cumulative_goal_difference,
        MAX(t006.round) OVER (PARTITION BY t006.unique_tournament_id, t006.season_id) AS max_round
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
),

positions_per_round AS (
    SELECT 
        *,
        RANK() OVER (
            PARTITION BY tournament_id, season_id, round
            ORDER BY 
                cumulative_points DESC,
                total_wins DESC,
                cumulative_goal_difference DESC,
                cumulative_goals_for DESC
        ) AS current_round_position
    FROM ranked_data
),

final_positions AS (
    SELECT 
        tournament_id,
        season_id,
        team_id,
        current_round_position AS final_position
    FROM positions_per_round
    WHERE round = max_round
)

SELECT 
    p.tournament_id,
    p.tournament_name,
    p.season_id,
    p.season_year,
    p.round,
    p.slug,
    p.team_id,
    p.team_name,
    p.match_result,
    p.match_points,
    p.home_or_away,
    p.opponent_id,
    p.opponent_name,
    p.goals_for,
    p.goals_against,
    p.goal_difference,
    p.cumulative_points,
    p.total_matches,
    p.total_wins,
    p.total_draws,
    p.total_losses,
    p.cumulative_goals_for,
    p.cumulative_goals_against,
    p.cumulative_goal_difference,
    p.current_round_position,
    f.final_position
FROM positions_per_round p
LEFT JOIN final_positions f
    ON p.tournament_id = f.tournament_id
    AND p.season_id = f.season_id
    AND p.team_id = f.team_id
ORDER BY
    p.tournament_name DESC,
    p.season_year DESC,
    p.round DESC,
    p.current_round_position ASC,
    p.team_name ASC;