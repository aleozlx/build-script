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

VERSION = sys.version_info[0]

def main():
	r_goofydef = re.compile(r'^#(?:if|elif)\s+([0-9a-z]+)$')
	r_goofyend = re.compile(r'^#endif$')
	for line in shell_stream(['cat', sys.argv[0]]):
		m = r_goofydef.match(line)
		if m:
			v = m.group(1)
			print(line, m.group(1))

if __name__ == '__main__':
	main()
