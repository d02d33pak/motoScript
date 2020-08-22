""" Downloader Util """

import os
from timeit import default_timer

import aiofiles
import aiohttp
from bs4 import BeautifulSoup


async def download_category(soup, path, category):
    """ Category Wise """
    event_names = []
    event_links = []

    body = soup.find("div", class_="list_wrapper row")

    for event in body.find_all("li"):
        event_year = event.get("data-sid")
        event_name = event_year + " " + event.div.a.picture.img.get("alt", "")
        event_names.append(event_name)
        event_links.append(event.div.a.get("href", ""))

    os.chdir(path)
    make_dir("moto")
    make_dir(category)
    print(f">>Downloading '{category}' category")
    for i, event in enumerate(event_links):
        year_of_event = event_names[i][:4]
        name_of_event = event_names[i][5:]
        await download_event(event, year_of_event, name_of_event)


async def download_event(event, yoe, noe):
    """ Events per Category """
    start_time = default_timer()
    make_dir(yoe)  # dir for each year
    make_dir(noe)  # dir for each event per year
    async with aiohttp.ClientSession() as session:
        async with session.get(event) as content:
            image_soup = BeautifulSoup(await content.read(), "lxml")
    await download_images(image_soup)
    os.chdir("..")  # come out of event dir
    os.chdir("..")  # come out of year dir
    elapsed_time = default_timer() - start_time
    print(f"\tTime Elapsed: {elapsed_time:0.3f} sec\n")


def make_dir(dir_name):
    """
    make specified directory if it doesn't exist
    and cd into it, if it already exists, simply cd
    """
    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
        except Exception as err:
            print(err)
    os.chdir(dir_name)


async def download_images(event_soup):
    """ Images per Event """
    section = event_soup.find("section", id="links")
    photos = section.find_all("li")
    counter = skips = success = 0
    for pic in photos:
        title = pic.div.a.get("title", "")
        title = str(counter + 1).zfill(2) + " " + title + ".jpg"
        dl_link = pic.div.a.get("data-image-fullscreen", "")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(dl_link) as image_file:
                    if not os.path.exists(title):
                        async with aiofiles.open(title, "wb") as output:
                            await output.write(await image_file.read())
                        success += 1
                        print(
                            f"\tTOTAL:{len(photos):03} Dowloaded:{success:03} Skipped:{skips:03}\t",
                            end="\r",
                        )
                    elif os.path.getsize(title) != len(await image_file.read()):
                        async with aiofiles.open(title, "wb") as output:
                            await output.write(await image_file.read())
                        success += 1
                        print(
                            f"\tTOTAL:{len(photos):03} Dowloaded:{success:03} Skipped:{skips:03}\t",
                            end="\r",
                        )
                    else:
                        # if exact file already exists skip saving it
                        skips += 1
                        print(
                            f"\tTOTAL:{len(photos):03} Dowloaded:{success:03} Skipped:{skips:03}\t",
                            end="\r",
                        )

        except Exception as err:
            print(err)
        finally:
            counter += 1

    print(f"\tTOTAL:{len(photos):03} Dowloaded:{success:03} Skipped:{skips:03}")
