import requests
import os
import time

#wordlist = ['index.html', 'index.asp', 'index.php', 'css', 'js', 'node_modules', 'modules', 'static']
def fuzz(url: str, wordlist: str, depth: int):
    with open('C:\\Users\\tomar\\Projects\\myprojects\\Wordlist.txt', 'r') as f:
        wordlist = f.read().splitlines()

    wordlist_use = wordlist.copy()
    wordlist_b = wordlist.copy()
    #url_b = url
    #url_list = []
    count = 1
    for x in range(depth):
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