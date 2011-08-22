#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from Pd import *

def main(argv):
	""" main """
	pd = Pd()
	pd.init()

	# output
	output = output()

	pd.quit()

def output():
	output = {}
	output["dac"] = Object(10, 10, "dac~")
	output["mL"] = Object(30, 30, "r~ mL")
	output["mR"] = Object(30, 30, "r~ mR")
	output["mM"] = Object(30, 30, "r~ mM")

	mMscale = Object(30, 30, "*~")

	return output

if __name__ == '__main__':
	main(sys.argv)
