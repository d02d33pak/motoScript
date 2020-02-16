import os
import urllib.error
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup


def makeDir(folder_name):
    if not os.path.exists(folder_name):
        try:
            os.makedirs(folder_name)
        except Exception as err:
            print(err)
            print('error creating '+folder_name)
    os.chdir(folder_name)


def download_images(image_soup):
    section = image_soup.find('section', id='links')
    photos = section.find_all('li')
    counter = success = 0
    for pic in photos: 
        title = pic.div.a.get('title', '') 
        #to create unique title since
        #many images have same name on website 
        title = str(counter).zfill(2) + ' ' + title
        title += '.jpg'
        dl_link = pic.div.a.get('data-image-fullscreen', '')
        try:
            '''can be done with below comment
            also but using urlopen coz its better'''
            #urlretrieve(dl_link, title)
            conn = urlopen(dl_link)
            if not os.path.exists(title) and os.path.getsize(title) == len(conn.read):
                output = open(title)
                output.write(conn.read())
                output.close()
                success+=1
        except Exception as err:
            print(err)
            print('**_err_:' + title)
        finally:
            counter+=1

    print(success,'/',len(photos),'downloaded')


def download_category(soup, path, category):

    div_id = 'mgp-carousel-'+category
    event_names = []
    event_links = []

    body = soup.find('div',id=div_id)

    for event in body.find_all('li'):
        event_year = event.get('data-sid')
        event_name = event_year + ' ' + event.div.a.picture.img.get('alt', '')
        event_names.append(event_name)
        event_links.append(event.div.a.get('href', ''))

    os.chdir(path)
    makeDir('moto')
    makeDir(category)
    makeDir(event_year)

    for i,event in enumerate(event_links):
        makeDir(event_names[i])
        content = urlopen(event)
        image_soup = BeautifulSoup(content, 'lxml')
        download_images(image_soup)
        os.chdir('..')

