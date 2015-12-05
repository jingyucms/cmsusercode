from ROOT import *
import ROOT
import array, math
import os
from math import *

def rebin(h1,nbins,binning):
    for b in range(h1.GetXaxis().GetNbins()):
        h1.SetBinContent(b+1,h1.GetBinContent(b+1)*h1.GetBinWidth(b+1))
        h1.SetBinError(b+1,h1.GetBinError(b+1)*h1.GetBinWidth(b+1))
    h1=h1.Rebin(nbins,h1.GetName()+"_rebin",binning)
    h1.Scale(1./h1.Integral())
    for b in range(h1.GetXaxis().GetNbins()):
        h1.SetBinContent(b+1,h1.GetBinContent(b+1)/h1.GetBinWidth(b+1))
        h1.SetBinError(b+1,h1.GetBinError(b+1)/h1.GetBinWidth(b+1))
    return h1

def rebin2(h1,nbins,binning):
    h1=h1.Rebin(nbins,h1.GetName()+"_rebin",binning)
    h1.Scale(1./h1.Integral())
    for b in range(h1.GetXaxis().GetNbins()):
        h1.SetBinContent(b+1,h1.GetBinContent(b+1)/h1.GetBinWidth(b+1))
        h1.SetBinError(b+1,h1.GetBinError(b+1)/h1.GetBinWidth(b+1))
    return h1

