SELECT
    dense_rank() OVER(ORDER BY AVG(stats.value) DESC) AS rank,
    countries.name AS country,
    ROUND(AVG(stats.value), 2) AS avg_percentage
FROM
    stats
    JOIN countries ON stats.country_code = countries.code
WHERE
    year >= (SELECT
        MAX(year) - 5
        FROM
            stats) AND
    indicator_id = 5
GROUP BY
    countries.name
ORDER BY
    AVG(stats.value) DESC
LIMIT 10;


SELECT
    dense_rank() OVER(ORDER BY AVG(stats.value) ASC) AS rank,
    countries.name AS country,
    ROUND(AVG(stats.value), 2) AS avg_percentage
FROM
    stats
    JOIN countries ON stats.country_code = countries.code
WHERE
    year >= (SELECT
        MAX(year) - 5
        FROM
            stats) AND
    indicator_id = 15
GROUP BY
    countries.name
ORDER BY
    AVG(stats.value) ASC
LIMIT 10;


SELECT
    dense_rank() OVER(ORDER BY AVG(stats.value) ASC) AS rank,
    countries.name AS country,
    ROUND(AVG(stats.value), 2) AS avg_percentage
FROM
    stats
    JOIN countries ON stats.country_code = countries.code
WHERE
    year >= (SELECT
        MAX(year) - 5
        FROM
            stats) AND
    indicator_id = 7
GROUP BY
    countries.name
ORDER BY
    AVG(stats.value) ASC
LIMIT 10;

