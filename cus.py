#!/usr/bin/env python 
import re
import readline
import bs4 as bs
from urllib import request as rq


class Solution:
    over = {}
    down = {}
    number = 0

    @staticmethod
    def get_solution_from_html():
            """ Returns a long string containing the latest 5 solutions from WordPresss website"""
            r = rq.urlopen('https://cusloesung.wordpress.com/').read()
            soup = bs.BeautifulSoup(r, "html.parser")
            return soup.find_all("div")[0].get_text()

    @staticmethod
    def remove_special_characters(string):
        # replace umlaute and accents
        replace_dict = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'é': 'e', 'Ä': 'Ae',
                        'Ö': 'Oe', 'Ü': 'Ue', 'É': 'E', 'È': 'E'}
        for key, value in replace_dict.items():
            string = string.replace(key, value)
        return string

    def __init__(self, post_number=0):
        """
            Initialize using string input from posts of website.
            post_number is 0 for the latest.
        """
        posts = self.get_solution_from_html()
        posts = self.remove_special_characters(posts)

        over = re.findall(r'Rueber: (.+)\n', posts)[post_number]
        down = re.findall(r'Runter: (.+)\n', posts)[post_number]
        
        # remove dots
        over = over.replace('.', '')
        down = down.replace('.', '')
        
        over = re.findall(r'(\d+ \w+[ a-zA-Z]*)', over)
        down = re.findall(r'(\d+ \w+[ a-zA-Z]*)', down)

        key = []
        value = []
        for item in over:
                key.append(int(re.findall(r'\d+', item)[0]))
                value.append(re.findall(r'\s+([a-zA-Z]+\s*[[a-zA-Z]+]?)', item)[0].replace(' ', ''))
                
        self.over = dict(zip(key, value))
            
        key = []
        value = []
        for item in down:
                key.append(int(re.findall(r'\d+', item)[0]))
                value.append(re.findall(r'\s+([a-zA-Z]+\s*[[a-zA-Z]+]?)', item)[0].replace(' ', ''))
                
        self.down = dict(zip(key, value))

        self.number = int(re.findall(r'Nr. (\d+)', posts)[post_number])


if __name__ == "__main__":

    riddle_number = input("Which riddle shoud I load? (Default: most recent - 0) : ")
    if riddle_number is '':
        riddle_number = 0
    else:
        riddle_number = int(riddle_number)

    s = Solution(riddle_number)
    print("Loaded riddle nr: {}".format(s.number))
    print('Type "q" to quit.')
    
    while True:
        # guess should be of form (where?) (what?)
        # v is vertical (down)
        # h is horizontal (over)
        # followed by number, than try
        # e.g. v5 house
        guess = input("Wanna make a guess? : ")

        if guess == 'q':
            break

        guess = re.match(r'^([vh])(\d+)\s(\w+)$', guess)

        if guess is None:
            print("Wrong input")
            continue

        if len(guess.groups()) != 3:
            print("Wrong input")
            continue

        # compare to value stored in solution object
        query = guess.groups()
        if query[0] == 'v':
            d = s.down
        elif query[0] == 'h':
            d = s.over

        if int(query[1]) not in d.keys():
            print("Element does not exist")
            continue

        answer = d[int(query[1])].lower()
        trial = query[2].lower()

        if trial == 'solve':
            print(answer)
            continue

        if len(answer) != len(trial):
            print("Wrong word length. Given: {}, Needed {}.".format(len(trial), len(answer)))
            continue
            
        if answer == trial:
            print("Correct!")
            continue

        response = ['x' if a == t else 'o' for (a, t) in zip(answer,trial) ]
        print(" ".join(response))

        
