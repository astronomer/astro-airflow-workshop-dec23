CREATE TABLE IF NOT EXISTS {{ params.db_name }}.{{ params.schema_name }}.program_analysis (
    program STRING,
    program_discount STRING,
    program_effective_year STRING,
    total_sales INTEGER,
    total_revenue NUMBER,
    total_savings NUMBER,
    PRIMARY KEY (program, program_effective_year)
);