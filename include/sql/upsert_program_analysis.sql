MERGE INTO {{ params.db_name }}.{{ params.schema_name }}.program_analysis AS target
USING (
    SELECT 
        program,
        program_effective_year,
        program_discount,
        COUNT(sale_id) AS total_sales,
        SUM(total_revenue) AS total_revenue
    FROM {{ params.db_name }}.{{ params.schema_name }}.enriched_sales
    GROUP BY program, program_effective_year, program_discount
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
        program, program_effective_year, program_discount, total_sales, total_revenue
    )
    VALUES (
        source.program, source.program_effective_year, source.program_discount, source.total_sales, source.total_revenue
    );
