import pandas as pd

def map_cities_to_weather(forecasts: list, cities_coordinates: list, type_of_forecast:str) -> pd.DataFrame:
    """
    Maps each city to its corresponding weather data based on the forecast type.
    
    Parameters:
    - forecasts: A list of dictionaries containing weather data.
    - cities_coordinates: A list of dictionaries containing city names and their coordinates.
    - type_of_forecast: A string indicating the type of forecast to extract from the hourly data.
    
    Returns:
    - A pandas DataFrame containing the weather data for each city for each timestamp.
    """

    # Create list of city names and initial timestamps from the forecasts
    list_of_cities = [city["city"] for city in cities_coordinates]
    timestamps = forecasts[0]["hourly"]["time"]

    # Initialize DataFrame
    df = pd.DataFrame(columns=list_of_cities, index=timestamps)

    # Define a small threshold for coordinate matching
    threshold = 0.05

    # Iterate over each city in the coordinates list
    for city in cities_coordinates:
        city_name = city['city']
        city_lat = city['lat']
        city_long = city['long']
        
        # Find and process each matching forecast
        for forecast in forecasts:
            # Check if forecast coordinates are within threshold of city coordinates
            if (abs(forecast['latitude'] - city_lat) < threshold and
                abs(forecast['longitude'] - city_long) < threshold):
                # If coordinates match, populate the DataFrame for this city
                for i, time in enumerate(forecast["hourly"]["time"]):
                    df.at[time, city_name] = forecast["hourly"][type_of_forecast][i]
    
    return df







def create_weather_table(timestamps, city_weather_info):
    """
    Creates a table from the weather data and timestamps.
    """
    print(city_weather_info)

    table = [
        [timestamp] + [city_weather_info[city][i] for city in city_weather_info]
        for i, timestamp in enumerate(timestamps)
    ]
    headers = ["Timestamp"] + list(city_weather_info.keys())
    return table, headers




def log_weather_table(table, headers):
    """
    Logs the weather table using the tabulate library.
    """
    from tabulate import tabulate

    print(tabulate(table, headers=headers, tablefmt="grid"))


def save_weather_table_to_csv(table, headers, dag_run_id):
    """
    Saves the weather table to a CSV file in the specified directory.
    """
    import os
    import csv

    os.makedirs(f"include/{dag_run_id}/", exist_ok=True)
    with open(f"include/{dag_run_id}/forecast.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(table)
