#!/usr/bin/python2
#-*- coding: utf-8 -*-


# import block begins
import math
import random
# import block ends

# RSA
class RSA():
# class RSA begins

	# __init__()
	#
	# init parameters including p, q, n, totient, e in RSA
	#
	# @parameters: k is the desired bit length of p and q
	#
	# @return: none
	#
	def __init__(self, k):
		self.k = k
		self.p = 0
		self.q = 0
		self.n = 0
		self.totient = 0
		self.public_key = None
		self.e = 0
		self.private_key = 0
	
	
	# rabinMiller
	#
	# the implementation of Rabin Miller algorithm in python that is used to primality test
	#
	# @reference: https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
	#
	# @parameter: n, is the number that you want to test if it is prime number
	#
	# @return: boolean,  if it's prime number, the function will return true. otherwise, it will return false.
	#
	
	def rabinMiller(self, n):
		s = n - 1
		t = 0
		
		while s & 1 == 0:					# while s is odd
			s = s / 2
			t += 1
		
		
		k = 0								# init k as 0
		
		while k < 128:
			a = random.randrange(2,n-1)		# get random number from 2 to n-1
			#a^s is computationally infeasible.  we need a more intelligent approach
			#v = (a**s)%n
			#python's core math module can do modular exponentiation
			#v = pow(a, s, n) #where values are (num,exp,mod)
			
			v = self.modPow(a, s, n);		# v = (a ** s) % n
			
			if v != 1:
				i = 0
				while v != (n - 1):
					if i == t - 1:
						return False
					else:
						i = i + 1
						v = (v ** 2) % n
			k += 2
			
		return True
	
	#
	# isPrime
	#
	# the function test prime number
	#
	# @parameter: n, the number of that you want to test if it is prime
	#
	# @return: boolean, if the nubmer is prime number, it will return true. otherwise, it will return false.
	#
	def isPrime(self, n):
		
		# the list will store all of the prime number from 3 to 1000
		lowPrimes = [3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97
					,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179
					,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269
					,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367
					,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461
					,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571
					,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661
					,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773
					,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883
					,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997]
		
		# pre primality test to choose prime number
		if (n >= 3):															# if the number is greater than 3
			if (n & 1 != 0):													# if the number is odd
				for p in lowPrimes:												# iteracte whole of the array
					
					if (n == p):												# if n equals any element in the array, the function will return true
						return True
					
					if (n % p == 0):											# if n could be divded by any element in the array, that function will return false
						return False
						
				return self.rabinMiller(n)										# After pre-check, use rablin miller algorithm
		
		return False															# otherwise, return false
	
	
	#
	# gcd
	#
	# greatest common dividor
	#
	# @parameter:	a, 
	#				b, 
	#
	# @return: number, the greatest common dividor of a and b 
	#
	def gcd(self, a, b):
		
		c = a / b;
		d = a % b;

		if d == 0:
			return b

		else:
			return self.gcd(b, d)
	
	#
	# generateLargePrime
	#
	# generate large prime
	#
	# @parameter: none
	#
	# @return: number, 
	#
	def generateLargePrime(self):
		#k is the desired bit length
		r = 100 * (math.log(self.k, 2) + 1) #number of attempts max
		r_ = r
     
		while r > 0:
			#randrange is mersenne twister and is completely deterministic
			#unusable for serious crypto purposes
			n = random.randrange(2 ** (self.k - 1), 2 ** (self.k))
			r -= 1
			
			if self.isPrime(n) == True:
				return n
				
		return "Failure after "+`r_` + " tries."
	
	#
	# egcd
	#
	# extended great common divisor 
	# ax + by = gcd(a, b)
	# 
	#
	def egcd(self, a, b):
		
		if a == 0:
			return (b, 0, 1)
		
		else:
			g, y, x = self.egcd(b % a, a)
			return (g, x - (b // a) * y, y)
	
	#
	# modInverse
	#
	# Modular Inverse
	#
	#
	def modInverse(self, a, m):
		g, x, y = self.egcd(a, m)
		
		if g != 1:
			raise Exception('modular inverse does not exist')
		else:
			return x % m
	
	
	# modPow
	#
	#
	# modular pow
	# do (a ** b) %c much more fast
	# (m ** e) % n
	#
	# @parameter:
	#
	# @return: number, result of modular pow
	#
	def modPow(self, m, e, n):
		result = 1;

		while e > 0:
		
			if (e & 1) == 1:
				result = (result * m) % n;

			m = (m * m) % n
			e = e >> 1

		return result
	
	# generatePublicKey
	#
	# the function is used to generate the public key pairs
	#
	# @parameter: none
	#
	# @return: a list with public key pair
	#
	def generatePublicKey(self):
		self.p = self.generateLargePrime()						# generate a self.k bits prime number
		self.q = self.generateLargePrime()						# generate a self.k bits prime number
		
		print "P: ", self.p
		print "Q: ", self.q
		
		self.n = self.p * self.q

		self.totient = (self.p - 1) * (self.q -1)
		
		print "N: ", self.n
		
		print "Totient: ", self.totient
		
		self.e = random.randint(2, self.totient-1)

		while(self.gcd(self.totient, self.e) != 1):
			self.e = random.randint(2, self.totient - 1)

		print "E: ", self.e
		
		self.public_key = (self.n, self.e);

		print "Public Key: (%d, %d)" % self.public_key
		
		return self.public_key
	
	# generatePrivateKey
	#
	#
	# generate private key in RSA
	#
	# @parameter: none
	#
	# @return: the private key of RSA
	#
	def generatePrivateKey(self):
		self.d = self.modInverse(self.e, self.totient)

		print "D: ", self.d
		
		self.private_key = self.d
		
		print "Private Key: (%d)" % (self.private_key)
		
		return self.private_key
	
	# encrypt
	#
	# encrypt s with built-in public keys pair and private key
	#
	# @parameter: s, the string you want to encrypt
	#
	# @return: string, return the cipher text after encryption
	#
	def encrypt(self, s):
		cipher = list()
		
		for c in s:
			cipher.append(str(self.modPow(ord(c), self.e, self.n)))
		
		print cipher
		
		return '\n'.join(cipher)
	
	# decrypt
	#
	# decrypt the prividing cipher text to plain text
	#
	# @parameter: c, the cipher text that you want to decrypt
	#
	# @return: s, the plain text after decryption
	#
	def decrypt(self, c):
		s = ""
		cipher = c.split('\n')
		
		for m in cipher:
			if m.isdigit():
				s += chr(self.modPow(int(m), self.d, self.n))
				
				#print m
		
		return s
	
	# encryptWithPublicKey
	#
	# encrypt plain text with providing public key and private key
	#
	# @parameter:	s, the plain text that you want to encrypt
	#				e and n, the public key pairs
	#
	# @return: string, of cipher
	#
	def encryptWithPublicKey(self, s, e, n):
		cipher = list()
		
		for c in s:
			cipher.append(str(self.modPow(ord(c), e, n)))
		
		print cipher
		
		return '\n'.join(cipher)
	
	# decryptWithPrivateKey
	#
	# decrypt cipher with providing private key
	#
	# @parameter:	c, cipher
	#				d, d in RSA
	#				n, n in RSA
	#
	# @return: s, the plain text you want to decrypt
	#
	def decryptWithPrivateKey(self, c, d, n):
		s = ""
		cipher = c.split('\n')
		
		for m in cipher:
			if m.isdigit():
				s += chr(self.modPow(int(m), d, n))
				
				#print m
		
		return s
# RSA class ends

if __name__ == '__main__':
	rsa = RSA(128)									# set length of big prime number
	
	rsa.generatePublicKey()							# generate public key with k bits
	rsa.generatePrivateKey()
	
	s = raw_input('Enter Plain Text: ')				# input
	
	a = rsa.encrypt(s)								# encrypt
	print rsa.decrypt(a);							# decrypt
