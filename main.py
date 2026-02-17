import requests
import smtplib
import os

# api key stored as a local env var
api_key = os.environ.get("OWN_API_KEY")
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
my_email = "your@email.com"
password = "yourpassword"

parameters = {
    "lat": 51.507351,
    "lon": -0.127758,
    "appid": api_key,
    "cnt": 4,
}

response = requests.get(OWM_Endpoint, params=parameters)
response.raise_for_status()
weather_data = response.json()


def write_error(message):
    """Will write  message to error file"""
    with open("./log/error.txt", 'a') as error_file:
        error_file.write(f"{message}\n")


will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as connection:
            connection.starttls()
            connection.login(my_email, password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg=f"Subject: Weather update\n\n Bring an umbrella it's raining"
            )
    except smtplib.SMTPAuthenticationError:
        write_error("Authentication Error Check Username and Password\n")
