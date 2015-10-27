import os, sys
from ROOT import * 
from DataFormats.FWLite import Events,Handle
import array

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

if __name__ == '__main__':
  
    prefix = "jet_mass_AOD"

    canvas = TCanvas("","",0,0,200,200)

    plots=[]
    
    for plot in plots:
        plot.Sumw2()

    jets="recoPFJets_ak5PFCHSPrunedJets__HLT.obj"

    events=TChain('Events')
    events.Add("/opt2/aodsim74.root")
    nevents=events.GetEntries()
    print nevents
    plots += [TH1F(prefix+'pruned jet mass 74',';pruned jet mass;N',50,0,200)]
    events.Project(prefix+'pruned jet mass 74',jets+'[0].mass()')
    if nevents>0:
        plots[-1].Scale(1./nevents)
    plots[-1].SetLineColor(1)
    plots[-1].Draw("he")
	
    events2=TChain('events2')
    events2.Add("/opt2/aodsim75.root")
    nevents2=events2.GetEntries()
    print nevents2
    plots += [TH1F(prefix+'pruned jet mass 75',';pruned jet mass;N',50,0,200)]
    events2.Project(prefix+'pruned jet mass 75',jets+'[0].mass()')
    if nevents2>0:
        plots[-1].Scale(1./nevents2)
    plots[-1].SetLineColor(2)
    plots[-1].Draw("hesame")
	
    legend1=TLegend(0.6,0.6,0.9,0.9)
    legend1.AddEntry(plots[0],"7_4_12_patch1","l")
    legend1.AddEntry(plots[1],"7_5_3_patch1","l")
    legend1.SetTextSize(0.04)
    legend1.SetFillStyle(0)
    legend1.Draw("same")

    canvas.SaveAs(prefix + '_prunedmass.pdf')
