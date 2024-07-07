-- Creating countries table
CREATE TABLE public.countries
(
   code TEXT PRIMARY KEY,
   name TEXT
);

-- Creating indicators table
CREATE TABLE public.indicators
(
    id INT PRIMARY KEY,
    name VARCHAR(255),
    definition TEXT
);

-- Creating stats table
CREATE TABLE public.stats
(
    indicator_id INT,
    country_code TEXT,
    year INT,
    value NUMERIC,
    FOREIGN KEY (indicator_id) REFERENCES public.indicators (id),
    FOREIGN KEY (country_code) REFERENCES public.countries (code)
);

-- Setting ownership
ALTER TABLE public.countries OWNER to postgres;
ALTER TABLE public.indicators OWNER to postgres;
ALTER TABLE public.stats OWNER to postgres;

-- Speeding up lookups
CREATE INDEX idx_indicator_id ON public.stats (indicator_id);
CREATE INDEX idx_country_code ON public.stats (country_code);
