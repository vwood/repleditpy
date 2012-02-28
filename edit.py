import sys
import os
import tempfile
import __main__

defined = {}
boilerplate = "#!/usr/bin/env python\n\n"

editor = os.environ.get('EDITOR', 'vim')

def edit(name, contents="", pos=0):
	"""Edit contents in an external editor, starting at pos (defaults to 0).
	The result is stored under name, and then evaluated in __main__."""
	tmp = tempfile.NamedTemporaryFile()
	tmp.write(contents)
	tmp.flush()
	os.system(editor + " %s +goto%s" % (tmp.name, str(pos)))
	tmp.seek(0)
	definition = tmp.read()
	defined[name] = definition
	exec definition in __main__.__dict__

def var_skel(name):
	return boilerplate + name + " = None\n" 

def fun_skel(name):
	return boilerplate + "def " + name + "():\n\t\"\"\"...\"\"\"\n\tpass\n"

def var_start_pos(name):
	return len(boilerplate) + len(name) + 4

def fun_start_pos(name):
	return len(boilerplate) + 4 + len(name) + 17

def get_var(name):
	return defined.get(name, var_skel(name))

def get_fun(name):
	return defined.get(name, fun_skel(name))

def ved(name):
	"""Edit a function definition in an editor."""
	edit(name, get_var(name), var_start_pos(name))

def fed(name):
	"""Edit a function definition in an editor."""
	edit(name, get_fun(name), fun_start_pos(name))

def dump(filename = "dump.py"):
	"""Dump definitions to a file."""
	f = open(filename, "w")
	f.write(boilerplate)
	for definition in defined.itervalues():
		if definition.startswith(boilerplate):
			definition = definition.replace(boilerplate, "", 1)
		f.write(definition)
		if not definition.endswith('\n\n'):
			f.write('\n')
	f.close()

