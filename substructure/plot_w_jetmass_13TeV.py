import os, sys
import array
from ROOT import * 
from os import path

#gROOT.Reset()
#gROOT.SetStyle("Plain")
gROOT.ProcessLine('.L tdrstyle.C')
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

if __name__ == '__main__':

 samples=[("data",[("JetHT_25ns_data6.txt",1.)]),
 	  #("QCD",[("QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6.txt",1.)])
 	  ("QCD",[("QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8.txt",0.000165),
 	  ("QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8.txt",0.006830),
 	  ("QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8.txt",0.114943),
 	  ("QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8.txt",0.842650),
 	  ("QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8.txt",9.4183),
 	  ("QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8.txt",32.293),
 	  ("QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8.txt",186.9),
 	  ("QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8.txt",648.2),
 	  ("QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8.txt",7823.0)],)
 	   ]
 colors=[1,2,4,6,1]
 styles=[1,1,2,3,1]
 widths=[2,2,2,2,2]

 plots = [("jetAK8_pruned_massCorr","AK8 pruned jet mass (GeV)"),
           ("jetAK8_softdrop_massCorr","AK8 softdrop jet mass (GeV)"),
           ("jetAK10_trimmed_massCorr","AK10 trimmed jet mass (GeV)", ),
           ]
 cuts= [0.1,0.2,0.3,0.4,0.45,0.5,0.6,0.7,0.75,1.0]

 histlist={}
 for plot in plots:
  for cut in cuts:
   for sample,files in samples:
    histname="plot"+plot[0]+str(cut)+sample
    if "jet mass" in plot[1]:
       histlist[plot[0]+str(cut)+sample]=TH1F(histname,histname,20,40,140);
       histlist[plot[0]+str(cut)+sample].GetYaxis().SetRangeUser(0,50000)

 fs={}
 ts=[]
 for sample,files in samples:
    for filename,weight in files:
      if filename.endswith(".txt"):
        files2=[]
        filelist=open(filename)
	for line in filelist.readlines():
	    if ".root" in line:
	        files2+=[(line.strip(),weight)]
      else:
        files2=[(filename,weight)]
	
    for filename,weight in files2:
     print filename,weight
     if filename in fs.keys():
       f=fs[filename]
     else:
       f=TFile.Open(filename)
     fs[filename]=f
     tree=f.Get("ntuplizer/tree")
     ts+=[tree]
     print tree.GetEntries()
  
     event_count=0
     for event in tree:
      event_count+=1
      #if event_count>10000: break####
      if len(event.jetAK8_pt)<1 or not event.jetAK8_IDTight[0]: continue
      if event.jetAK8_pt[0]<500 or event.jetAK8_pt[0]>700: continue
      if event.jetAK8_eta[0]>2.4: continue
      for plot in plots:
       for cut in cuts:
         if event.jetAK8_tau2[0]/event.jetAK8_tau1[0]<cut:
           histlist[plot[0]+str(cut)+sample].Fill(getattr(event,plot[0])[0],weight)
     #break####


 for plot in plots:
  for cut in cuts:
   canvas = TCanvas("c1","c1",0,0,200,260)
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
   legend=TLegend(0.45,0.7,0.85,0.9)
   dataPlotted=False
   counter=0
   integral=1
   originalIntegral={}
   maximum=0
   s=0
   hists=[]
   firsthist=None

   for sample,files in samples:
    hist=histlist[plot[0]+str(cut)+sample]

    hist.SetTitle("")
    hist.SetFillStyle(0)
    hist.SetMarkerStyle(20)
    #hist.SetMarkerSize(2)
    hist.GetXaxis().SetTitle("")
    hist.GetXaxis().SetLabelColor(0)
    hist.GetYaxis().SetTitle("Events")
    if "pruned jet mass" in plot[1]:
        hist.GetYaxis().SetTitle("Events / (5 GeV)")
    if "data" in sample:
        integral=hist.Integral()
    if hist.Integral()>0:
        hist.Scale(integral/hist.Integral())

    hists+=[hist]
    print hists

    hist.SetLineColor(colors[counter])
    hist.SetLineStyle(styles[counter])        
    hist.SetLineWidth(widths[counter])
    
    if counter==0:
      firsthist=hist
      if "data" in sample:
        hist.Draw("pe")
      else:
        hist.Draw("hist")
    else:
      if "data" in sample:
        hist.Draw("pesame")
      else:
        hist.Draw("histsame")

    if hist.GetMaximum()>maximum and hist.GetMaximum()<hist.Integral():
        maximum=hist.GetMaximum()

    if "jet p_{T}" in plot[1]:
  	firsthist.GetYaxis().SetRangeUser(100,maximum*20.0)
    elif "jet p_{T}" in plot[1]:
  	firsthist.GetYaxis().SetRangeUser(0.001,maximum*20.0)
    else:
        firsthist.GetYaxis().SetRangeUser(0,maximum*1.3)

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
    ratio.GetXaxis().SetTitle(plot[1])
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

    if "data" in sample:
      legend.AddEntry(hist,sample,"ple")
    else:
      legend.AddEntry(hist,sample,"l")
    counter+=1

   legend.SetTextSize(0.036)
   legend.SetFillStyle(0)
   legend.Draw("same")

   if "AK10" in plot[0]:
     legend4=TLegend(0.23,0.85,0.5,0.9,"AK R=1.0")
   else:
     legend4=TLegend(0.23,0.85,0.5,0.9,"AK R=0.8")
   legend4.SetTextSize(0.03)
   legend4.SetFillStyle(0)
   legend4.Draw("same")

   legend2=TLegend(0.17,0.8,0.5,0.85,"500 < p_{T} < 700 GeV")
   legend2.SetTextSize(0.03)
   legend2.SetFillStyle(0)
   legend2.Draw("same")

   legend2a=TLegend(0.24,0.75,0.5,0.8,"|#eta|<2.4")
   legend2a.SetTextSize(0.03)
   legend2a.SetFillStyle(0)
   legend2a.Draw("same")

   banner = TLatex(0.27,0.93,"  CMS	     L = 2.3 fb^{-1} at #sqrt{s} = 13 TeV, dijets");
   banner.SetNDC()
   banner.SetTextSize(0.04)
   banner.Draw();  

   legend3=TLegend(0.17,0.7,0.5,0.75,"#tau_{2}/#tau_{1}<0.45")
   #legend3=TLegend(0.17,0.7,0.5,0.75,"massdrop < 0.2")
   legend3.SetTextSize(0.03)
   legend3.SetFillStyle(0)
   legend3.Draw("same")

   canvas.SaveAs("w_jet_mass13TeV_"+plot[0]+str(cut)+".png")
   canvas.SaveAs("w_jet_mass13TeV_"+plot[0]+str(cut)+".pdf")
   canvas.SaveAs("w_jet_mass13TeV_"+plot[0]+str(cut)+".root")
   canvas.SaveAs("w_jet_mass13TeV_"+plot[0]+str(cut)+".C")
   canvas.SaveAs("w_jet_mass13TeV_"+plot[0]+str(cut)+".eps")
