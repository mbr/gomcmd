#!/usr/bin/env python
# coding=utf8

# Copyright (c) 2010 Marc Brinkmann
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
import os
import optparse
import re
import urllib

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
	m = re.match('^.*(http://.*)$', url)
	if not m:
		raise ProgException('Not in URL format: %s' % url)
	data = urllib.urlopen(m.group(1)).read()
	m = re.search(r'(http://[^"]*)', data)
	return m.group(1)


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
	url = parse_url(args[0])

	print "opening %s %s" % (opts.media_player, url)
	os.execlp(opts.media_player, opts.media_player, url)
except ProgException, e:
	sys.stderr.write('%s: %s%s' % (parser.get_prog_name(), e, os.linesep))
