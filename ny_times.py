from bs4 import BeautifulSoup
import requests


def scrape_ny_times():
    requested_page = requests.get("https://www.nytimes.com/")
    page_content = requested_page.content
    soup1 = BeautifulSoup(page_content, 'html5lib')
    page_top_stories = soup1.find_all("section", attrs={'data-testid': 'block-TopStories'})
    headline = [section.h2.get_text() for section in page_top_stories]
    headline_url = [section.a['href'] for section in page_top_stories]
    top_headline_text = f"The top headline in New York Times right now is '{headline[0]}. "
    top_headline_url = f"You can read it in this link: https://www.nytimes.com{headline_url[0]}"
    return top_headline_text + top_headline_url
