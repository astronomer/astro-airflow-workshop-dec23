CREATE TABLE IF NOT EXISTS 
{{ params.db_name }}.{{ params.schema_name }}.programs (
    program_id STRING PRIMARY KEY,
    program STRING,
    program_discount STRING,
    program_effective_year STRING,
    updated_at TIMESTAMP
);
