import time

def get_stopwords_list(stop_word_file):

    stop_word_file = open(os.path.join(os.getcwd(), stop_word_file), 'r', encoding='utf8')
    stop_word_file = stop_word_file.read()
    stop_word_list = stop_word_file.split()
    return stop_word_list


# hint for get_stopwords_list
# file = open(os.path.join(os.getcwd(), stop_word_file), 'r', encoding="utf8")
# stop_words = file.read() -> stop_words contains all the stop words but needs to be translated to a list of stop_words

def preprocess(original_content):
    # makes a DEEP copy of the original_content, so the original original_content remains unchanged
    cleaned_content = original_content[:]
    # made entire file lowercase to make comparisons easier
    cleaned_content = cleaned_content.lower()
    alphabet_string = "abcdefghijklmnopqrstuvwxyz '"
    # Now work on the original_content in cleaned_content variable

    # Optimized solution ---------------------------------------------

    # This solution is the fastest of the solutions we have so far.
    # scanning the string from left to right, once you find a double space, replace all double spaces
    # with a single space, then continue from where you left off at this point we know all elements
    # to the left of that point do not have double spaces, so we do not need to check them again
    # now go through the rest of the string with this same logic

    # Here we are starting with the first character in the string
    character_index = 0

    # we find the length of the string
    last_index = len(cleaned_content)

    # this will run for as many characters exist in the string
    # we are constantly updating the length when elements are removed
    while character_index < (last_index-1):

        # if the current character under consideration is not in the defined string of wanted
        # characters it replaces all occurrences of that character in the entire string with a space
        if cleaned_content[character_index] not in alphabet_string:
            cleaned_content = cleaned_content.replace(cleaned_content[character_index], ' ')

        # if the character under consideration is a space and the character after it is a space
        # then we replace all double spaces in the string with a single space then move to the next character
        elif cleaned_content[character_index] == ' ' == cleaned_content[character_index+1]:
                cleaned_content = cleaned_content.replace('  ', ' ')
                last_index = len(cleaned_content)
        character_index += 1

    cleaned_content = auto_correct_word(cleaned_content)
    # -------------------------------------------------------------

    # # Original Solution----------------------------------------------
    # for character in cleaned_content:
    #     if character not in alphabet_string:
    #         cleaned_content = cleaned_content.replace(character, ' ')
    # character_index = 0
    # # Optimized "Double space" loop ---------------------------------
    # # Updated this loop to be more efficient: The logic for this is...
    #
    # last_index = len(cleaned_content)
    # while character_index < last_index-1:
    #     if cleaned_content[character_index] == ' ' == cleaned_content[character_index+1]:
    #             cleaned_content = cleaned_content.replace('  ', ' ')
    #             last_index = len(cleaned_content)
    #     character_index+=1
    #
    # # Original "Double space" loop ---------------------------------
    # last_index = len(cleaned_content)
    # while character_index < (last_index-1):
    #     if cleaned_content[character_index] == ' ':
    #         while cleaned_content[character_index] == cleaned_content[character_index+1]:
    #             cleaned_content = cleaned_content.replace('  ', ' ', 1)
    #             last_index = len(cleaned_content)
    #     character_index += 1
    # cleaned_content = auto_correct_word(cleaned_content)
    # ----------------------------------------------------------------
    return cleaned_content  # This is a cleaned string


def auto_correct_word(word):  # already implemented, you need not do anything

    from autocorrect import Speller
    spell = Speller(lang='en')
    return spell(word)


def get_letter_frequency(cleaned_content):

    letter_freq_dict = dict()

    # we remove spaces in the content but do not need to make a deep copy because
    # strings are immutable
    cleaned_content = cleaned_content.replace(' ', '')

    for character in cleaned_content:
        if character in letter_freq_dict:
            letter_freq_dict[character] += 1
        else:
            letter_freq_dict[character] = 1

    return letter_freq_dict


def get_word_frequency(cleaned_content):

    word_freq_dict = dict()

    cleaned_content_words = cleaned_content.split()

    for word in cleaned_content_words:
        if word not in word_freq_dict:
            word_freq_dict[word] = 1
        else:
            word_freq_dict[word] += 1

    return word_freq_dict


