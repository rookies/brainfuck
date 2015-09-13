#!/usr/bin/python3

def find_all(string, substring):
	beg = 0
	result = []
	pos = string.find(substring, beg)
	while pos != -1:
		beg = pos+1
		result.append(pos)
		pos = string.find(substring, beg)
	return result
	
def find_bracketpairs(text, bopen="(", bclose=")"):
	opening = find_all(text, bopen)
	closing = find_all(text, bclose)
	## Check if the number of both is the same:
	if len(opening) != len(closing):
		raise ValueError("Can't find bracket pairs, %d opening brackets, but %d closing." % (len(opening), len(closing)))
	## Create pairs and register them:
	brackets = []
	for i in range(len(closing)):
		if opening[0] > closing[i]:
			raise ValueError("Can't find bracket pairs, no matching found for closing one at position %d." % closing[i])
		j = 0
		while (len(opening) > j+1) and (opening[j+1] < closing[i]):
			j += 1
		brackets.append((opening[j], closing[i]))
		del opening[j]
	return brackets
