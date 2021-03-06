import sys
import os
import requests
from bs4 import BeautifulSoup
from functools import reduce
import re
import time

# Even though 50000 is the stated limit, adding some extra space for added newlines, HTML tags, etc...
max_char_count = 50000 - 1000
output_dir = "./wiki_parser_output/"

def main(universe_name, character_name = "", wiki_page_url = ""):
    ''' Needs two arguments: 
        1) The name of the character. Used only for determining output file names.
        2) The URL of the wiki page to parse.
    '''
    character_name = sys.argv[1] if character_name == "" else character_name
    wiki_page_url = sys.argv[2] if wiki_page_url == "" else wiki_page_url
    tag_texts = get_tag_texts(wiki_page_url)

    
    # Create output directory if not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Write tag_texts to numbered output files.
    # No output file of length > 50000.
    start = 0
    file_number = 1
    
    while start < len(tag_texts):
        end = next_chunk(tag_texts, start, max_char_count)
        subslice = tag_texts[start:end]
        output_string = reduce(lambda prev, curr: f"{prev}\n{curr}", subslice)
        output_file_path = os.path.join(output_dir, f"{universe_name}_{character_name}_{file_number}.html")
        output_file = open(output_file_path, "w", encoding="utf-8")
        
        # Write the <html> and <p> tags to satisfy watson needing this to be HTML
        output_file.write("<html><p>")
        output_file.write(output_string)
        output_file.write("</p></html>")
        output_file.close()

        start = end
        file_number += 1


def next_chunk(tag_texts, start, max_char_count):
    ''' Given the tag texts and a start index, return the end index such that the sum length of 
        all texts in range [start,end) <= upper limit.
    '''
    end = start
    sum_length = 0
    # 1000 margin of safety for added newlines
    while end < len(tag_texts) and sum_length + len(tag_texts[end]) <= max_char_count: 
        sum_length += len(tag_texts[end])
        end += 1
    return end

def get_tag_texts(page_url):
    ''' Get an array of the texts of all the interesting tags (ex: p, h1, etc...) in 
        the main content mw-parser-output of a wiki url.
    '''
    try:
        response = requests.get(page_url)
    except:
        time.sleep(5)
        return []
    time.sleep(1)
    parsed = BeautifulSoup(response.text, 'html.parser')
    interesting_data = parsed.find(class_="mw-parser-output")
    
    # Want the content of all paragraphs, h1s, h2s, ..., h6s, and the content in lists.
    find_tags = ["p", "h1", "h2", "h3", "h4", "h5", "h6", "li"]
    tags = interesting_data.find_all(find_tags)
    tag_texts = list(map(lambda elem: elem.text, tags))

    # Remove bad characters ?????? and any instance of wiki links like [1] [19]
    for i in range(len(tag_texts)):
        tag_texts[i] = re.sub(r"(???|???|\[\d+\])", "", tag_texts[i])

    return tag_texts
    

if __name__ == "__main__":
    main()
    