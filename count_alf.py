from os import system
import os

videos = [["BQTerrace_1920x1080_60","60","60","1920","1080"],["Cactus_1920x1080_50","50","50","1920","1080"],["BasketballDrive_1920x1080_50","50","50","1920","1080"]]

videos = [["BQTerrace_1920x1080_60","5","60","1920","1080"]]
videos = [["BlowingBubbles_416x240_50","5","50","416","240"]]

#RODAR PRA TODOS FULL-HD E 4 VIDEOS 4K
videos = [["BQTerrace_1920x1080_60","60","60","1920","1080"],["Cactus_1920x1080_50","50","50","1920","1080"],["BasketballDrive_1920x1080_50","50","50","1920","1080"],["HoneyBee_3840x2160","120","120","3840","2160"],["ShakeNDry_3840x2160","120","120","3840","2160"],["Jockey_3840x2160","120","120","3840","2160"]]
videos = [["Jockey_3840x2160","120","120","3840","2160"]]

qps = ["32"]

fps = {}
fps["24"] = "2"
fps["25"] = "3"
fps["30"] = "5"
fps["50"] = "6"
fps["60"] = "8"
fps["120"] = "9"

alf_common = ["ExtendPicBorder","checkFilterCoeffValue","check_filtering_unit_boundary_extension","copyALFparam","filterOneCompRegion","getLCUCtrCtx_Idx","reconstructCoefInfo","reconstructCoefficients","setFilterImage"]
alf_enc = ["ADD_AlfCorrData","ALFParamBitrateEstimate","ALFProcess","AllocateAlfCorrData","AllocateAlfPar","Copy_frame_for_ALF","QuantizeIntegerFilterPP","accumulateLCUCorrelations","add_A","add_b","allocateAlfAPS","calcAlfLCUDist","calcCorrOneCompRegionChma","calcCorrOneCompRegionLuma","calculateErrorAbs","calculateErrorCoeffProvided","copyOneAlfBlk","copyToImage","createAlfGlobalBuffers","decideAlfPictureParam","deriveBoundaryAvail","deriveFilterInfo","deriveLoopFilterBoundaryAvailibility","destroyAlfGlobalBuffers","estimateALFBitrateInPicHeader","estimateFilterDistortion","executePicLCUOnOffDecision","filterCoeffBitrateEstimate","filterOneCTB","findFilterCoeff","freeAlfAPS","freeAlfCorrData","freeAlfPar","getStatistics","getStatisticsOneLCU","getTemporalLayerNo","gnsBacksubstitution","gnsCholeskyDec","gnsSolveByChol","gnsTransposeBacksubstitution","mergeFiltersGreedy","mergeFrom","predictALFCoeff","reset_alfCorr","roundFiltCoeff","setCurAlfParam","storeAlfTemporalLayerInfo","svlcBitrateEsitmate","uvlcBitrateEstimate","xCalcSSD","xFastFiltDistEstimation","xFilterCoefQuickSort","xQuantFilterCoef","xcodeFiltCoeff","xfindBestCoeffCodMethod","xfindBestFilterVarPred"]
alf_dec = ["ALFProcess_dec","AllocateAlfPar","CreateAlfGlobalBuffer","Read_ALF_param","ReleaseAlfGlobalBuffer","allocateAlfAPS","deriveBoundaryAvail","deriveLoopFilterBoundaryAvailibility","filterOneCTB","freeAlfAPS","freeAlfPar"]
dct_common = ["partialButterfly16","partialButterfly32","partialButterfly4","partialButterfly8"]


enc_dec = "0" # "0" = encoder, "1" = decoder


if os.path.isdir("OUTPUT_GPROF_AVS2") == False:
	system("mkdir OUTPUT_GPROF_AVS2")

if os.path.isdir("RESULTS_GPROF_AVS2") == False:
	system("mkdir RESULTS_GPROF_AVS2")

