import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import re
import time

start = 'https://processing.ruscorpora.ru/search.xml?env=alpha&api=1.0&mycorp=&mysent=&mysize=&mysentsize=&dpp=&spp' \
        '=&spd=&mydocsize=&mode=main&lang=ru&sort=i_grtagging&nodia=1&text=lexgramm&parent1=0&level1=0&lex1= '
middle = '&gramm1=&sem1=&flags1=&sem-mod1=sem&sem-mod1=sem2&parent2=0&level2=0&min2=1&max2=1&lex2='
end = '&gramm2=&sem2=&flags2=-amark&sem-mod2=sem&sem-mod2=sem2'
end1 = '&gramm1=&sem1=&flags1=&sem-mod1=sem&sem-mod1=sem2&parent2=0&level2=0&min2=1&max2=1&lex2=&gramm2=&sem2=&flags2' \
       '=&sem-mod2=sem&sem-mod2=sem2 '

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


def bigramm_search(word1, word2):
    url = start + word1 + middle + word2 + end
    while True:
        r = session.get(url)
        if r.status_code == 200:
            break
        else:
            time.sleep(10)
            bigramm_search(word1, word2)
    return r


def one_word_search(word):
    url = start + word + end1
    while True:
        r = session.get(url)
        if r.status_code == 200:
            break
        else:
            time.sleep(10)
            one_word_search(word)
    return r


def frequency(word, frequency_dict):
    r = one_word_search(word)
    soup = BeautifulSoup(r.text, features='lxml')
    result = re.search('[0-9 ]+( вхожден.{2})', soup.get_text())
    if result is not None:
        freq = result.group(0).replace(' ', '')
        freq = int(re.search('\d+', freq).group(0))
        frequency_dict[word] = freq
    else:
        frequency_dict[word] = 0
    return
