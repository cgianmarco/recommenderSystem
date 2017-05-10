import pandas as pd
import numpy as np
from collections import Counter
import re
from nltk import pos_tag, word_tokenize


#######################################

# Preprocessing

#######################################

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>.*?</.*?>')
  cleantext = re.sub(cleanr, ' ', raw_html)
  return cleantext

def cleantags(raw_html):
  cleanr = re.compile('&.*?;')
  cleantext = re.sub(cleanr, ' ', raw_html)
  return cleantext


def preprocess(line):
	regex = re.compile('[^a-zA-Z]')
	line = cleantags(line)
	line = cleanhtml(line)
	line = regex.sub(' ', line)
	line = line.lower()
	return line


#######################################

# Getting stats

#######################################


def count_nouns(dataset):
	cnt = Counter()

	for line in dataset:
		line = preprocess(line)
		line = word_tokenize(line)
		for token in pos_tag(line):
			# token is a tuple (word, tag)
			word = token[0]
			tag = token[1]

			# Only consider names
			if 'NN' in tag:
				# Longer than three chars
				if len(word) > 3:
					cnt[word] += 1
	return cnt


def from_counts_to_probability(cnt):
	for key in cnt.keys():
		cnt[key] = float(cnt[key])/np.sum(cnt.values())
	return cnt




#######################################

# External Dataset

#######################################

columns = ['ID', 'videoID', 'authorID', 'posted', 'content', 'rating']
df = pd.read_csv("data.csv", delimiter=';', error_bad_lines=False, nrows=1000, names=columns)

corpus_cnt = count_nouns(df['content'])
corpus_cnt = from_counts_to_probability(corpus_cnt)
average_p = np.mean(corpus_cnt.values())




#######################################

# Movie Comments Dataset

#######################################

comments_filename = "comments_titanic.txt"

dataset = open(comments_filename)
comments = dataset.readlines()

movie_cnt = count_nouns(comments)
total = np.sum(movie_cnt.values())


#######################################

# Calculate log(Pnx)

#######################################

log_Pnx = Counter()

for key in movie_cnt.keys():

	# if word in corpus use corpus_cnt
	# else use average probability value
	if corpus_cnt[key] > 0:
		log_Pnx[key] = (movie_cnt[key] - corpus_cnt[key] * total) - movie_cnt[key] * np.log(movie_cnt[key]/(corpus_cnt[key] * total)) - np.log(movie_cnt[key])/2

	else:
		log_Pnx[key] = (movie_cnt[key] - average_p * total) - movie_cnt[key] * np.log(movie_cnt[key]/(average_p * total)) - np.log(movie_cnt[key])/2



#######################################

# Print tags and log(Pnx)

#######################################

tags = []

for tag in log_Pnx.most_common():
	word = tag[0]
	if corpus_cnt[word] > 0:
		if movie_cnt[word] > corpus_cnt[word] * total:
			tags.append(word)
			print tag
	else:
		if movie_cnt[word] > average_p * total:
			tags.append(word)
			print tag





