import pandas as pd


def map_cities_to_weather(
    forecasts: list, cities_coordinates: list, type_of_forecast: str
) -> pd.DataFrame:
    """
    Maps each city to its corresponding weather data based on the forecast type.

    Parameters:
    - forecasts: A list of dictionaries containing weather data.
    - cities_coordinates: A list of dictionaries containing city names and their coordinates.
    - type_of_forecast: A string indicating the type of forecast to extract from the hourly data.

    Returns:
    - A pandas DataFrame containing the weather data for each city for each timestamp.
    """
    list_of_cities = [city["city"] for city in cities_coordinates]
    timestamps = forecasts[0]["hourly"]["time"]

    df = pd.DataFrame(columns=list_of_cities, index=timestamps)

    threshold = 0.05

    for city in cities_coordinates:
        city_name = city["city"]
        city_lat = city["lat"]
        city_long = city["long"]

        for forecast in forecasts:
            if (
                abs(forecast["latitude"] - city_lat) < threshold
                and abs(forecast["longitude"] - city_long) < threshold
            ):
                for i, time in enumerate(forecast["hourly"]["time"]):
                    df.at[time, city_name] = forecast["hourly"][type_of_forecast][i]

    return df
