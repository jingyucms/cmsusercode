import os

if __name__ == '__main__':

    samples=[
#             ("QCD",[("fileList_pythia8_qcd_m2500___May27_grid.txt",[(3000,3600),(3600,4200)]),
#		     ("fileList_pythia8_qcd_m3700___May27_grid.txt",[(4200,8000)])]),
#             ("QCDCI4000",[("fileList_pythia8_ci_m2500_4000_1_0_0_May27_grid.txt",[(3600,4200)]),
#		        ("fileList_pythia8_ci_m3700_4000_1_0_0_May27_grid.txt",[(4200,8000)])]),
#             ("QCDCI6000",[("fileList_pythia8_ci_m2500_6000_1_0_0_May27_grid.txt",[(3600,4200)]),
#		        ("fileList_pythia8_ci_m3700_6000_1_0_0_May27_grid.txt",[(4200,8000)])]),
#             ("QCDCI8000",[("fileList_pythia8_ci_m2500_8000_1_0_0_May27_grid.txt",[(3600,4200)]),
#		        ("fileList_pythia8_ci_m3700_8000_1_0_0_May27_grid.txt",[(4200,8000)])]),
#             ("QCDCI9000",[("fileList_pythia8_ci_m2500_9000_1_0_0_May27_grid.txt",[(3600,4200)]),
#		        ("fileList_pythia8_ci_m3700_9000_1_0_0_May27_grid.txt",[(4200,8000)])]),
#             ("QCDCI10000",[("fileList_pythia8_ci_m2500_10000_1_0_0_May27_grid.txt",[(3600,4200)]),
#		        ("fileList_pythia8_ci_m3700_10000_1_0_0_May27_grid.txt",[(4200,8000)])]),
#             ("QCDCI12000",[("fileList_pythia8_ci_m2500_12000_1_0_0_May27_grid.txt",[(3600,4200)]),
#		        ("fileList_pythia8_ci_m3700_12000_1_0_0_May27_grid.txt",[(4200,8000)])]),
#             ("QCDCI14000",[("fileList_pythia8_ci_m2500_14000_1_0_0_May27_grid.txt",[(3600,4200)]),
#		        ("fileList_pythia8_ci_m3700_14000_1_0_0_May27_grid.txt",[(4200,8000)])]),
#             ("QCDCI15000",[("fileList_pythia8_ci_m2500_15000_1_0_0_May27_grid.txt",[(3600,4200)]),
#		        ("fileList_pythia8_ci_m3700_15000_1_0_0_May27_grid.txt",[(4200,8000)])]),
#             ("QCDCI16000",[("fileList_pythia8_ci_m2500_16000_1_0_0_May27_grid.txt",[(3600,4200)]),
#		        ("fileList_pythia8_ci_m3700_16000_1_0_0_May27_grid.txt",[(4200,8000)])]),
#             ("QCDCI18000",[("fileList_pythia8_ci_m2500_18000_1_0_0_May27_grid.txt",[(3600,4200)]),
#		        ("fileList_pythia8_ci_m3700_18000_1_0_0_May27_grid.txt",[(4200,8000)])]),
#             ("QCDCI20000",[("fileList_pythia8_ci_m2500_20000_1_0_0_May27_grid.txt",[(3600,4200)]),
#		        ("fileList_pythia8_ci_m3700_20000_1_0_0_May27_grid.txt",[(4200,8000)])]),

             ("QCDCIminusLL6000",[("fileList_pythia8_ci_m2500_6000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_6000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL8000",[("fileList_pythia8_ci_m2500_8000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_8000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL9000",[("fileList_pythia8_ci_m2500_9000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_9000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL10000",[("fileList_pythia8_ci_m2500_10000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_10000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL12000",[("fileList_pythia8_ci_m2500_12000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_12000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL14000",[("fileList_pythia8_ci_m2500_14000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_14000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL15000",[("fileList_pythia8_ci_m2500_15000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_15000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL16000",[("fileList_pythia8_ci_m2500_16000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_16000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL18000",[("fileList_pythia8_ci_m2500_18000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_18000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL20000",[("fileList_pythia8_ci_m2500_20000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_20000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),

#             ("QCDADD_4_0_0_4000",[("fileList_pythia8_add_m2500_4000_4000_4_0_0_Aug19_grid.txt",[(3600,4200)]),
#		        ("fileList_pythia8_add_m3700_4000_4000_4_0_0_Aug19_grid.txt",[(4200,8000)])]),
#             ("QCDADD_4_0_0_5000",[("fileList_pythia8_add_m2500_5000_5000_4_0_0_Aug19_grid.txt",[(3600,4200)]),
#		        ("fileList_pythia8_add_m3700_5000_5000_4_0_0_Aug19_grid.txt",[(4200,8000)])]),
#             ("QCDADD_4_0_0_6000",[("fileList_pythia8_add_m2500_6000_6000_4_0_0_Aug19_grid.txt",[(3600,4200)]),
#		        ("fileList_pythia8_add_m3700_6000_6000_4_0_0_Aug19_grid.txt",[(4200,8000)])]),
#             ("QCDADD_4_0_0_7000",[("fileList_pythia8_add_m2500_7000_7000_4_0_0_Aug19_grid.txt",[(3600,4200)]),
#		        ("fileList_pythia8_add_m3700_7000_7000_4_0_0_Aug19_grid.txt",[(4200,8000)])]),
#             ("QCDADD_4_0_0_8000",[("fileList_pythia8_add_m2500_8000_8000_4_0_0_Aug19_grid.txt",[(3600,4200)]),
#		        ("fileList_pythia8_add_m3700_8000_8000_4_0_0_Aug19_grid.txt",[(4200,8000)])]),

#             ("QCDADD_4_0_1_4000",[("fileList_pythia8_add_m2500_4000_0_0_0_1_Aug19_grid.txt",[(3600,4200)]),
#		        ("fileList_pythia8_add_m3700_4000_0_0_0_1_Aug19_grid.txt",[(4200,8000)])]),
#             ("QCDADD_4_0_1_5000",[("fileList_pythia8_add_m2500_5000_0_0_0_1_Aug19_grid.txt",[(3600,4200)]),
#		        ("fileList_pythia8_add_m3700_5000_0_0_0_1_Aug19_grid.txt",[(4200,8000)])]),
#             ("QCDADD_4_0_1_6000",[("fileList_pythia8_add_m2500_6000_0_0_0_1_Aug19_grid.txt",[(3600,4200)]),
#		        ("fileList_pythia8_add_m3700_6000_0_0_0_1_Aug19_grid.txt",[(4200,8000)])]),
#             ("QCDADD_4_0_1_7000",[("fileList_pythia8_add_m2500_7000_0_0_0_1_Aug19_grid.txt",[(3600,4200)]),
#		        ("fileList_pythia8_add_m3700_7000_0_0_0_1_Aug19_grid.txt",[(4200,8000)])]),
#             ("QCDADD_4_0_1_8000",[("fileList_pythia8_add_m2500_8000_0_0_0_1_Aug19_grid.txt",[(3600,4200)]),
#		        ("fileList_pythia8_add_m3700_8000_0_0_0_1_Aug19_grid.txt",[(4200,8000)])]),
#             ("QCDADD_4_0_1_9000",[("fileList_pythia8_add_m2500_9000_0_0_0_1_Aug19_grid.txt",[(3600,4200)]),
#		        ("fileList_pythia8_add_m3700_9000_0_0_0_1_Aug19_grid.txt",[(4200,8000)])]),
#             ("QCDADD_4_0_1_10000",[("fileList_pythia8_add_m2500_10000_0_0_0_1_Aug19_grid.txt",[(3600,4200)]),
#		        ("fileList_pythia8_add_m3700_10000_0_0_0_1_Aug19_grid.txt",[(4200,8000)])]),
             ]

    crosssections=[]
    for i in range(len(samples)):
      for j in range(len(samples[i][1])):
       for k in range(200):
         d=samples[i][1][j][0].replace("_grid.txt","_jobs/Job_"+str(k)+"/").replace("fileList_","")
	 try:
	   files=os.listdir(d)
	 except:
	   continue
	 for f in files:
	  if "LSFJOB" in f:
	    d+=f+"/STDOUT"
         print "logfile",d
         break
       try:
         f=file(d)
       except:
         print "no cross section found for ",d
	 continue
       for l in f.readlines():
	    if "| sum" in l:
                crosssections+=[(samples[i][0],samples[i][1][j][1],l.strip().split(" ")[-4],l.strip().split(" ")[-2])]
		break

print crosssections
fout=file("xsecs2.txt","w")
fout.write(str(crosssections))
fout.close()
