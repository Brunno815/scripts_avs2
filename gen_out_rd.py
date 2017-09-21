from os import system

exe = "lencod.exe"
cfg = "encoder_ldp.cfg"
videos = [["BasketballDrive_1920x1080_50","5","50","1920","1080"],["BQTerrace_1920x1080_60","5","60","1920","1080"],["Cactus_1920x1080_50","5","50","1920","1080"],["Jockey_3840x2160","5","120","3840","2160"],["ShakeNDry_3840x2160","5","120","3840","2160"],["HoneyBee_3840x2160","5","120","3840","2160"]]
#videos = [["Jockey_3840x2160","5","120","3840","2160"]]

#videos = [["BasketballDrive_1920x1080_50","5","50","1920","1080"]]

sizes_btrfly = ["0","4","8","16","32"]
alfs = ["0"]
qps = ["32"]

fps = {}
fps["24"] = "2"
fps["25"] = "3"
fps["30"] = "5"
fps["50"] = "6"
fps["60"] = "8"
fps["120"] = "9"

for video in videos:
	for size_btrfly in sizes_btrfly:
		for alf in alfs:
			for qp in qps:
				if (alf == "0" and size_btrfly == "0") or (alf == "1" and size_btrfly != "0"):
					continue
				name_video = video[0].split("_")[0]
				cmd = "./%s -f %s -p QPPFrame=%s -p InputFile= ~/origCfP/%s.yuv -p SizePrint=%s -p PrintALF=%s -p FramesToBeEncoded=%s -p SourceWidth=%s -p SourceHeight=%s -p ReconFile=enc_%s.yuv -p OutputFile=video_%s.avs -p FrameRate=%s" % (exe, cfg, qp, video[0], size_btrfly, alf, video[1], video[3], video[4], name_video, name_video, fps[video[2]])
				#print cmd
				system(cmd)
