CREATE TABLE IF NOT EXISTS {{ params.db_name }}.{{ params.schema_name }}.enriched_sales (
    sale_id STRING,
    user_id STRING,
    user_name STRING,
    appliance_name STRING,
    appliance_type STRING,
    quantity INT,
    sale_date TIMESTAMP,
    program STRING,
    program_discount STRING,
    program_effective_year STRING,
    total_revenue NUMBER,
    CONSTRAINT unique_sale_id UNIQUE (sale_id)
) AS
SELECT 
    s.sale_id,
    s.user_id,
    u.user_name,
    t.appliance_name,
    t.appliance_type,
    s.quantity,
    s.sale_date,
    up.program,
    up.program_discount,
    up.program_effective_year,
    t.price * s.quantity AS total_revenue
FROM {{ params.db_name }}.{{ params.schema_name }}.sales s
JOIN {{ params.db_name }}.{{ params.schema_name }}.users u ON s.user_id = u.user_id
JOIN {{ params.db_name }}.{{ params.schema_name }}.appliances t ON s.appliance_id = t.appliance_id
JOIN {{ params.db_name }}.{{ params.schema_name }}.programs up ON s.program_id = up.program_id;
