#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import csv
import multiprocessing
import sys
import itertools

def get_new_search_terms(file_name):
    """gets the new items to search"""
    try:
        fh = open(file_name, "r")
    except:
        print("File {} not found, execute again with the correct source file".format(file_name))
        exit()
    lines = csv.reader(fh)
    newsearch = []
    for row in lines:
        newsearch.append(row[0])
    fh.close
    return newsearch

def write_csv(search_string, links):
    csv_f = open("withlinks.csv", "a", newline="")
    writer = csv.writer(csv_f)
    writer.writerow([search_string] + links)
    csv_f.close


def get_links(search_string,extra_keyword):
    """get the links using selenium"""
    chrome_options = Options()  
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # replace the spaces with +
    modified_search_string = search_string.replace(' ', '+')  
    
    # Assigning the browser variable with chromedriver of Chrome. 
    # options is to go headless and no-verbose
    browser = webdriver.Chrome("./resources/chromedriver", options=chrome_options)
    url = "https://www.google.com/search?tbm=isch&q="+extra_keyword+"+"+modified_search_string+"&tbs=isz%3Al"
    retries = 0
    output = [url]
    while True:
        try:
            browser.get(url)
            print("Fetching: {}".format(search_string))
            source = browser.page_source
            browser.close()
            links = re.findall(r'\[\"(http.?://.*\.[JjPp][PpNn][Ee]?[Gg])', source)
            if len(links) > 10:
                limit = 10
            else:
                limit = len(links)

            for i in range(limit):
                output.append(links[i])
            write_csv(search_string, output)
            break
        except:
            print("retrying")
            retries += 1
            if retries > 3:
                break
            continue


if __name__ == '__main__':
    #extra_keyword = ""
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        extra_keyword = sys.argv[2]
    else:
        file_name = input("Enter the source file name: ")
        extra_keyword = input("Enter the extra keyword if any: ")
    search = get_new_search_terms(file_name)

    available_cores = multiprocessing.cpu_count()
    print("Available cores: {}, currently using: {}".format(available_cores, available_cores-2))
    p = multiprocessing.Pool(available_cores-2)
    p.starmap(get_links, zip(search, itertools.repeat(extra_keyword)))

    sys.exit()
