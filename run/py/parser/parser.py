#!/usr/bin/python
# LL(1)
import xml.etree.cElementTree as ET 
__author__ = 'TaQini'

# production rule
class rule:
	def __init__(self, left, right):
		self.left = left
		self.right = right
	def show(self):
		print self.left, '->',
		for i in self.right:
			print i,
		print ''

# input string
class r: 
	def __init__(self, value, typ):
		self.type = typ
		self.value = value
		if typ == "identifer": 
			self.text = 'ID'
		elif 'constant' in typ: 
			self.text = 'CONST'
		else:
			self.text = value

# symbol (terminal or nonterminal)
class sym:
	def __init__(self, value, Vn, Vt):
		self.value = value
		self.FIRST = []
		self.FOLLOW = []
'''
	to be continue............
		if value in Vt:
			self.FIRST.append(value)
		else:
			pass
'''		

# xml file -> input string
def read_XML(xmlfile):
	tree = ET.ElementTree(file = xmlfile)
	root = tree.getroot()
	rst = [r(t.find("value").text, t.find("type").text) for t in root.iter("token")]
	return rst

# grammar file -> grammar list, Vn & Vt
def read_grammar(gramfile):
	with open(gramfile,'r') as f:
		g = [line[:-1] for line in f.readlines() if '->' in line and line[0] != '#']
	grammar = []
	for line in g:
		l,r = line.split('->')
		grammar.append(rule(l.split()[0], r.split()))
	return grammar

# get Vn and Vt
def get_symbols(grammar):
	V  = set()
	Vn = set()
	for rule in grammar:
		Vn.add(rule.left)
		V.add(rule.left)
		for i in rule.right:
			V.add(i)
	V.discard('epsilon') # except null string
	Vt = V-Vn
	rst_Vn = [sym(i, Vn, Vt) for i in Vn]
	rst_Vt = [sym(i, Vn, Vt) for i in Vt]
	return rst_Vn, rst_Vt

# create LL analyzing table
def create_table():
	pass


def FIRST(V, Vn, grammar):
	pass

def FOLLOW():
	pass

# Entry point
def main():
	# init input string
	r = read_XML('./a.token.xml')
	# for i in r: print i.text,

	# init production rules
	grammar = read_grammar('./grammar')
	# for r in grammar: r.show()

	# init symbols
	Vn, Vt = get_symbols(grammar)
	for i in Vt: print i.value,i.FIRST


if __name__ == "__main__":
	main()

