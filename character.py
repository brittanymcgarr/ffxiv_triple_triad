################################################################################
## character.py                                                               ##
##                                                                            ##
## Character parsing from FFXIV Lodestone for Triple Triad Generator.         ##
##                                                                            ##
## britmcgarr@gmail.com                                                       ##
################################################################################

import re
import requests
from bs4 import BeautifulSoup


CLASS_REGEX=r'frame__chara__name'
CHARACTER_NAME_REGEX=r'[a-zA-Z_\-\']+\s[a-zA-Z_\-\']+'
JOB_LEVEL_REGEX=r'character__job__level'
JOB_LEVEL=r'[0-9\-]+'
JOB_CLASS_REGEX=r'character__job__name js__tooltip'
JOB_CLASS_NAME=r'[a-zA-Z]+\s*[a-zA-Z]*'
IMAGE_DIV=r'character__detail__image'
IMAGE_CLASS=r'js__image_popup'
IMAGE_REGEX=r'https:\/\/img2\.finalfantasyxiv\.com\/f\/[a-zA-Z0-9_]+\.jpg\?[0-9]+'


class Character:

    def __init__(self, name, jobs, image):
        self.name = name
        self.jobs = jobs
        self.image = image

    def __repr__(self):
        return f"< Character: {self.name}, Jobs: {self.jobs}, Image Link: {self.image} >"




def get_character_data(url):
    # get the html from the site
    html_text = requests.get(url + "/class_job/").text
    image_text = requests.get(url + "/#profile").text

    if not html_text:
        raise ValueError("ERROR: Could not retrieve character from url.")

    # parse with beautiful soup
    soup = BeautifulSoup(html_text, "html.parser")

    # find the character name
    name = soup.find('p', class_=CLASS_REGEX, string=re.compile(CHARACTER_NAME_REGEX))
    name = name.contents[0]

    # find the character's jobs
    levelled_jobs = {}
    job_levels = soup.find_all('div', class_=JOB_LEVEL_REGEX, string=re.compile(JOB_LEVEL))
    job_classes = soup.find_all('div', class_=JOB_CLASS_REGEX, string=re.compile(JOB_CLASS_NAME))

    for index in range(0, len(job_classes)):
        job_level = job_levels[index].contents[0]

        if job_level != "-":
            job = job_classes[index].contents[0]
            levelled_jobs[job] = job_level

    # Get the character portrait link
    if not image_text:
        raise ValueError("ERROR: Could not find character portrait data.")

    soup = BeautifulSoup(image_text, "html.parser")
    div = soup.find('a', class_=IMAGE_CLASS)
    portrait = div['href']

    # create character object
    character = Character(name, levelled_jobs, portrait)
    
    return character
