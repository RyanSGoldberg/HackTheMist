from __future__ import annotations
import requests
import sys
import urllib.parse
from bs4 import BeautifulSoup
import re
import urllib
from pdfreader import SimplePDFViewer
import os
import logging

def download_url(filename, url):
    r = requests.get(url)
    if (r.status_code == 200):
        output_file = open(filename, "wb")
        output_file.write(r.content)
        output_file.close()
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

    # Iterate through all document pages and extract text
    for canvas in viewer:
        for token in canvas.strings:
            result += token
    
    fd.close()
    
    print("Extracted text from: " + filepath)
    return result

def extract_relevant_blocks(filename, keywords):
    with open(filename, "r") as fd:
        content = fd.read()
        blocks = re.findall(r'\.([^\\.]+\b{}\b[^\\.]*.)'.format(keywords), content, re.IGNORECASE)

        return blocks

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.ERROR)

    # Inputs
    company_name = sys.argv[1]
    search_keywords = "sustainability report"
    text_extraction_keywords = ["green"]

    # Ouputs
    pipeline_output = []

    # Implementation
    
    query = urllib.parse.quote_plus(company_name + " " + search_keywords)

    url = "https://www.google.com/search?q=filetype:pdf+" + query
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
            
            download_url(base_output_filename + ".pdf", pdf_url)
            extracted_text = extract_pdf_text(base_output_filename + ".pdf")
            write_string_to_file(base_output_filename + ".txt", extracted_text)

            for text_extraction_keyword in text_extraction_keywords:
                pipeline_output += extract_relevant_blocks(base_output_filename + ".txt", text_extraction_keyword)

            cur_result += 1

    print(pipeline_output)
