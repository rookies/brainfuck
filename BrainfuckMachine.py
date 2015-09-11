#!/usr/bin/python3
import sys

class BrainfuckMachine(object):
	def init(self, code):
		## Find [ and ] commands:
		beg = 0
		wstart = []
		while True:
			f = code.find("[", beg)
			if f == -1:
				break
			else:
				beg = f+1
				wstart.append(f)
		beg = 0
		wend = []
		while True:
			f = code.find("]", beg)
			if f == -1:
				break
			else:
				beg = f+1
				wend.append(f)
		## Check if the number of both is the same:
		if len(wstart) != len(wend):
			raise ValueError("Invalid code, %d occurrences of [, but %d of ]." % (len(wstart), len(wend)))
		## Create pairs and register them:
		loops = []
		for i in range(len(wend)):
			if wstart[0] > wend[i]:
				raise ValueError
			j = 0
			while (len(wstart) > j+1) and (wstart[j+1] < wend[i]):
				j += 1
			loops.append((wstart[j], wend[i]))
			del wstart[j]
		## Valid code, set variables:
		self.dataptr = 0
		self.data = [0]
		self.code = code
		self.codeptr = 0
		self.loops = loops
		
	def run(self, verbose=False):
		while self.codeptr < len(self.code):
			try:
				self.cmd(self.code[self.codeptr])
			except NotImplementedError:
				if self.code[self.codeptr] == "[":
					if self.data[self.dataptr] == 0:
						## Jump to the matching ] ##
						for l in self.loops:
							if l[0] == self.codeptr:
								self.codeptr = l[1]
				elif self.code[self.codeptr] == "]":
					if self.data[self.dataptr] != 0:
						## Jump to the matching [ ##
						for l in self.loops:
							if l[1] == self.codeptr:
								self.codeptr = l[0]
			self.codeptr += 1
			if verbose:
				self.state()
		
	def state(self):
		print("cptr=%d, data=[" % self.codeptr, end="", file=sys.stderr)
		for i in range(len(self.data)):
			if i+1 == len(self.data):
				e = ""
			else:
				e = ","
			if i == self.dataptr:
				print("{%d}" % self.data[i], end=e, file=sys.stderr)
			else:
				print("%d" % self.data[i], end=e, file=sys.stderr)
		print("]", file=sys.stderr)
		
	def cmd(self, c):
		if c == ">":
			if self.dataptr+1 == len(self.data):
				self.data.append(0)
			self.dataptr += 1
		elif c == "<":
			if self.dataptr == 0:
				raise ValueError("dataptr is at zero, decreasing not allowed.")
			self.dataptr -= 1
		elif c == "+":
			self.data[self.dataptr] += 1
		elif c == "-":
			self.data[self.dataptr] -= 1
		elif c == ".":
			print(chr(self.data[self.dataptr]), end="")
		elif c == ",":
			self.data[self.dataptr] = ord(input())
		elif c == "[":
			raise NotImplementedError("Loops not implemented in cmd(), please use run().")
		elif c == "]":
			raise NotImplementedError("Loops not implemented in cmd(), please use run().")
		
	def __init__(self):
		self.init("")
		
	def __getitem__(self, key):
		return self.data[key]
		
	def __setitem__(self, key, value):
		self.data[key] = value

if __name__ == "__main__":
	m = BrainfuckMachine()
	## Example 1, Calculate 5^3:
	m.init("+++++[>+++++[>+++++<-]<-]")
	m.run(True)
	print(m[2])
	## Example 2:
	m.init(""" ++++++++[>++++++++<-]>[-<++>]<-----     schreibt die Zahl 123 in die erste Zelle
 #>[-]++++++++[>[-]<[->+<]>-]<<<<<<<<<    Löschen der nächsten Zellen
 #[->+<]>[>+<-<+>]>[>>>>>[->+<]>+<<<<<    der eigentliche Code
 #++++++++++<[->>+<-[>>>]>[[<+>-]>+>>]
 #<<<<<]>[-]>[-<<+>>]>[-<<+>>]<<]>>>>>
 #[<<<<+++++++[-<+++++++>]<-[<+>-]<.[-
 #]>>>>>>[-<+>]<-]<<<<<<<""")
	m.run(True)
