import pandas as pd
import numpy as np
from faker import Faker
import random
import uuid

fake = Faker()


def generate_uuids(n):
    return [str(uuid.uuid4()) for _ in range(n)]


def generate_users_data(num_users=100, date=None, filename="users.csv"):
    data = {
        "user_id": generate_uuids(num_users),
        "user_name": [fake.name() for _ in range(num_users)],
        "date_of_birth": [
            fake.date_of_birth(minimum_age=18, maximum_age=70) for _ in range(num_users)
        ],
        "sign_up_date": [
            fake.date_between(start_date="-3y", end_date="today")
            for _ in range(num_users)
        ],
        "updated_at": date,
    }
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    return df


def generate_appliances_data(filename="appliances.csv", date=None):

    uuids = [
       "e9b1d2d2-7b67-4d8b-9e7f-5b2c2f42a0b8", 
       "2b3b5e8d-92d3-4e3a-bd76-8d3e9f8c5a32", 
       "d8b93c41-9f5b-48c8-a9e7-49a22c9f7321", 
       "5b2f88d2-5e5d-4b2d-bd52-9c7d1e4d7b3a", 
       "a2e4f8c2-3d0e-4d1f-96b3-6a9f1d8a2b4c", 
       "fc9e4f77-2c8a-4a1b-b5d6-8f3d4b6e7a9b", 
       "8d3f4e2b-9a6c-4e3d-b7c2-7d1e8a5f2c6b", 
       "0b9c3e2a-7d8b-4f6d-b9e5-3a7f4c8d2e9a", 
       "4e5a6b3d-1f8e-4d7a-9c2b-3d8e2f7b9a6c", 
       "b1a2c3d4-5e6f-7a8b-9c0d-1e2f3g4h5i6j", 
       "2d3e4f5b-9a6c-7d8e-1f2a-3b4c5d6e7f8a", 
       "7f8d9c0e-1a2b-3c4d-5e6f-7a8b9c0d1e2f"
    ]

    appliance_names = [
        "Electric Heat Pump", 
        "Electric Fireplace", 
        "Electric Water Heater", 
        "Induction Stove / Cooktop", 
        "Electric Oven", 
        "Electric Dryer", 
        "Electric Grill", 
        "Electric Lawn Mower", 
        "Electric Leaf Blower", 
        "Battery-Powered Generator",
        "Electric Pool Heater", 
        "Electric Space Heater"
    ]

    appliance_types = [
        "Heating and Cooling", 
        "Heating and Cooling", 
        "Heating and Cooling", 
        "Cooking Appliances", 
        "Cooking Appliances", 
        "Drying and Laundry", 
        "Outdoor and Other Appliances", 
        "Outdoor and Other Appliances", 
        "Outdoor and Other Appliances", 
        "Outdoor and Other Appliances", 
        "Specialized and Additional Appliances", 
        "Specialized and Additional Appliances"
    ]

    prices = [
        5000, 
        600, 
        1000, 
        800, 
        1200, 
        800, 
        300, 
        500, 
        250, 
        2000, 
        500, 
        300
    ]

    data = {
        "appliance_id": uuids,
        "appliance_name": appliance_names,
        "appliance_type": appliance_types,
        "price": prices,
        "updated_at": date,
    }
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    return df


def generate_program_data(num_programs=100, date=None, filename="programs.csv"):
    program_effective_year = ["2022", "2023", "2024", "2025", "2026"]
    program_discount = ["10%", "20%", "30%", "40%", "50%"]
    programs = [
        "Energy Star Rebates",
        "Federal Tax Credits",
        "California Energy Savings Assistance Program",
        "NYSERDA",
        "Home Energy Efficiency Programs",
    ]

    data = {
        "program_id": generate_uuids(num_programs),
        "program_discount": random.choices(programs, k=num_programs),
        "program": random.choices(programs, k=num_programs),
        "program_effective_year": random.choices(program_effective_year, k=num_programs),
        "updated_at": date,
    }
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    return df


def generate_sales_data(
    num_sales=1000, users_df=None, appliances_df=None, program_df=None, filename="sales.csv", date=None
):
    if num_sales == 1:
        data = {
            "sale_id": generate_uuids(num_sales),
            "user_id": users_df["user_id"].values[0],
            "appliance_id": appliances_df["appliance_id"].values[0],
            "program_id": appliances_df["program_id"].values[0],
            "quantity": 1,
            "sale_date": date,
        }

    elif num_sales > 1:
        data = {
            "sale_id": generate_uuids(num_sales),
            "user_id": np.random.choice(users_df["user_id"], size=num_sales),
            "appliance_id": np.random.choice(appliances_df["appliance_id"], size=num_sales),
            "program_id": np.random.choice(program_df["program_id"], size=num_sales),
            "quantity": 1,
            "sale_date": date,
        }
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    return df


def get_new_sales_from_internal_api(num_sales, date):
    num_users = int(0.85 * num_sales)
    if num_users < 1:
        num_users = 1
    users_df = generate_users_data(num_users=num_users, date=date)
    appliances_df = generate_appliances_data(date=date)
    program_df = generate_program_data(num_programs=num_users, date=date)
    sales_df = generate_sales_data(
        num_sales=num_sales, users_df=users_df, appliances_df=appliances_df, program_df=program_df, date=date
    )
    return sales_df, users_df, appliances_df, program_df
