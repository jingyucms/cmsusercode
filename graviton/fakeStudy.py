from ROOT import *
import ROOT
import array, math
import os
from CMGTools.RootTools.RootTools import *

prefix = "plots/fakeStudy_graviton"

#gROOT.Macro( os.path.expanduser( '~/rootlogon.C' ) )
gROOT.Reset()
gROOT.SetStyle("Plain")
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetTitleOffset(1.2,"Y")
gStyle.SetPadLeftMargin(0.18)
gStyle.SetPadBottomMargin(0.15)
gStyle.SetPadTopMargin(0.03)
gStyle.SetPadRightMargin(0.05)
gStyle.SetMarkerSize(1.5)
gStyle.SetHistLineWidth(1)
gStyle.SetStatFontSize(0.020)
gStyle.SetTitleSize(0.06, "XYZ")
gStyle.SetLabelSize(0.05, "XYZ")
gStyle.SetNdivisions(510, "XYZ")
gStyle.SetLegendBorderSize(0)

def plot(samples,weights,files,variable,rebin):
    hists=[]
    colors=[1,2,3,4,6,7,8,9,10,11,12,13,14]
    
    canvas = TCanvas("","",0,0,300,150)
    canvas.Divide(2,1)
    canvas.cd(1)
    canvas.GetPad(1).SetLogy()
    legend=TLegend(0.5,0.6,0.9,0.9,"")
    same=""
    for i in range(len(samples)):
        weight=weights[i]
        h = TH1F(files[i].Get("cmgPFDiJetHistograms0tag/"+variable))
	h.Scale(weight)
	h.Rebin(rebin)
        #h=h.Rebin(len(mass_binning)-1,h.GetName()+"_rebin",mass_binning)
	h.SetLineColor(colors[i])
	h.SetMarkerColor(colors[i])
	h.Draw("hist"+same)
	same="same"
	if variable=="mass":
            h.GetXaxis().SetTitle("dijet mass [GeV]")
	    h.GetXaxis().SetRangeUser(500,1500)
	if variable=="pt1":
            h.GetXaxis().SetTitle("jet 1 p_T [GeV]")
	    h.GetXaxis().SetRangeUser(0,1500)
	if variable=="mass1":
            h.GetXaxis().SetTitle("jet 1 mass [GeV]")
	    h.GetXaxis().SetRangeUser(0,200)
	h.GetYaxis().SetTitle("d#sigma [fb]")
	h.GetYaxis().SetRangeUser(1e-3,1e7)
	h.SetTitle("")
	h.GetXaxis().SetTitleOffset(1.0)
	h.GetYaxis().SetTitleOffset(1.4)
	h.GetXaxis().SetLabelSize(0.05)
	h.GetYaxis().SetLabelSize(0.05)
	h.GetXaxis().SetTitleSize(0.06)
	h.GetYaxis().SetTitleSize(0.06)
	hists+=[h]
        legend.AddEntry(h,samples[i][2]+" all","l")
        h2 = TH1F(files[i].Get("cmgPFDiJetHistograms1tag/"+variable))
	h2.Scale(weight)
	h2.Rebin(rebin)
        #h2=h2.Rebin(len(mass_binning)-1,h2.GetName()+"_rebin",mass_binning)
	h2.SetLineColor(colors[i])
	h2.SetMarkerColor(colors[i])
	h2.SetLineStyle(2)
	h2.Draw("histsame")
	hists+=[h2]
        legend.AddEntry(h2,samples[i][2]+" 1tag","l")
        h3 = TH1F(files[i].Get("cmgPFDiJetHistograms2tag/"+variable))
	h3.Scale(weight)
	h3.Rebin(rebin)
        #h3=h3.Rebin(len(mass_binning)-1,h3.GetName()+"_rebin",mass_binning)
	h3.SetLineColor(colors[i])
	h3.SetMarkerColor(colors[i])
	h3.SetLineStyle(3)
	h3.Draw("histsame")
	hists+=[h3]
        legend.AddEntry(h3,samples[i][2]+" 2tag","l")
    legend.SetTextSize(0.04)
    legend.SetFillStyle(0)
    legend.Draw("same")
    canvas.cd(2)
    #canvas.GetPad(2).SetLogy()
    legend2=TLegend(0.4,0.2,0.9,0.5,"")
    #same="A"
    same=""
    for i in range(len(samples)):
        weight=weights[i]
        href = TH1F(files[i].Get("cmgPFDiJetHistograms0tag/"+variable))
	href.Scale(weight)
	href.Rebin(rebin)
        #href=href.Rebin(len(mass_binning)-1,href.GetName()+"_rebin",mass_binning)
        h2ref = TH1F(files[i].Get("cmgPFDiJetHistograms1tag/"+variable))
	h2ref.Scale(weight)
	h2ref.Rebin(rebin)
        #h2ref=h2ref.Rebin(len(mass_binning)-1,h2ref.GetName()+"_rebin",mass_binning)
        #h2ref.Scale(0.5)
        h2 = TH1F(files[i].Get("cmgPFDiJetHistograms1tag/"+variable))
	h2.Scale(weight)
	h2.Rebin(rebin)
        #h2=h2.Rebin(len(mass_binning)-1,h2.GetName()+"_rebin",mass_binning)
        #h2.Scale(0.5)
	#for b in range(h2.GetXaxis().GetNbins()):
	#    if h2.GetBinContent(b+1)>0 and h2.GetBinError(b+1)/h2.GetBinContent(b+1)>0.3:
	#        h2.SetBinContent(b+1,1)
	#        h2.SetBinError(b+1,1)
	#        href.SetBinContent(b+1,1)
	#        href.SetBinError(b+1,1)
	#h2=TGraphAsymmErrors(h2,href)
	#h2.Draw("lz"+same)
        h2.Divide(h2,href,1,1,'B')
	h2.Draw("hc"+same)
	h2.SetLineColor(colors[i])
	h2.SetMarkerColor(colors[i])
	#h2.SetFillColor(colors[i])
	h2.SetLineStyle(2)
	same="same"
	if variable=="mass":
            h2.GetXaxis().SetTitle("dijet mass [GeV]")
	    h2.GetXaxis().SetRangeUser(500,1500)
	if variable=="pt1":
            h2.GetXaxis().SetTitle("jet 1 p_T [GeV]")
	    h2.GetXaxis().SetRangeUser(0,1500)
	if variable=="mass1":
            h2.GetXaxis().SetTitle("jet 1 mass [GeV]")
	    h2.GetXaxis().SetRangeUser(0,200)
	h2.GetYaxis().SetTitle("Efficiency")
	h2.GetYaxis().SetRangeUser(0,1)
	h2.SetTitle("")
	h2.GetXaxis().SetTitleOffset(1.0)
	h2.GetYaxis().SetTitleOffset(1.4)
	h2.GetXaxis().SetLabelSize(0.05)
	h2.GetYaxis().SetLabelSize(0.05)
	h2.GetXaxis().SetTitleSize(0.06)
	h2.GetYaxis().SetTitleSize(0.06)
	hists+=[h2]
        legend2.AddEntry(h2,samples[i][2]+" 1tag / all","l")
        h3 = TH1F(files[i].Get("cmgPFDiJetHistograms2tag/"+variable))
	h3.Scale(weight)
	h3.Rebin(rebin)
        #h3=h3.Rebin(len(mass_binning)-1,h3.GetName()+"_rebin",mass_binning)
        #h3.Scale(4)
	#for b in range(h3.GetXaxis().GetNbins()):
	#    if h3.GetBinContent(b+1)>0 and h3.GetBinError(b+1)/h3.GetBinContent(b+1)>0.3:
	#        h3.SetBinContent(b+1,1)
	#        h3.SetBinError(b+1,1)
	#        h2ref.SetBinContent(b+1,1)
	#        h2ref.SetBinError(b+1,1)
	#h3=TGraphAsymmErrors(h3,h2ref)
	#h3.Draw("lz"+same)
        h3.Divide(h3,h2ref,1,1,'B')
	h3.Draw("hc"+same)
	h3.SetLineColor(colors[i])
	h3.SetMarkerColor(colors[i])
	#h3.SetFillColor(colors[i])
	h3.SetLineStyle(3)
	h3.Draw("csame")
	hists+=[h3]
        #legend2.AddEntry(h3,samples[i][2]+" 4 x 2tag / 1tag","l")
        legend2.AddEntry(h3,samples[i][2]+" 2tag / 1tag","l")
    legend2.SetTextSize(0.04)
    legend2.SetFillStyle(0)
    #legend2.Draw("same")

    canvas.SaveAs(prefix + '_dijet'+variable+'.root')
    canvas.SaveAs(prefix + '_dijet'+variable+'.pdf')
    canvas.SaveAs(prefix + '_dijet'+variable+'.eps')
    if wait:
        os.system("ghostview "+prefix + '_dijet'+variable+'.eps')

