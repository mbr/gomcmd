#!/usr/bin/env python
# coding=utf8

import sys
import os
import optparse
import re

class ProgException(Exception): pass

def parse_url(url):
	m = re.match('(.*?)://(.*)$', url)
	if not m:
		raise ProgException('Not in URL format: %s' % url)
	return (m.group(1), m.group(2))

try:
	parser = optparse.OptionParser()
	parser.add_option('-M','--media-player',default='vlc',help='the media player to use. defaults to VLC')

	opts, args = parser.parse_args()

	if not args:
		raise ProgException('No arguments')
	if 1 != len(args):
		raise ProgException('Too many arguments')

	# convert the argument
	protocol, target = parse_url(args[0])

	if not 'gomcmd' == protocol: raise ProgException("Don't know how to handle protocol: %s" % protocol)

	# extra stream from target:
	url = 'http://%s' % target[target.index('://')+3:]
	print "opening %s %s" % (opts.media_player, url)
	os.execlp(opts.media_player, opts.media_player, url)
except ProgException, e:
	sys.stderr.write('%s: %s%s' % (parser.get_prog_name(), e, os.linesep))

