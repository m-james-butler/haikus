import sys
from string import punctuation
from pprint import pprint
import json
from nltk.corpus import cmudict

cmudict = cmudict.dict()

def main():
    haiku = load_text("train.txt")
    exceptions = cmudict_missing(haiku)
    build_dict = input("\nManually build an exceptions dictionary? Y or N? \n")
    if build_dict.lower() == "n":
        sys.exit()
    else:
        missing_dict = make_exceptions_dict(exceptions)
        save_exceptions(missing_dict)


def load_text(filename):
    """Opens and returns the training corpus as a set"""
    try:
        with open(filename) as in_file:
            haiku = set(in_file.read().replace('-',' ').split())
            return haiku
    except:
        print("Unable to open train.txt. Please verify file is in program directory.")
        print("Exiting program")
        sys.exit()


def cmudict_missing(word_set):
    """Find and return the words missing from the dictionary"""
    exceptions = set()
    for word in word_set:
        word = word.lower().strip(punctuation)
        if word.endswith("'s") or word.endswith("’s"):
            word = word[:-2]
        if word not in cmudict:
            exceptions.add(word)

    print("There are {} words in the training set.".format(len(word_set)))
    print("There are {} missing words.".format(len(exceptions)))
    return exceptions


def make_exceptions_dict(exception_set):
    missing_words = {}
    print("Input the # of syllables in each word. Mistakes can be corrected at the end.\n")
    for word in exception_set:
        while True:
            num_sylls = input("{} has how many syllables? ".format(word))
            if num_sylls.isdigit():
                break
            else:
                print("      THAT IS NOT A NUMBER! Input a number", file=sys.stderr)
        missing_words[word] = int(num_sylls)
    print()
    pprint(missing_words, width=1)

    print("\nMake changes to dictionary before saving?")
    print("""
    0 - Exit & Save
    1 - Add a word or Change a count
    2 - Remove a word
    """)

    while True:
        choice = input("\nEnter Choice: ")
        if choice == '0':
            break
        elif choice == '1':
            word = input("\nWhat word do you want to change?")
            missing_words[word] = int(input("\nHow many syllables are in {}? ".format(word)))
        elif choice == '2':
            word = input("\nWord to delete = ? ")
            missing_words.pop(word, None)
    pprint(missing_words, width=1)
    return missing_words


def save_exceptions(missing_words):
    json_string = json.dumps(missing_words)
    f = open('missing_words.json', 'w')
    f.write(json_string)
    f.close()
    print("\nFile saved as missing_words.json")

if __name__ == '__main__':
    main()
