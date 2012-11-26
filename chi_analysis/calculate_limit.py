import os
from ROOT import *
import array

#massbins=[(4000,8000),
#	      (3000,4000),
#	      #(2400,3000),
#	      #(1900,2400),
#              ]
massbins=[(4200,8000),
	      (3600,4200),
	      (3000,3600),
	      (2400,3000),
	      #(1900,2400),
              ]

signalMasses=[4000,6000,8000,10000,12000,14000,16000,18000,20000]

prefix="datacard_3600"

binning=array.array('d')
for signalMass in signalMasses:
    binning.append(signalMass-1000)
binning.append(signalMass+1000)

canvas = TCanvas("","",0,0,600,400)
hists=[]
for b in range(6):
   hists+=[TH1F("limits"+str(b),';#Lambda;limit',len(binning)-1,binning)]

for signalMass in signalMasses:
    cfg=open("chi_datacard.txt","w")
    cfg.writelines("""
imax """+str(len(massbins))+""" number of channels
jmax 1 number of backgrounds
kmax 2 number of nuisance parameters
-----------
""")
    for i in range(len(massbins)):
        cfg.writelines("""shapes * bin"""+str(i)+""" """+prefix+"""_$PROCESS_chi.root $PROCESS#chi"""+str(massbins[i][0])+"""_"""+str(massbins[i][1])+"""_rebin1 $PROCESS#chi"""+str(massbins[i][0])+"""_"""+str(massbins[i][1])+"""_rebin1_$SYSTEMATIC
""")
    cfg.writelines("""-----------
""")
    text="bin "
    for i in range(len(massbins)):
       text+=str(i)+" "
    text+="\nobservation "
    fQCD=TFile(prefix+"_QCD_chi.root")
    for i in range(len(massbins)):
       hData=fQCD.Get("data_obs#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1")
       text+=str(hData.Integral())+" "
    cfg.writelines(text+"""
-----------
""")
    text="bin "
    for i in range(len(massbins)):
       text+=str(i)+" "+str(i)+" "
    text+="\nprocess "
    for i in range(len(massbins)):
       text+="CI"+str(signalMass)+" QCD "
    text+="\nprocess "
    for i in range(len(massbins)):
       text+="0 1 "
    text+="\nrate "
    f=TFile(prefix+"_CI"+str(signalMass)+"_chi.root")
    for i in range(len(massbins)):
       hQCD=fQCD.Get("QCD#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1")
       h=f.Get("CI"+str(signalMass)+"#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1")
       print "CI"+str(signalMass)+"#chi"+str(massbins[i][0])+"_"+str(massbins[i][1])+"_rebin1",h.Integral()
       text+=str(h.Integral())+" "+str(hQCD.Integral())+" "
    cfg.writelines(text+"""
-----------
""")
    #text="normqcd lnN "
    #for i in range(len(massbins)):
    #   text+="- 100.0 "
    text="\nnormjes lnN "
    for i in range(len(massbins)):
       text+="1.1 - "
    text+="\njes shape "
    for i in range(len(massbins)):
       text+="1.0 1.0 "
    cfg.writelines(text+"""
-----------
""")

    cfg.close()
    os.system("combine -M Asymptotic chi_datacard.txt | grep ': r <' > limits.txt")
    #os.system("combine -M ProfileLikelihood chi_datacard.txt -t 20 | grep ': r <' > limits.txt")
    #os.system("combine -M BayesianToyMC chi_datacard.txt -t 20 | grep ': r <' > limits.txt")
    #os.system("combine -M HybridNew --rule CLs --testStat LEP chi_datacard.txt | grep ': r <' > limits.txt")

    f=file("limits.txt")
    
    limits=[]
    for line in f.readlines():
        if "@" in line:
	   if "median" in line:
               limits+=[float(line.split("<")[-1].split("@")[0].strip())]
	else:
           limits+=[float(line.split("<")[-1].split("+")[0].strip())]

    if len(limits)==0:
       limits=[0]
    print limits
    for b in range(len(limits)):
        hists[b].SetBinContent(hists[b].FindBin(signalMass),limits[b])

hists[0].Draw("l")
hists[0].GetYaxis().SetRangeUser(0,2)
for b in range(1,len(limits)):
    hists[b].SetLineColor(b+1)
    hists[b].Draw("lsame")
line=TLine(signalMasses[0]-1000,1,signalMasses[-1]+1000,1)
line.SetLineColor(1)
line.Draw()

limitss=[]
for b in range(len(limits)):
  limitss+=[[0]]
  for i in range(len(signalMasses)):
    bin=hists[b].FindBin(signalMasses[i])
    if hists[b].GetBinContent(bin)>1.0:
        weightA=1.0/hists[b].GetBinContent(bin)
        weightB=hists[b].GetBinContent(bin-1)/1.0
        limitss[-1]=[weightA/(weightA+weightB)*signalMasses[i]+weightB/(weightA+weightB)*signalMasses[i-1]]
        break
print limitss
    
canvas.SaveAs('limits.pdf')
