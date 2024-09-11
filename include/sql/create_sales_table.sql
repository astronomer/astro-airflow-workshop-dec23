CREATE TABLE IF NOT EXISTS 
{{ params.db_name }}.{{ params.schema_name }}.sales (
    sale_id STRING PRIMARY KEY,
    user_id STRING,
    appliance_id STRING,
    program_id STRING,
    quantity INTEGER,
    sale_date TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES {{ params.db_name }}.{{ params.schema_name }}.users(user_id),
    FOREIGN KEY (appliance_id) REFERENCES {{ params.db_name }}.{{ params.schema_name }}.appliances(appliance_id),
    FOREIGN KEY (program_id) REFERENCES {{ params.db_name }}.{{ params.schema_name }}.programs(program_id)
);