for video in videos:
	for qp in qps:
		com_codec = ""
		com_gprof = ""

		if enc_dec == "0":
			com_codec = "./lencod_gprof.exe -f encoder_ldp.cfg -p QPPFrame=%s -p InputFile=\"/home/brunno/origCfP/%s.yuv\" -p FramesToBeEncoded=%s -p SourceWidth=%s -p SourceHeight=%s -p ReconFile=enc_%s.yuv -p OutputFile=video_%s.avs -p FrameRate=%s" % (qp,video[0],video[1],video[3],video[4],video[0],video[0],fps[video[2]])
			com_gprof = "gprof lencod_gprof.exe gmon.out > OUTPUT_GPROF_AVS2/out_enc_gprof_%s_%s.txt" % (video[0],qp)
		else:
			com_codec = "./ldecod_gprof.exe -f encoder_ldp.cfg -p QPPFrame=%s -p InputFile=\"/home/brunno/origCfP/%s.yuv\" -p FramesToBeEncoded=%s -p SourceWidth=%s -p SourceHeight=%s -p ReconFile=dec_%s.yuv -p OutputFile=video_%s.avs -p FrameRate=%s" % (qp,video[0],video[1],video[2],video[3],video[0],video[0],fps[video[2]])
			com_gprof = "gprof ldecod_gprof.exe gmon.out > OUTPUT_GPROF_AVS2/out_dec_gprof_%s_%s.txt" % (video[0],qp)
		
		print com_codec
		system(com_codec)
		print com_gprof
		system(com_gprof)

name_file = ""

with open("RESULTS_GPROF_AVS2/out_params.csv","w") as f_out:
	print >> f_out, "\t".join(["Video","frames","qp","calls_alf_com","calls_alf_enc","calls_alf_dec", "calls_alf_all", "% calls_alf_enc", "% calls_alf_dec", "% calls_alf_com", "% calls_alf_all", "calls_dct_com", "% calls_dct_com", "time_alf_com", "time_alf_enc", "time_alf_dec", "time_alf_all", "% time_alf_com", "% time_alf_enc", "% time_alf_dec", "% time_alf_all", "time_dct_com", "% time_dct_com"])

if enc_dec == "0":
	name_file = "out_enc_gprof_"
else:
	name_file = "out_dec_gprof_"


for video in videos:
	for qp in qps:
		with open("OUTPUT_GPROF_AVS2/%s%s_%s.txt" % (name_file,video[0],qp), "r") as f_gprof:
		
			time_alf = [0.0, 0.0, 0.0] #common, enc, dec
			time_dct = [0.0] #common
			calls_alf = [0,0,0] #common, enc, dec
			calls_dct = [0] #common
			total_time = 0.0
			total_calls = 0
			
			lines = f_gprof.readlines()
			for idx,line in enumerate(lines):
			
				if idx >= 2:
					previousLine = lines[idx-2]
				
				if "the percentage of the total" in line:
					total_time = float(previousLine.split()[1])
					#print total_time
					break
					
				splitLine = line.split()
				
				if len(splitLine) == 7 and splitLine[0] != "time":
					total_calls += float(splitLine[3])
					
					if splitLine[6] in alf_common:
						time_alf[0] += float(splitLine[2])
						calls_alf[0] += float(splitLine[3])
					
					if splitLine[6] in alf_enc:
						time_alf[1] += float(splitLine[2])
						calls_alf[1] += float(splitLine[3])
					
					if splitLine[6] in alf_dec:
						time_alf[2] += float(splitLine[2])
						calls_alf[2] += float(splitLine[3])
					
					if splitLine[6] in dct_common:
						time_dct[0] += float(splitLine[2])
						calls_dct[0] += float(splitLine[3])
						
			with open("RESULTS_GPROF_AVS2/out_params.csv","a") as f_out:
				out_result = video[0:2] + [qp] + calls_alf + [sum(calls_alf)] + [x/total_calls for x in calls_alf] + [sum(calls_alf)/total_calls] + calls_dct + [x/total_calls for x in calls_dct] + time_alf + [sum(time_alf)] + [x/total_time for x in time_alf] + [sum(time_alf)/total_time] + time_dct + [x/total_time for x in time_dct]
				print >> f_out, "\t".join([str(x) for x in out_result])
