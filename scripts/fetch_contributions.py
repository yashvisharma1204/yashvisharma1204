# scripts/fetch_contributions.py
import requests
from bs4 import BeautifulSoup
import json

USERNAME = "yashvisharma1204"  # Replace with your handle
url = f"https://github.com/users/{USERNAME}/contributions"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
days = soup.find_all('td', class_='ContributionCalendar-day')

contrib_data = []
for day in days:
    date = day.get('data-date')
    count = day.get('data-level', '0')
    if date:
        contrib_data.append({"date": date, "level": int(count)})

with open('data/contributions.json', 'w') as f:
    json.dump(contrib_data, f)