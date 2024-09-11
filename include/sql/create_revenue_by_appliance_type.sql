CREATE TABLE IF NOT EXISTS {{ params.db_name }}.{{ params.schema_name }}.revenue_by_appliance_type (
    appliance_type STRING PRIMARY KEY,
    total_revenue NUMBER
);