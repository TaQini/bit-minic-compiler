#!/usr/bin/python
# LL(1)
import xml.etree.cElementTree as ET 
__author__ = 'TaQini'

# production rule
class rule:
	def __init__(self, left, right):
		self.left = left
		self.right = right
		self.first = set()
		self.follow = set()
		# init first
		for i in right:
			for c in i:
				if c != 'epsilon':
					self.first.add(c)
					eps = 0
					break
				else:
					eps = 1
			if eps == 1:
				self.first.add('epsilon')
	def update_first(self, g):
		while True:
			tmp = self.first & g.Vn
			if len(tmp) == 0:
				break
			for i in tmp:
				r = g.get_rule(i)
				self.first.remove(i)
				self.first = self.first | r.first
	def update_follow(self, g):
		if g.rules[0].left == self.left:
			self.follow.add('#')
	def show_first(self):
		print self.left, self.first
	def show_follow(self):
		print self.left, self.follow
	def show_rules(self):
		print self.left,'->',
		for i in self.right:
			for c in i:
				print c,
			print '|',
		print '\b\b', ''

class grammar:
	def __init__(self, rules):
		self.rules = rules
		self.V  = set()
		self.Vn = set()
		self.Vt = set()
		for rule in self.rules:
			self.Vn.add(rule.left)
			self.V.add(rule.left)
			for i in rule.right:
				for c in i:
					self.V.add(c)
		self.V.discard('epsilon')
		self.Vt = self.V - self.Vn
		# update first
		for r in self.rules:
			r.update_first(self)
		for r in self.rules:
			r.update_follow(self)
	def get_rule(self, s):
		for rule in self.rules:
			if rule.left == s:
				return rule

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
	gram = dict()
	for line in g:
		l,r = line.split('->')
		l = l.split()[0]
		r = r.split()
		if l in gram.keys():
			gram[l].append(r)
		else:
			gram[l] = [r,]
	rst = grammar([rule(k, gram[k]) for k in gram.keys()])
	return rst

# create LL analyzing table
def create_table():
	pass

# Entry point
def main():
	# init input string
	r = read_XML('./a.token.xml')

	# init production rules, FIRST, FOLLOW
	g = read_grammar('./grammar')

	for r in g.rules: r.show_first()
	for r in g.rules: r.show_follow()
	
if __name__ == "__main__":
	main()

