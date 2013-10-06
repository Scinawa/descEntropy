#!/usr/bin/python
# -*- coding: latin-1 -*-

import numpy
import datetime
import string
import random
from sets import Set
from random import choice
from string import lowercase

# a caso 10 char
#text="abaaabbbab"

# meno a caso 10 char
text="aaaaabbbbb"

#256 byte
#text="826fd4116bdd9d5b1904bae5d2f0be6d37d7f5c9a19c1a3ad4759cd7bd3f12cabe934225e95e1207a6acd6a736a066e8538fe601ab26ae3e00b2f201780242fb8320a00685927a29b0c19c054834aed0c033dd45696afd77845dba56d3820e40acfa11bfdf65baad60a465d30cf5149feb92b2a5129fb5b229d888f1f195f36f"

# 128 bit -> 16byte
#text="cccccccccccccccc"

#text="`	¡	.	®	ð	.	Ð	%	±	q	¤	ï	í	.	*	"

def timeMeasure(function_to_decorate):
	result=""
	def a_wrapper_accepting_arbitrary_arguments(*args, **kwargs):
		d1=datetime.datetime.now()
		result=function_to_decorate(*args, **kwargs)
		d2=datetime.datetime.now()
		print "- ", (d2-d1).seconds,"sec"
		return result
	return a_wrapper_accepting_arbitrary_arguments


def descEntropyRaw(text):
	entropy=0
	already=Set()
	for lenCurSub in xrange(1,len(text)): #numero delle sottostringhe di lunghezza diversa
		#print "\n\n\n------"
		#print "lenCurSub", lenCurSub
		possible=len(text)-lenCurSub+1. #numero di quante sottostringhe abbiamo per questa lunghezza
		for index in xrange(int(possible)):
			#print "\n"
			substr=text[0+index:index+lenCurSub]
			if substr in already:
				continue
			already.add(substr)
			#print "sottostringa", substr
			
			# vediamo quante volte occorre questa sottostringa
			hitCounter=0
			for i in xrange(int(possible)):
				evaluateMe=text[0+i:i+lenCurSub]
				if evaluateMe==substr:
					hitCounter=hitCounter+1

			pofx=numpy.divide(hitCounter,possible) #probability to have that substring in the text
			logValue=numpy.log2(pofx)   #log_2

			entropy=entropy+(pofx*logValue)

	return (-entropy,len(already))

def descEntropyNorm(text):
	tmp=descEntropyRaw(text)
	normalized=numpy.divide(tmp[0],numpy.log2(tmp[1]))	
	return normalized

def descEntropy(text):
	tmp=descEntropyRaw(text)
	#print text, tmp[0]  #utile per vedere con la funzione cento ogni stringa
	return tmp[0]

#print descEntropy(text)
#print descEntropyNorm(text)



# qua si potrebbe aggiunger altri caratteri al charset
calderone=[]
for x in range(10000):
	calderone.append("".join(choice(string.ascii_uppercase + string.digits) for i in range(17)))

@timeMeasure
def cento(calderone):
	for i in calderone:
		descEntropy(i)

cento(calderone)
