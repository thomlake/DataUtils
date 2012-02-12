#---------------------------------------#
#	This file is part of DataUtils.
#
#	DataUtils is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	BowNlPy is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with DataUtils.  If not, see <http://www.gnu.org/licenses/>.
#---------------------------------------#
# author:
#	tllake 
# email:
#	<thomas.l.lake@wmich.edu>
#	<thom.l.lake@gmail.com>
# date:
#	2011.01.16
# file:
#	tokenizer.py
# description:
#	composable functions for tokenizing strings	
#---------------------------------------#

from collections import defaultdict

ORD_Z = ord('z')
ORD_A = ord('a')
ORD_0 = ord('0')
ORD_9 = ord('9')

## Docs
#  for this fun
def not_number(c):
	"""Return True if c is not a number
	
	:param c: to test
	:type c: chr
	:rtype: bool
	"""
	c = ord(c)
	if c > ORD_9 or c < ORD_0:
		return True
	return False

def not_letter(c):
	"""Return True if c is not a letter.
	
	:param c: to test
	:type c: chr
	:rtype: bool
	"""	
	c = ord(c)
	if c > ORD_Z or c < ORD_A:
		return True
	return False

def alphanumeric(c):
	"""Return True if c is an aphanumeric character.
	
	:param c: to test
	:type c: chr
	:rtype: bool
	"""
	if not_number(c) and not_letter(c):
		return False
	return True

def non_alphanumeric(c):
	"""Return True if c is not an alphanumeric character.
	
	:param c: to test
	:type c: chr
	:rtype: bool
	"""
	if alphanumeric(c):
		return False
	return True

def initialize_tokenizer():
	"""Intitial and empty tokenizer. (hint: it is just an empty list)
	
	:rtype: list
	"""
	return []

def add_to_tokenizer(t, f, args = None):
	"""Add a function call and arguments to a series of function calls.
	
	:param f: must take a string or list as a first argument and return a string or list of strings
	:param args: additional argument passed to f
	
	:type f: function
	:type args: list

	:rtype: None
	"""
	t.append((f, args))	

def tokenize(s, funcs):
	"""Split s into a list of tokens by composing of function calls.
		
	:param s: to be tokenized
	:param funcs: to be called to tokenize s

	:type s: string or list of strings
	:type funcs: list of (function, arguments) tuples

	:rtype: list of strings
	"""
	for f, args in funcs:
		if args is None:
			s = f(s)
		elif type(args) is list:
				s = f(s, *args)
		else:
			s = f(s, args)
	s = [x for x in s if x != '\t' and x != '\n'] # no tabs or newlines
	s = [x for x in s if len(x) > 0] # no empty string
	return s

def lower_case(s):
	"""Return a list where each substing in s converted to lowercase.
	
	:param s: to be lowercased
	:type s: string or list of strings
	:rtype: list of strings
	"""
	if not type(s) is list:
		s = [s]
	return [sub.lower() for sub in s]

def rm_dup_letters(s, n = 2, ignore = []):
	"""Replace any consecutive character occurrence of length greater than n with n occurrences.
	
	:param s: to have letters removed
	:param n: consecutive restriction
	:type s: string or list of strings
	:type n: int
	:rtype: list of strings
	"""
	if not type(s) is list:
		s = [s]
	result = []
	for substring in s:
		if substring in ignore:
			result.append(substring)
		else:
			temp = substring[:n]
			for c in substring[n:]:
				dup = 0
				for i in range(1, n + 1):
					if c == temp[-i]:
						dup += 1
				if dup != n:
					temp += c
			result.append(temp)
	return result

def split_ditch_char(s, c, ignore = []):
	"""Return a list where each string is split on c, with c removed. 
	
	:param s: to be split
	:param c: to split on and remove
	:param ignore: substrings to ignore
	:type s: string or list of strings
	:type c: chr
	:type ignore: list of strings
	:rtype: list of strings
	"""
	if not type(s) is list:
		s = [s]
	result = []
	for substring in s:
		if substring in ignore:
			result.append(substring)
		else:
			splits = substring.split(c)
			for split in splits:
				result.append(split)
	return result

def split_ditch_func(s, f, ignore = []):
	"""Return a list where each string is split if f(c) returns True for each c in s. c is removed.

	:param s: to be split
	:param f: should take a chr and return a bool
	:param ignore: substrings to ignore
	:type s: string or list of strings
	:type f: function
	:type ignore: list of strings
	:rtype: list of strings
	"""
	result = []
	if not type(s) is list:
		s = [s]
	for substring in s:
		if substring in ignore:
			result.append(substring)
		else:
			stack = ''
			for c in substring:
				if f(c):
					if len(stack) > 0:
						result.append(stack)
						stack = ''
				else:
					stack += c
			if len(stack) > 0:
				result.append(stack)
	return result

