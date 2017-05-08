import pandas as pd
import numpy as np
from collections import Counter
import re
from nltk import pos_tag, word_tokenize

columns = ['ID', 'videoID', 'authorID', 'posted', 'content', 'rating']
df = pd.read_csv("data.csv", delimiter=';', error_bad_lines=False, nrows=100000, names=columns)

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>.*?</.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def cleantags(raw_html):
  cleanr = re.compile('&.*?;')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

regex = re.compile('[^a-zA-Z]')
#First parameter is the replacement, second parameter is your input string


cnt = Counter()
total = 0
i = 0

for line in df['content']:
	line = cleantags(line)
	line = cleanhtml(line)
	line = regex.sub(' ', line)
	line = line.lower()
	line = word_tokenize(line)
	i += 1
	print i
	for token in pos_tag(line):
		word = token[0]
		tag = token[1]
		if tag == 'NN':
			if len(word) > 2:
				cnt[word] += 1
				total += 1

for key in cnt.keys():
	cnt[key] = float(cnt[key])/total



average_p = np.mean(cnt.values())







dataset = open("comments_Arrival.txt")
comments = dataset.readlines()

cnt2 = Counter()

for line in comments:
	line = cleantags(line)
	line = cleanhtml(line)
	line = regex.sub(' ', line)
	line = line.lower()
	line = word_tokenize(line)
	for token in pos_tag(line):
		word = token[0]
		tag = token[1]
		if tag == 'NN':
			if len(word) > 2:
				cnt2[word] += 1
				total += 1


# for key in cnt2.keys()[:10]:
# 	print key, cnt2[key]


log_Pnx = Counter()

for key in cnt2.keys():
	if cnt[key] > 0:
		log_Pnx[key] = (cnt2[key] - cnt[key] * total) - cnt2[key] * np.log(cnt2[key]/(cnt[key] * total)) - np.log(cnt2[key])/2

	else:
		log_Pnx[key] = (cnt2[key] - average_p * total) - cnt2[key] * np.log(cnt2[key]/(average_p * total)) - np.log(cnt2[key])/2


for tag in log_Pnx.most_common():
	word = tag[0]
	if cnt[word] > 0:
		if cnt2[word] > cnt[word] * total:
			print tag
	else:
		if cnt2[word] > average_p * total:
			print tag











