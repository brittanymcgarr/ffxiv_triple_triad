import re
import character
from card import Card


LODESTONE_URL_REGEX = r'^https:\/\/na\.finalfantasyxiv\.com\/lodestone\/character\/[0-9]+'
URL_PROMPT = \
    "Please input a valid lodestone url. Format should be: https://na.finalfantasyxiv.com/lodestone/character/0..9"

if __name__ == '__main__':
    valid_url = False
    character_url = ""

    while not valid_url:
        character_url = input("Please input the target character's lodestone url: ")
        valid_url = re.match(LODESTONE_URL_REGEX, character_url)

        if not valid_url:
            print(URL_PROMPT)

    print("Finding character...")
    print(character)

    try:
        character = character.get_character_data(character_url)
    except ValueError as err:
        print("Could not find character data.")

    card = Card(character)
    print(card)

    card.create_card_image()
