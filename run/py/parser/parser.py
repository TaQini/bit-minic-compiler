#!/usr/bin/python
# LL(1)
import xml.etree.cElementTree as ET 
__author__ = 'TaQini'
DEBUG = False
# production rule
class rule:
	def __init__(self, left, right, start):
		self.start = start
		self.left = left
		self.right = right
		self.first = set()
		# init FIRST
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
		# init FOLLOW
		self.follow = set()
		if self.start:
			self.follow.add('#')
	def set_start(self):
		self.start = True
	def init_follow(self, g): # create gram of follow
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

# grammar file -> grammar obj (include rules, Vn & Vt)
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
# create LL analysis table
class LL_table:
	def __init__(self, g):
		self.table = dict()
		for rule in g.rules:
			for P in rule.right:
				for X in P: # P -> X0X1...Xn
					if X in g.Vt:
						self.table[(rule.left,X)] = rule.show_rule(rule.right.index(P))
						break
					elif X in g.Vn:
						no_eps = True
						for a in g.get_rule(X).first:
							if a == 'epsilon':
								no_eps = False
							else:
								self.table[(rule.left,a)] = rule.show_rule(rule.right.index(P))
						if no_eps:
							break
				for X in P: # P -> X0X1...Xn
					if X in g.Vt:
						break
					elif X in g.Vn:
						if 'epsilon' not in g.get_rule(X).first:
							break # if eps not all Xi.first, then eps not in X0X1...Xn.first
					for b in rule.follow:
						self.table[(rule.left,b)] = rule.show_rule(rule.right.index(P))
	def show(self):
		for i in self.table.keys():
			print 'M('+i[0]+','+i[1]+') = '+self.table[i]
# Entry point
def main():
	# init input string
	r = read_XML('./a.token.xml')

	# init production rules, FIRST, FOLLOW
	g = read_grammar('./grammar')
	#for r in g.rules: r.show_first()
	#for r in g.rules: r.show_follow()
	t = LL_table(g)
	#t.show()

if __name__ == "__main__":
	main()
