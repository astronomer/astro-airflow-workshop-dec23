def map_cities_to_weather(forecast, cities_coordinates, type_of_forecast):
    """
    Maps each city to its corresponding weather data based on the forecast type.
    """
    print(cities_coordinates)

    if type(cities_coordinates) == dict:
        city_weather_info = {cities_coordinates["city"]: []}

        city = cities_coordinates["city"]
        if (
            abs(cities_coordinates["lat"] - forecast["latitude"]) < 0.01
            and abs(cities_coordinates["long"] - forecast["longitude"]) < 0.01
        ):
            city_weather_info[city] = forecast["hourly"][type_of_forecast]

    else:
        city_weather_info = {city["city"]: [] for city in cities_coordinates}

        for entry in forecast:
            for city_info in cities_coordinates:
                city = city_info["city"]
                if (
                    abs(city_info["lat"] - entry["latitude"]) < 0.01
                    and abs(city_info["long"] - entry["longitude"]) < 0.01
                ):
                    city_weather_info[city] = entry["hourly"][type_of_forecast]
                    break

    return city_weather_info


def create_weather_table(timestamps, city_weather_info):
    """
    Creates a table from the weather data and timestamps.
    """
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
