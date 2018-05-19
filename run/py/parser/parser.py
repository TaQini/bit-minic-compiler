#!/usr/bin/python
# LL(1)
import xml.etree.ElementTree as ET 
from lxml import etree
import xlwt
import sys
__author__ = 'TaQini'
DEBUG = False
# production rule
class rule:
	def __init__(self, left, right, start):
		self.start = start
		self.left = left
		self.right = right
		self.first = set()
		# init FIRST-set: relation diagram of first-set
		for i in right:
			for c in i:
				if c != 'epsilon':
					self.first.add(c)
					eps = False
					break
				else:
					eps = True
			if eps:
				self.first.add('epsilon')
		# init FOLLOW-set
		self.follow = set()
		if self.start:
			self.follow.add('#')
	def init_follow(self, g): # relation diagram of follow-set
		for X in self.right:
			for i in range(len(X)): # rule: self -> X[0]X[1]...X[len]
				if DEBUG: print "X[i] = " + str(X[i]), "i = " + str(i+1),"len = " + str(len(X))
				if X[i] in (g.Vt | {'epsilon'}):
					pass
				elif X[i] in g.Vn:
					if i == len(X)-1: # no X[i+1]
						if DEBUG: self.show_rule(self.right.index(X))
						if X[i] != self.left :
							g.get_rule(X[i]).follow.add(self.left)
							if DEBUG: print "FOLLOW " + str(self.left) + "--> FOLLOW " + str(X[i])
					else: # has X[i+1]
						if DEBUG: print "have rest string:"
						eps = True
						for j in range(i+1,len(X)): # the rest
							if DEBUG: print X[j]
							if X[j] in g.Vt:
								g.get_rule(X[i]).follow.add(X[j])
								eps = False
								continue
							if ['epsilon'] in g.get_rule(X[j]).right: # X[j] => epsilon
								if DEBUG: g.get_rule(X[j]).show_rule(g.get_rule(X[j]).right.index(['epsilon']))
								if DEBUG: g.get_rule(X[j]).show_first()
								if len(g.get_rule(X[j]).right) > 1:
									g.get_rule(X[i]).follow = g.get_rule(X[i]).follow | (g.get_rule(X[j]).first - {'epsilon'})
							else:
								eps = False
								g.get_rule(X[i]).follow = g.get_rule(X[i]).follow | (g.get_rule(X[j]).first - {'epsilon'})
						if eps: # rest => eps
							if DEBUG: self.show_rule(self.right.index(X))
							if X[i] != self.left :
								g.get_rule(X[i]).follow.add(self.left)
								if DEBUG: print "FOLLOW " + str(self.left) + "--> FOLLOW " + str(X[i])
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
		while True:
			tmp = self.follow & g.Vn
			for i in tmp:
				r = g.get_rule(i)
				self.follow = self.follow | r.follow 
			new_tmp = self.follow & g.Vn
			if new_tmp == tmp:
				break
		self.follow = self.follow - g.Vn
	def show_first(self):
		print 'FIRST(' + self.left + ') =', self.first
	def show_follow(self):
		print 'FOLLOW(' + self.left + ') =', self.follow
	def show_rule(self, index):
		rst = self.left + ' -> '
		for c in self.right[index]:
			rst += c + ' '
		return rst
	def set_start(self):
		self.start = True
# grammar - a set of rules
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
		# init and update follow
		for r in self.rules:
			r.init_follow(self)
		for r in self.rules:
			r.update_follow(self)
	def get_rule(self, s):
		for rule in self.rules:
			if rule.left == s:
				return rule
# char in input stream
class char: 
	def __init__(self, value, typ):
		self.type = typ
		self.value = value
		if typ == "identifer": 
			self.text = 'ID'
		elif 'constant' in typ: 
			self.text = 'CONST'
		else:
			self.text = value
# input stream
class stream:
	def __init__(self, r):
		self.r = r
	def show(self):
		rst = ''
		for c in self.r:
			rst += c.text + ' '
		return rst
	def move(self):
		self.r.pop(0)
	def p(self):
		return (self.r[0].text, self.r[0].value)