if __name__=="__main__":

    print "start ROOT"
    gROOT.Reset()
    gROOT.SetStyle("Plain")
    gStyle.SetOptStat(0)
    gStyle.SetOptFit(0)
    gStyle.SetTitleOffset(1.2,"Y")
    gStyle.SetPadLeftMargin(0.18)
    gStyle.SetPadBottomMargin(0.11)
    gStyle.SetPadTopMargin(0.055)
    gStyle.SetPadRightMargin(0.05)
    gStyle.SetMarkerSize(1.5)
    gStyle.SetHistLineWidth(1)
    gStyle.SetStatFontSize(0.020)
    gStyle.SetTitleSize(0.06, "XYZ")
    gStyle.SetLabelSize(0.05, "XYZ")
    gStyle.SetNdivisions(510, "XYZ")
    gStyle.SetLegendBorderSize(0)
    gStyle.SetPadTickX(1)
    gStyle.SetPadTickY(1)
    
    print "start CMS_lumi"

    gROOT.LoadMacro("CMS_lumi.C");
    writeExtraText = True;	 #// if extra text
    extraText  = "Preliminary";  #// default extra text is "Preliminary"
    lumi_13TeV  = "150 pb^{-1}"; #// default is "19.7 fb^{-1}"
    iPeriod = 4;	#// 1=7TeV, 2=8TeV, 3=7+8TeV, 7=7+8+13TeV 
    iPos = 1;
    #// second parameter in example_plot is iPos, which drives the position of the CMS logo in the plot
    #// iPos=11 : top-left, left-aligned
    #// iPos=33 : top-right, right-aligned
    #// iPos=22 : center, centered
    #// mode generally : 
    #//   iPos = 10*(alignement 1/2/3) + position (1/2/3 = left/center/right)

    massbins13=[(1900,2400),
              (2400,3000),
              (3000,3600),
              (3600,4200),
              (4200,4800),
              (4800,13000),
              #(5400,13000)
	      ]

    chi_bins=[(1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               #(1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,3,6,9,12,16),
              ]
    chi_binnings=[]
    for mass_bin in chi_bins:
        chi_binnings+=[array.array('d')]
        for chi_bin in mass_bin:
            chi_binnings[-1].append(chi_bin)

    c = TCanvas("combined", "combined", 0, 0, 600, 400)
    c.Divide(3,2)
    new_hists=[]
    for massbin in range(len(massbins13)):

        c.cd(massbin+1)
      
        filename="datacards/Unfolded_chiNtuple_data_2pt4invfb_teff_fromCB2_AK4SF_DataToMCSF_Pythia_M_1000to13000.root"
        masstext=str(massbins13[massbin]).strip("()").replace(',',"-").replace(' ',"")
        histname='dijet_mass1_chi2__projY_'+masstext+'_unfolded'
        f13 = TFile.Open(filename)
        new_hists+=[f13]
        print histname
        h0=f13.Get(histname)
	h0=h0.Rebin(len(chi_binnings[massbin])-1,h0.GetName()+"rebinorig",chi_binnings[massbin])
	alpha=1.-0.6827
	for b in range(h0.GetNbinsX()):
            N=h0.GetBinContent(b+1)
	    print N
	    L=0
	    if N>0:
	      L=ROOT.Math.gamma_quantile(alpha/2.,N,1.)
            U=ROOT.Math.gamma_quantile_c(alpha/2.,N+1,1.)
            h0.SetBinContent(b+1,(U-N)/N)

        filename="datacards/datacard_shapelimit13TeV_25nsData6_chi.root"
        masstext=str(massbins13[massbin]).strip("()").replace(',',"_").replace(' ',"")
        histname='data_obs#chi'+masstext+'_rebin1'
        print filename
        f14 = TFile.Open(filename)
        new_hists+=[f14]
        print histname
        h1=f14.Get(histname)
	h1=h1.Rebin(len(chi_binnings[massbin])-1,h1.GetName()+"rebinorig",chi_binnings[massbin])
	for b in range(h0.GetNbinsX()):
            N=1./pow(h1.GetBinError(b+1)/h1.GetBinContent(b+1),2)
	    print N
	    L=0
	    if N>0:
	      L=ROOT.Math.gamma_quantile(alpha/2.,N,1.)
            U=ROOT.Math.gamma_quantile_c(alpha/2.,N+1,1.)
            h1.SetBinContent(b+1,(U-N)/N)
	   
        h0.SetTitle("")
	h0.GetYaxis().SetRangeUser(0,h0.GetMaximum()*2.0)
        h0.GetXaxis().SetTitle("#chi_{dijet}")
        h0.GetYaxis().SetTitle("Fractional statistical error")
        h0.GetYaxis().SetTitleOffset(1.4)
        h0.GetXaxis().SetTitleOffset(0.8)
        h0.GetYaxis().SetTitleSize(0.05)
        h0.GetYaxis().SetLabelSize(0.04)
        h0.GetXaxis().SetTitleSize(0.05)
        h0.GetXaxis().SetLabelSize(0.04)
        h0.GetXaxis().SetTickLength(0.02)
	h0.Draw("hist")
	h1.SetLineColor(4)
	h1.SetLineStyle(2)
	h1.Draw("histsame")
        
        if massbin==0: title="1.9 < #font[72]{M_{jj}} < 2.4"
        if massbin==1: title="2.4 < #font[72]{M_{jj}} < 3.0"
        if massbin==2: title="3.0 < #font[72]{M_{jj}} < 3.6"
        if massbin==3: title="3.6 < #font[72]{M_{jj}} < 4.2"
        if massbin==4: title="4.2 < #font[72]{M_{jj}} < 4.8"
        #if massbin==5: title="4.8 < #font[72]{M_{jj}} < 5.4"
        if massbin==5: title="#font[72]{M_{jj}} > 4.8"
        #if massbin==6: title="#font[72]{M_{jj}} > 5.4"

        lo=TLegend(0.5,0.70,1.0,0.75,title)
        lo.SetTextSize(0.033)
        lo.SetFillStyle(0)
        lo.Draw("same")
        new_hists+=[lo]

        l2=TLegend(0.23,0.77,0.76,0.93,"")
        l2.SetTextSize(0.035)
        l2.AddEntry(h0,"Unfolded data","l")
        l2.AddEntry(h1,"Raw data","l")
        l2.SetFillStyle(0)
        l2.Draw("same")
        new_hists+=[l2]

    c.SaveAs("unfolded_error_RunII_25ns.pdf")
    c.SaveAs("unfolded_error_RunII_25ns.eps")
