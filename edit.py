import sys
import os
import tempfile
import __main__

defined = {}
modeline = "#!/usr/bin/env python\n\n"
line_no = 5

editor = os.environ.get('EDITOR', 'vim')

def ed(name, g = globals()):
	tmp = tempfile.NamedTemporaryFile()	
	if defined.has_key(name):
		tmp.write(defined[name])
		tmp.flush()
	else:
		tmp.write(modeline + "def " + name + "():\n\t\"\"\"...\"\"\"\n\tpass\n")
		tmp.flush()
	os.system("vim %s +%s" % (tmp.name, str(line_no)))
	tmp.flush()
	tmp.seek(0)
	definition = tmp.read()
	defined[name] = definition
	exec definition in __main__.__dict__

def dump(filename = "dump.py"):
	f = open(filename, "w")
	for definition in defined.itervalues():
		f.write(definition)
	f.close()

