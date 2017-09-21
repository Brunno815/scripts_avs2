
def file_len(fname):
        i = 0
        with open(fname,"r") as f:
                for i,l in enumerate(f):
                        pass
        return i+1


sizes = ["4","8","16","32"]
#sizes = ["2"]
#models = ["org","cur"]
videos = ["BasketballDrive_1920x1080_50","BQTerrace_1920x1080_60","Cactus_1920x1080_50","HoneyBee_3840x2160","Jockey_3840x2160","ShakeNDry_3840x2160"]

for video in videos:
        for size in sizes:
	        for i in range(int(size)):
                	str_i = str(i)
                        n_lines = file_len("%s/%s.txt" % ("/".join(["OUTPUT_BINARY",video,size]), str_i))
                        if n_lines != 100000:
                        	print [video,size,str_i, n_lines]
