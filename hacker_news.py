import requests  # allows us to download that html file
from bs4 import BeautifulSoup  # allows us to use the html to grab different data
import pprint

# grab data and then use Beautiful soup to clean it up
res = requests.get('https://news.ycombinator.com/')
res2 = requests.get('https://news.ycombinator.com/news?p=2')
# this creates html file to an object so we can manipulate it
soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')
links = soup.select('.titleline > a')
links2 = soup2.select('.titleline > a')
subtext = soup.select('.subtext')
subtext2 = soup2.select('.subtext')

mega_links = links + links2
mega_subtext = subtext + subtext2


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)


pprint.pprint(create_custom_hn(mega_links, mega_subtext))
