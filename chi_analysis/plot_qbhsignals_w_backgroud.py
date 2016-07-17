import os, sys
from ROOT import *

gROOT.ForceStyle()
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetMarkerSize(0.5)
gStyle.SetHistLineWidth(1)
gStyle.SetMarkerStyle(20)
gStyle.SetLegendBorderSize(0)

energies=[3500,4000,4500,5000,5500,6000,6500,7000]
#energies=[6500,7000,7500,8000,8500,9000,9500]
#energies=[6000,7000,8000,9000]

for energy in energies:
    fileName="datacard_shapelimit13TeV_QBH_"+str(energy)+"_RS1_chi_v1.root"
    savename="signal_qbh_"+str(energy)+"_RS1_wbackgroud.gif"
    
    file=TFile.Open(fileName)

    canvas = TCanvas("MyCanvas",str(energy)+"GeV QBH",0,0,1200,600)
    canvas.Draw()
    
    pad1=TPad("","",0, 0, 0.5, 1)
    pad2=TPad("","",0.5, 0, 1, 1)
    pad=[pad1,pad2]

    massbins=[[4200,4800],[4800,13000]]

    hqcds=[]
    hqbhs=[]
    hadds=[]

    for massbin in massbins:
        hqbh=file.Get("qbh_"+str(energy)+"_6_#chi"+str(massbin[0])+"_"+str(massbin[1])+"_rebin1_backup")
        hqcd=file.Get("fastNloQCD#chi"+str(massbin[0])+"_"+str(massbin[1])+"_rebin1_backup")
        hadd=file.Get("qbh_"+str(energy)+"_6_#chi"+str(massbin[0])+"_"+str(massbin[1])+"_rebin1_add_backup")
        hqbhs.append(hqbh)
        hqcds.append(hqcd)
        hadds.append(hadd)

    legends=[]
    
    for massbin in massbins:
        legend=TLegend(0.3,0.6,0.6,0.85,str(massbin[0])+"<m_{jj}<"+str(massbin[1])+" GeV")
        legend.AddEntry(hqbhs[massbins.index(massbin)], "QBH", "l")
        legend.AddEntry(hqcds[massbins.index(massbin)], "NLOQCD", "l")
        legend.AddEntry(hadds[massbins.index(massbin)], "QBH+NLOQCD", "l")
        legends.append(legend)
    
    for massbin in massbins:
        canvas.cd()
        pad[massbins.index(massbin)].Draw()
        pad[massbins.index(massbin)].cd()
        hadds[massbins.index(massbin)].SetMinimum(0)
        if energy==6500:
            hadds[massbins.index(massbin)].SetMaximum(0.1)
        else:
            hadds[massbins.index(massbin)].SetMaximum(0.04)
        hadds[massbins.index(massbin)].SetLineColor(6)
        hadds[massbins.index(massbin)].Draw('hist')
        hadds[massbins.index(massbin)].GetYaxis().SetTitle("#sigma * A")
        hadds[massbins.index(massbin)].GetYaxis().SetTitleOffset(1.5)
        hadds[massbins.index(massbin)].GetYaxis().SetNdivisions(505)
        hqcds[massbins.index(massbin)].SetLineColor(1)
        hqcds[massbins.index(massbin)].Draw('samehist')
        hqbhs[massbins.index(massbin)].SetLineColor(2)
        hqbhs[massbins.index(massbin)].Draw("same")
        legends[massbins.index(massbin)].SetFillStyle(0)
        legends[massbins.index(massbin)].Draw()
        canvas.Update()
        
    canvas.SaveAs(savename)
    


