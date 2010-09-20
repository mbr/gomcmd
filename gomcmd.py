#!/usr/bin/env python
# coding=utf8

import sys
import os
import optparse
import re

class ProgException(Exception): pass

def register_gnome_url_handler(urltype, command, enabled = True, needs_terminal = False):
	import gconf # not everyone has gconf, small non-critical performance hit importing
	             # it here!

	dirname = '/desktop/gnome/url-handlers/%s' % urltype
	c = gconf.client_get_default()

	# create the directory
	if not c.dir_exists(dirname):
		print "created %s" % dirname
		c.add_dir(dirname, gconf.CLIENT_PRELOAD_NONE)

	# create the values
	v = gconf.Value(gconf.VALUE_STRING)
	v.set_string(command)
	c.set(dirname + '/command', v)

	v = gconf.Value(gconf.VALUE_BOOL)
	v.set_bool(enabled)
	c.set(dirname + '/enabled', v)

	v = gconf.Value(gconf.VALUE_BOOL)
	v.set_bool(needs_terminal)
	c.set(dirname + '/needs_terminal', v)

def parse_url(url):
	m = re.match('(.*?)://(.*)$', url)
	if not m:
		raise ProgException('Not in URL format: %s' % url)
	return (m.group(1), m.group(2))

try:
	parser = optparse.OptionParser()
	parser.add_option('-M','--media-player',default='vlc',help='the media player to use. defaults to VLC')
	parser.add_option('-G','--register-gnome-handlers',default=False,action='store_true',help='register url handlers with gnome')

	opts, args = parser.parse_args()

	# register url handlers?
	if opts.register_gnome_handlers:
		import gconf
		register_gnome_url_handler('gomcmd', "%s '%%s'" % os.path.abspath(sys.argv[0]))
		# do nothing else
		sys.exit(0)

	if not args:
		raise ProgException('No arguments')
	if 1 != len(args):
		raise ProgException('Too many arguments')

	# convert the argument
	protocol, target = parse_url(args[0])

	if not 'gomcmd' == protocol: raise ProgException("Don't know how to handle protocol: %s" % protocol)

	# extra stream from target:
	try:
		url = 'http://%s' % target[target.index('://')+3:]
	except ValueError:
		raise ProgException('Not a valid GomTV stream URL: %s' % target)
	print "opening %s %s" % (opts.media_player, url)
	os.execlp(opts.media_player, opts.media_player, url)
except ProgException, e:
	sys.stderr.write('%s: %s%s' % (parser.get_prog_name(), e, os.linesep))

