#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import csv
import concurrent.futures
import sys
import itertools
import os

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

def write_csv(list):
    csv_f = open("withlinks.csv", "w", newline="")
    writer = csv.writer(csv_f)
    writer.writerows(list)
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
    browser = webdriver.Chrome("/usr/bin/chromedriver", options=chrome_options)
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
            return [search_string] + output
            #write_csv(search_string, output)
            #break
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
    search_terms = get_new_search_terms(file_name)
    final_output = []
    #clear_file = open('withlinks.csv', 'w')
    #clear_file.close
    #available_cores = multiprocessing.cpu_count()
    #print("Available cores: {}, currently using: {}".format(available_cores, available_cores))
    #p = multiprocessing.Pool(available_cores)

    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
        futures = {executor.submit(get_links, term, extra_keyword): term for term in search_terms}
        for future in concurrent.futures.as_completed(futures):
            final_output.append(future.result())

    write_csv(final_output)
    print('completed')
    #os._exit(0)

