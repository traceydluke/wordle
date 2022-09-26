# makeDictionary.py
#
# this script generally shouldn't need to be re-run and is mostly here as a proof of concept for
# how the word lists could be updated.

# solutions: https://www.wordfrequency.info/samples.asp (5000 most frequently used words)
# all words: https://github.com/dwyl/english-words/raw/master/words_dictionary.json

import os.path
import requests
import pandas as pd


pwd = os.path.dirname(__file__)
solutionsFile = os.path.join(pwd, "wordFrequency.xlsx")
validWordsFile = os.path.join(pwd, "words_dictionary.json")
outputFile = os.path.join(pwd, "possible_answers.py")

# fetch files if they don't exist
for filename, url in [
    (solutionsFile, "https://www.wordfrequency.info/samples/wordFrequency.xlsx"),
    (validWordsFile, "https://github.com/dwyl/english-words/raw/master/words_dictionary.json"),
]:
    if not os.path.exists(filename):
        response = requests.get(url)
        with open(filename, "wb") as f:
            f.write(response.content)


# filter for 5-letter words and convert to python
with open(outputFile, "w") as output:
    output.write("# source: https://www.wordfrequency.info/samples.asp\n")
    output.write("ANSWERS = ")
    data = pd.read_excel(solutionsFile, sheet_name=1)
    # need to cast to string so the word 'False' gets converted from bool to str
    filteredWords = [
        str(word).lower() for word in data["lemma"] if len(str(word)) == 5 and str(word).isalpha()
    ]
    output.write(str(filteredWords))
