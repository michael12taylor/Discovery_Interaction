import csv
import scrape_wiki

def main():
    
    file_name = "./scripts/universes/dc_names_urls.csv"
    characters_file = open(file_name)
    csv_reader = csv.reader(characters_file)

    for row in csv_reader:
        universe = row[0]
        name = row[1]
        url = row[2]
        print(f"Handling {name} at URL {url}")
        scrape_wiki.main(universe, name, url)

    characters_file.close()
        
if __name__ == "__main__":
    main()