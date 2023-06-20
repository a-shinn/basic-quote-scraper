import numpy as np
import pandas as pd
import bs4 as bs
import requests

# scrapes quotes, authors, and tags for each entry in the given webpage and creates a dataframe from the results.
webpage = requests.get('https://quotes.toscrape.com/tag/books/')
soup = bs.BeautifulSoup(webpage.text, 'html.parser')
quotes = soup.findAll('span', attrs={'class':'text'})
authors = soup.findAll('small', attrs={'class':'author'})
tags = soup.findAll('div', attrs={'class':'tags'})
login = soup.findAll('div', attrs={'class':'col-md-4'})

# combines quotes,authors,tags into a list then converts into a dataframe
list1 = [[author.text,quote.text,tags.text] for author,quote,tags in zip(authors,quotes,tags)]
data = pd.DataFrame(list1,columns=['Author','Quote','Tags'],index=range(1,11))

# cleaning up the tags column
data['Tags'] = data['Tags'].str.split()
for tags in data['Tags']:
    tags = tags.remove('Tags:')

# counts frequency of each tag in the list of books
tag_counts = {}
for series in data['Tags']:
    for taglist in series:
        # tag_counts[taglist] += 1
        if taglist in tag_counts:
            tag_counts[taglist] += 1
        else:
            tag_counts[taglist] = 1

print(data.sort_values('Author'))
print()
print(data.describe())

data.to_csv('src/quotes.csv', index=False)
