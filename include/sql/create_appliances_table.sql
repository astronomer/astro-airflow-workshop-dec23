CREATE TABLE IF NOT EXISTS 
{{ params.db_name }}.{{ params.schema_name }}.appliances (
    appliances_id STRING PRIMARY KEY,
    appliances_name STRING,
    appliances_type STRING,
    price FLOAT,
    updated_at TIMESTAMP
);
