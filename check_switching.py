import os
from os import system

def diff_letters(a,b):
    return sum ( a[i] != b[i] for i in range(len(a)) )


nr_lines_file = 100000
nr_comparisons = nr_lines_file - 1

system("mkdir -p RESULT_SWITCHING")

for directory in os.listdir("OUTPUT_BINARY"):

	with open("RESULT_SWITCHING/"+directory+".csv", "w") as f_out:
		print >> f_out, "\t".join(["Size","Nr_Input","% switching"])

		for size in ["4","8","16","32"]:
			for name_file in [str(x)+".txt" for x in range(int(size))]:
				with open("OUTPUT_BINARY/"+directory+"/"+size+"/"+name_file,"r") as f_in:
					lines = f_in.readlines()
					split_old = lines[0].split()[0]
	
					diff = 0
					for line in lines[1:]:
						split = line.split()[0]
						#print [split_old,split,directory+"/"+name_file]
						diff += diff_letters(split_old, split)
						split_old = split

					diff /= float(nr_comparisons)
					print >> f_out, "%s\t%s\t%.5f%%" % (size, name_file.split(".")[0], diff*100.0/8.0)
