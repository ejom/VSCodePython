import pandas as pd
from bs4 import BeautifulSoup
import re

raw_df = pd.read_csv('django_filtered.csv')
seo_df = raw_df[['url', 'title', 'h1', 'h2', 'h3', 'h4', 'h5']]
target_tags = ['title', 'h1', 'h2', 'h3', 'h4', 'h5']

page_txt_files = {
    'home': 'seo_html_data1.txt',
    'install': 'seo_html_data2.txt'
}

page_urls = {
    'home': 'https://www.djangoproject.com/',
    'install': 'https://docs.djangoproject.com/en/3.1/intro/install/'
}

def compare_HTML(target_page: str):
    # Read the whole text file
    with open(page_txt_files[target_page], "r", encoding="utf-8") as f:
        html = f.read()

    # Parse it
    soup = BeautifulSoup(html, "html.parser")

    #Find the values of all the target tags
    tag_vals = dict.fromkeys(target_tags)
    for tag in target_tags:
        tag_vals[tag] = [val.get_text(strip=True) for val in soup.find_all(tag)]

    #Print actual vs expected values
    print("Analyzing homepage HTML")
    sel_row = seo_df.loc[seo_df['url']==page_urls[target_page]]
    print(f"URL: {sel_row['url']}")

    exp = dict()
    act = dict()
    for tag in target_tags:
        exp[tag] = str(sel_row[tag].iloc[0]).lower().split('@@')
        act[tag] = [val.lower() for val in tag_vals[tag]]

        #clean string
        for i in range(len(exp[tag])):
            exp[tag][i] = exp[tag][i].strip()
            exp[tag][i] = re.sub(r"[^0-9A-Za-z ]+", "", exp[tag][i])
        for i in range(len(act[tag])):
            act[tag][i] = act[tag][i].strip()
            act[tag][i] = re.sub(r"[^0-9A-Za-z ]+", "", act[tag][i])

        print(f"Expected values for {tag}")
        print(exp[tag])
        print(f"Actual values for {tag}")
        print(act[tag])
        print("Number of different values")
        n = 0
        for val in exp[tag]:
            if not val or val=='nan':
                continue
            if val not in act[tag]:
                n+=1
        for val in act[tag]:
            if not val or val=='nan':
                continue
            if val not in exp[tag]:
                n+=1
        print(n)
        print()

print("HOME")
compare_HTML('home')
print()
print("INSTALL")
compare_HTML('install')

