import requests
import os
import time

#wordlist = ['index.html', 'index.asp', 'index.php', 'css', 'js', 'node_modules', 'modules', 'static']

with open('C:\\Users\\tomar\\Projects\\myprojects\\Wordlist.txt', 'r') as f:
    wordlist = f.read().splitlines()

wordlist_use = wordlist.copy()
wordlist_b = wordlist.copy()

it = input('number of directories to deep in: ')
if not it:
    it = 1
else:
    it = int(it)

url = input('Enter url of target (Enter full url): ')

if not url:
    url = 'https://ptu.ac.in/'

#url_b = url
#url_list = []
count = 1
for x in range(it):
    for something in wordlist_use:
        for someword in wordlist_b:
            if someword+'/'+something not in wordlist:
                count += 1
                print(count, end='\r')
                #print(someword+'/'+something)
                wordlist.append(someword+'/'+something)

    wordlist_use = wordlist.copy()

print(len(wordlist_use))
wordlist_use.clear()
wordlist.clear()
wordlist_b.clear()