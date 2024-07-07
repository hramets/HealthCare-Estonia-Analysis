WITH avg_eu_stats AS (
    SELECT
        indicator_id,
        year,
        AVG(value) AS value 
    FROM
        stats
    GROUP BY
        indicator_id,
        year
    HAVING
        indicator_id = 15
    ORDER BY
        indicator_id, year
),

    avg_baltic_states_stats AS (
    SELECT
            year,
            AVG(value) AS value 
        FROM
            stats
        WHERE 
            country_code in (
                SELECT
                    code
                FROM
                    countries
                WHERE
                    name IN ('Estonia', 'Latvia', 'Lithuania')
            ) AND
            indicator_id = 15
        GROUP BY
            year
        ORDER BY
            year
)

SELECT
    indicators.name AS indicator,
    stats.year,
    ROUND(stats.value, 2) AS est_percentage,
    ROUND(avg_eu_stats.value, 2) AS avg_eu_percentage,
    ROUND(avg_baltic_states_stats.value, 2) AS avg_baltic_percentage
FROM stats
    LEFT JOIN indicators ON stats.indicator_id = indicators.id
    LEFT JOIN countries ON stats.country_code = countries.code
    LEFT JOIN avg_eu_stats ON stats.year = avg_eu_stats.year
    LEFT JOIN avg_baltic_states_stats ON stats.year = avg_baltic_states_stats.year
WHERE
    country_code = 'EST' AND
    stats.indicator_id = 15 AND
    stats.year >= 2000