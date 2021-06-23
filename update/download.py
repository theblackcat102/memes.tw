import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re

def update():

    with open('results.tsv', 'w') as f:
        for page in tqdm(range(8000), dynamic_ncols=True):
            postfix = '' if page == 0 else '?page={}'.format(page+1)
            res =  requests.get('https://memes.tw/maker'+ postfix)
            soup = BeautifulSoup(res.text, 'lxml')
            found = False
            for meme in soup.findAll('div', {'class': '-shadow mt-3 mx-2'}):
                title = meme.find('header', {'class': 'text-center'}).text
                image = meme.find('img').get('src')
                f.write('{}\t{}\t{}\n'.format(page, title, image))
                found = True

            if not found: # break if nothing found
                break


if __name__ == "__main__":
    black_list_titles = [
        '.....',
    ]
    update()

    template_pattern = re.compile(r'模板 ([0-9])\w+')
    number_pattern = re.compile(r'([0-9])\w+')
    data = []

    with open('results.tsv', 'r') as f, open('meme_captions.tsv', 'w') as g:
        for line in f:
            page, title, image_url = line.strip().split('\t')
            if template_pattern.search(title) is not None or title.isnumeric():
                continue
            if len(title) > 2:
                g.write('{}\t{}\n'.format(image_url, title))
