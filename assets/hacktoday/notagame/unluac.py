#!/usr/bin/env python
import os
import argparse

from xxtea import decrypt, encrypt

parser = argparse.ArgumentParser(description='Decrypt/Encrypt XXTEA Block chiper recursively in a folder')
parser.add_argument("-d", "--dir", help="Input directory", required=True)
parser.add_argument("-k", "--key", help="Key for decryption", required=True)
parser.add_argument("-s", "--sign", help="File signature", required=True)
parser.add_argument("-o", "--out", help="Output directory")
parser.add_argument("-vv", "--verbose", help="Verbose output", action="store_true")
args = parser.parse_args()

curdir = args.dir

for file in os.listdir(curdir):
	curfile = curdir + '/' + file
	print('\n\n' + curfile + '\n\n')
	if not os.path.isdir(curfile):
		fp = open(curfile, 'rb')
		raw = fp.read()
		if raw[:len(args.sign)] == args.sign:
			print(decrypt(raw[len(args.sign):], args.key))
		else:
			print('Error!')