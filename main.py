'''
I recommend you visit the motogp website 
and inspect element to understand the script better
'''

import requests
from bs4 import BeautifulSoup
from downloader import download_category 


def start_download(category, path):
    base_url = 'https://motogp.com/en/photos/'
    pathByCategory = {'gp':'events', 'best_of':'best+of', 'riders':'riders', 'teams':'teams'}
    try:
        full_url = base_url + pathByCategory[category]
        content = requests.get(full_url).text
        soup = BeautifulSoup(content, 'lxml')
        download_category(soup, path, category)
    except KeyError:
        print('wrong category, exiting...')
        exit(1)


if __name__ == '__main__':
    '''
    can pass gp, best_of, teams
    or riders as category.
    path is where you would like
    to download all the images to
    '''
    path = '/home/d02/Downloads'
    start_download('teams', path)


