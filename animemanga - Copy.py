import requests
import re
from discord import Embed
from datetime import datetime
import random

ANILIST_API_URL = "https://graphql.anilist.co"

# Clean HTML function
def clean_html(raw_html):
    clean_text = re.sub(r'<br\s*/?>', '\n', raw_html)  # Replace <br> with new lines
    clean_text = re.sub(r'</?i>', '', clean_text)      # Remove <i> and </i>
    clean_text = re.sub(r'\s+', ' ', clean_text)       # Replace multiple spaces with a single space
    clean_text = clean_text.strip()                    # Remove leading and trailing spaces
    return clean_text

# Determine season based on the month
def determine_season(month):
    if month in [12, 1, 2]:
        return "Winter ❄️"
    elif month in [3, 4, 5]:
        return "Spring 🌱"
    elif month in [6, 7, 8]:
        return "Summer 🌞"
    elif month in [9, 10, 11]:
        return "Fall 🍁"

# Generate a random color for embeds
def generate_random_color():
    return random.randint(0, 0xFFFFFF)

# Format date for display in embed
def format_date(day, month, year):
    day_str = str(day) if day is not None else '?'
    month_str = str(month) if month is not None else '?'
    year_str = str(year) if year is not None else '?'
    return f"{day_str}/{month_str}/{year_str}"

# Fetch Anime info from Anilist API
def fetch_anime_info(title):
    query = '''
    query ($search: String) {
        Media (search: $search, type: ANIME) {
            title {
                romaji
                english
                native
            }
            description
            startDate {
                year
                month
                day
            }
            endDate {
                year
                month
                day
            }
            episodes
            genres
            averageScore
            status
            coverImage {
                large
            }
            rankings {
                rank
                type
                allTime
            }
        }
    }
    '''
    variables = {'search': title}
    response = requests.post(ANILIST_API_URL, json={'query': query, 'variables': variables})
    if response.status_code == 200:
        data = response.json()
        return data['data']['Media']
    else:
        return None

# Fetch Manga info from Anilist API
def fetch_manga_info(title):
    query = '''
    query ($search: String) {
        Media (search: $search, type: MANGA) {
            title {
                romaji
                english
                native
            }
            description
            startDate {
                year
                month
                day
            }
            endDate {
                year
                month
                day
            }
            chapters
            genres
            averageScore
            status
            coverImage {
                large
            }
            rankings {
                rank
                type
                allTime
            }
        }
    }
    '''
    variables = {'search': title}
    response = requests.post(ANILIST_API_URL, json={'query': query, 'variables': variables})
    if response.status_code == 200:
        data = response.json()
        return data['data']['Media']
    else:
        return None

# Create Embed for Anime
def create_anime_embed(data):
    title = data['title']['romaji'] if data['title']['english'] is None else data['title']['english']
    description = clean_html(data['description'])
    season = determine_season(data['startDate']['month']) if data['startDate']['month'] else "Unknown Season"
    rankings = [f"{r['rank']} ({r['type']})" for r in data['rankings'] if r['allTime']]
    rankings_str = ', '.join(rankings) if rankings else 'No rankings available'

    # Format release dates with fallback
    start_date = format_date(data['startDate'].get('day'), data['startDate'].get('month'), data['startDate'].get('year'))
    end_date = format_date(data['endDate'].get('day'), data['endDate'].get('month'), data['endDate'].get('year')) if data.get('endDate') else '?/?/?'

    # Try to create a release_date object if possible
    try:
        release_date = datetime(data['startDate'].get('year'), data['startDate'].get('month'), data['startDate'].get('day'))
    except (TypeError, ValueError):
        release_date = None

    # Determine the status
    current_date = datetime.now()
    if release_date and release_date > current_date:
        status = 'Not yet released'
    else:
        status = data['status']

    release_date_str = f"{start_date} - {end_date}"
    embed = Embed(title=title, description=description, color=generate_random_color())
    embed.add_field(name="Season", value=season, inline=False)
    embed.add_field(name="Release Dates", value=release_date_str, inline=False)
    embed.add_field(name="Total Episodes", value=f"{data['episodes']}", inline=True)
    embed.add_field(name="Genre", value=", ".join(data['genres']), inline=True)
    embed.add_field(name="Average Score", value=f"{data['averageScore']}", inline=True)
    embed.add_field(name="Status", value=status, inline=True)
    embed.add_field(name="Rankings", value=rankings_str, inline=False)
    embed.set_thumbnail(url=data['coverImage']['large'])
    return embed

# Create Embed for Manga
def create_manga_embed(data):
    title = data['title']['romaji'] if data['title']['english'] is None else data['title']['english']
    description = clean_html(data['description'])
    rankings = [f"{r['rank']} ({r['type']})" for r in data['rankings'] if r['allTime']]
    rankings_str = ', '.join(rankings) if rankings else 'No rankings available'

    # Format release dates
    start_date = format_date(data['startDate'].get('day'), data['startDate'].get('month'), data['startDate'].get('year'))
    end_date = format_date(data['endDate'].get('day'), data['endDate'].get('month'), data['endDate'].get('year')) if data.get('endDate') else '?/?/?'

    release_date_str = f"{start_date} - {end_date}"

    embed = Embed(title=title, description=description, color=generate_random_color())
    embed.add_field(name="Release Dates", value=release_date_str, inline=False)
    embed.add_field(name="Chapters", value=f"{data['chapters']}", inline=True)
    embed.add_field(name="Genre", value=", ".join(data['genres']), inline=True)
    embed.add_field(name="Average Score", value=f"{data['averageScore']}", inline=True)
    embed.add_field(name="Status", value=data['status'], inline=True)
    embed.add_field(name="Rankings", value=rankings_str, inline=False)
    embed.set_thumbnail(url=data['coverImage']['large'])
    return embed