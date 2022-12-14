from datetime import date
import string
import random
import requests


def get_age(birthdate):
    """
    Return number of year(age).
    """
    today = date.today()
    return (
        today.year
        - birthdate.year
        - ((today.month, today.day) < (birthdate.month, birthdate.day))
    )


def get_random_password():
    """
    Return randon password string length of 6.
    """
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=6))


def get_gender_by_name(name):
    """
    API call for get gender by name.
    """
    url = f"https://api.genderize.io/?name={name}"
    data = requests.get(url).json()
    return str(data["gender"])