def get_list_of_unique_words(cleaned_content):

    unique_word_list = []

    # this separates the words in cleaned content into a list of words to be iterated over
    cleaned_content_words = cleaned_content.split()

    # this creates a list of all the unique words with no repeats
    unique_word_list = [word for word in cleaned_content_words if word not in unique_word_list]

    return unique_word_list


def get_useful_words(cleaned_content, stop_word_list):
    # this separates the words in cleaned content into a list to be iterated over
    cleaned_content_words = cleaned_content.split()
    # this creates a list of all the words that are not in stop words
    useful_word_list = [word for word in cleaned_content_words if word not in stop_word_list]

    return useful_word_list


def get_keywords(useful_word_list):
    # returns a list of UP TO 6 most frequent out of useful_word_list
    # if there is a tie return all the words tied.
    # for example: word1:6, word2:6, word3: 5, word4: 5, word5: 4, word6: 4, word7: 4, word8:4
    # all words from word1 to word8 shall be returned as the output in a list
    # print the useful_word_list in order of their frequency, the most frequent words come first
    possible_keywords_count = {}
    possible_keywords = []

    # in this loop we are counting the words that are in the useful_word_list
    # and adding them to a dictionary if they do not exist in it already
    # if they already exist then the count is increased by 1
    for word in useful_word_list:
        if word not in possible_keywords_count:
            possible_keywords_count[word] = 1
        else:
            possible_keywords_count[word] += 1

    # This loop goes through the dictionary to find the count of the word that is most frequent
    # this will be used in the following loop as a point to start from
    max_frequency = 0
    for word in possible_keywords_count:
        if possible_keywords_count[word] > max_frequency:
            max_frequency = possible_keywords_count[word]

    # This loop will run while there are at least six items in the possible_keywords
    # here old represents the current count we are comparing all counts to.
    old = max_frequency
    while len(possible_keywords) < 6: # need another condition here
        new = 0

        for word in possible_keywords_count:
            # if the word currently under consideration has the same count as the current max frequency
            # then add that word to the list
            if word not in possible_keywords and possible_keywords_count[word] == old:
                possible_keywords.append((word, possible_keywords_count[word]))

            # if the count of the word currently under consideration is less than the current old
            # and greater than the new at this point then that is the next frequency we check for
            # once the outer loop runs again
            elif new < possible_keywords_count[word] < old:
                new = possible_keywords_count[word]
        old = new

    return possible_keywords


# *****Following code need not be changed*****#
if __name__ == "__main__":
    # install the following package(s) as prompted
    # please do not install any other package(s) than the following unless stated inline otherwise
    import os

    stop_word_file = "stop_words.txt"
    stop_word_list = get_stopwords_list(stop_word_file)
    filename = "amazon_reviews_large.txt"
    file = open(os.path.join(os.getcwd(), filename), 'r',
                encoding="utf8")
    # it may happen that the file does not exist
    # os.getcwd(): gets the current working directory (cwd)
    # os.path.join(os.getcwd(), filename) joins the cwd with the file name to create an absolute path to the file
    # 'r': indicated read more, since we just want to read the file this is the safest mode to open the file
    # encoding="utf8" this is the encoding scheme for each of the characters that is going to be read
    original_content = file.read()
    print('original_content:', original_content)
    cleaned_content = preprocess(original_content)
    print('cleaned_content:', cleaned_content)
    letter_frequency = get_letter_frequency(cleaned_content)
    print('letter_frequency:', letter_frequency)
    get_word_frequency = get_word_frequency(cleaned_content)
    print('get_word_frequency:', get_word_frequency)
    unique_word_list = get_list_of_unique_words(cleaned_content)
    print('unique_word_list:', unique_word_list)
    useful_word_list = get_useful_words(cleaned_content, stop_word_list)
    print('useful_word_list:', useful_word_list)
    possible_keywords = get_keywords(useful_word_list)
    print('possible_keywords:', possible_keywords)
