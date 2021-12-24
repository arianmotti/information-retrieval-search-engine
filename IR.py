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

    # plt.plot(l1, l2)
    # plt.show()

    for i in range(10):
        # print(freq_words[i])
        positional_index.pop(freq_words[i], None)

    freq_words = sorted(positional_index.keys(), key=lambda x: positional_index[x][0], reverse=True)

    for i in range(len(freq_words)):
        l3.append(math.log(i + 1, 10))
        l4.append(math.log(positional_index[freq_words[i]][0], 10))

    # plt.plot(l3, l4)
    # plt.show()
    return positional_index


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


def tf_idf(term_frequency, doc_frequency, N):
    tf = 1 + math.log10(term_frequency)
    idf = math.log10(N / doc_frequency)
    return tf * idf


def create_champion_list(positional_index):
    champion_list = {}
    weighted_list = {}
    for term in positional_index.keys():
        weighted_list[term] = []
        weighted_list[term].append(len(positional_index[term][1].keys()))
        weighted_list[term].append({})
        for docID in positional_index[term][1].keys():
            weighted_list[term][1][docID] = tf_idf((len(positional_index[term][1][docID])), weighted_list[term][0],
                                                   len(positional_index))
    for term in weighted_list:
        champion_list[term] = []
        champion_list[term].append(weighted_list[term][0])
        champion_list[term].append({})
        doc_list = sorted(weighted_list[term][1].keys(), key=lambda x: weighted_list[term][1][x],
                          reverse=True)
        if len(doc_list) < 20:
            k = len(doc_list)
        else:
            k = 20
        for i in range(k):
            champion_list[term][1][doc_list[i]] = weighted_list[term][1][doc_list[i]]
    return champion_list


def create_weighted_content_list(positional_index):
    weighted_list = {}
    for term in positional_index.keys():
        weighted_list[term] = []
        weighted_list[term].append(len(positional_index[term][1].keys()))
        weighted_list[term].append({})
        for docID in positional_index[term][1].keys():
            weighted_list[term][1][docID] = tf_idf((len(positional_index[term][1][docID])), weighted_list[term][0],
                                                   len(positional_index))
    return weighted_list


def create_weighted_search_query(weighted_content_list, content_lenght, query):
    query_posting = {}
    weighted_query = {}
    for term in query:
        if term in weighted_content_list:
            if term in query_posting.keys():
                query_posting[term] += 1
            else:
                query_posting[term] = 1
    for term in query_posting.keys():
        weighted_query[term] = tf_idf(query_posting[term], len(weighted_content_list[term][1].keys()), content_lenght)
    return weighted_query


def calculate_document_vector(docID, weighted_posting_list):
    sigma_doc = 0
    for term in weighted_posting_list:
        if docID in weighted_posting_list[term][1].keys():
            sigma_doc += pow(weighted_posting_list[term][1][docID], 2)
    return sigma_doc


def cosinus_similarity(weighted_content_list, weighted_search_word, content_lenght):
    similarity_list = []
    for docID in range(content_lenght):
        sigma_dot = 0
        sigma_query = 0
        sigma_doc = 0
        for term in weighted_search_word.keys():
            if docID in weighted_content_list[term][1].keys():
                sigma_dot += weighted_search_word[term] * weighted_content_list[term][1][docID]
                sigma_query += (weighted_search_word[term] * weighted_search_word[term])
                sigma_doc = calculate_document_vector(docID, weighted_content_list)
                similarity_list.append([docID, sigma_dot / (math.sqrt(sigma_doc) * math.sqrt(sigma_query))])
    return similarity_list


data = pd.read_excel(r'IR.xlsx')
positional_index = {}
weighted_content_list = {}
weighted_search_query = {}
cosinus_similarity_list = {}
content = data['content'].tolist()
title = data['title'].tolist()
preprocessed_data = preproccesing(content)
positional_index = create_positional_index(positional_index, preprocessed_data)
search_word = input()
search_word = preproccesing(search_word, 1)
print('enter 1 for phase 1 or enter 2 for phase 2')
phase = input()
if phase == '1':
    print('phase 1')

    if len(search_word) == 1:
        search_single_word(search_word, positional_index, title)
    else:
        search_complex_word(search_word, positional_index, title)

if phase == '2':
    print('phase 2')
    print('enter 1 for weighted list or enter 2 for champion list')
    method = input()
    if method == '1':

        weighted_content_list = create_weighted_content_list(positional_index)
        weighted_search_word = create_weighted_search_query(weighted_content_list, len(content), search_word)
        cosinus_similarity_list = cosinus_similarity(weighted_content_list, weighted_search_word, len(content))
        # print(cosinus_similarity_list)
        sorted_cosinus_similarity_list = sorted(cosinus_similarity_list, key=lambda x: x[1], reverse=True)
        if len(sorted_cosinus_similarity_list) > 10:
            for i in range(10):
                print(sorted_cosinus_similarity_list[i])
                print(title[sorted_cosinus_similarity_list[i][0]])
        else:
            for i in range(len(sorted_cosinus_similarity_list)):
                print(sorted_cosinus_similarity_list[i])
                print(title[sorted_cosinus_similarity_list[i][0]])
    if method == '2':
        champion_list = create_champion_list(positional_index)
        # print(champion_list)
        weighted_search_word = create_weighted_search_query(champion_list, len(content), search_word)
        cosinus_similarity_list = cosinus_similarity(champion_list, weighted_search_word, len(content))
        sorted_cosinus_similarity_list = sorted(cosinus_similarity_list, key=lambda x: x[1], reverse=True)
        if len(sorted_cosinus_similarity_list) > 10:
            for i in range(10):
                print(sorted_cosinus_similarity_list[i])
                print(title[sorted_cosinus_similarity_list[i][0]])
        else:
            for i in range(len(sorted_cosinus_similarity_list)):
                print(sorted_cosinus_similarity_list[i])
                print(title[sorted_cosinus_similarity_list[i][0]])
