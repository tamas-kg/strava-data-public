{{ config(
    materialized='table'
) }}

WITH lap_agg AS (
    SELECT 
        activity_id,
        SUM(total_elevation_gain) AS total_elevation_gain
    FROM 
        {{ ref('lap') }}
    GROUP BY 
        activity_id
)

SELECT 
    EXTRACT(YEAR FROM a.start_date)::INT AS year,
    EXTRACT(MONTH FROM a.start_date)::INT AS month,
    ROUND(SUM(a.distance)/1000, 1) AS total_distance,
    SUM(a.moving_time) AS total_time,
    SUM(l.total_elevation_gain) AS total_elevation,
    SUM(a.calories) AS total_calories,
    SUM(a.pr_count) AS total_prs
FROM 
    {{ ref('activity') }} a
LEFT JOIN 
    lap_agg l ON a.id = l.activity_id
WHERE 
    a.activity_type = 'Ride'
GROUP BY 
    year, month
ORDER BY 
    year, month
