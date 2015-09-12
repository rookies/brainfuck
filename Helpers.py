#!/usr/bin/python3

def find_brackets(text, bracket):
	beg = 0
	result = []
	pos = text.find(bracket, beg)
	while pos != -1:
		beg = pos+1
		result.append(pos)
		pos = text.find(bracket, beg)
	return result
