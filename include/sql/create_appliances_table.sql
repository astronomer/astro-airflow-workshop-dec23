CREATE TABLE IF NOT EXISTS 
{{ params.db_name }}.{{ params.schema_name }}.appliances (
    appliance_id STRING PRIMARY KEY,
    appliance_name STRING,
    appliance_type STRING,
    price FLOAT,
    updated_at TIMESTAMP
);