if __name__ == '__main__':

    wait=True

    samples=[
             #("diJetAnalysis_Histograms_QCD.root",3.326e-04*1e9*6e4,'QCD'),
             ("diJetAnalysis_Histograms_WW.root",27.80,'WW'),
             ("diJetAnalysis_Histograms_graviton-ZZ-1000.root",40.3e-3*5.4,'G*->ZZ,1TeV'),
             ("diJetAnalysis_Histograms_graviton-WW-1000.root",80.5e-3*5.4,'G*->WW,1TeV'),
             #("diJetAnalysis_Histograms_graviton-ZZ-2000.root",1.16e-3,'G*->ZZ 2TeV'),
             #("diJetAnalysis_Histograms_graviton-WW-2000.root",2.34e-3,'G*->WW 2TeV'),
             #("diJetAnalysis_Histograms_Wfast.root",7.314e-05*1e9,'W'),
             #("diJetAnalysis_Histograms_QCDfast.root",3.326e-04*1e9,'QCD'),
             #("diJetAnalysis_Histograms_graviton-ZZ-1000.root",2.558e-10*1e9,'G*->ZZ,1TeV'),
             #("diJetAnalysis_Histograms_graviton-WW-1000.root",2.558e-10*1e9,'G*->WW,1TeV'),
             #("diJetAnalysis_Histograms_graviton-ZZ-2000.root",1.827e-12*1e9,'G*->ZZ 2TeV'),
             #("diJetAnalysis_Histograms_graviton-WW-2000.root",1.827e-12*1e9,'G*->WW 2TeV'),
         #("cmgtrees/pythia6_gravitonWW_500_tree_CMG.root",1.313e-08*1e9,'G*->WW,0.5TeV,0.1k/M'),
         #("cmgtrees/herwigpp_graviton_WW_500_tree_CMG.root",0.981*5.4*0.1/500*10000,'G*->WW,0.5TeV'),
         #("cmgtrees/herwigpp_graviton_WW_1000_tree_CMG.root",80.5e-03*5.4*0.1/1000*10000.,'G*->WW,1TeV'),
         #("cmgtrees/herwigpp_graviton_ZZ_1000_tree_CMG.root",40.3e-3,'H++ G*->ZZ,1TeV'),
         #("cmgtrees/herwigpp_graviton_ZZ_1000_noMPI_noHAD_noSHOWER_PFAOD.root",40.3e-3,'H++ G*->ZZ,1TeV'),
         #("cmgtrees/pythia6_gravitonZZ_500_tree_CMG.root",1.313e-08*1e9,'G*->ZZ 0.5 TeV,0.1k/M'),
         #("cmgtrees/pythia6_graviton_0.01_WW_1000_tree_CMG.root",2.573e-12*1e9,'G*->WW,1TeV,0.01k/M'),
         #("cmgtrees/pythia6_Wprime_WZ_500_tree_CMG.root",2.455e-09*1e9,"W'->WZ 0.5TeV"),
         #("cmgtrees/pythia6_Wprime_WZ_1000_tree_CMG.root",1.021e-10*1e9,"W'->WZ 1TeV"),
         #("cmgtrees/pythia6_Wprime_WZ_2000_tree_CMG.root",1.697e-12*1e9,"W'->WZ 2TeV"),
         #("cmgtrees/pythia6_WW_tree_CMG.root",2.780e-08*1e9,'WW'),
         #(sourceQCD.fileNames,3.326e-04*1e9*6e4,'QCDflat'),
         #(sourceW.fileNames,27770.0,'W'),
         #(sourceWW.fileNames,27.80,'WW'),
         #("/tmp/hinzmann/W_tree.root",27770.0,'W'),
         #("cmgtrees/LHE.root",0.43538820803E-02,'JHU G*->ZZ,1TeV'),
         ]
    weights=[]
    files=[]
    for sample,weight,name in samples:
        files+=[TFile.Open(sample)]
        nevents=files[-1].Get("baseMETHistograms/met").GetEntries()
        print sample,", number of events:",nevents
	weights+=[1000*weight/nevents] #/fb
        print [key.GetName() for key in files[-1].GetListOfKeys()]
        print [key.GetName() for key in files[-1].GetDirectory("cmgPFDiJetHistograms0tag").GetListOfKeys()]

    mass_bins=[1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808, 7000]
    mass_binning=array.array('d')
    for mass_bin in mass_bins:
        mass_binning.append(mass_bin)

    plot(samples,weights,files,"mass",6)
    plot(samples,weights,files,"mass1",1)
    plot(samples,weights,files,"pt1",6)
