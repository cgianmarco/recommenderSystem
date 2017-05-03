#########################################

# Get IDs of videos about a movie

#########################################


import subprocess

movie_title = "Titanic"

# Execute YTFS
test = subprocess.Popen(["java","-jar","YTFS.jar","--limit","20",movie_title], stdout=subprocess.PIPE)

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

print videoIds







#########################################

# Get comments from videoIDs

#########################################

import urllib, urllib2
import json

comments = []
# videoId = "l9PxOanFjxQ"
maxResults = 100


for videoId in videoIds:

	# Youtube query
	query = "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId=" + str(videoId) + "&maxResults=" + str(maxResults) + "&key=AIzaSyBHWLQQO7jtOu1i49pgKL4h0uupCDjK-Iw"
	print query


	try:
		response = urllib2.urlopen(query).read()

	# Ignore HTTP Error if comments disabled
	except urllib2.HTTPError:
		continue

	else:
		# From string to JSON
		response = json.loads(response)

		# Get comments
		for i in range(len(response['items'])):
			comments.append(response['items'][i]['snippet']['topLevelComment']['snippet']['textDisplay'])


# Save comments to file
file = open('comments.txt', 'w')
for item in comments:
	file.write("%s\n" % item.encode('utf-8'))

	
print "Number of saved comments: " + str(len(comments))

