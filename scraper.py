from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os
from datetime import datetime, timedelta
from model import Odd, engine
from sqlalchemy.orm import Session

import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

HTML_FILE_PATH = 'html_cache/{url}.html'
CACHE_DURATION = timedelta(minutes=5)

def fetch_html_with_selenium(url):
    # Set up Selenium WebDriver
    options = Options()
    options.headless = True  # Run in headless mode
    #service = Service('/opt/homebrew/Cellar/geckodriver')  # Update with the path to your WebDriver
    driver = webdriver.Chrome(options=options)
    
    # Load the page
    driver.get(url)
    
    # Wait for the JavaScript to load the content
    time.sleep(5)  # Adjust the sleep time as needed
    
    # Get the page source
    html_content = driver.page_source
    
    # Close the WebDriver
    driver.quit()
    
    # Save the HTML content to a file
    os.makedirs(os.path.dirname(HTML_FILE_PATH.format(url=url)), exist_ok=True)
    with open(HTML_FILE_PATH.format(url=url), 'w', encoding='utf-8') as file:
        file.write(html_content)
    
    return html_content

def load_html_from_file(url):
    with open(HTML_FILE_PATH.format(url=url), 'r', encoding='utf-8') as file:
        return file.read()

def is_cache_valid(url):
    if not os.path.exists(HTML_FILE_PATH.format(url=url)):
        return False
    file_mod_time = datetime.fromtimestamp(os.path.getmtime(HTML_FILE_PATH.format(url=url)))
    return datetime.now() - file_mod_time < CACHE_DURATION


def save_odds_to_db(odds):
    with Session(engine) as session:
        for odd in odds:
            odd_entry = (
                session.query(Odd)
                .filter(
                    Odd.match_time == odd['match_time'], 
                    Odd.home_team == odd['home'], 
                    Odd.away_team == odd['away']
                )
            ).first()
            if odd_entry:
                odd_entry.home_odds = odd['odds']['home']
                odd_entry.draw_odds = odd['odds']['draw']
                odd_entry.away_odds = odd['odds']['away']
            else:
                odd_entry = Odd(
                    match_time=odd['match_time'],
                    home_team=odd['home'],
                    away_team=odd['away'],
                    home_odds=odd['odds']['home'],
                    draw_odds=odd['odds']['draw'],
                    away_odds=odd['odds']['away']
            )
            session.add(odd_entry)
        session.commit()


def scrape_matches():
    url = 'https://oddspedia.com/football/brazil/serie-a/odds'
    
    if is_cache_valid(url):
        html_content = load_html_from_file(url)
    else:
        html_content = fetch_html_with_selenium(url)
    
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    matches_odds = []

    matches = soup.find('div', id='match-odds')
    for match in matches.find_all('div', class_='match-list-item'):
        match_time = match.find('span', class_='match-date__time').text.strip()
        teams = match.find_all('div', class_='match-team')
        home, away = (team.text.strip() for team in teams)
        odds = match.find_all('span', class_='odd__value')

        odd_values = (float(odd.text.strip()) for odd in odds)
        home_odds, draw_odds, away_odds = odd_values

        match_odds = {
            'match_time': match_time,
            'home': home, 
            'away': away,
            'odds': {
                'home': home_odds, 
                'draw': draw_odds, 
                'away': away_odds
            }
        }
        print(match_odds)  # Debug: Print the extracted odds
        matches_odds.append(match_odds)
    
    save_odds_to_db(matches_odds)

    return matches_odds