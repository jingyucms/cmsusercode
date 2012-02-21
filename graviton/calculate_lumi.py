import os

def trigger_name(selected_mass_bin,run):
    for runmin,runmax,trigger in trigger_bins[selected_mass_bin]:
        if int(run)>=runmin and int(run)<=runmax:
            return trigger
    return "noTrigger"


if __name__=="__main__":
    data_dirs=[#"lumi_full_JSON",
               "lumi_vv9_JSON",
               #"Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON_v3",
               ]

    triggers=["HLT_HT450_v","HLT_HT500_v","HLT_HT550_v","HLT_HT600_v","HLT_HT650_v","HLT_HT700_v","HLT_FatJetMass850_DR1p1_Deta2p0_v",
              ]
    
    for dataset in data_dirs:
        # --correctionv2 not yet in
        command="lumiCalc2.py -c frontier://LumiProd/CMS_LUMI_PROD -i "+dataset+".txt -hltpath HLT_HT* -o "+dataset+"-HT.cvs recorded"
        print command
        os.system(command)
        command="lumiCalc2.py -c frontier://LumiProd/CMS_LUMI_PROD -i "+dataset+".txt -hltpath HLT_FatJetMass* -o "+dataset+"-FatJetMass.cvs recorded"
        print command
        os.system(command)

    lumi={}
    for trigger in triggers:
        for dataset in data_dirs:
	    if "HT" in trigger:
                f=file(dataset+"-HT.cvs")
	    else:
                f=file(dataset+"-FatJetMass.cvs")
            lines=f.readlines()
            for line in lines[1:]:
                try:
                    if trigger in line.split(',')[-3].replace('"','').split("(")[0]:
                        lumi[line.split(',')[0]+","+trigger]=float(line.split(',')[-1])
                        #print "",line.split(',')[0],trigger,float(line.split(',')[-1])/1000000.,"/pb"
                    lumi[line.split(',')[0]]=float(line.split(',')[-1])
                except:
                    print "No info for run:",line.split(',')[0]

    alllumi=0.0
    triggerlumi={}
    for trigger in triggers:
        triggerlumi[trigger]=0
    for run in range(160329,180296+1):
        runlumi=0
	runtrigger="noTrigger"
	for trigger in triggers:
            if not str(run)+","+trigger in lumi.keys():
                continue
	    if lumi[str(run)+","+trigger]>runlumi:
	        runlumi=lumi[str(run)+","+trigger]
		runtrigger=trigger
	if str(run) in lumi.keys() and lumi[str(run)]>0:
            print run, ",", runtrigger, ",", runlumi/1000000.,"/pb"
	    if runtrigger in triggers:
                triggerlumi[runtrigger]+=runlumi
        alllumi+=runlumi
    for trigger in triggers:
        print "",trigger,triggerlumi[trigger]/1000000.,"/pb"
    print "total",alllumi/1000000.,"/pb"
