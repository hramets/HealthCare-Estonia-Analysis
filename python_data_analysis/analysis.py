import pandas as pd                         # For data manipulating
import matplotlib.pyplot as plt             # For creating visualizations
import seaborn as sns                       # For creating visualizations
from sqlalchemy import create_engine        # For creating SQL queries inside Python
from matplotlib.ticker import FuncFormatter # For formatting values on visualization

# Connection details to connect a database
db_user = 'user'
db_pass = 'password'
db_host = 'host'
db_port = 'port'
db_name = 'database_name'

connection_str = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}" # Connection string for PostgreSQL database

engine = create_engine(connection_str) # Creating object engine to execute SQL queries in Python.


### ANALYSIS QUESTIONS

""" 1.	How have Estonian government expenses on healthcare changed over time? 
        How these changes compare to EU countries' indicators? How these changes compare to Baltic countries' indicators?
    2.	How have people’s out-of-pocket expenses on healthcare changed in Estonia? 
        How these changes compare to EU countries' indicators? How these changes compare to Baltic countries' indicators?
    3.	How have expenses in private healthcare changed in Estonia? 
        How these changes compare to EU countries' indicators? How these changes compare to Baltic countries' indicators?
    4.	Which is the best country in the EU based on healthcare indicators?"""


## Indicator for the 1st question - Domestic general government health expenditure (% of general government expenditure).

question_1 = """
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
        indicator_id = 5
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
            indicator_id = 5
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
    stats.indicator_id = 5 AND
    stats.year >= 2000
"""

df_1 = pd.read_sql(question_1, engine) # Dataframe for the question

## Indicator for the 2nd question - Out-of-pocket expenditure (% of current health expenditure).

question_2 = """
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
"""

df_2 = pd.read_sql(question_2, engine) # Dataframe for the question

## Indicator for the 3rd question - Domestic private health expenditure (% of current health expenditure).

question_3 = """
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
        indicator_id = 7
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
            indicator_id = 7
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
    stats.indicator_id = 7 AND
    stats.year >= 2000
"""

df_3 = pd.read_sql(question_3, engine) # Dataframe for the question


## Creating visualizations for the question 1, 2, 3.

# To format values on visualizations.
def to_percent(y, position):
    return f"{y:.0f}%"


def to_create_plots_on_fig_for_main_questions(dataframe, question_ind):
    values = ['est_percentage', 'avg_eu_percentage', 'avg_baltic_percentage']
    titles = ["Domestic general government health expenditure (% of general government expenditure)",
                "Out-of-pocket expenditure (% of current health expenditure)",
                "Domestic private health expenditure (% of current health expenditure)"]
    colors = ['darkgreen', 'palegreen', 'lightpink']
    
    fig, ax = plt.subplots(figsize=(15, 7))
    count_for_vals = 0
    while count_for_vals != 3:
        sns.lineplot(data=dataframe, x='year', y=values[count_for_vals], color=colors[count_for_vals], label=values[count_for_vals])
        count_for_vals += 1
        
    sns.despine()
    ax.yaxis.set_major_formatter(FuncFormatter(to_percent))
    ax.set_title(titles[question_ind])
    ax.set_xticks(dataframe['year'])
    plt.tight_layout()
    plt.savefig(f"C:\\Users\\artjo\\.vscode\\HealthCare Estonia Analysis\\visualizations\\question_{question_ind + 1}")
  
    
dataframes = [df_1, df_2, df_3]    
for ind, df in enumerate(dataframes):
    to_create_plots_on_fig_for_main_questions(df, ind)
    
    
## 4th question - What is the best country in EU basing on healthcare indicators?

# For the last question making 3 queries for all indicators from previous questions.
# The results are ranked - top 10 countries in an every query.
query_1 = """
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
"""
df_4_1 = pd.read_sql(query_1, engine)

query_2 = """
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
"""
df_4_2 = pd.read_sql(query_2, engine)

query_3 = """
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
"""
df_4_3 = pd.read_sql(query_3, engine)

# Extracting countries that appear in all top ranks above. Then calculating an average position for every country based on a rank in every query and
# creating dictionary with pairs "country: avg_rank_postion".
best_countries = dict()
for country in df_4_1['country']:
    if df_4_2['country'].isin([country]).any() and df_4_3['country'].isin([country]).any():
        dataframes_best = [df_4_1, df_4_2, df_4_3]
        avg_rnk_position = 0
        for ind, df in enumerate(dataframes_best):
            avg_rnk_position +=  df.loc[df['country'] == country, 'rank'].values[0]
            if ind == 2:
                avg_rnk_position /= 3
                best_countries[country] = round(avg_rnk_position)
# Turned out that the best healthcare system EU countries have almost the same average postion - from 5 to 6.

# Creating new dataframes with the best healthcare system countries in EU based on three main indicators, that were written above.  
df_4_1_best = df_4_1[df_4_1['country'].isin(best_countries.keys())]
df_4_2_best = df_4_2[df_4_2['country'].isin(best_countries.keys())]
df_4_3_best = df_4_3[df_4_3['country'].isin(best_countries.keys())]


## Creating visualizations showing compared results between the best healthcare system countries in EU.

best_countries_dfs = [df_4_1_best, df_4_2_best, df_4_3_best]

titles = ["Domestic general government health expenditure \n(avg last 5 year % of general government expenditure)",
                "Out-of-pocket expenditure \n(avg last 5 year % of current health expenditure)",
                "Domestic private health expenditure \n(avg last 5 year % of current health expenditure)"] 
   
for ind, df in enumerate(best_countries_dfs):
    fig, ax= plt.subplots(figsize=(5, 5))
    
    sns.barplot(data=df, x='country', y='avg_percentage', legend=False, 
                palette="PiYG", hue=df.sort_index(ascending=False).index)
    
    ax.set_title(titles[ind], fontsize=11)
    ax.set_xlabel('')
    ax.set_ylabel('')
    
    for i in range(len(df['country'])):
        ax.text(i, df['avg_percentage'].iloc[i], f'{df["avg_percentage"].iloc[i]:.2f}%', ha='center')
    
    ax.yaxis.set_major_formatter(FuncFormatter(to_percent))
    
    sns.despine()
    plt.tight_layout()
    plt.savefig(f"C:\\Users\\artjo\\.vscode\\HealthCare Estonia Analysis\\visualizations\\question_4_{ind + 1}")
    