def split_keep_char(s, c, ignore = []):
	"""Return a list where each string is split on c, c is kept as a token of length 1. 

	:param s: to be split
	:param c: to split on
	:param ignore: substrings to ignore
	:type s: string or list of strings
	:type c: chr	
	:type ignore: list of strings
	:rtype: list of strings
	"""
	result = []
	if not type(s) is list:
		s = [s]
	for substring in s:
		if substring in ignore:
			result.append(substring)
		else:
			rest = substring
			while len(rest) > 0:
				splits = rest.partition(c)
				result.append(splits[0])
				if len(splits[1]) > 0: 
					result.append(splits[1])
				rest = splits[2] 
	return result

def split_keep_func(s, f, ignore = []):
	"""Return a list where each string is split if f(c) returns True for each c in s. c is kept as a token.

	:param s: to be split
	:param f: should take a chr and return a bool
	:param ignore: substrings to ignore
	:type s: string or list of strings
	:type f: function
	:type ignore: list of strings
	:rtype: list of strings
	"""
	result = []
	if not type(s) is list:
		s = [s]
	for substring in s:
		if substring in ignore:
			result.append(substring)
		else:
			stack = ''
			for c in substring:
				if f(c):
					if len(stack) > 0:
						result.append(stack)
						stack = ''
					result.append(c)
				else:
					stack += c
			if len(stack) > 0:
				result.append(stack)
	return result

def replace_full_match(s, token, replacement):
	"""Replace a substring in s with replacement if substring **is** token.
	
	:param s: to be modified
	:param token: to match
	:param replacement: to replace token
	:type s: string or list of strings
	:type token: string	
	:type replacement: string
	:rtype: list of strings
	"""
	if not type(s) is list:
		s = [s]
	return [replacement if substring is token else substring for substring in s]

def replace_partial_match(s, token, replacement):
	"""Replace a substring in s with replacement if token **is in** substring.
	
	:param s: to be modified
	:param token: to match
	:param replacement: to replace token
	:type s: string or list of strings
	:type token: string	
	:type replacement: string
	:rtype: list of strings
	"""
	if not type(s) is list:
		s = [s]
	return [replacement if token in substring else substring for substring in s]

def replace_and_split(s, token, replacement):
	"""Split each substring at an occurence of token, replacing token with replacement.
	
	:param s: to be split
	:param token: to match
	:param replacement: to replace token
	:type s: string or list of strings
	:type token: string	
	:type replacement: string
	:rtype: list of strings
	"""
	result = []
	if not type(s) is list:
		s = [s]
	for substring in s:
		rest = substring
		while len(rest) > 0:
			splits = rest.partition(token)
			result.append(splits[0])
			if len(splits[1]) > 0: 
				result.append(replacement)
			rest = splits[2]
	return result

def replace_if_startswith(s, token, replacement):
	"""Replace each substring in s with replacement if substring starts with token.
	
	:param s: to be modified
	:param token: to match
	:param replacement: to replace token
	:type s: string or list of strings
	:type token: string	
	:type replacement: string
	:rtype: list of strings
	"""
	if not type(s) is list:
		s = [s]
	return [replacement if substring.startswith(token) else substring for substring in s]

def replace_if_endswith(s, token, replacement):
	"""Replace each substring in s with replacement if substring ends with token.
	
	:param s: to be split
	:param token: to match
	:param replacement: to replace token
	:type s: string or list of strings
	:type token: string	
	:type replacement: string
	:rtype: list of strings
	"""
	if not type(s) is list:
		s = [s]
	return [replacement if substring.endswith(token) else substring for substring in s]

def make_bigram_poset(tokens):
	"""strict order"""
	d = defaultdict(set)
	for t1 in tokens:
		for t2 in tokens:
			if t1 != t2:
				if t1 < t2:
					d[t1].add(t2)
				else:
					d[t2].add(t1)
					
	poset = [[parent,child] for parent, children in d.items() for child in children]
	return poset

if __name__ == '__main__':
	s = 'HHHEEYYYY?hellllo @somebody My WONder:-(fulll, www.google.com fri:-)en:-)ds!'
	t = initialize_tokenizer()
	add_to_tokenizer(t, lower_case)
	add_to_tokenizer(t, split_ditch_char, [' '])
	add_to_tokenizer(t, rm_dup_letters)
	add_to_tokenizer(t, replace_and_split, [':-)', '<smileyface>'])
	add_to_tokenizer(t, replace_and_split, [':-(', '<frownyface>'])
	for url_part in ['http://', '.com', '.net', '.org', 'www.']:
		add_to_tokenizer(t, replace_partial_match, [url_part, '<url>'])
	add_to_tokenizer(t, replace_if_startswith, ['@', '<mention>'])
	add_to_tokenizer(t, split_ditch_func, [non_alphanumeric, ['<url>', '<smileyface>', '<frownyface>', '<mention>']])
	tokens = tokenize(s, t)
	print sorted(tokens)
	print len(tokens)
	bitokens = sorted(make_bigram_poset(tokens))
	for bt in bitokens:
		print bt
	print len(bitokens)

