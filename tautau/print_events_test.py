import os, sys
import array
from ROOT import * 
from os import path

gROOT.Reset()
gROOT.SetStyle("Plain")
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetTitleOffset(1.2,"Y")
gStyle.SetPadLeftMargin(0.18)
gStyle.SetPadBottomMargin(0.15)
gStyle.SetPadTopMargin(0.08)
gStyle.SetPadRightMargin(0.15)
gStyle.SetMarkerSize(0.5)
gStyle.SetHistLineWidth(1)
gStyle.SetStatFontSize(0.020)
gStyle.SetTitleSize(0.06, "XYZ")
gStyle.SetLabelSize(0.05, "XYZ")
gStyle.SetNdivisions(510, "XYZ")
gStyle.SetLegendBorderSize(0)
gStyle.SetPalette(1)

if __name__ == '__main__':

    baseline           =  'l1Pt>35 && l2Pt>35 && abs(l1Eta)<2.1 && abs(l2Eta)<2.1 && diTauCharge==0 && abs(jet1Eta) < 3.0'
    baselineSS         =  'l1Pt>35 && l2Pt>35 && abs(l1Eta)<2.1 && abs(l2Eta)<2.1 && diTauCharge!=0 && abs(jet1Eta) < 3.0'
    baseline           += ' && l2MVAEle>0.5'
    baselineSS         += ' && l2MVAEle>0.5'
    l1Pt35l2Pt35       =  ' && l1Pt>35 && l2Pt>35'
    
    l1Pt40l2Pt40_down  =  ' && l1Pt>40*0.97 && l2Pt>40*0.97'
    l1Pt40l2Pt40_up    =  ' && l1Pt>40*1.03 && l2Pt>40*1.03'
    l1Pt40l2Pt40       =  ' && l1Pt>40 && l2Pt>40'
    
    l1Pt45l2Pt40       =  ' && l1Pt>45 && l2Pt>40'
    l1Pt45l2Pt45       =  ' && l1Pt>45 && l2Pt>45'
    l1Pt50l2Pt50       =  ' && l1Pt>50 && l2Pt>50'
    isolationL         =  ' && (l1RawMVAIso>0.795 || l2RawMVAIso>0.795)'
    isolationMLL       =  ' && ((l1MedMVAIso>0.5 && l2RawMVAIso>0.5) || (l1RawMVAIso>0.5 && l2MedMVAIso>0.5))'

    isolationMNM       =  ' && ((l1MedMVAIso>0.5 && l2MedMVAIso<0.5) || (l1MedMVAIso<0.5 && l2MedMVAIso>0.5))'

    isolationM         =  ' && (l1MedMVAIso>0.5 || l2MedMVAIso>0.5)'
    isolationLL        =  ' && l1RawMVAIso>0.795 && l2RawMVAIso>0.795'
    isolationLL2       =  ' && l1RawMVAIso>0.7 && l2RawMVAIso>0.7'
    isolationLL3       =  ' && l1RawMVAIso>0.3 && l2RawMVAIso>0.3'
    isolationLL4       =  ' && l1RawMVAIso>0.5 && l2RawMVAIso>0.5'
    isolationLL1       =  ' && l1RawMVAIso>0.1 && l2RawMVAIso>0.1'
    isolationLL4old    =  ' && l1LooIso>0.5 && l2LooIso>0.5'
    isolationML        =  ' && ((l1MedMVAIso>0.5 && l2RawMVAIso>0.795) || (l1RawMVAIso>0.795 && l2MedMVAIso>0.5))'
    isolationMM        =  ' && l1MedMVAIso>0.5 && l2MedMVAIso>0.5'
    isolationMMold     =  ' && l1MedIso>0.5 && l2MedIso>0.5'
    isolationTM        =  ' && ((l1MedMVAIso>0.5 && l2TigMVAIso>0.5) || (l1TigMVAIso>0.5 && l2MedMVAIso>0.5))'
    isolationTT        =  ' && l1TigMVAIso>0.5 && l2TigMVAIso>0.5'
    Jet0               =  ' && jet1Pt<50'
    BOOSTED            =  ' && jet1Pt>50'
    VBF                =  ' &&  jet1Pt>50 && jet2Pt>30 && abs(jet1Eta - jet2Eta)>2.5 && (jet1Eta*jet2Eta)<0 && mjj>250 && nCentralJets==0'
    VBFlooser          =  ' &&  jet1Pt>50 && jet2Pt>30 && abs(jet1Eta - jet2Eta)>2.5 && (jet1Eta*jet2Eta)<0 && mjj>150 && nCentralJets==0'
    VBFtight           =  ' &&  jet1Pt>50 && jet2Pt>30 && abs(jet1Eta - jet2Eta)>4.0 && (jet1Eta*jet2Eta)<0 && mjj>400 && nCentralJets==0 '
    VBFmedium          =  ' &&  jet1Pt>50 && jet2Pt>30 && abs(jet1Eta - jet2Eta)>2.5 && (jet1Eta*jet2Eta)<0 && mjj>500 && nCentralJets==0 '
    NOVBF              =  ' && (jet1Pt<50 || jet2Pt<30 || abs(jet1Eta - jet2Eta)<2.5 || (jet1Eta*jet2Eta)>0 || mjj<250 || nCentralJets >0)'
    NOVBFmedium        =  ' && (jet1Pt<50 || jet2Pt<30 || abs(jet1Eta - jet2Eta)<2.5 || (jet1Eta*jet2Eta)>0 || mjj<500 || nCentralJets >0)'
    NOVBFtight         =  ' && (jet1Pt<50 || jet2Pt<30 || abs(jet1Eta - jet2Eta)<4.0 || (jet1Eta*jet2Eta)>0 || mjj<400 || nCentralJets >0)'

    weight='weight'
    cut = baseline + BOOSTED + NOVBF
    antiqcdcut = ' && dRtt<2.0'
    isocut = isolationMM
    #looseisocut = isolationLL4+" && !(1 "+isocut+")"
    looseisocut = ' && l2MedMVAIso>0.5'

    cut += l1Pt40l2Pt40

    cutSS=cut.replace("diTauCharge==0","diTauCharge!=0")

    canvas = TCanvas("","",0,0,200,200)

    f=TFile.Open("test1/DYJets_14/H2TauTauTreeProducerTauTau/H2TauTauTreeProducerTauTau_tree.root")
    tree=f.Get("H2TauTauTreeProducerTauTau")
    tree.SetScanField(0)
    print "############ Run2012A event list #############"
    tree.Scan( "run:lumi:event:svfitMass:met:rawMET:jet1Pt:jet1Eta:jet1Phi:l1Pt:l1Eta:l1Phi:l2Pt:l2Eta:l2Phi", '{weight}*({cut})'.format(cut=cut+isocut+antiqcdcut, weight="weight"), 'colsize=15' )
