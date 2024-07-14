import pandas as pd


### TRANSFORMING TABLES AND CREATING NEW ONES

# Importing data
table = "Initial dataset\HealthCare_Data.xlsx"
initial_data = pd.read_excel(table, sheet_name='Data')
df_initial_data = pd.DataFrame(initial_data)

# Transforming year columns to one column 
data_main = df_initial_data.melt(id_vars=['Country Name', 'Country Code', 'Series Name', 'Series Code'])
# Saving data
#df_melted_data.to_csv("HealthCare_transformed.csv", index=True)

# Creating separate table for Indicators with id numbers
data_indicators = pd.read_excel(table, sheet_name='Series - Metadata')
df_data_indicators = pd.DataFrame(data_indicators)

# Creating separate table for Countries
data_countries = data_main[['Country Code', 'Country Name']]
'''data_countries = data_countries.drop_duplicates(subset='Country Code')
data_countries.dropna(inplace=True)
data_countries = data_countries.reset_index()
data_countries = data_countries.drop('index', axis=1)'''


### MANIPULATING DATA

# Creating list of EU countries for filtering
eu_countries = [
    "Austria",
    "Belgium",
    "Bulgaria",
    "Croatia",
    "Cyprus",
    "Czechia",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Hungary",
    "Ireland",
    "Italy",
    "Latvia",
    "Lithuania",
    "Luxembourg",
    "Malta",
    "Netherlands",
    "Poland",
    "Portugal",
    "Romania",
    "Slovak Republic",
    "Slovenia",
    "Spain",
    "Sweden"
]
# Filtering EU countries
data_main = data_main[data_main['Country Name'].isin(eu_countries)]
# Filtering EU countries
data_countries = data_countries[data_countries['Country Name'].isin(eu_countries)]

## Indicators table manipulating
# Deleting redudant columns
ind_redudant_columns = [column for column in data_indicators.columns if column not in ['Indicator Name', 'Long definition']]
data_indicators.drop(columns=ind_redudant_columns, inplace=True)
# Creating new columns with indicators id
data_indicators['Id'] = data_indicators.index + 1
# Renaming columns
data_indicators.rename(columns={'Indicator Name': 'name', 'Long definition': 'definition', 'Id': 'id'}, inplace=True)
# Final table
data_indicators = data_indicators[['id', 'name', 'definition']]

                                  
## Countries table manipulating
# Dropping duplicates
data_countries.drop_duplicates(subset='Country Code', inplace=True)

# Renaming columns
data_countries.rename(columns={'Country Code': 'code', 'Country Name': 'name'}, inplace=True)    

## Main data table
# Adding Id indicator column to main table
data_main = pd.merge(data_main, data_indicators[['id', 'name']], how='left', left_on='Series Name', right_on='name')
# Deleting redudant columns
main_tab_redudant_columns = [column for column in data_main.columns if column not in ['Country Code', 'variable', 'value', 'id']]
data_main.drop(columns=main_tab_redudant_columns, inplace=True)

# Renaming columns
data_main.rename(columns={'Country Code': 'country_code', 'variable': 'year', 'id': 'indicator_id'}, inplace=True)
# Removing NaN values
data_main = data_main[data_main['value'] != '..'] # In the dataset instead of NaN values here were strings ".."
# Converting values in "Value" column to float
data_main['value'] = data_main['value'].astype(float)


# Creating function for reformatting "Year" column (example of an exsiting value: "2023 [YR2023]")
def to_format_year_value(value):
    year = value.split(' ')[0]
    return year
# Reformatting values in "Year" column
data_main['year'] = data_main['year'].apply(to_format_year_value)
# Final table
data_main = data_main[['indicator_id', 'country_code', 'year', 'value']]


### SAVING TABLES
data_main.to_csv('stats.csv', index=False)
data_countries.to_csv('countries.csv', index=False)
data_indicators.to_csv('indicators.csv', index=False)


