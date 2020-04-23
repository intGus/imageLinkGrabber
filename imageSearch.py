from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import csv

def get_new_search_terms():
    """gets the new items to search"""
    fh = open("source50.csv", "r")
    lines = csv.reader(fh)
    newsearch = []
    for row in lines:
        newsearch.append(row[0])
    fh.close
    return newsearch

def get_links(search_string):
    """get the links using selenium"""
    chrome_options = Options()  
    chrome_options.add_argument("--headless")
    #chrome_options.add_argument("--disable-logging")

    # replace the spaces with +
    search_string = search_string.replace(' ', '+')  
    
    # Assigning the browser variable with chromedriver of Chrome. 
    # options is to go headless 
    browser = webdriver.Chrome("D:/PythonLessons/imageTest/chromedriver.exe", options=chrome_options)
    url = "https://www.google.com/search?tbm=isch&q=polish+"+search_string+"&tbs=isz%3Al"
    retries = 0
    output = [url]
    while True:
        try:
            browser.get(url)
            print(search_string)
            source = browser.page_source
            browser.close()
            links = re.findall(r'\[\"(http.?://.*\.[JjPp][PpNn][Ee]?[Gg])', source)
            if len(links) > 10:
                limit = 10
            else:
                limit = len(links)

            for i in range(limit):
                output.append(links[i])
            return output
        except:
            print("retrying")
            retries += 1
            if retries > 3:
                break
            continue

#print(get_links("sheer your toys"))
search = (get_new_search_terms())
#search = ["fair pinkum"]
csv_f = open("withlinks2.csv", "a", newline="")
writer = csv.writer(csv_f)
for item in search:
    print(item)
    links = get_links(item)
    writer.writerow([item] + links)

csv_f.close