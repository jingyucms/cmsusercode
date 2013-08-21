import os, sys
import array
from ROOT import * 

gROOT.Reset()
gROOT.SetStyle("Plain")
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetTitleOffset(1.2,"Y")
gStyle.SetPadLeftMargin(0.18)
gStyle.SetPadBottomMargin(0.15)
gStyle.SetPadTopMargin(0.08)
gStyle.SetPadRightMargin(0.05)
gStyle.SetMarkerSize(0.5)
gStyle.SetHistLineWidth(1)
gStyle.SetStatFontSize(0.020)
gStyle.SetTitleSize(0.06, "XYZ")
gStyle.SetLabelSize(0.05, "XYZ")
gStyle.SetNdivisions(510, "XYZ")
gStyle.SetLegendBorderSize(0)

if __name__ == '__main__':

   var="chi"
   label="#chi"

   masses=[1900,2400,3000,3600,4200,7000]

   colors=[1,2,3,4,6,7,8,9,10,11,12,13]
   styles=[1,2,3,4,5,6,7,8,9,11,12,13]
   
   sources=["Absolute", "HighPtExtra", "SinglePionECAL", "SinglePionHCAL",
   "Flavor", "Time",
   "RelativeJEREC1", "RelativeJEREC2", "RelativeJERHF",
   "RelativePtEC1", "RelativePtEC2", "RelativePtHF",
   "RelativeStatEC2", "RelativeStatHF", 
   "PileUpDataMC",  "PileUpBias",
   "PileUpPtBB", "PileUpPtEC", "PileUpPtHF"]
   sourcesets=[[0,1,2,3,4,5],[6,7,8,9,10,11,12,13],[14,15,16,17,18]]

   prefix="Moriond"

   mc=[("chi_QCD_1000",204.0/13479218),
       ("chi_QCD_500",8426.0/31743483),
       ("chi_QCD_250",276000.0/26900255),
       ("chi_QCD_100",1.036e7/48365102),
       ]
   mc=[("chi_EPS2",1)]
   mc=[("chi_QCDHerwig",1)]
   f_mc=[]
   for name,xsec in mc:
      f_mc+=[TFile.Open(name+".root")]

   for sourceset in sourcesets:
    canvas = TCanvas("","",0,0,600,400)
    canvas.Divide(3,2)
    log="pt" in var or "et" in var or "dphi" in var
    legends=[]
    hists=[]
    for mass in range(len(masses)-1):
        canvas.cd(mass+1)
        canvas.GetPad(mass+1).SetLogy(log)
        legend=TLegend(0.4,0.5,0.95,0.90,str(masses[mass])+"<m_{jj}<"+str(masses[mass+1])+" GeV")
	legends+=[legend]
    
        hist=f_mc[0].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var)
	hist=hist.Clone(hist.GetName()+"main"+str(sourcesets.index(sourceset)))
	hists+=[hist]
        for i in range(1,len(mc)):
            hist.Add(f_mc[i].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var),mc[i][1]/mc[0][1])
        hist.SetLineWidth(2)
      	hist.SetLineColor(1)
	if "metsumet" in var:
	    hist.Rebin(4)
	miny=0
	if hist.Integral()>0:
            miny=log*0.1
	hist.SetTitle("")
	histref=hist.Clone(hist.GetName()+"ref"+str(sourcesets.index(sourceset)))
	hists+=[histref]
        for b in range(hist.GetNbinsX()):
	    hist.SetBinError(b+1,0)
	    hist.SetBinContent(b+1,1)
	hist.GetXaxis().SetTitle(label)
	hist.GetYaxis().SetTitle("N")
	hist.GetYaxis().SetRangeUser(0.97,1.05)
        hist.GetXaxis().SetTitleOffset(1.1)
        hist.GetYaxis().SetTitleOffset(1.1)
        hist.GetXaxis().SetLabelSize(0.05)
        hist.GetYaxis().SetLabelSize(0.05)
        hist.GetXaxis().SetTitleSize(0.06)
        hist.GetYaxis().SetTitleSize(0.06)
        hist.Draw("le")
        legend.AddEntry(hist,"central","l")
	
	for i in range(len(sourceset)):
            hist2=f_mc[0].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var+"_JECup"+str(sourceset[i]))
            for j in range(1,len(mc)):
                hist2.Add(f_mc[j].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var+"_JECup"+str(sourceset[i])),mc[j][1]/mc[0][1])
	    if hist2.Integral()>0:
                hist2.Scale(histref.Integral()/hist2.Integral())
            hist2.SetLineWidth(1)
            hist2.SetLineColor(colors[i])
            hist2.SetLineStyle(2)
	    if "metsumet" in var:
	        hist2.Rebin(4)
            hist2.Divide(hist2,histref)
            miny=0
            if hist2.Integral()>0:
                miny=log*0.1
	    hist2.SetTitle("")
            hist2.Draw("histsame")
            legend.AddEntry(hist2,"JEC "+sources[sourceset[i]],"l")

	for i in range(len(sourceset)):
            hist3=f_mc[0].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var+"_JECdown"+str(sourceset[i]))
            for j in range(1,len(mc)):
                hist3.Add(f_mc[j].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var+"_JECdown"+str(sourceset[i])),mc[j][1]/mc[0][1])
            if hist3.Integral()>0:
                hist3.Scale(histref.Integral()/hist3.Integral())
            hist3.SetLineWidth(1)
            hist3.SetLineColor(colors[i])
            hist3.SetLineStyle(3)
	    if "metsumet" in var:
	        hist3.Rebin(4)
            hist3.Divide(hist3,histref)
            miny=0
            if hist3.Integral()>0:
                miny=log*0.1
	    hist3.SetTitle("")
            hist3.Draw("histsame")

        legend.SetTextSize(0.04)
        legend.SetFillStyle(0)
        legend.Draw("same")

    canvas.SaveAs("chi_systematic_plots"+var+"_"+prefix+str(sourcesets.index(sourceset))+".root")
    canvas.SaveAs("chi_systematic_plots"+var+"_"+prefix+str(sourcesets.index(sourceset))+".pdf")
