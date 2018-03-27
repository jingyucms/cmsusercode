from ROOT import *
import ROOT
import array, math
import os
from math import *

#! /usr/bin/env python         

if __name__=="__main__":

  for mDM in [1,3000]:

    print "start ROOT"
    gROOT.Reset()
    gROOT.SetStyle("Plain")
    gStyle.SetOptStat(0)
    gStyle.SetOptFit(0)
    gStyle.SetTitleOffset(1.2,"Y")
    gStyle.SetPadLeftMargin(0.16)
    gStyle.SetPadBottomMargin(0.16)
    gStyle.SetPadTopMargin(0.05)
    gStyle.SetPadRightMargin(0.05)
    gStyle.SetMarkerSize(2.5)
    gStyle.SetHistLineWidth(1)
    gStyle.SetStatFontSize(0.020)
    gStyle.SetTitleSize(0.06, "XYZ")
    gStyle.SetLabelSize(0.05, "XYZ")
    gStyle.SetLegendBorderSize(0)
    gStyle.SetPadTickX(1)
    gStyle.SetPadTickY(1)
    gStyle.SetEndErrorSize(5)

    print "start CMS_lumi"

    #gROOT.LoadMacro("CMS_lumi.C");
    #iPeriod = 4;	#// 1=7TeV, 2=8TeV, 3=7+8TeV, 7=7+8+13TeV 
    #iPos = 11;
    
    c = TCanvas("dmwidth", "dmwidth", 0, 0, 300, 300)
    c.SetLogy()
    mg=TMultiGraph()
    colors=[1,2,3,4,6,7,8,9,15,1,2,3,4,6,7,8,9,15]
    styles=[20,21,22,23,25,26,27,28,29,30,32,33,34]
    
    if mDM==1:
      l3=TLegend(0.4,0.2,0.8,0.5,"g_{DM}=1, m_{DM}=1 GeV")
    else:
      l3=TLegend(0.4,0.2,0.8,0.5,"g_{DM}=1, m_{DM}>m_{Med}")
    l3.SetTextSize(0.05)
    
    style=0
    for scenario in range(4):
       pointsX=array.array("f",[1,1.5,2,2.5,3,4,5,6])
       if mDM==1:
        if scenario==0:
         pointsY=array.array("f",[0.00061,0.0026,0.0140,0.163,0.336,0.332,0.239,0.154])
        elif scenario==1:
         pointsY=array.array("f",[0.00093,0.0036,0.0164,0.158,0.326,0.340,0.224,0.173])
        elif scenario==2:
         pointsY=array.array("f",[0.00095,0.0052,0.0261,0.085,0.134,0.141,0.121,0.097])
        else:
         pointsY=array.array("f",[0.00102,0.0044,0.0299,0.081,0.137,0.153,0.114,0.111])
       else:
        if scenario==0:
	 pointsX=array.array("f",[1,1.5,2.5,3,5,6])
         pointsY=array.array("f",[0.000438,0.00239,0.1815,0.368,0.262,0.164])
        elif scenario==1:
	 pointsX=array.array("f",[1,2,2.5,4,5])
         pointsY=array.array("f",[0.00093,0.02538,0.0888,0.147,0.122])
        elif scenario==2:
	 pointsX=array.array("f",[1.5,2,3,4,6])
         pointsY=array.array("f",[0.0034,0.01349,0.339,0.4299,0.178])
        else:
	 pointsX=array.array("f",[1,1.5,2.5,3,5,6])
         pointsY=array.array("f",[0.0004,0.0061,0.0831,0.138,0.095,0.108])
       g=TGraph(len(pointsX),pointsX,pointsY)
       #g.SetMarkerStyle(styles[style])
       #g.SetMarkerSize(1)
       g.SetLineColor(colors[style])
       g.SetLineStyle(style+1)
       g.SetLineWidth(2)
       mg.Add(g)
       if scenario==0:
         l3.AddEntry(g,"Axial g_{q}=0.5","pl")
       elif scenario==1:
         l3.AddEntry(g,"Vector g_{q}=0.5","pl")
       elif scenario==2:
         l3.AddEntry(g,"Axial g_{q}=1.0","pl")
       else:
         l3.AddEntry(g,"Vector g_{q}=1.0","pl")
       style+=1
    
    mg.Draw("al")
    mg.SetTitle("")
    mg.GetXaxis().SetTitle("m_{Med} (TeV)")
    mg.GetYaxis().SetTitle("Acceptance")
    mg.GetXaxis().SetRangeUser(1,6)
    mg.GetYaxis().SetRangeUser(0.0005,1)

    l3.SetFillStyle(0)
    l3.Draw("same")
    
    #// writing the lumi information and the CMS "logo"
    #CMS_lumi( c, iPeriod, iPos );
    
    c.SaveAs("dm_acceptance"+str(mDM)+".pdf")
    c.SaveAs("dm_acceptance"+str(mDM)+".eps")
