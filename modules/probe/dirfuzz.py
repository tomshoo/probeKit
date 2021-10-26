import requests
import os

def fuzz(url: str, wordlist_path: str, depth: int):
    depth = 0 if not depth else depth
    if os.path.exists(wordlist_path):
        with open(wordlist_path, 'r') as f:
            wordlist = f.read().splitlines()
    else:
        raise FileNotFoundError(f'Error: file \'{wordlist_path}\' does not exist')
        return 1

    wordlist_use = wordlist.copy()
    wordlist_b = wordlist.copy()
    #url_b = url
    #url_list = []
    count = 1
    for x in range(depth):
        for something in wordlist_use:
            for someword in wordlist_b:
                if someword+'/'+something not in wordlist and ('index.' not in someword+something):
                    count += 1
                    #print(someword+'/'+something)
                    wordlist.append(someword+'/'+something)

        wordlist_use = wordlist.copy()

    length = len(wordlist)
    for word in wordlist:
        response = requests.get(url+'/'+word)
        if response:
            print('url: ', url+word, 'status code: ', response.status_code)
        
        print(f'tried: {wordlist.index(word)}/{length}', end='\r')

    wordlist_use.clear()
    wordlist.clear()
    wordlist_b.clear()