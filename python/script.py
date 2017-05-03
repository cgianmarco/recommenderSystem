#########################################

# Get IDs of videos about a movie

#########################################


import subprocess

movie_title = "The thing"

# Execute YTFS
test = subprocess.Popen(["java","-jar","YTFS.jar","--limit","5",movie_title], stdout=subprocess.PIPE)

# Get output
output = test.communicate()[0]

# Get found links
links = []
for line in output.splitlines():
	words = line.split()
	if "Positivo:" in words:
		links.append(words[1])


# Extrapolate videoIDs
videoIds = []
for link in links:
	videoIds.append(link.split('?v=')[1])







#########################################

# Get comments from videoID

#########################################

import urllib2
import json

videoId = "l9PxOanFjxQ"
maxResults = 30

# Youtube query
query = "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId=" + str(videoId) + "&maxResults=" + str(maxResults) + "&key=AIzaSyBHWLQQO7jtOu1i49pgKL4h0uupCDjK-Iw"
response = urllib2.urlopen(query).read()

# From string to JSON
response = json.loads(response)

# Print comments
for i in range(len(response['items'])):
	print response['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal']

