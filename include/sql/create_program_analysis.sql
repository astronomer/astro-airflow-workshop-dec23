CREATE TABLE IF NOT EXISTS {{ params.db_name }}.{{ params.schema_name }}.program_analysis (
    program_id STRING,
    program STRING,
    program_effective_year STRING,
    program_discount STRING,
    total_sales INTEGER,
    total_revenue NUMBER,
    total_savings NUMBER
    PRIMARY KEY (program_id, program, program_effective_year)
);