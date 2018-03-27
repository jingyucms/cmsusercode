print "start"
import os, sys
import array,math
from ROOT import gROOT,gStyle,TH1F,TGaxis,TFile,TCanvas,TLegend,TLatex
from os import path

print "start"
#gROOT.Reset()
#gROOT.SetStyle("Plain")
gROOT.ProcessLine('.L tdrstyle.C')
gROOT.ProcessLine('.L vector.h+')
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

if __name__ == '__main__':

 samples=[("data",[("JetHT_25ns_data7.txt",1.)]),
 	  ("V+jets",[("ZJetsToQQ_HT600toInf_13TeV-madgraph.txt",5.67),
	            ("WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.txt",95.14),]),
 	  #("QCD",[("QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6.txt",1.)])
 	  #("QCD",[("QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8.txt",0.000165),
 	  #("QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8.txt",0.006830),
 	  #("QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8.txt",0.114943),
 	  #("QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8.txt",0.842650),
 	  #("QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8.txt",9.4183),
 	  #("QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8.txt",32.293),
 	  #("QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8.txt",186.9),
 	  #("QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8.txt",648.2),
 	  #("QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8.txt",7823.0),
	  #("QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8.txt",117276.0),
	  #],)
 	  ("QCD",[("QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.txt",347700.),
 	  ("QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.txt",32100.),
 	  ("QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.txt",6831.),
 	  ("QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.txt",1207.),
 	  ("QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.txt",119.9),
 	  ("QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.txt",25.24),
	  ],)
 	   ]
 colors=[1,2,4,6,1]
 styles=[1,1,2,3,1]
 widths=[2,2,2,2,2]

 plots = [("jetAK8_pruned_massCorr","pruned jet mass (GeV)"),
           ("jetAK8_softdrop_mass","softdrop jet mass (GeV)"),
           #("jetAK10_trimmed_massCorr","trimmed jet mass (GeV)", ),
	    ("jetAK8_pt","jet p_{T} (GeV)"),
	    ("jetAK8_eta","jet #eta"),
	    #("jetAK8_massdrop","jet massdrop"),
	    ("jetAK8_tau21","jet #tau_{21}'"),
	    ("jetAK8_cm","jet N constituents"),
	    ("jetAK8_chm","jet N charged constituents"),
	    #("subjetAK8_softdrop_N","jet N subjets"),
	    #("subjetAK8_softdrop_pt","subjets p_{T}"),
           ]
 cuts= [0,0.45,0.6,1.0]
 minpt=400
 maxpt=13000
 minmass=0

 histlist={}
 for plot in plots:
  for cut in cuts:
   for sample,files in samples:
    histname="plot"+plot[0]+str(cut)+sample
    if "jet mass " in plot[1]:
       histlist[plot[0]+str(cut)+sample]=TH1F(histname,histname,(300-minmass)/5,minmass,300);
    if "jet p_{T}" in plot[1]:
       histlist[plot[0]+str(cut)+sample]=TH1F(histname,histname,40,0,1000);
    if "jet #eta" in plot[1]:
       histlist[plot[0]+str(cut)+sample]=TH1F(histname,histname,25,-2.4,2.4);
    #if "jet massdrop" in plot[1]:
    #   histlist[plot[0]+str(cut)+sample]=TH1F(histname,histname,40,0,1);
    if "jet #tau_{21}'" in plot[1]:
       histlist[plot[0]+str(cut)+sample]=TH1F(histname,histname,40,0,1);
    if "jet N constituents" in plot[1]:
       histlist[plot[0]+str(cut)+sample]=TH1F(histname,histname,100,0,100);
    if "jet N charged constituents" in plot[1]:
       histlist[plot[0]+str(cut)+sample]=TH1F(histname,histname,100,0,100);
    #if "jet N subjets" in plot[1]:
    #   histlist[plot[0]+str(cut)+sample]=TH1F(histname,histname,10,0,10);
    #if "subjets p_{T}" in plot[1]:
    #   histlist[plot[0]+str(cut)+sample]=TH1F(histname,histname,50,0,500);
    histlist[plot[0]+str(cut)+sample].GetYaxis().SetRangeUser(0,50000)
    histlist[plot[0]+str(cut)+sample].Sumw2()

 for sample,files in samples:
    files2=[]
    for filename,weight in files:
      if filename.endswith(".txt"):
        filelist=open(filename)
        nevents=0
	flist=[]
	for line in filelist.readlines():
	    if ".root" in line:
	      flist+=[line.strip()]
              try:
                f=TFile.Open(line.strip())
                tree=f.Get("ntuplizer/tree")
                nevents+=tree.GetEntries()
		f.Close()
              except:
                print "error opening tree"
              #nevents=10000#####
	      #break#####
	for fi in flist:
           files2+=[(fi,weight,nevents)]
      else:
        try:
          f=TFile.Open(filename)
          tree=f.Get("ntuplizer/tree")
          nevents=tree.GetEntries()
	  f.Close()
        except:
          print "error opening tree"
          nevents=0
        files2=[(filename,weight,nevents)]

    for filename,weight,nevents in files2:
     print filename,weight,nevents
     if not "data" in sample:
       weight/=nevents
     try:
       f=TFile.Open(filename)
       tree=f.Get("ntuplizer/tree")
       tree.GetEntries()
     except:
       print "error opening tree"
       continue
  
     event_count=0
     for event in tree:
      if event_count>nevents: break
      event_count+=1
      if not event.passFilter_HBHE or not event.passFilter_CSCHalo or not event.passFilter_GoodVtx or not event.passFilter_EEBadSc: continue
      if len(event.jetAK8_pt)<2: continue
      if event.jetAK8_IDTight[0] and abs(event.jetAK8_eta[0])<2.4 and event.jetAK8_pt[0]>minpt and event.jetAK8_pt[0]<maxpt and event.jetAK8_pruned_massCorr[0]>minmass:
        index=0
      elif event.jetAK8_IDTight[1] and abs(event.jetAK8_eta[1])<2.4 and event.jetAK8_pt[1]>minpt and event.jetAK8_pt[1]<maxpt and event.jetAK8_pruned_massCorr[1]>minmass:
        index=1
      else: continue
      #if event.jetAK8_chm[index]<25 or event.jetAK8_chm[index]>55: continue
      #if event.subjetAK8_softdrop_N[index]>1 and event.jetAK8_softdrop_mass[index]>0:
      #  massdrop=max(event.subjetAK8_softdrop_mass[index][0],event.subjetAK8_softdrop_mass[index][1])/event.jetAK8_softdrop_mass[index]
      #else:
      #  massdrop=0.9999
      #if massdrop>0.4: continue
      tau21=event.jetAK8_tau2[index]/event.jetAK8_tau1[index]
      if event.jetAK8_softdrop_mass[index]>0:
        tau21p=0.67-0.067*math.log(pow(event.jetAK8_softdrop_mass[index],2)/event.jetAK8_pt[index])
      else:
        tau21p=0.9999
      for plot in plots:
        #if "jet massdrop" in plot[1]:
	#  var=massdrop
        if "jet #tau_{21}'" in plot[1]:
	  var=tau21
        #elif "subjets p_{T}" in plot[1]:
        #  if event.subjetAK8_softdrop_N[index]>1:
        #    var=min(event.subjetAK8_softdrop_pt[index][0],event.subjetAK8_softdrop_pt[index][1])
	#  else:
	#    var=0.
        else:
           var=getattr(event,plot[0])[index]
        for cut in cuts:
          if tau21<cut and tau21>cuts[max(0,cuts.index(cut)-1)]:
            histlist[plot[0]+str(cut)+sample].Fill(var,weight)
     f.Close()

 print "done with files, now plotting"

 f=TFile.Open("w_jet_mass13TeV_76_"+str(minpt)+"_"+str(minmass)+".root","RECREATE")
 f.cd()
 for p in histlist.values():
   p.Write()
 f.Close()

 for plot in plots:
  for cut in cuts:
   canvas = TCanvas("c1"+plot[0]+str(cut),"c1"+plot[0]+str(cut),0,0,200,260)
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
   integrals=[]

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
    integrals+=[(plot[0]+str(cut)+sample,hist.Integral())]
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

   #legend2=TLegend(0.17,0.8,0.5,0.85,str(minpt)+" < p_{T} < "+str(maxpt)+" GeV")
   legend2=TLegend(0.17,0.8,0.5,0.85,"p_{T} > "+str(minpt)+" GeV, |#eta|<2.4")
   legend2.SetTextSize(0.03)
   legend2.SetFillStyle(0)
   legend2.Draw("same")

   legend2a=TLegend(0.17,0.75,0.5,0.8,"massdrop < 0.4")
   legend2a.SetTextSize(0.03)
   legend2a.SetFillStyle(0)
   #legend2a.Draw("same")

   banner = TLatex(0.27,0.93,"  CMS	     L = 2.3 fb^{-1} at #sqrt{s} = 13 TeV, dijets");
   banner.SetNDC()
   banner.SetTextSize(0.04)
   banner.Draw();  

   legend3=TLegend(0.17,0.7,0.5,0.75,str(cuts[max(0,cuts.index(cut)-1)])+"<#tau_{2}/#tau_{1}<"+str(cut))
   legend3.SetTextSize(0.03)
   legend3.SetFillStyle(0)
   #legend3.Draw("same")

   legend3=TLegend(0.17,0.7,0.5,0.75,str(cuts[max(0,cuts.index(cut)-1)])+"<#tau_{21}'<"+str(cut))
   legend3.SetTextSize(0.03)
   legend3.SetFillStyle(0)
   legend3.Draw("same")

   canvas.SaveAs("w_jet_mass13TeV_76_"+str(minpt)+"_"+str(minmass)+"_"+plot[0]+str(cut)+".png")
   canvas.SaveAs("w_jet_mass13TeV_76_"+str(minpt)+"_"+str(minmass)+"_"+plot[0]+str(cut)+".pdf")
   canvas.SaveAs("w_jet_mass13TeV_76_"+str(minpt)+"_"+str(minmass)+"_"+plot[0]+str(cut)+".root")
   canvas.SaveAs("w_jet_mass13TeV_76_"+str(minpt)+"_"+str(minmass)+"_"+plot[0]+str(cut)+".C")
   canvas.SaveAs("w_jet_mass13TeV_76_"+str(minpt)+"_"+str(minmass)+"_"+plot[0]+str(cut)+".eps")
   out=open("w_jet_mass13TeV_76_"+str(minpt)+"_"+str(minmass)+"_"+plot[0]+str(cut)+".txt",'w')
   out.write(str(integrals))
   out.close()
