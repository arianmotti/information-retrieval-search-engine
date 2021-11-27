from __future__ import unicode_literals
from hazm import *
import pandas as pd
import matplotlib.pyplot as plt
import math


def preproccesing(content, input=0):
    if not input:
        normalizer = Normalizer()
        stemmer = Stemmer()
        lemmatizer = Lemmatizer()
        stop_words = []
        normalized_content = []
        tokenized_content = []
        stemmed_content = []
        all_stemmed_content = []

        for i in range(len(content)):
            normalized_content.append(normalizer.normalize(content[i]))

        for i in range(len(normalized_content)):
            tokenized_content.append(word_tokenize(normalized_content[i]))

        j = 0
        for i in range(len(tokenized_content)):
            while j in range(len(tokenized_content[i])):
                tokenized_content[i][j] = stemmer.stem(tokenized_content[i][j])
                tokenized_content[i][j] = lemmatizer.lemmatize(tokenized_content[i][j])
                j += 1
    else:
        normalizer = Normalizer()
        stemmer = Stemmer()
        lemmatizer = Lemmatizer()
        normalized_content = normalizer.normalize(content)
        tokenized_content = word_tokenize(normalized_content)
        for i in range(len(tokenized_content)):
            tokenized_content[i] = stemmer.stem(tokenized_content[i])
            tokenized_content[i] = lemmatizer.lemmatize(tokenized_content[i])
    return tokenized_content


def create_positional_index(positional_index, p_data):
    for docID in range(len(p_data)):
        for i in range(len(p_data[docID])):
            if p_data[docID][i] in positional_index:
                positional_index[p_data[docID][i]][0] = positional_index[p_data[docID][i]][0] + 1
                if docID in positional_index[p_data[docID][i]][1]:
                    positional_index[p_data[docID][i]][1][docID].append(i)
                else:
                    positional_index[p_data[docID][i]][1][docID] = [i]
            else:
                positional_index[p_data[docID][i]] = []
                positional_index[p_data[docID][i]].append(1)
                positional_index[p_data[docID][i]].append({})
                positional_index[p_data[docID][i]][1][docID] = [i]

    freq_words = sorted(positional_index.keys(), key=lambda x: positional_index[x][0], reverse=True)
    l1 = []
    l2 = []
    l3 = []
    l4 = []

    for i in range(len(freq_words)):
        l1.append(math.log(i + 1, 10))
        l2.append(math.log(positional_index[freq_words[i]][0], 10))

    plt.plot(l1, l2)
    plt.show()

    for i in range(10):
        print(freq_words[i])
        positional_index.pop(freq_words[i], None)

    freq_words = sorted(positional_index.keys(), key=lambda x: positional_index[x][0], reverse=True)

    for i in range(len(freq_words)):
        l3.append(math.log(i + 1, 10))
        l4.append(math.log(positional_index[freq_words[i]][0], 10))

    plt.plot(l3, l4)
    plt.show()


def search_single_word(word, positional_index, title):
    tmp = []

    for i in range(len(positional_index)):
        if word[0] in positional_index:
            tmp = positional_index[word[0]][1].keys()

    for i in tmp:
        print(title[i])


def search_complex_word(search_word, positional_index, title):
    for word in search_word:
        if word not in positional_index:
            search_word.remove(word)

    search_word_substrings = []
    for i in range(len(search_word)):
        for j in range(len(search_word) - i):
            search_word_substrings.append(search_word[j:j + i + 1])
    search_word_substrings.reverse()

    priority = 0
    min_len = len(search_word_substrings[0])
    related_content = {}
    for query in search_word_substrings:
        merge_list = positional_index[query[0]][1]
        for i in range(len(query) - 1):
            tmp = {}
            for doc in merge_list.keys():
                if doc in positional_index[query[i + 1]][1].keys():
                    tmp[doc] = list(set([x + 1 for x in positional_index[query[i]][1][doc]]) & set(
                        positional_index[query[i + 1]][1][doc]))
            merge_list = tmp
        related_content[priority] = merge_list
        priority += 1

    for i in range(priority):
        print('Substring: ', ' '.join(search_word_substrings[i]), end='\n')
        for doc in related_content[i].keys():
            print('Title:', title[doc])
        # print(related_content[i])


data = pd.read_excel(r'IR.xlsx')
positional_index = {}
content = data['content'].tolist()
title = data['title'].tolist()
preprocessed_data = preproccesing(content)
create_positional_index(positional_index, preprocessed_data)
search_word = input()
search_word = preproccesing(search_word, 1)

if len(search_word) == 1:
    search_single_word(search_word, positional_index, title)
else:
    search_complex_word(search_word, positional_index, title)
