"""
# vim: set ft=python:
# vim usage:
# :set mp=make\ %\\\|&\ detemplate
"""
import sys
import os
import os.path
import re

remove_namespaces = [] #['wiselib']
depth = 1

# if you use an IDE, you might want to set this to a very high value so the
# IDE sees the full file paths!
filename_parts = 2

def bracedepth(line, maxdepth, braces='<>'):
	depth = 0
	r = ''
	escaped = False
	for c in line:
		if not escaped and c == braces[1]:
			depth -= 1

		if depth <= maxdepth:
			r += c

		if not escaped and c == braces[0]:
			depth += 1

		if c == '-':
			escaped = True
		elif escaped:
			escaped = False

	return r

def shorten_filenames(s, parts):
	r = ''
	for line in s.splitlines():
		m = re.match('^([^:]+)(:\d+:\d+:.*$)', line)
		if m:
			r += os.path.split(m.group(1))[1] + m.group(2) + '\n'
			#print "----- " + line + " ---> " + '/'.join(os.path.split(m.group(1))[-parts:]) + m.group(2) + '\n'
		else:
			r += line + '\n'
	return r

def highlight_errors(s):
	colors = {
			'error': 31,
			'warning': 33,
	}

	r = ''
	for line in s.splitlines():
		for keyword, color in colors.items():
			if keyword in line:
				r += '\x1b[' + str(color) + 'm' + line + '\x1b[m\n'
				break
		else:
			r += line + '\n'
	return r

def filter(s, cutaway, filename_parts):
	for ns in remove_namespaces:
		s = s.replace(ns + '::', '')
	s = bracedepth(s, cutaway, '<>')
	s = bracedepth(s, 0, '[]')
	s = shorten_filenames(s, filename_parts)
	s = highlight_errors(s)
	return s

if __name__ == '__main__':
	print filter(sys.stdin.read(), depth, filename_parts)


