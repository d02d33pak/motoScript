import os
import asyncio
import aiohttp
import aiofiles
import requests
from timeit import default_timer
from bs4 import BeautifulSoup


def download_category(soup, path, category):
    event_names = []
    event_links = []

    body = soup.find('div', class_='list_wrapper row')

    for event in body.find_all('li'):
        event_year = event.get('data-sid')
        event_name = event_year + ' ' + event.div.a.picture.img.get('alt', '')
        event_names.append(event_name)
        event_links.append(event.div.a.get('href', ''))

    os.chdir(path)
    makeDir('moto')
    makeDir(category)
    print(f">>Downloading '{category}' category")

    for i,event in enumerate(event_links):
        start_time = default_timer()
        makeDir(event_names[i][:4])     # year-wise folder
        makeDir(event_names[i][5:])     # event per year)
        print(f'[{i+1}/{len(event_links)}] {event_names[i][:4]} → {event_names[i][5:]}')
        content = requests.get(event).text
        image_soup = BeautifulSoup(content, 'lxml')
        asyncio.run(download_images(image_soup))
        os.chdir('..')      # come out of event dir
        os.chdir('..')      # come out of year dir
        elapsed_time = default_timer() - start_time 
        print(f'\tTime Elapsed: {elapsed_time:0.3f}\n')


def makeDir(folder_name):
    if not os.path.exists(folder_name):
        try:
            os.makedirs(folder_name)
        except Exception as err:
            print(err)
    os.chdir(folder_name)


async def download_images(event_soup):
    section = event_soup.find('section', id='links')
    photos = section.find_all('li')
    counter = skips = success = 0
    for pic in photos: 
        title = pic.div.a.get('title', '') 
        title = str(counter+1).zfill(2) + ' ' + title + '.jpg'
        dl_link = pic.div.a.get('data-image-fullscreen', '')
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(dl_link) as image_file:
                    if (not os.path.exists(title)) :
                        jpg_image = await aiofiles.open(title, 'wb')
                        await jpg_image.write(await image_file.read())
                        success+=1
                        await jpg_image.close()
                        print(f'\tTOTAL:{len(photos):03} Dowloaded:{success:03} Skipped:{skips:03}\t', end='\r')
                    elif os.path.getsize(title) != len(await image_file.read()):
                        jpg_image = await aiofiles.open(title, 'wb')
                        await jpg_image.write(await image_file.read())
                        success+=1
                        await jpg_image.close()
                        print(f'\tTOTAL:{len(photos):03} Dowloaded:{success:03} Skipped:{skips:03}\t', end='\r')
                    else:
                        # * if exact file already exists skip the download
                        skips+=1
                        print(f'\tTOTAL:{len(photos):03} Dowloaded:{success:03} Skipped:{skips:03}\t', end='\r')

        except Exception as err:
            print(err)
        finally:
            counter+=1

    print(f'\tTOTAL:{len(photos):03} Dowloaded:{success:03} Skipped:{skips:03}')

