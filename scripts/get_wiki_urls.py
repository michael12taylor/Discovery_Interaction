from requests.api import request
import scrape_wiki
import requests
from bs4 import BeautifulSoup

# Multiple URLs are needed when all the characters don't fit on a single page
# Looks like rails is being used so I don't think I can just easily reverse engineer the BPI :(
avatar = {
    "min_content_length": 20000,
    "base_url": "https://avatar.fandom.com",
    "character_listing_urls": [
        "https://avatar.fandom.com/wiki/Category:Characters",
        "https://avatar.fandom.com/wiki/Category:Characters?from=Hou-Ting%27s+prisoner",
        "https://avatar.fandom.com/wiki/Category:Characters?from=Ozai",
        "https://avatar.fandom.com/wiki/Category:Characters?from=Yi+Ming"
    ]
}

harry_potter = {
    "min_content_length": 20000,
    "base_url": "https://harrypotter.fandom.com",
    "character_listing_urls": [
        "https://harrypotter.fandom.com/wiki/Category:Wizards",
        "https://harrypotter.fandom.com/wiki/Category:Wizards?from=Bienbon%2C+Archibald%0AArchibald+Bienbon",
        "https://harrypotter.fandom.com/wiki/Category:Wizards?from=Carusus%2C+Luccas%0ALuccas+Carusus",
        "https://harrypotter.fandom.com/wiki/Category:Wizards?from=Doge%2C+Elphias%0AElphias+Doge",
        "https://harrypotter.fandom.com/wiki/Category:Wizards?from=Frick%2C+Otmar%0AOtmar+Frick",
        "https://harrypotter.fandom.com/wiki/Category:Wizards?from=Heizenbert%2C+Matildus%0AMatildus+Heizenbert",
        "https://harrypotter.fandom.com/wiki/Category:Wizards?from=Knatchbull%2C+Porteus%0APorteus+Knatchbull",
        "https://harrypotter.fandom.com/wiki/Category:Wizards?from=Male+Ravenclaw+Quidditch+Seeker%0AUnidentified+Ravenclaw+Seeker",
        "https://harrypotter.fandom.com/wiki/Category:Wizards?from=Murley%2C+Eric%0AEric+Murley",
        "https://harrypotter.fandom.com/wiki/Category:Wizards?from=Picquery%2C+Seraphina%0ASeraphina+Picquery",
        "https://harrypotter.fandom.com/wiki/Category:Wizards?from=Romsey%2C+Graham%0AGraham+Romsey",
        "https://harrypotter.fandom.com/wiki/Category:Wizards?from=Stokke%2C+Brunhilde%0ABrunhilde+Stokke",
        "https://harrypotter.fandom.com/wiki/Category:Wizards?from=Unidentified+Chaser+%28I%29",
        "https://harrypotter.fandom.com/wiki/Category:Wizards?from=Volkov%2C+Ivan%0AIvan+Volkov",
    ]
}

def get_characters(base_wiki_url, listing_urls, min_length, output_file):
    '''
    Outupts list of parings of {Character Name, Wiki URL} for all characters 
    listed in the standard character list wiki format 
    (ex: https://avatar.fandom.com/wiki/Category:Characters)
    with a main body length greater than the set minimum.
    '''
    characters = []
    for listing_url in listing_urls:
        characters = characters + get_characters_in_listing(listing_url, base_wiki_url)

    for character in characters:
        print(f"Checking length of character {character['name']}")
        tags = scrape_wiki.get_tag_texts(character["url"])
        sum_length = sum(len(s) for s in tags)
        if sum_length >= min_length:
            output_file.write(f"{character['name']},{character['url']}\n")

def get_characters_in_listing(listing_url, base_wiki_url):
    ''' Accepts the URL of a single listing page
        (ex: https://avatar.fandom.com/wiki/Category:Characters?from=Ozai)
        and returns a list of {Character Names, Page URLs}
    '''
    response = requests.get(listing_url)
    parsed = BeautifulSoup(response.text, 'html.parser')
    link_nodes = parsed.find_all(class_="category-page__member-link")
    characters = [
        {
            "name": a.text, 
            "url": base_wiki_url + a["href"]
        }
        for a in link_nodes
    ]
    return characters

def main():
    universe = harry_potter    
    
    output_file_name = "names_urls.csv"
    output_file = open(output_file_name, 'w')

    get_characters(universe["base_url"], universe["character_listing_urls"], universe["min_content_length"], output_file)

    output_file.close()


if __name__ == "__main__":
    main()