import os
import subprocess

samples = [
#('/pythia8_qcd_m2500___May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_qcd_m3700___May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_ci_m2500_4000_1_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_ci_m3700_4000_1_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_ci_m2500_6000_1_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_ci_m3700_6000_1_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_ci_m2500_8000_1_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_ci_m3700_8000_1_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_ci_m2500_9000_1_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_ci_m3700_9000_1_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_ci_m2500_10000_1_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_ci_m3700_10000_1_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_ci_m2500_12000_1_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_ci_m3700_12000_1_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_ci_m2500_14000_1_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_ci_m3700_14000_1_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_ci_m2500_15000_1_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_ci_m3700_15000_1_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_ci_m2500_16000_1_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_ci_m3700_16000_1_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_ci_m2500_18000_1_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_ci_m3700_18000_1_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_ci_m2500_20000_1_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_ci_m3700_20000_1_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_add_m3700_2000_2_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_add_m3700_3000_2_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_add_m3700_4000_2_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_add_m3700_2000_6_0_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_add_m3700_2000_2_1_0_May27',True,True, 'cmsBatchFastsim'),
#('/pythia8_add_m3700_2000_2_0_1_May27',True,True, 'cmsBatchFastsim'),
('/pythia8_add_m2500_2000_2000_4_0_0_Aug19',True,True, 'cmsBatchFastsim'),
('/pythia8_add_m3700_2000_2000_4_0_0_Aug19',True,True, 'cmsBatchFastsim'),
('/pythia8_add_m2500_3000_3000_4_0_0_Aug19',True,True, 'cmsBatchFastsim'),
('/pythia8_add_m3700_3000_3000_4_0_0_Aug19',True,True, 'cmsBatchFastsim'),
('/pythia8_add_m2500_4000_4000_4_0_0_Aug19',True,True, 'cmsBatchFastsim'),
('/pythia8_add_m3700_4000_4000_4_0_0_Aug19',True,True, 'cmsBatchFastsim'),
('/pythia8_add_m2500_5000_5000_4_0_0_Aug19',True,True, 'cmsBatchFastsim'),
('/pythia8_add_m3700_5000_5000_4_0_0_Aug19',True,True, 'cmsBatchFastsim'),
('/pythia8_add_m2500_6000_6000_4_0_0_Aug19',True,True, 'cmsBatchFastsim'),
('/pythia8_add_m3700_6000_6000_4_0_0_Aug19',True,True, 'cmsBatchFastsim'),
('/pythia8_add_m2500_7000_7000_4_0_0_Aug19',True,True, 'cmsBatchFastsim'),
('/pythia8_add_m3700_7000_7000_4_0_0_Aug19',True,True, 'cmsBatchFastsim'),
('/pythia8_add_m2500_8000_8000_4_0_0_Aug19',True,True, 'cmsBatchFastsim'),
('/pythia8_add_m3700_8000_8000_4_0_0_Aug19',True,True, 'cmsBatchFastsim'),
('/pythia8_add_m2500_4000_0_0_0_1_Aug19',True,True, 'cmsBatchFastsim'),
('/pythia8_add_m3700_4000_0_0_0_1_Aug19',True,True, 'cmsBatchFastsim'),
('/pythia8_add_m2500_5000_0_0_0_1_Aug19',True,True, 'cmsBatchFastsim'),
('/pythia8_add_m3700_5000_0_0_0_1_Aug19',True,True, 'cmsBatchFastsim'),
('/pythia8_add_m2500_6000_0_0_0_1_Aug19',True,True, 'cmsBatchFastsim'),
('/pythia8_add_m3700_6000_0_0_0_1_Aug19',True,True, 'cmsBatchFastsim'),
('/pythia8_add_m2500_7000_0_0_0_1_Aug19',True,True, 'cmsBatchFastsim'),
('/pythia8_add_m3700_7000_0_0_0_1_Aug19',True,True, 'cmsBatchFastsim'),
('/pythia8_add_m2500_8000_0_0_0_1_Aug19',True,True, 'cmsBatchFastsim'),
('/pythia8_add_m3700_8000_0_0_0_1_Aug19',True,True, 'cmsBatchFastsim'),
]

for sample, mc, fastsim, production in samples:
    print sample, "mc", mc, "fastsim", fastsim
    #if mc:
    #	shortsample=sample.strip("/").split("/")[0]+"_grid"
    #else:
    shortsample="_".join(sample.strip("/").split("/"))+"_grid"
    filelist=open("fileList_"+shortsample+".txt","w")
    if production=="ProductionTask":
      command="cmsLs -l /store/cmst3/user/hinzmann/CMG"+sample+"""/ | awk '{size+=$2}END{print size/1024/1024/1024" GB"}'"""
      os.system(command)
      command="cmsLs -l /store/cmst3/user/hinzmann/CMG"+sample
    elif production=="cmsBatch":
      command="cmsLs -l /store/cmst3/user/hinzmann/NTUPLE"+sample+""+"""/ | awk '{size+=$2}END{print size/1024/1024/1024" GB"}'"""
      os.system(command)
      command="cmsLs -l /store/cmst3/user/hinzmann/NTUPLE"+sample+""
    elif production=="cmsBatchFastsim":
      command="cmsLs -l /store/cmst3/user/hinzmann/fastsim"+sample+""+"""/ | awk '{size+=$2}END{print size/1024/1024/1024" GB"}'"""
      os.system(command)
      command="cmsLs -l /store/cmst3/user/hinzmann/fastsim"+sample+""
    else:
      command="cmsLs -l /store/cmst3/user/hinzmann/NTUPLE/"+shortsample+"""/ | awk '{size+=$2}END{print size/1024/1024/1024" GB"}'"""
      os.system(command)
      command="cmsLs -l /store/cmst3/user/hinzmann/NTUPLE/"+shortsample
    print command
    p=subprocess.Popen([command],shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    files=p.stdout
    filesl=[]
    for line in files:
      if ".root" in line:
        filename=line.split(" ")[-1].strip()
        if filename.endswith(".root"):
	  sample_id="_".join(filename.split("/")[-1].strip(".root").split("_")[0:2])
	  print 'edmFileUtil',"root://eoscms//eos/cms"+filename
	  fileOk=True
          stdout = subprocess.Popen(['edmFileUtil',"root://eoscms//eos/cms"+filename], stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0]
          for error in ["Fatal Root Error","Could not open file","Tree Events appears to be missing. Not a valid collection"]:
              if error in stdout:
	          print stdout
	          fileOk=False
	  if not fileOk:
	      continue
	  found=False
	  if not "Fastsim" in production:
	   for f in filesl:
	    if sample_id+"." in f or sample_id+"_" in f:
	      filesl[filesl.index(f)]=filename
	      found=True
	  if not found:
	    filesl+=[filename]
    print "files:",len(filesl)
    for filename in filesl:
        filelist.write("root://eoscms//eos/cms"+filename+"\n")
    filelist.close()

    #os.system("heavy_tagged_dijet_analysis fileList_"+shortsample+".txt "+shortsample+".root &> "+shortsample+".log &")

    continue
    # make local copy
    filelist=open("fileList_"+shortsample+"_local.txt","w")
    command="mkdir /tmp/hinzmann/"+shortsample
    print command
    os.system(command)
    for filename in filesl:
      command="cmsStage "+filename+" /tmp/hinzmann/"+shortsample
      print command
      os.system(command)
    for filename in filesl:
        filelist.write("/tmp/hinzmann/"+shortsample+"/"+filename.split("/")[-1]+"\n")
    filelist.close()
