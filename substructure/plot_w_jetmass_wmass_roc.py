import os, sys
import array
from ROOT import * 
from os import path
import subprocess

#gROOT.Reset()
#gROOT.SetStyle("Plain")
#gROOT.ProcessLine('.L tdrstyle.C')
gROOT.SetBatch(True)
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetTitleOffset(1.3,"Y")
gStyle.SetPadLeftMargin(0.15)
gStyle.SetPadBottomMargin(0.15)
gStyle.SetPadTopMargin(0.08)
gStyle.SetPadRightMargin(0.08)
gStyle.SetMarkerSize(0.5)
gStyle.SetHistLineWidth(1)
#gStyle.SetStatFontSize(0.020)
gStyle.SetTitleSize(0.06, "XYZ")
gStyle.SetLabelSize(0.05, "XYZ")
gStyle.SetNdivisions(506, "XYZ")
gStyle.SetLegendBorderSize(0)

TGaxis.SetMaxDigits(3)

if path.exists('rootlogon.C'):
    gROOT.Macro('rootlogon.C')  # Run ROOT logon script

if __name__ == '__main__':

 #for runSet in [10,11,12,13,14,15,16,17]:
 for runSet in [10]:
  theory=3
 
  if runSet==10 or runSet==11:
   samples = [#"root://eoscms.cern.ch//eos/cms/store/cmst3/group/exovv/precision/QCD_HT1000to1500_tarball.tar.xz/ntupler/",
 	      #"root://eoscms.cern.ch//eos/cms/store/cmst3/group/exovv/precision/WJetsToQQ_HT-600toInf_tarball.tar.xz/ntupler/",
 	      #"root://eoscms.cern.ch//eos/cms/store/cmst3/group/exovv/precision/ZJetsToQQ_HT600toInf_gridpack.tar.gz/ntupler/",
 	      "../../trackObservables/processing/processed-output.dat-rth:Qd.root",
 	      "../../trackObservables/processing/processed-output.dat-rth:Wd.root",
	      #"../../trackObservables/processing/processed-pythia82-lhC_{1}3-qq-pt1-50k-2-rth.root",
 	      #"../../trackObservables/processing/processed-pythia82-lhC_{1}3-WW-pt1-50k-2-rth.root",
 	      ]
   ma="mmdt"
  if runSet==12 or runSet==13:
   samples = ["../../trackObservables/processing/processed-pythia82-lhC_{1}3-qq-pt1-50k-2-rth:p40:i.root",
 	      "../../trackObservables/processing/processed-pythia82-lhC_{1}3-WW-pt1-50k-2-rth:p40:i.root",
 	      ]
   ma="mmdt"
  if runSet==14 or runSet==15:
   samples = ["../../trackObservables/processing/processed-pythia82-lhC_{1}3-qq-pt1-50k-2-no.root",
 	      "../../trackObservables/processing/processed-pythia82-lhC_{1}3-WW-pt1-50k-2-no.root",
 	      ]
   ma="mmdt"
  
  if runSet==16:
   samples = ["../../trackObservables/processing/processed-pythia82-lhC_{1}3-qq-pt1-50k-2-rth:p40.root",
 	      "../../trackObservables/processing/processed-pythia82-lhC_{1}3-WW-pt1-50k-2-rth:p40.root",
 	      ]
   ma="prun"

  if runSet==17:
   samples = ["../../trackObservables/processing/processed-pythia82-lhC_{1}3-qq-pt1-50k-2-no.root",
 	      "../../trackObservables/processing/processed-pythia82-lhC_{1}3-WW-pt1-50k-2-no.root",
 	      ]
   ma="prun"
	   
  colors=[1,2,4,6,1,2,4,6,1,2,4,6,1,2,4,6,1,2,4,6]
  styles=[1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5]
  widths=[2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6]
  ndata=10000
  sets=[""]
 
  #selection = "weight*vertexWeight*((deta<1.3)&&(abs(Jet1eta)<1.0)&&(Jet1pt>500)&&(Jet1pt<7000)&&(Jet1MassDrop<0.3))"
  selection = "((abs(j_eta[0])<2.5)&&(j_pt[0]>400)&&(j_pt[0]<600))"
  if runSet==10 or runSet==12 or runSet==14:
    names = ["tau21_b1_aftermass",
 	   #"tau21_b2_aftermass",
 	   #"C_{1}_b0_aftermass",
 	   #"C_{1}_b1_aftermass",
 	   #"C_{1}_b2_aftermass",
 	   #"c2_b1_aftermass",
 	   #"c2_b2_aftermass",
 	   #"d2_b1_aftermass",
 	   #"d2_b2_aftermass",
 	   #"d2_a1_b1_aftermass",
 	   #"d2_a1_b2_aftermass",
 	   #"m2_b1_aftermass",
 	   #"m2_b2_aftermass",
 	   "n2_b1_aftermass",
 	   "n2_b1_rsd_aftermass",
 	   "n2_b2_aftermass",
	   "n2_b1_ddt_aftermass",
 	   "n2_b2_ddt_aftermass",
 	   ]
    plots = [("j_tau21_b1[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","#tau_{2}/#tau_{1} (#beta=1)", ),
 	   #("j_tau21_b2[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","#tau_{2}/#tau_{1} (#beta=2)", ),
 	   #("j_C_{1}_b0[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","C_{1} (#beta=0)", ),
 	   #("j_C_{1}_b1[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","C_{1}^{#beta=1}", ),
 	   #("j_C_{1}_b2[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","C_{1}^{#beta=2}", ),
 	   #("j_c2_b1[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","C_{2}^{#beta=1}", ),
 	   #("j_c2_b2[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","C_{2}^{#beta=2}", ),
 	   #("j_d2_b1[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","D_{2}^{#beta=1}", ),
 	   #("j_d2_b2[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","D_{2}^{#beta=2}", ),
 	   #("j_d2_a1_b1[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","D_{2} (#alpha=1,#beta=1)", ),
 	   #("j_d2_a1_b2[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","D_{2} (#alpha=1,#beta=2)", ),
 	   #("j_m2_b1[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","M_{2}^{#beta=1}", ),
 	   #("j_m2_b2[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","M_{2}^{#beta=2}", ),
 	   ("j_n2_b1[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","N_{2}^{#beta=1}", ),
 	   ("j_n2_b1[0]",selection+"&&(j_mass_rsd[0]>60)&&(j_mass_rsd[0]<110)","N_{2}^{#beta=1} (rSD)", ),
 	   ("j_n2_b2[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","N_{2}^{#beta=2}", ),
 	   ("ddt1(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","decorrelated N_{2}^{#beta=1} 1%", ),
 	   ("ddtb21(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","decorrelated N_{2}^{#beta=2} 1%", ),
 	   ]
  elif runSet==16 or runSet==17:
    names = ["tau21_b1_aftermass",
 	   ]
    plots = [("j_tau21_b1[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<100)","#tau_{2}/#tau_{1} (#beta=1)", ),
 	   ]
  else:
    names = ["tau21_b1_mmdt_aftermass",
 	   "tau21_b2_mmdt_aftermass",
 	   "C_{1}_b0_mmdt_aftermass",
 	   "C_{1}_b1_mmdt_aftermass",
 	   "C_{1}_b2_mmdt_aftermass",
 	   "c2_b1_mmdt_aftermass",
 	   "c2_b2_mmdt_aftermass",
 	   #"d2_b1_mmdt_aftermass",
 	   #"d2_b2_mmdt_aftermass",
 	   "d2_a1_b1_mmdt_aftermass",
 	   "d2_a1_b2_mmdt_aftermass",
 	   "m2_b1_mmdt_aftermass",
 	   "m2_b2_mmdt_aftermass",
 	   "n2_b1_mmdt_aftermass",
 	   "n2_b2_mmdt_aftermass",
 	   ]
    plots = [("j_tau21_b1_mmdt[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","#tau_{2}/#tau_{1} (#beta=1)", ),
 	   ("j_tau21_b2_mmdt[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","#tau_{2}/#tau_{1} (#beta=2)", ),
 	   ("j_C_{1}_b0_mmdt[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","C_{1} (#beta=0)", ),
 	   ("j_C_{1}_b1_mmdt[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","C_{1}^{#beta=1}", ),
 	   ("j_C_{1}_b2_mmdt[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","C_{1}^{#beta=2}", ),
 	   ("j_c2_b1_mmdt[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","C_{2}^{#beta=1}", ),
 	   ("j_c2_b2_mmdt[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","C_{2}^{#beta=2}", ),
 	   #("j_d2_b1_mmdt[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","D_{2}^{#beta=1}", ),
 	   #("j_d2_b2_mmdt[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","D_{2}^{#beta=2}", ),
 	   ("j_d2_a1_b1_mmdt[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","D_{2} (#alpha=1,#beta=1)", ),
 	   ("j_d2_a1_b2_mmdt[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","D_{2} (#alpha=1,#beta=2)", ),
 	   ("j_m2_b1_mmdt[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","M_{2}^{#beta=1}", ),
 	   ("j_m2_b2_mmdt[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","M_{2}^{#beta=2}", ),
 	   ("j_n2_b1_mmdt[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","N_{2}^{#beta=1}", ),
 	   ("j_n2_b2_mmdt[0]",selection+"&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)","N_{2}^{#beta=2}", ),
 	   ]
 
  results=[]
  event_count={}
  for plot in plots:
   if runSet>100:
     canvas = TCanvas("C_{1}","C_{1}",0,0,200,260)
     canvas.Divide(1,2,0,0,0)
     canvas.GetPad(1).SetPad(0.0,0.28,1.0,1.0)
     canvas.GetPad(1).SetLeftMargin(0.15)
     canvas.GetPad(1).SetRightMargin(0.08)
     canvas.GetPad(1).SetTopMargin(0.08)
     canvas.GetPad(1).SetBottomMargin(0.05)
     canvas.GetPad(2).SetPad(0.0,0.0,1.0,0.28)
     canvas.GetPad(2).SetLeftMargin(0.15)
     canvas.GetPad(2).SetRightMargin(0.08)
     canvas.GetPad(2).SetTopMargin(0.08)
     canvas.GetPad(2).SetBottomMargin(0.45)
     canvas.cd(1)
     canvas.GetPad(1).SetLogy(False)
   else:
     canvas = TCanvas("C_{1}","C_{1}",0,0,200,200)
     canvas.SetLogy(False)
   if runSet>100:
     legend=TLegend(0.55,0.7,0.85,0.9)
   else:
     legend=TLegend(0.55,0.6,0.85,0.9)
   dataPlotted=False
   counter=0
   integral=1
   originalIntegral={}
   maximum=0
   s=0
   hists=[]
   fs=[]
   ts=[]
   firsthist=None
   event_count[names[plots.index(plot)]]=[]
   for sample in samples:
    s+=1
    for gen in sets:
     print sample, gen
 
     if ".root" in sample:
       f=TFile.Open(sample)
       fs+=[f]
       tree=f.Get("t_allpar")
     else:
       tree=TChain("t_allpar")
       p=subprocess.Popen(["eos ls "+sample.replace("root://eoscms.cern.ch/","")],shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
       count=0
       for fn in p.stdout:
         if not ".root" in fn: continue
	 count+=1
	 tree.Add(sample+fn.replace("\n",""))
	 #if count>100: break ###
     ts+=[tree]
 
     signal = "Hpp" in sample or "Py6" in sample
     histname="plot"+names[plots.index(plot)]+gen+str(s)
     if plot[2]=="jet #eta":
 	hist=TH1F(histname,histname,25,-2.5,2.5);
 	hist.GetYaxis().SetRangeUser(0,50000)
     elif "jet p_{T}" in plot[2]:
 	hist=TH1F(histname,histname,40,300,700);
 	hist.GetYaxis().SetRangeUser(0.001,50000)
 	if runSet>100:
 	  canvas.GetPad(1).SetLogy(True)
 	else:
 	  canvas.SetLogy(True)
     elif "pruned jet mass" in plot[2]:
 	hist=TH1F(histname,histname,30,0,150);
 	hist.GetYaxis().SetRangeUser(0,50000)
 	if runSet==6:
 	  hist=TH1F(histname,histname,50,0,150);
 	  hist.GetYaxis().SetRangeUser(0,50000)
     elif "jet mass (GeV)" in plot[2]:
 	hist=TH1F(histname,histname,30,0,150);
 	hist.GetYaxis().SetRangeUser(0,50000)
     elif "#tau_{2}/#tau_{1}" in plot[2]:
 	hist=TH1F(histname,histname,20,0,1);
 	hist.GetYaxis().SetRangeUser(0,75000)
 	if "aftermass" in names[plots.index(plot)]:
 	    hist.GetYaxis().SetRangeUser(0,5000)
     elif "decorrelated" in plot[2]:
 	hist=TH1F(histname,histname,30,-0.5,0.5);
 	hist.GetYaxis().SetRangeUser(0,75000)
 	if "aftermass" in names[plots.index(plot)]:
 	    hist.GetYaxis().SetRangeUser(0,5000)
     elif "N_{2}^{#beta=2}" in plot[2]:
 	hist=TH1F(histname,histname,30,0,0.1);
 	hist.GetYaxis().SetRangeUser(0,75000)
 	if "aftermass" in names[plots.index(plot)]:
 	    hist.GetYaxis().SetRangeUser(0,5000)
     elif "C_{1}" in plot[2] or "C_{2}" in plot[2] or "D_{2} (#alpha=1,#beta=2)" in plot[2] or "M_{2}" in plot[2] or "N_{2}" in plot[2]:
 	hist=TH1F(histname,histname,30,0,0.5);
 	hist.GetYaxis().SetRangeUser(0,75000)
 	if "aftermass" in names[plots.index(plot)]:
 	    hist.GetYaxis().SetRangeUser(0,5000)
     elif "D_{2}" in plot[2]:
 	hist=TH1F(histname,histname,30,0,5);
 	hist.GetYaxis().SetRangeUser(0,75000)
 	if "aftermass" in names[plots.index(plot)]:
 	    hist.GetYaxis().SetRangeUser(0,5000)
     elif "#beta=" in plot[2]:
 	hist=TH1F(histname,histname,30,0,1);
 	hist.GetYaxis().SetRangeUser(0,75000)
 	if "aftermass" in names[plots.index(plot)]:
 	    hist.GetYaxis().SetRangeUser(0,5000)
 
     variable,cutstring=plot[0],plot[1]
     
     print histname,variable,cutstring
     tree.Project(histname,variable,cutstring)
     if "aftermass" in names[plots.index(plot)]:
       hist_before=hist.Clone(histname+"_before")
       tree.Project(histname+"_before",variable,cutstring.replace("&&(j_mass_"+ma+"[0]>60)&&(j_mass_"+ma+"[0]<110)",""))
       inte=[]
       for b in range(hist.GetNbinsX()):
         inte+=[hist.Integral(0,b+1)]
       event_count[names[plots.index(plot)]]+=[[hist_before.GetEntries(),hist.Integral(),inte]]
     if "QCD" in sample:
 	 originalIntegral[histname]=hist.Integral()
     hist.SetTitle("")
     hist.SetFillStyle(0)
     hist.SetMarkerStyle(20)
     #hist.SetMarkerSize(2)
     if runSet>100:
       hist.GetXaxis().SetTitle("")
       hist.GetXaxis().SetLabelColor(0)
       hist.GetYaxis().SetTitle("Events")
       if "pruned jet mass" in plot[2]:
 	   hist.GetYaxis().SetTitle("Events / (3 GeV)")
     else:
       hist.GetXaxis().SetTitle(plot[2])
       hist.GetYaxis().SetTitle("Normalized Distribution")
     if "Run" in sample:
 	 integral=hist.Integral()
     if hist.Integral()>0:
 	 hist.Scale(integral/hist.Integral())
 
     print "mean",hist.GetMean()

     hists+=[hist]
     print hists
 
     if "QCD1000" in sample:
 	 histname500="plot"+names[plots.index(plot)]+gen+str(s-1)
 	 for his in reversed(hists):
 	     if histname500==his.GetName():
 		 oldIntegral=his.Integral()
 		 if his.Integral()>0:
 		     his.Scale(originalIntegral[histname500]/his.Integral())
 		 if hist.Integral()>0:
 		     hist.Scale(originalIntegral[histname]/hist.Integral())
 		 weight=204.0/13798133*30522161/8426.0
 		 his.Add(hist,weight)
 		 if oldIntegral>0:
 		     his.Scale(oldIntegral/his.Integral())
 		 else:
 		     his.Scale(integral/his.Integral())
 		 hist=his
 		 break
     if "QCD500" in sample:
 	 continue
     
     if "QCDPythia8" in sample and not "170" in sample:
 	 samplenames=["170","300","470","600","800","1000","1400","1800"]
 	 samplenumbers=[800046,490042,500051,492988,400059,400050,200070,194313]
 	 samplecrossections=[37974.99,1938.868,124.8942,29.55049,3.871308,0.8031018,0.03637225,0.00197726]
 	 samplenumber=0
 	 for samplename in samplenames:
 	   if samplename in sample:
 	     samplenumber=samplenames.index(samplename)
 	 histnameFirst="plot"+names[plots.index(plot)]+gen+str(s-samplenumber)
 	 for his in reversed(hists):
 	     if histnameFirst==his.GetName():
 		 oldIntegral=his.Integral()
 		 if his.Integral()>0:
 		     his.Scale(originalIntegral[histnameFirst]/his.Integral())
 		 if hist.Integral()>0:
 		     hist.Scale(originalIntegral[histname]/hist.Integral())
 		 weight=samplecrossections[samplenumber]/samplenumbers[samplenumber]*samplenumbers[0]/samplecrossections[0]
 		 his.Add(hist,weight)
 		 if oldIntegral>0:
 		     originalIntegral[histnameFirst]=his.Integral()
 		     his.Scale(oldIntegral/his.Integral())
 		 elif his.Integral()>0:
 		     originalIntegral[histnameFirst]=his.Integral()
 		     his.Scale(integral/his.Integral())
 		 hist=his
 		 break
     if "QCDPythia8" in sample and not "1800" in sample:
 	 continue
 
     #if "WW" in sample:
     #    hist.Scale(1./30.)
     #    hist.Add(hists[2])
 
     hist.SetLineColor(colors[counter])
     hist.SetLineStyle(styles[counter])        
     hist.SetLineWidth(widths[counter])
     
     if counter==0:
       firsthist=hist
       hist.Draw("hist")
     else:
       hist.Draw("histsame")

     if hist.GetMaximum()>maximum and hist.GetMaximum()<hist.Integral():
 	 maximum=hist.GetMaximum()
 
     if "jet p_{T}" in plot[2]:
 	 firsthist.GetYaxis().SetRangeUser(100,maximum*20.0)
     else:
 	 firsthist.GetYaxis().SetRangeUser(0,maximum*1.3)
 
     if runSet>100:
       canvas.cd(2)
       ratio=hist.Clone(hist.GetName()+"clone")
       hists+=[ratio]
       ratio.Divide(hists[0],hist)
       for b in range(hist.GetNbinsX()):
 	 if hists[0].GetBinContent(b+1)>0:
 	   ratio.SetBinError(b+1,hists[0].GetBinError(b+1)/hists[0].GetBinContent(b+1))
       ratio.GetYaxis().SetTitle("Data / Sim")
       ratio.GetYaxis().SetTitleSize(0.13)
       ratio.GetYaxis().SetTitleOffset(0.5)
       ratio.SetMarkerSize(0.1)
       ratio.GetYaxis().SetLabelSize(0.14)
       ratio.GetYaxis().SetRangeUser(0.8,1.2)
       ratio.GetYaxis().SetNdivisions(503)
       ratio.GetXaxis().SetLabelColor(1)
       ratio.GetXaxis().SetTitle(plot[2])
       ratio.GetXaxis().SetTitleSize(0.16)
       ratio.GetXaxis().SetTitleOffset(0.8)
       ratio.GetXaxis().SetLabelSize(0.14)
       if counter==0:
 	 ratio.Draw("histe")
       else:
 	 ratio.Draw("histsame")
       #line=TLine(ratio.GetXaxis().GetBinLowEdge(1),1,ratio.GetXaxis().GetBinLowEdge(ratio.GetNbinsX()+1),1)
       #hists+=[line]
       #line.Draw("same")
       canvas.cd(1)
       firsthist.GetYaxis().SetTitleOffset(1.2)
 
     if "WW" in sample and "pt1-" in sample and ((samples.index(sample)==0) or runSet==3):
       entry="W (pT=1 TeV)"
     elif "qq" in sample and (samples.index(sample)==0 or runSet==3):
       entry="q (pT=1 TeV)"
     elif "ZZ" in sample:
       entry="Z (pT=500 GeV)"
     elif "QCD" in sample:
       entry="q/g (pT=500 GeV)"
     elif "Qd" in sample:
       entry="q/g"
     elif "Wd" in sample:
       entry="W"
     elif "WW" in sample and "pt5-" in sample and ((samples.index(sample)==0) or runSet==3):
       entry="W (pT=5 TeV)"
     elif "WW" in sample and "pt500-" in sample and ((samples.index(sample)==0) or runSet==3):
       entry="W (pT=0.5 TeV)"
     elif "-thpq" in sample:
       entry="Tpt,H,PU=11"
     elif "-thp" in sample:
       entry="Tpt,H,PU=1"
     elif "-sh" in sample:
       entry="Tdr,H"
     elif "-th" in sample:
       entry="Tpt,H"
     elif "-rh" in sample:
       entry="Teff,H"
     elif "-eh" in sample:
       entry="E,H"
     elif "-h" in sample:
       entry="H"
 
     if "mass" in plot[2]:
       maxbin=0
       maxcontent=0
       for b in range(hist.GetXaxis().GetNbins()):
 	 if hist.GetXaxis().GetBinCenter(b+1)>50 and hist.GetBinContent(b+1)>maxcontent:
 	   maxbin=b
 	   maxcontent=hist.GetBinContent(b+1)
       mean=hist.GetXaxis().GetBinCenter(maxbin)
       g1 = TF1("g1","gaus", mean-30.,mean+30.)
       hist.Fit(g1, "R0")
       if g1.GetParameter(1)>50 and g1.GetParameter(1)<120:
 	 hres = int(g1.GetParameter(2)/g1.GetParameter(1)*1000.)/10.
 	 entry+= " ("+str(hres)+"%)"

     legend.AddEntry(hist,entry,"l")
     counter+=1
 
   legend.SetTextSize(0.036)
   legend.SetFillStyle(0)
   legend.Draw("same")
 
   legend4=TLegend(0.23,0.84,0.5,0.9,"AK R=0.8")
   legend4.SetTextSize(0.036)
   legend4.SetFillStyle(0)
   legend4.Draw("same")
 
   #legend2=TLegend(0.17,0.8,0.5,0.85,"p_{T} > 500 GeV")
   #legend2.SetTextSize(0.03)
   #legend2.SetFillStyle(0)
   #legend2.Draw("same")
 
   #if runSet==11:
   #  legend2=TLegend(0.17,0.8,0.5,0.85,"1.4 < p_{T} < 1.6 TeV")
   #  legend2.SetTextSize(0.03)
   #  legend2.SetFillStyle(0)
   #  legend2.Draw("same")
 
   legend2a=TLegend(0.24,0.78,0.5,0.84,"|#eta|<2.5")
   legend2a.SetTextSize(0.036)
   legend2a.SetFillStyle(0)
   legend2a.Draw("same")
 
   #if runSet==2:
   #  banner = TLatex(0.27,0.93,"  CMS  	L = 19.6 fb^{-1} at #sqrt{s} = 8 TeV, dijets");
   #elif runSet==6 and theory:
   banner = TLatex(0.32,0.93,"Pythia8, #sqrt{s} = 13 TeV");
   #else:
   #  banner = TLatex(0.24,0.93,"CMS Simulation, #sqrt{s} = 8 TeV, dijets");
   banner.SetNDC()
   banner.SetTextSize(0.04)
   #banner.Draw();  
 
   if "aftermass" in names[plots.index(plot)]:
   #if False:
      #legend3=TLegend(0.17,0.7,0.5,0.75,"#tau_{2}/#tau_{1}<0.25")
      legend3=TLegend(0.17,0.72,0.5,0.78,"60 < "+ma+" jet mass < 110")
      legend3.SetTextSize(0.036)
      legend3.SetFillStyle(0)
      legend3.Draw("same")
 
   canvas.SaveAs("w_jet_wmass_"+names[plots.index(plot)]+"_"+str(runSet+100*theory)+".png")
   canvas.SaveAs("w_jet_wmass_"+names[plots.index(plot)]+"_"+str(runSet+100*theory)+".pdf")
   canvas.SaveAs("w_jet_wmass_"+names[plots.index(plot)]+"_"+str(runSet+100*theory)+".root")
   canvas.SaveAs("w_jet_wmass_"+names[plots.index(plot)]+"_"+str(runSet+100*theory)+".C")
   canvas.SaveAs("w_jet_wmass_"+names[plots.index(plot)]+"_"+str(runSet+100*theory)+".eps")

  canvas = TCanvas("","",0,0,200,200)
  canvas.SetLogy(False)
  mg = TMultiGraph()
  mg2 = TMultiGraph()
  legend=TLegend(0.2,0.2,0.7,0.6)

  for plot in plots:
   if "aftermass" in names[plots.index(plot)]:
    if "d2" in names[plots.index(plot)]:
      print names[plots.index(plot)],event_count[names[plots.index(plot)]]
    groc = TGraphErrors(1)
    groc.SetLineColor(colors[plots.index(plot)])
    groc.SetLineWidth(widths[plots.index(plot)])
    groc.SetLineStyle(styles[plots.index(plot)])
    if runSet==16:
       groc.SetLineStyle(1)        
       groc.SetLineWidth(4)
    if runSet==17:
       groc.SetLineStyle(2)        
       groc.SetLineWidth(4)
    for b in range(len(event_count[names[plots.index(plot)]][0][2])):
      groc.SetPoint(b, event_count[names[plots.index(plot)]][1][2][b]/event_count[names[plots.index(plot)]][1][0], 1.-event_count[names[plots.index(plot)]][0][2][b]/event_count[names[plots.index(plot)]][0][0])
    mg.Add(groc,"L")
    legend.AddEntry(groc,plot[2],"l")

    groc2 = TGraphErrors(1)
    groc2.SetLineColor(colors[plots.index(plot)])
    groc2.SetLineWidth(widths[plots.index(plot)])
    groc2.SetLineStyle(styles[plots.index(plot)])
    if runSet==16:
       groc.SetLineStyle(1)        
       groc.SetLineWidth(4)
    if runSet==17:
       groc.SetLineStyle(2)        
       groc.SetLineWidth(4)
    for b in range(len(event_count[names[plots.index(plot)]][0][2])):
      groc2.SetPoint(b, event_count[names[plots.index(plot)]][1][2][b]/event_count[names[plots.index(plot)]][1][1], 1.-event_count[names[plots.index(plot)]][0][2][b]/event_count[names[plots.index(plot)]][0][1])
    mg2.Add(groc2,"L")

  mg.SetTitle("")
  mg.Draw("AP")
  mg.GetXaxis().SetTitle("#epsilon_{sig}")
  mg.GetYaxis().SetTitle("1 - #epsilon_{bkg}")
  mg.GetXaxis().SetRangeUser(0,0.25)
  if runSet==16 or runSet==17:
    mg.GetYaxis().SetRangeUser(0.85,1)
  else:
    mg.GetYaxis().SetRangeUser(0.9,1)
 
  legend.SetTextSize(0.036)
  legend.SetFillStyle(0)
  legend.Draw("same")
 
  legend4=TLegend(0.73,0.84,0.9,0.9,"AK R=0.8")
  legend4.SetTextSize(0.036)
  legend4.SetFillStyle(0)
  legend4.Draw("same")
 
  legend2a=TLegend(0.73,0.78,0.9,0.84,"|#eta|<2.5")
  legend2a.SetTextSize(0.036)
  legend2a.SetFillStyle(0)
  legend2a.Draw("same")
 
  banner = TLatex(0.24,0.93,"Pythia8, #sqrt{s} = 13 TeV");
  banner.SetNDC()
  banner.SetTextSize(0.04)
  #banner.Draw();  

  canvas.SaveAs("w_jet_wmass_"+str(runSet+100*theory)+"_roc.png")
  canvas.SaveAs("w_jet_wmass_"+str(runSet+100*theory)+"_roc.pdf")
  canvas.SaveAs("w_jet_wmass_"+str(runSet+100*theory)+"_roc.root")
  canvas.SaveAs("w_jet_wmass_"+str(runSet+100*theory)+"_roc.C")
  canvas.SaveAs("w_jet_wmass_"+str(runSet+100*theory)+"_roc.eps")
 
  canvas = TCanvas("","",0,0,200,200)
  canvas.SetLogy(False)
  mg2.SetTitle("")
  mg2.Draw("AP")
  mg2.GetXaxis().SetTitle("#epsilon_{sig}")
  mg2.GetYaxis().SetTitle("1 - #epsilon_{bkg}")
  mg2.GetXaxis().SetRangeUser(0,0.5)
  mg2.GetYaxis().SetRangeUser(0.8,1)
  legend.Draw("same")
  legend4.Draw("same")
  legend2a.Draw("same")
  banner.Draw();  
 
  canvas.SaveAs("w_jet_wmass_"+str(runSet+100*theory)+"_roc2.png")
  canvas.SaveAs("w_jet_wmass_"+str(runSet+100*theory)+"_roc2.pdf")
  canvas.SaveAs("w_jet_wmass_"+str(runSet+100*theory)+"_roc2.root")
  canvas.SaveAs("w_jet_wmass_"+str(runSet+100*theory)+"_roc2.C")
  canvas.SaveAs("w_jet_wmass_"+str(runSet+100*theory)+"_roc2.eps")  
 
 
 
