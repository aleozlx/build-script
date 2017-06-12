#if python2
#!/usr/bin/env python
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
#elif python3
#!/usr/bin/env python3
#endif
import os, sys, subprocess, io, csv, re, uuid, multiprocessing, subprocess
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
def shell_stream(cmd):
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	for line in proc.stdout:
		yield unicode(line).rstrip()

@python3
def shell_stream(cmd):
	with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
		for line in proc.stdout:
			yield str(line, encoding='utf-8').rstrip()

#if 0
VERSION = sys.version_info[0]

def main():
	r_goofydef = re.compile(r'^(#)(?:if|elif)\s+([0-9a-z]+)$')
	r_goofyend = re.compile(r'^(#)(end)if$')
	r_verdecor = re.compile(r'^(@)(python\d+)$')
	transitions = { 'python2': VERSION == 2, 'python3': VERSION == 3, 'end': True }
	state = ('#', True)
	for line in shell_stream(['cat', sys.argv[0]]):
		m = r_goofydef.match(line) or r_goofyend.match(line) or r_verdecor.match(line)
		if m:
			state = (m.group(1), transitions.get(m.group(2), False))
		elif not line and state[0] == '@':
			state = ('#', True)
		elif state[1]:
			print(line)

if __name__ == '__main__':
	main()
#endif
