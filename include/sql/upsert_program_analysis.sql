MERGE INTO {{ params.db_name }}.{{ params.schema_name }}.program_analysis AS target
USING (
    SELECT 
        program,
        program_discount,
        program_effective_year,
        COUNT(sale_id) AS total_sales,
        SUM(total_revenue) AS total_revenue,
        SUM(total_savings) AS total_savings
    FROM {{ params.db_name }}.{{ params.schema_name }}.enriched_sales
    GROUP BY program, program_discount, program_effective_year,
) AS source
ON target.program = source.program 
   AND target.program_effective_year = source.program_effective_year 
   AND target.program_discount = source.program_discount
WHEN MATCHED THEN
    UPDATE SET
        target.total_sales = source.total_sales,
        target.total_revenue = source.total_revenue
WHEN NOT MATCHED THEN
    INSERT (
        program, program_discount, program_effective_year, total_sales, total_revenue, total_savings
    )
    VALUES (
        source.program, source.program_discount, source.program_effective_year, source.total_sales, source.total_revenue, source.total_savings
    );
