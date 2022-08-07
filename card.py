################################################################################
## card.py                                                                    ##
##                                                                            ##
## Creates a Triple Triad card from the prompted character.                   ##
##                                                                            ##
## britmcgarr@gmail.com                                                       ##
################################################################################

import random
import re
import requests
import datetime
from character import Character


RANGE_5_STAR = (5,10)
RANGE_4_STAR = (1,9)
RANGE_3_STAR = (1,7)
RANGE_2_STAR = (1,5)
RANGE_1_STAR = (1,4)

VALUE_5_STAR = (30, 99)
VALUE_4_STAR = (25,29)
VALUE_3_STAR = (20,24)
VALUE_2_STAR = (15,19)
VALUE_1_STAR = (4,14)


class Card:

    def __init__(self, character):
        self.character = character
        self.id = self.create_card_id()
        self.star_rating = 1
        self.values = []

        self.generate_edge_values()

    def __repr__(self):
        card_string = \
            f"< Card: {self.id}, Character: {self.character.name}, Stars: {self.star_rating}, Values: {self.values} >"
        return card_string

    def create_card_id(self):
        time = datetime.datetime.now()
        id_string = self.character.name + "_" + time.strftime("%Y%m%d%H%M%S")
        id_string = re.sub(r'(\s\'-)*', '', id_string)

        return id_string

    # Generate character card value and star ranking
    def generate_edge_values(self):
        total_jobs = len(self.character.jobs.keys())
        total_capped = 0
        random_ranges = ()
        star_value = ()

        for job, level in self.character.jobs.items():
            if level >= 90:
                total_capped += 1

        # <14 => 1 star
        # 15-19 => 2 star
        # 20-24 => 3 star
        # 25-29 => 4 star
        # 30+ => 5 star
        if total_jobs > 30 and total_capped == total_jobs:
            self.star_rating = 5
            random_ranges = RANGE_5_STAR
            star_value = VALUE_5_STAR
        elif total_jobs > 20 and total_capped / total_jobs > 0.90:
            self.star_rating = 4
            random_ranges = RANGE_4_STAR
            star_value = VALUE_4_STAR
        elif total_jobs > 10:
            self.star_rating = 3
            random_ranges = RANGE_3_STAR
            star_value = VALUE_3_STAR
        elif total_jobs > 3:
            self.star_rating = 2
            random_ranges = RANGE_2_STAR
            star_value = VALUE_2_STAR
        else:
            self.star_rating = 1
            random_ranges = RANGE_1_STAR
            star_value = VALUE_1_STAR

        # pick four numbers for the values
        random.seed(datetime.datetime.now())
        star_value_achieved = False

        while not star_value_achieved:
            north = random.randint(random_ranges[0], random_ranges[1])
            east = random.randint(random_ranges[0], random_ranges[1])
            south = random.randint(random_ranges[0], random_ranges[1])
            west = random.randint(random_ranges[0], random_ranges[1])

            if north + south + east + west in range(star_value[0], star_value[1]):
                star_value_achieved = True
                self.values = [north, south, east, west]

    def create_card_image(self):
        pass

    def host_card(self):
        pass
