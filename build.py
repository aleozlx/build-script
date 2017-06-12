#if python2
#!/usr/bin/env python
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
#elif python3
#!/usr/bin/env python3
#endif
import os, sys, subprocess, io, csv, re, uuid, multiprocessing, subprocess, itertools
#if 0
class IncompatibleFunction(dict):
	def __call__(self, *args, **kwargs):
		return self[VERSION](*args, **kwargs)

ifuncs = dict()
from functools import wraps
def __pyversion(v):
	def decorator(f):
		@wraps(f)
		def wrapped(*args, **kwargs):
			return f(*args, **kwargs)
		if not f.__name__ in ifuncs:
			ifuncs[f.__name__] = IncompatibleFunction()
		ifunc = ifuncs[f.__name__]
		ifunc[v] = wrapped
		return ifunc
	return decorator

python2, python3 = list(map(__pyversion, [2, 3]))
#endif

@python2
def popen_stream(cmd, **options):
	options = options or dict(stdout=subprocess.PIPE)
	proc = subprocess.Popen(cmd, **options)
	for line in proc.stdout:
		yield unicode(line).rstrip()

@python3
def popen_stream(cmd, **options):
	options = options or dict(stdout=subprocess.PIPE)
	with subprocess.Popen(cmd, **options) as proc:
		for line in proc.stdout:
			yield str(line, encoding='utf-8').rstrip()

class BasePathFunction(str):
	def __call__(self, pth):
		return os.path.join(self, pth)
class Step(object):
	def __init__(self, cmd, **options):
		self.cmd = cmd
		self.options = options
	def get_argv(self):
		return '\x20'.join(map(lambda i: ("'%s'"%i) if '\x20' in i else i, self.cmd))
	def __str__(self):
		argv = self.get_argv()
		if self.options:
			argv = '{} \x1B[35m{}\x1B[0m'.format(argv, str(self.options))
		return argv
	@staticmethod
	def ctor_mapper(s):
		return s if isinstance(s, Step) else Step(s)

#if 0
@python2
def proc_goofy(code, **options):
	py_future = '\n'.join(map('from __future__ import {}'.format, ['print_function', 'unicode_literals', 'division']))
	py_script = '\n'.join([py_future, 'import os, sys', code])
	return popen_stream(['python2', '-c', py_script], **options)

@python3
def proc_goofy(code, **options):
	return popen_stream(['python3', '-c', '\n'.join(['import os, sys', code])], **options)

VERSION = sys.version_info[0]

def main():
	r_goofydef = re.compile(r'^(#)(?:if|elif)\s+([0-9a-z]+)$')
	r_goofyend = re.compile(r'^(#)(end)if$')
	r_verdecor = re.compile(r'^(@)(python\d+)$')
	transitions = { 'python2': VERSION == 2, 'python3': VERSION == 3, 'end': True }
	state = ('#', True)
	for line in popen_stream(['cat', sys.argv[0]]):
		m = r_goofydef.match(line) or r_goofyend.match(line) or r_verdecor.match(line)
		if m:
			if m.group(1) == '@' and state[1] == False:
				continue # '@' can be disabled by '#'
			state = (m.group(1), transitions.get(m.group(2), False))
		elif not line and state[0] == '@':
			state = ('#', True)
		elif state[1]:
			print(line)

if __name__ == '__main__':
	main()
#endif
#if python2
"""
Python2 example
"""
#elif python3
"""
Python3 example
"""
#endif