# create LL(1) parsing table
class LL_table:
	def __init__(self, g):
		self.table = dict()
		for rule in g.rules:
			for P in rule.right:
				for X in P: # P -> X0X1...Xn
					if X in g.Vt:
						if DEBUG and (rule.left,X) in self.table.keys(): 
							print "!!!!! not LL1 grammar"
							rle, idx = self.table[(rule.left,X)]
							print rle.show_rule(idx)
							print rule.show_rule(rule.right.index(P))
							print "#####"
						self.table[(rule.left,X)] = (rule, rule.right.index(P))
							
						break
					elif X in g.Vn:
						no_eps = True
						for a in g.get_rule(X).first:
							if a == 'epsilon':
								no_eps = False
							else:
								if DEBUG and (rule.left,a) in self.table.keys(): 
									print "!!!!! not LL1 grammar"
									rle, idx = self.table[(rule.left,a)]
									print rle.show_rule(idx)
									print rule.show_rule(rule.right.index(P))
									print "#####"
								self.table[(rule.left,a)] = (rule, rule.right.index(P))
						if no_eps:
							break
				for X in P: # P -> X0X1...Xn
					if X in g.Vt:
						break
					elif X in g.Vn:
						if 'epsilon' not in g.get_rule(X).first:
							break # if eps not all Xi.first, then eps not in X0X1...Xn.first
					for b in rule.follow:
						if DEBUG and (rule.left,b) in self.table.keys(): 
							print "!!!!! not LL1 grammar"
							rle, idx = self.table[(rule.left,b)]
							print rle.show_rule(idx)
							print rule.show_rule(rule.right.index(P))
							print "#####"
						self.table[(rule.left,b)] = (rule, rule.right.index(P))
	def show(self):
		for i in self.table.keys():
			rule, index = self.table[i]
			print 'M('+i[0]+', '+i[1]+') = '+ rule.show_rule(index)
	def query(self, Vn, Vt):
		try:
			rst = self.table[(Vn,Vt)]
		except KeyError, err:
			error(err)
		else:
			return rst
# LL(1) parsing stack
class stack:
	def __init__(self, g):
		for rule in g.rules:
			if rule.start:
				S = rule.left
				break
		self.s = ['#',S]
	def pop(self):
		return self.s.pop(-1)
	def push(self, l):
		self.s.extend(l[::-1])
		if 'epsilon' in self.s:
			self.s.remove('epsilon')
	def show(self):
		rst = ''
		for i in self.s:
			rst += i + ' '
		return rst
# parser tree 
class tree:
	def __init__(self, root):
		self.root = root
		self.children = []
	def add_children(self, children):
		pass

# INPUT: xml file -> input stream object
def read_XML(xmlfile):
	tree = ET.ElementTree(file = xmlfile)
	root = tree.getroot()
	rst = stream([char(t.find("value").text, t.find("type").text) for t in root.iter("token")])
	return rst
# INPUT: grammar file -> grammar object
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
	# start symbol
	S = g[0].split()[0]
	tmp = [rule(k, gram[k], False) for k in gram.keys() if k != S]
	tmp.append(rule(S, gram[S], True))
	rst = grammar(tmp)
	return rst
# Error handler
def error(err):
	print '[!] ERROR:', 
	print 'missing M('+err[0][0]+', '+err[0][1]+')'
	exit()
def get_element(l, tag):
	for ele in l:
		if ele.tag == tag:
			return ele
# Entry point
def main():
	# init input stream
	r = read_XML(sys.argv[1]) # iFile
	r = stream([char(i, 'a') for i in "i+i*i#"])
	# init production rules
	g = read_grammar('./grammar')
	# init LL(1) parsing table
	t = LL_table(g)
	# init LL(1) parsing stack
	s = stack(g)
	# init List of parsing procedure
	output = [['step', 'stack', 'rest string', 'action']]
	step = 1

	new_xml = ET.Element("ParserTree",attrib={"name":sys.argv[1].split('.')[0]+'.tree.xml'})
	l = [new_xml,]
	# mainloop 
	while True:
		line = [step, s.show(), r.show()]
		tmp = s.pop()
		if tmp in g.Vt | {'#'}:
			text, value = r.p()
			if tmp == text:
				if tmp == '#':
					line.append('done')
					output.append(line)
					break
				else:
					r.move()
			if text in ['ID', 'CONST']:
				action = 'pop '+text+'('+value+'), p++'
			else:
				action = 'pop '+text+', p++'
		else:
			rule, index = t.query(tmp, r.p()[0])
			if rule.start:
				l.append(ET.SubElement(new_xml, rule.left))
				l[-1].text = 'test'
			for item in rule.right[index]:
				l.append(ET.SubElement(get_element(l, rule.left), item))
				l[-1].text = 'test'

			action = rule.show_rule(index)
			s.push(rule.right[index])
			
		line.append(action)
		step += 1
		output.append(line)

	# OUTPUT: parsing tree in xml format
	for i in l:
		print i.tag

	et = ET.ElementTree(new_xml)
	print et
	print et.getroot()
	tmp = ET.tostring(et.getroot())
	#root = etree.fromstring(tmp)
	#res = etree.tostring(root, pretty_print=True)
	print tmp
	# OUTPUT: parsing procedure in xls format
	workbook = xlwt.Workbook()
	sheet1 = workbook.add_sheet('sheet1',cell_overwrite_ok=True)
	for r in range(len(output)):
		for c in range(len(line)):
			sheet1.write(r,c,output[r][c])
	workbook.save('./a.xls')

if __name__ == "__main__":
	main()
