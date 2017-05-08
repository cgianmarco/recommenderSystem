#########################################

# Get IDs of videos about a movie

#########################################


import subprocess

movie_title = "Arrival"

# Execute YTFS
test = subprocess.Popen(["java","-jar","YTFS.jar","--limit","50",movie_title], stdout=subprocess.PIPE)

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
# videoIds = ["kVrqfYjkTdQ"]
maxResults = 100


for videoId in videoIds:

	# Youtube query
	query = "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet,replies&videoId=" + str(videoId) + "&maxResults=" + str(maxResults) + "&key=AIzaSyBHWLQQO7jtOu1i49pgKL4h0uupCDjK-Iw"
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
			if 'replies' in response['items'][i]:
				for j in range(len(response['items'][i]['replies']['comments'])):
					comments.append(response['items'][i]['replies']['comments'][j]['snippet']['textDisplay'])



# Save comments to file
file = open('comments_' + str(movie_title) + '.txt', 'w')
for item in comments:
	file.write("%s\n" % item.encode('utf-8'))

	
print "Number of saved comments: " + str(len(comments))

# {u'snippet': {u'totalReplyCount': 1, u'canReply': False, u'topLevelComment': {u'snippet': {u'authorChannelUrl': u'http://www.youtube.com/channel/UCJy9frQKoo0vf55AMDHacKw', u'authorDisplayName': u'buguedsteve55', u'updatedAt': u'2017-05-05T13:06:37.000Z', u'videoId': u'l9PxOanFjxQ', u'publishedAt': u'2017-05-05T13:06:37.000Z', u'viewerRating': u'none', u'authorChannelId': {u'value': u'UCJy9frQKoo0vf55AMDHacKw'}, u'canRate': False, u'textOriginal': u'what is the song ID', u'likeCount': 0, u'authorProfileImageUrl': u'https://yt3.ggpht.com/-O3ogszEdZaY/AAAAAAAAAAI/AAAAAAAAAAA/rB9Lzv7kYgY/s28-c-k-no-mo-rj-c0xffffff/photo.jpg', u'textDisplay': u'what is the song ID'}, u'kind': u'youtube#comment', u'etag': u'"m2yskBQFythfE4irbTIeOgYYfBU/h0M9k97yhd_Yqx8DtZZ-oL8l7mM"', u'id': u'z12le5oy1qyfjry2t23att3aqvj3tbjte'}, u'videoId': u'l9PxOanFjxQ', u'isPublic': True}, u'kind': u'youtube#commentThread', u'etag': u'"m2yskBQFythfE4irbTIeOgYYfBU/_BjhspLOV3ey9q3Paeb7-k2dZJw"', u'id': u'z12le5oy1qyfjry2t23att3aqvj3tbjte'}
