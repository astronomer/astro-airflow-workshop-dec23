MERGE INTO {{ params.db_name }}.{{ params.schema_name }}.revenue_by_appliance_type AS target
USING (
    SELECT 
        appliance_type,
        SUM(total_revenue) AS total_revenue
    FROM {{ params.db_name }}.{{ params.schema_name }}.enriched_sales
    GROUP BY appliance_type
) AS source
ON target.appliance_type = source.appliance_type
WHEN MATCHED THEN
    UPDATE SET
        target.total_revenue = source.total_revenue
WHEN NOT MATCHED THEN
    INSERT (
        appliance_type, total_revenue
    )
    VALUES (
        source.appliance_type, source.total_revenue
    );