COPY countries
FROM 'C:\Users\artjo\.vscode\HealthCare Estonia Analysis\tables\countries.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');

COPY indicators
FROM 'C:\Users\artjo\.vscode\HealthCare Estonia Analysis\tables\indicators.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');

COPY stats
FROM 'C:\Users\artjo\.vscode\HealthCare Estonia Analysis\tables\stats.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');