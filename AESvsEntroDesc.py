#!/usr/bin/python
# -*- coding: latin-1 -*-


import numpy
import datetime
import string
import random
from sets import Set
from random import choice
from string import lowercase

from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from os import urandom
from Crypto.Hash import MD5
from operator import itemgetter

bigConteiner=[]
key="pippo"
iv=urandom(16)


def generateData():
	obj = Encryption(key,iv)
	for y in xrange(32,256):
	        print "Range:", y
	        for x in xrange(0,100):
	                #print random.randint(0,y)
	                stringa=''.join(chr(random.randint(32,y)) for z in xrange(0,16))
	                #stringa=open("/dev/urandom","rb").read(16) perfetto, ma usa tutto random
	                #print stringa, len(stringa)
			entroDesc1=descEntropy(stringa)
	                stringaAES=obj.encrypt(stringa)
			entroDesc2=descEntropy(stringaAES)
			#print stringa,entroDesc1,stringaAES,entroDesc2
			#print entroDesc1,entroDesc2
			bigConteiner.append((string,entroDesc1,stringaAES,entroDesc2))
			#fila.write(stringa)
	                #file.write(str(len(stringa)))
	                #file.write("\n")
	print "Finished computation. Sorting"
	return sorted(bigConteiner,key=itemgetter(1))


def writeCSV(data,filedest):
	csv = open(filedest, "w")
	i=0
	for line in data:
		csv.write(str(i)+","+str(line[1])+","+str(line[3])+";\n")
		i=i+1
	csv.close()

class Encryption():
    def __init__(self, key, iv):
   
	self.key=MD5.new(key).hexdigest()[:16]
	self.iv=iv

    def values(self, data):
        self.data = data
        self.mode = AES.MODE_CBC
        if not self.key:
            self.key = Cfg_Encrypt_Key
        #self.key = self.h.md5(self.key, True)

    def encrypt(self, data):
        self.values(data)
        return  AES.new(self.key, self.mode, self.iv).encrypt(self.data)

    def decrypt(self, data):
        self.values(data)
        return AES.new(self.key, self.mode, self.iv).decrypt(self.data)


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
	return tmp[0]




data=generateData()
writeCSV(data,"/root/entropy/graphME.csv")
