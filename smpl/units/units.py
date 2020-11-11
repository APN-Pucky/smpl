#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 23:26:59 2019

@author: apn
"""
import math
def convert(x,u):
    return x/u
def to(u):
    return 1/u
# factors 
T = tera = 1e12
G = giga   = 1e9
M = mega   = 1e6
K = k = kilo   = 1e3
c = centi  = 1e-2
m = milli  = 1e-3
mu= micro  = 1e-6
n = nano   = 1e-9
p = pico   = 1e-12
f = fempto = 1e-15
a = atto = 1e-18
z = zepto = 1e-21
y = yocto = 1e-24

pi = math.pi

eV = 1
c = 1
kb = 1
hbar = 1

#fundamental
c0 = 299792458 # m/s
hbar0 = 4.135667662e-15/(2*pi)
kb0 = 8.617333262145e-5
# from wikipedia https://de.wikipedia.org/wiki/Nat%C3%BCrliche_Einheiten
joule = 1/(1.60218e-19)
meter = 1/hbar0/c0
s = second = 1/hbar0
gram = 1/kilo*(1/1.78266e-36) #*c0*c0
kelvin = 1*kb0

#composite
barn = 1e-28*meter**2
u = 1/(6.022141e26)*kilo*gram
Bq = 1/s
Ci = 37*giga *Bq
year = 31556952 *s# inclusive 

#print(convert(1*(y*meter)**2,z*barn))

#print(1e24*u *to(kilo*gram))
#print( (G*eV)**-2 * to(m*barn))
