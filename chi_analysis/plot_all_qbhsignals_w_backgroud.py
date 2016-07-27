import os, sys
from ROOT import *

gROOT.ForceStyle()
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetMarkerSize(0.5)
gStyle.SetHistLineWidth(1)
gStyle.SetMarkerStyle(20)
gStyle.SetLegendBorderSize(0)

## RS1 Black Hole
#energies=[3500,4000,4500,5000,5500,6000,6500,7000]

## ADD6 Black Hole
energies=[6500,7000,7500,8000]
massbins=[[4200,4800],[4800,13000]]

canvas = TCanvas("MyCanvas","(ADD) QBH",0,0,1200,600)
canvas.Draw()
    
pad1=TPad("","",0, 0, 0.5, 1)
pad2=TPad("","",0.5, 0, 1, 1)
pad=[pad1,pad2]

for massbin in massbins:

    canvas.cd()
    pad[massbins.index(massbin)].Draw()
    pad[massbins.index(massbin)].cd()
    
    qcdFileName="datacard_shapelimit13TeV_QBH_6500_6_chi_v1.root"
    qcdFile=TFile.Open(qcdFileName)
    hqcd=qcdFile.Get("fastNloQCD#chi"+str(massbin[0])+"_"+str(massbin[1])+"_rebin1_backup")
    hqcd.Draw("hist")
    hqcd.GetYaxis().SetTitle("#sigma * A")
    hqcd.GetYaxis().SetTitleOffset(1.5)
    legend=TLegend(0.3,0.6,0.6,0.85,str(massbin[0])+"<m_{jj}<"+str(massbin[1])+" GeV")
    legend.AddEntry(hqcd,"NLO QCD+EWK Correction","l")
    
    for energy in energies:
        fileName="datacard_shapelimit13TeV_QBH_"+str(energy)+"_6_chi_v1.root"
        file=TFile.Open(fileName)
        hqbh=file.Get("qbh_"+str(energy)+"_6_#chi"+str(massbin[0])+"_"+str(massbin[1])+"_rebin1_backup")
        hadd=file.Get("qbh_"+str(energy)+"_6_#chi"+str(massbin[0])+"_"+str(massbin[1])+"_rebin1_add_backup")
        hqbh.Draw("samehist")
        hadd.Draw("samehist")
        legend.AddEntry(hqbh, str(energy)+" TeV (ADD)QBH", "l")
        legend.AddEntry(hadd, str(energy)+" TeV (ADD)QBH + NLOQCD", "l")
    legend.SetFillStyle(0)
    legend.Draw("same")
        
savename="signal_qbh_ADD_6_wbackgroud.gif"    
canvas.SaveAs(savename)
