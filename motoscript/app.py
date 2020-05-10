'''
I recommend you visit the motogp website and 
inspect element to understand the script better
'''

import sys
import requests
from bs4 import BeautifulSoup
from downloader import download_category 


def start_download(category, path):
    base_url = 'https://motogp.com/en/photos/'
    pathByCategory = {'gp':'events', 'best_of':'best+of', 'riders':'riders', 'teams':'teams'}
    try:
        full_url = base_url + pathByCategory[category]
        content = requests.get(full_url).text
        # parsing the content 
        soup = BeautifulSoup(content, 'lxml')
        download_category(soup, path, category)
    except KeyError:
        print('wrong category, exiting...')
        exit(1)


def run():
    '''
    categories gp, best_of, riders, teams
    can be passed as cmd line args
    '''
    default_category = 'teams'
    path = '/home/d02/Downloads'
    category = str(sys.argv[1]) if len(sys.argv) > 1 else default_category 
    start_download(category, path)


