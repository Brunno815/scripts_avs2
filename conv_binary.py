import os
from os import system

def num_to_bin(num, wordsize):
    if num < 0:
        num = 2**wordsize+num
    base = bin(num)[2:]
    padding_size = wordsize - len(base)
    return '0' * padding_size + base

sizes = ["4","8","16","32"]

system("mkdir -p OUTPUT_BINARY")

for directory in os.listdir("OUTPUT"):

	system("mkdir -p OUTPUT_BINARY/" + directory)
	
	for size in sizes:
		system("mkdir -p OUTPUT_BINARY/"+directory+"/"+size)

	for name_file in os.listdir("OUTPUT/"+directory):

		n_bits = 9
		param_file = name_file.split("_")

		with open("OUTPUT/"+directory+"/"+name_file, "r") as f_in, open("OUTPUT_BINARY/"+directory+"/"+param_file[0]+"/"+param_file[1]+".txt","w") as f_out:
			for line in f_in.readlines():
				split_line = line.split()
				bin_value = num_to_bin(int(split_line[0]), n_bits)
				print >> f_out, "%s" % (bin_value)
