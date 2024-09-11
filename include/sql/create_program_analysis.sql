CREATE TABLE IF NOT EXISTS {{ params.db_name }}.{{ params.schema_name }}.program_analysis (
    program_id STRING,
    program STRING,
    program_effective_year STRING,
    total_sales INTEGER,
    total_revenue NUMBER,
    PRIMARY KEY (utm_source, utm_medium, utm_campaign)
);