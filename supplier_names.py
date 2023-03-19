import requests
import sys
import urllib.parse
from bs4 import BeautifulSoup
import re
import urllib
from typing import *
import os
from pdfreader import SimplePDFViewer


def get_suppliers(filename, url):
    r = requests.get(url)
    if (r.status_code == 200):
        output_file = open(filename, "wb")
        output_file.write(r.content)
        print("Downloaded: " + url)

def write_string_to_file(filename, content):
    fd = open(filename, "w")
    fd.write(content)
    fd.close()
    print("Wrote data to " + filename)

def extract_pdf_text(filepath):
    fd = open(filepath, "rb")
    viewer = SimplePDFViewer(fd)
    
    result = ""
    for canvas in viewer:
        for token in canvas.strings:
            result += token
    
    fd.close()
    
    print("Extracted text from: " + filepath)
    return result

if __name__ == "__main__":
    company_name = sys.argv[1]
    keywords = "suppliers list"
    
    query = urllib.parse.quote_plus(company_name + " " + keywords)

    url = "https://www.google.com/search?q=filetype:pdf+" + query
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    result_block = soup.find_all("a", href=True)

   
    cur_result = 0

    for result in result_block:
        href = result['href']
        pdf_href = re.search(r'(\/url\?q\=)(.+\b\.pdf\b)', href)
        
        # Check if this link contains a downloadable pdf file
        if pdf_href:
            pdf_url = pdf_href.group(2)

            os.makedirs("tmp", exist_ok=True)
            base_output_filename = "tmp/result_" + str(cur_result)
            
            get_suppliers(base_output_filename + ".pdf", pdf_url)
            extracted_text = extract_pdf_text(base_output_filename + ".pdf")
            write_string_to_file(base_output_filename + ".txt", extracted_text)
            
            cur_result += 1
            lst = []
            with open('tmp/result_0.txt', 'r') as fp:
                for line in fp:
                    for word in line.split():
                        if word.istitle():
                            lst.append(word)
            # if 'Inc.' in lst:
            #     print('True1')
            # if 'Corp' in lst:
            #     print('True2')
            # if 'Ltd' in lst:
            #     print('True3')
            # if 'Plc' in lst:
            #     print('True4') 
            # else:
            #     print('False')
            names = []
            for i in range(len(lst)):
                if lst[i] == 'Inc.' or lst[i] == 'Corp' or lst[i] == 'Ltd':
                    names.append (lst[i-1])
            with open('company_names.txt', 'r') as fp:
                for line in fp:
                    for word in line.split():
                        if word in lst:
                            names.append(word)

                
            print(set(names))


            