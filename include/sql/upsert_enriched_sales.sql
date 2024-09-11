MERGE INTO DESIGN_REVIEWS.DEV.enriched_sales AS target
USING (
    SELECT 
        *
    FROM (
        SELECT 
            s.sale_id,
            s.user_id,
            u.user_name,
            t.appliance_name,
            t.appliance_type,
            s.quantity,
            s.sale_date,
            up.program,
            up.program_effective_year,
            up.program_discount,
            t.price * s.quantity AS total_revenue,
            ROW_NUMBER() OVER (PARTITION BY s.sale_id ORDER BY s.sale_date DESC) AS rn
        FROM 
            {{ params.db_name }}.{{ params.schema_name }}.sales s
        JOIN 
            {{ params.db_name }}.{{ params.schema_name }}.users u ON s.user_id = u.user_id
        JOIN 
            {{ params.db_name }}.{{ params.schema_name }}.appliances t ON s.appliance_id = t.appliance_id
        JOIN 
            {{ params.db_name }}.{{ params.schema_name }}.programs up ON s.program_id = up.program_id
    ) AS subquery
    WHERE 
        rn = 1
) AS source
ON 
    target.sale_id = source.sale_id
WHEN MATCHED THEN
    UPDATE SET
        target.user_id = source.user_id,
        target.user_name = source.user_name,
        target.appliance_name = source.appliance_name,
        target.appliance_type = source.appliance_type,
        target.quantity = source.quantity,
        target.sale_date = source.sale_date,
        target.program = source.program,
        target.program_effective_year = source.program_effective_year,
        target.program_discount = source.program_discount,
        target.total_revenue = source.total_revenue
WHEN NOT MATCHED THEN
    INSERT (
        sale_id, user_id, user_name, appliance_name, appliance_type, quantity, sale_date,
        program, program_effective_year, program_discount, total_revenue
    )
    VALUES (
        source.sale_id, source.user_id, source.user_name, source.appliance_name, source.appliance_type, 
        source.quantity, source.sale_date, source.program, source.program_effective_year, source.program_discount, 
        source.total_revenue
    );
