from bs4 import BeautifulSoup
from urllib.request import urlopen
from downloader import download_category 

def start_download(category, path):
    main_url = 'https://motogp.com/en/photos/'
    if category == 'gp': 
        content = urlopen(main_url+'events')
        soup = BeautifulSoup(content, 'lxml')
        download_category(soup, path, category)
    elif category == 'best_of': 
        content = urlopen(main_url+'best+of')
        soup = BeautifulSoup(content, 'lxml')
        download_category(soup, path, category)
    elif category == 'riders': 
        content = urlopen(main_url+'riders')
        soup = BeautifulSoup(content, 'lxml')
        download_category(soup, path, category)
    elif category == 'teams': 
        content = urlopen(main_url+'teams')
        soup = BeautifulSoup(content, 'lxml')
        download_category(soup, path, category)
    else:
        print('wrong category')
    

if __name__ == '__main__':
    '''
    can pass gp, best_of, teams
    or riders as category.
    path is where you would like
    to download all the images to
    '''
    path = '/home/d02/Downloads'
    start_download('teams', path)

