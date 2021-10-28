import requests
import os

class fuzzer:
    def __init__(self, url: str, type: str, wordlist_path: str, depth: int, verbose: bool = False):
        self.url = url
        self.type = type
        self.wordlist_path = wordlist_path
        self.depth = 0 if not depth else int(depth)
        self.verbose = verbose

    def __depth_gen(self, wordlist_primary: list) -> list:
        depth = self.depth
        wordlist_secondary = wordlist_primary.copy()
        wordlist_tertiary = wordlist_primary.copy()

        for x in range(depth):
            for word in wordlist_secondary:
                for root in wordlist_tertiary:
                    root : str = root
                    if root+'/'+word not in wordlist_primary and (not root.startswith('.') and '.' in word):
                        wordlist_primary.append(root+'/'+word)

            wordlist_secondary = wordlist_primary.copy()

        wordlist_secondary.clear()
        wordlist_tertiary.clear()

        return wordlist_primary

    def fuzz(self):
        url = self.url
        verbose = self.verbose

        try:
            if requests.get(url):
                pass
            else:
                print('Please check the input url')
                return
        except requests.exceptions.ConnectionError as e:
            print(e)
            return

        if self.type.lower() == "subdomain":
            url = url.replace('://', '://FUZZ.')
        elif self.type.lower() == "directory":
            if url[-1] != '/':
                url = url+'/FUZZ'
            else:
                url = url + 'FUZZ'
        
        if not url or type(url) is not str:
            print('Err: No url found')
            return 1

        elif 'FUZZ' not in url:
            print('Err: FUZZ keyword not found')
            return 1

        if os.path.exists(self.wordlist_path):
            with open(self.wordlist_path, 'r') as f:
                wordlist = f.read().splitlines()
        else:
            raise FileNotFoundError(f'Error: file \'{self.wordlist_path}\' does not exist')
            return 1

        wordlist = wordlist if not depth and self.type.lower() == "directory" else self.__depth_gen(wordlist)

        length = len(wordlist)
        for word in wordlist:
            global response
            response = None
            try:
                response = requests.get(url.replace('FUZZ', word))
            except requests.exceptions.ConnectionError as e:
                print(e) if verbose else print(end="")
            if response:
                print('url: ', url.replace('FUZZ', word), 'status code: ', response.status_code)

            print(f'tried: {wordlist.index(word)}/{length}', end='\r')

        wordlist.clear()