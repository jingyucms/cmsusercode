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

    plots=[]

    canvas = TCanvas("","",0,0,200,200)

    jets="recoBasicJets_ak8PFJetsCHSSoftDrop__HLT.obj"

    events=TChain('Events')
    events.Add("file:////opt2/aodsim74.root")
    nevents=events.GetEntries()
    print nevents
    plots += [TH1F(prefix+'pruned jet mass 74',';softdrop jet mass;N',50,0,200)]
    plots[-1].Sumw2()
    events.Project(prefix+'pruned jet mass 74',jets+'[0].mass()')
    if nevents>0:
        plots[-1].Scale(1./nevents)
    plots[-1].SetLineColor(1)
    plots[-1].Draw("he")

    maxbin=0
    maxcontent=0
    for b in range(plots[-1].GetXaxis().GetNbins()):
      if plots[-1].GetXaxis().GetBinCenter(b+1)>50 and plots[-1].GetBinContent(b+1)>maxcontent:
    	 maxbin=b
         maxcontent=plots[-1].GetBinContent(b+1)
    mean=plots[-1].GetXaxis().GetBinCenter(maxbin)
    g1 = TF1("g1","gaus", mean-15.,mean+15.)
    plots[-1].Fit(g1, "R0")
    print g1.GetParameter(1),g1.GetParameter(2)
	
    events2=TChain('Events')
    events2.Add("file:////opt2/aodsim75.root")
    nevents2=events2.GetEntries()
    print nevents2
    plots += [TH1F(prefix+'pruned jet mass 75',';softdrop jet mass;N',50,0,200)]
    plots[-1].Sumw2()
    events2.Project(prefix+'pruned jet mass 75',jets+'[0].mass()')
    if nevents2>0:
        plots[-1].Scale(1./nevents2)
    plots[-1].SetLineColor(2)
    plots[-1].Draw("hesame")
	
    maxbin=0
    maxcontent=0
    for b in range(plots[-1].GetXaxis().GetNbins()):
      if plots[-1].GetXaxis().GetBinCenter(b+1)>50 and plots[-1].GetBinContent(b+1)>maxcontent:
    	 maxbin=b
         maxcontent=plots[-1].GetBinContent(b+1)
    mean=plots[-1].GetXaxis().GetBinCenter(maxbin)
    g2 = TF1("g2","gaus", mean-15.,mean+15.)
    plots[-1].Fit(g2, "R0")
    print g2.GetParameter(1),g2.GetParameter(2)
	
    legend1=TLegend(0.6,0.6,0.9,0.9)
    legend1.AddEntry(plots[0],"7_4_12_patch1","l")
    legend1.AddEntry(plots[1],"7_5_3_patch1","l")
    legend1.SetTextSize(0.04)
    legend1.SetFillStyle(0)
    legend1.Draw("same")

    canvas.SaveAs(prefix + '_prunedmass.pdf')

    canvas = TCanvas("","",0,0,200,200)

    plots=[]
    
    jets="recoBasicJets_ak8PFJetsCHSSoftDrop__HLT.obj"
    jets2="recoPFJets_ak8PFJetsCHS__HLT.obj"

    events=TChain('Events')
    events.Add("file:////opt2/aodsim74.root")
    nevents=events.GetEntries()
    print nevents
    plots += [TH1F(prefix+'pruned jet mass over pt 74',';softdrop jet mass / p_{T};N',50,0,1)]
    plots[-1].Sumw2()
    events.Project(prefix+'pruned jet mass over pt 74',jets+'[0].mass()/'+jets2+'[0].pt()')
    if nevents>0:
        plots[-1].Scale(1./nevents)
    plots[-1].SetLineColor(1)
    plots[-1].Draw("he")
	
    events2=TChain('Events')
    events2.Add("file:////opt2/aodsim75.root")
    nevents2=events2.GetEntries()
    print nevents2
    plots += [TH1F(prefix+'pruned jet mass over pt 75',';softdrop jet mass / p_{T};N',50,0,1)]
    plots[-1].Sumw2()
    events2.Project(prefix+'pruned jet mass over pt 75',jets+'[0].mass()/'+jets2+'[0].pt()')
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

    canvas.SaveAs(prefix + '_prunedmassoverpt.pdf')
