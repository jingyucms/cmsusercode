from ROOT import *
import ROOT
import array, math
import os
from math import *

#! /usr/bin/env python         

def avwidth(iType,g,med,mfm):
    front=g*g*(med*med+2*mfm*mfm)/(12*med*3.141159265)
    if abs(iType) == 2:
        front=g*g*(med*med-4*mfm*mfm)/(12*med*3.141159265)
    if 2.*mfm > med:
        return 0.001
    sqrtV=math.sqrt(1-4*(mfm/med)*(mfm/med))
    return front*sqrtV

def avtotwidth(iType,gdm,gsm,med,mdm):
    u=avwidth(iType,gsm,med,0.001)
    d=u
    s=avwidth(iType,gsm,med,0.135)
    c=avwidth(iType,gsm,med,1.5)
    b=avwidth(iType,gsm,med,5.1)
    t=0
    if med > 2.*172.5:
        t=avwidth(iType,gsm,med,172.5)
    quarks=3*(u+d+s+c+b+t)
    dm=avwidth(iType,gdm,med,mdm)
    print dm/med,quarks/med
    return dm+quarks

if __name__=="__main__":

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
    mg=TMultiGraph()
    colors=[1,2,3,4,6,7,8,9,15,1,2,3,4,6,7,8,9,15]
    styles=[20,21,22,23,25,26,27,28,29,30,32,33,34]
    
    l3=TLegend(0.2,0.6,0.80,0.83,"g_{DM}=1, m_{DM}=1 GeV, m_{Med}>>m_{DM}")
    l3.SetTextSize(0.05)
    
    mMeds=[2000,2250,2500,3000,3500,4000,4500,5000,6000,7000,8000]
    mMeds=[3000]
    gqs=[0.01,0.05,0.1,0.2,0.25,0.3,0.5,0.75,1.0,1.5,2.0,2.5,3.0]
    gqs=[i/100. for i in range(200)]
    gDM=1
    mDM=1
    mq=0
    style=0
    for scenario in range(2):
     for mMed in mMeds:
       widths=[]
       for gq in gqs:
          #widthDM=gDM*gDM*mMed/12/pi*sqrt(1.-4.*mDM*mDM/mMed/mMed)*(1.+2*mDM*mDM/mMed/mMed)
	  #widthSM=gq*gq*mMed/4/pi*sqrt(1.-4.*mq*mq/mMed/mMed)*(1.+2*mq*mq/mMed/mMed)
	  #print widthDM/mMed,widthSM/mMed
	  if scenario==0:
  	    widths+=[avtotwidth(0,gDM,gq,mMed,mDM)/mMed]
	  else:
  	    widths+=[avtotwidth(2,gDM,gq,mMed,mDM)/mMed]
       pointsX=array.array("f",[float(qg) for qg in gqs])
       pointsY=array.array("f",[float(width) for width in widths])
       g=TGraph(len(pointsX),pointsX,pointsY)
       #g.SetMarkerStyle(styles[style])
       #g.SetMarkerSize(1)
       g.SetLineColor(colors[style])
       g.SetLineStyle(style)
       g.SetLineWidth(2)
       mg.Add(g)
       if scenario==0:
         l3.AddEntry(g,"Vector","pl")
       else:
         l3.AddEntry(g,"Axial","pl")
       style+=1
    
    mg.Draw("al")
    mg.SetTitle("")
    mg.GetXaxis().SetTitle("g_{q}")
    mg.GetYaxis().SetTitle("#Gamma / m_{Med}")
    mg.GetXaxis().SetRangeUser(0,1.43)
    mg.GetYaxis().SetRangeUser(0,1)

    l3.SetFillStyle(0)
    l3.Draw("same")
    
    #// writing the lumi information and the CMS "logo"
    #CMS_lumi( c, iPeriod, iPos );
    
    c.SaveAs("dm_width.pdf")
    c.SaveAs("dm_width.eps")
