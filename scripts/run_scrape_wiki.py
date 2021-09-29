

# Characters to parse
import subprocess
import os
import scrape_wiki

characters_urls = {
    "Harry Potter": "https://harrypotter.fandom.com/wiki/Harry_Potter",
    "Ron Weasley": "https://harrypotter.fandom.com/wiki/Ronald_Weasley ",
    "Hermione Granger": "https://harrypotter.fandom.com/wiki/Hermione_Granger",
    "Frodo Baggins": "https://lotr.fandom.com/wiki/Frodo_Baggins",
    "Samwise Gamgee": "https://lotr.fandom.com/wiki/Samwise_Gamgee",
    "Gandalf": "https://lotr.fandom.com/wiki/Gandalf",
    "Thor": "https://marvelcinematicuniverse.fandom.com/wiki/Thor",
    "Iron Man": "https://marvelcinematicuniverse.fandom.com/wiki/Iron_Man",
    "Black Widow": "https://marvelcinematicuniverse.fandom.com/wiki/Black_Widow",
    "Thanos": "https://marvelcinematicuniverse.fandom.com/wiki/Thanos"
}
scraper_executable_name = "./scrape_wiki.py"

def main():
    for character_name in characters_urls: 
        print(f"Handling {character_name} at URL {characters_urls[character_name]}")
        scrape_wiki.main(character_name, characters_urls[character_name])
        


if __name__ == "__main__":
    main()