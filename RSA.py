#!/usr/bin/python2
#-*- coding: utf-8 -*-

import random
import math

def generateBigRandomNumber():
	num = 0
	r = 2

	for i in range(r - 1):
		num += random.randint(0, 9) * (10 ** i)

	num += random.randint(1, 9) * (10 ** (r - 1));

	return num

def isPrime(num):
	i = 2;

	while(i <= math.sqrt(num)):
		
		if(num % i == 0):
			return False

		i += 1

	return True

def generatePrimeBigRandomNumber():
	num = generateBigRandomNumber();

	while not isPrime(num):
		num = generateBigRandomNumber();

	return num;

def gcd(a, b):
    c = a / b;
    d = a % b;

    if d == 0:
        return b

    else:
        return gcd(b, d)

def modInverse(n, p):
	n = n % p

	i = 1;

	while (i < p):
		if((n * i) % p == 1):
			return i

		i += 1

	return 0

if __name__ == '__main__':
	#print generateBigRandomNumber()

	#print isPrime(generateBigRandomNumber())

	#print generatePrimeBigRandomNumber()

	p = generatePrimeBigRandomNumber()
	q = generatePrimeBigRandomNumber()

	print "P: ", p
	print "Q: ", q

	n = p * q;

	totient = (p - 1) * (q -1)

	print "N: ", n
	print "Totient: ", totient

	e = random.randint(2, totient-1)

	while(gcd(totient, e) != 1):
		e = random.randint(2, totient-1)

	print "E: ", e

	print "Public Key: (%d, %d)" % (n, e)

	d = modInverse(e, totient)

	print "D: ", d

	print "Private Key: (%d)" % (d)

	m = input("Enter a number: ")

	print "Plain Text: ", m

	c = int(m ** e) % n

	print "Encryption: ", c

	m = int(c ** d) % n

	print "Descryption: ", m
