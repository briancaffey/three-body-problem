from bs4 import BeautifulSoup
import logging
import urllib.request
url = "https://docs.python.org/3.4/howto/urllib2.html"
HEADERS = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }

# https://www.kunnu.com/santi/
BASE_URL = 'https://www.kunnu.com/santi/'
START = 26651
# END = 26653
END = 26695
PAGE_IDS = [x for x in range(START, END)]

def get_soup_from_url(url):
    logging.info(f"Getting HTML for {url}")
    print(f"getting html for {url}")
    req = urllib.request.Request(url, headers=HEADERS)
    response = urllib.request.urlopen(req)
    page = response.read()

    soup = BeautifulSoup(page, 'html.parser')
    return soup



def run():
    urls = [f"{BASE_URL}{page_id}.htm" for page_id in PAGE_IDS]
    for url in urls:
        try:
            soup = get_soup_from_url(url)
            # chapter title
            title = soup.find('h1', {'id': 'nr_title'}).text
            print(title)
            main_div = soup.find('div', {'id': 'nr1'})
            paragraphs = main_div.findChildren('p')
            chapter_text = "".join([x.text for x in paragraphs])
            print(len(paragraphs))

            with open(f"chapters/{url.split('/')[-1]}", 'w+') as f:
                f.write(chapter_text)
        except urllib.error.HTTPError as e:
            print(f"not able to get text for URL, going to next URL")
            continue


if __name__ == "__main__":
    run()
