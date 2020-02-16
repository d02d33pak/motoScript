from bs4 import BeautifulSoup
from urllib.request import urlopen
from downloader import download_category 

def start_download(category, path):
    main_url = 'https://motogp.com/en/photos'
    content = urlopen(main_url)
    soup = BeautifulSoup(content, 'lxml')

    if category in ('gp', 'best_of', 'riders', 'teams'):
        download_category(soup, path, category)
    else:
        print('wrong category')


if __name__ == '__main__':
    '''
    can pass gp, best_of, teams
    or riders as category
    '''
    path = '/home/d02/Downloads'
    start_download('gp', path)

