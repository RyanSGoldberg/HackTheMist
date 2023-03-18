import requests
import sys
import urllib.parse
from bs4 import BeautifulSoup
import re
import urllib

def download_url(filename, url):
    r = requests.get(url)
    if (r.status_code == 200):
        output_file = open(filename, "wb")
        output_file.write(r.content)
        print("Downloaded: " + url)

if __name__ == "__main__":
    company_name = sys.argv[1]
    keywords = "sustainability report"
    
    query = urllib.parse.quote_plus(company_name + " " + keywords)

    url = "https://www.google.com/search?q=filetype:pdf+" + query
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    result_block = soup.find_all("a", href=True)

    iterator = 0

    for result in result_block:
        href = result['href']
        pdf_href = re.search(r'(\/url\?q\=)(.+\b\.pdf\b)', href)
        
        if pdf_href:
            pdf_url = pdf_href.group(2)
            download_url("result" + str(iterator) + ".pdf", pdf_url)
            iterator += 1
        