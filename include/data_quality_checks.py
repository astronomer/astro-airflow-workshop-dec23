from datetime import datetime, timedelta


column_mapping_users = {
    "DATE_OF_BIRTH": {
        "min": {"geq_to": datetime.strptime("1900-01-01", "%Y-%m-%d").date()},
        # Users need to be at least 13 years old
        "max": {"leq_to": (datetime.now() - timedelta(days=13 * 365)).date()},
    },
    "SIGN_UP_DATE": {
        "min": {"geq_to": datetime.strptime("2020-01-01", "%Y-%m-%d").date()},
        "max": {"leq_to": datetime.now().date()},
    },
}

column_mapping_programs = {
    "PROGRAM": {
        "null_check": {"equal_to": 0},
    },
    "PROGRAM_EFFECTIVE_YEAR": {
        "null_check": {"equal_to": 0},
    },
    "PROGRAM_DISCOUNT": {
        "null_check": {"equal_to": 0},
    },
}

column_mapping_sales = {
    "QUANTITY": {
        "null_check": {"equal_to": 0},
        "min": {"geq_to": 0},
        "max": {"leq_to": 100},
    }
}

column_mappings = {
    "users": column_mapping_users,
    "programs": column_mapping_programs,
    "sales": column_mapping_sales,
}
