from ROOT import *
import ROOT,sys,os,math
from math import *
import numpy as np

gROOT.ForceStyle()
gStyle.SetLegendBorderSize(0)
gStyle.SetPadTickX(1)
#gStyle.SetPadTickY(1)
gStyle.SetPadLeftMargin(0.09)
gStyle.SetPadBottomMargin(0.12)
gStyle.SetPadTopMargin(0.075)
gStyle.SetPadRightMargin(0.09)


def SetCurveStyle(gr,color,lineStyle,lineWidth,markerSize):
    gr.SetMarkerColor(color)
    gr.SetMarkerSize(markerSize)
    gr.SetLineColor(color)
    gr.SetLineWidth(lineWidth)
    gr.SetFillStyle(lineStyle)
    gr.SetFillColor(color)
    return 


def medWidth(gq):
  return 6*gq**2/(4*3.141592653)+1/(12*3.141592653)

if __name__=="__main__":

    file_res=TFile("gB.root")
    file_chi=TFile("limitsLHCa_DMAxial_mdm1_v4.root")

    exp_res=file_res.Get("exp")
    SetCurveStyle(exp_res,kRed-10,3004,402,0.1)
    
    obs_res=file_res.Get("obs")
    SetCurveStyle(obs_res,kRed+2,3004,402,0.1)

    exp_chi=file_chi.Get("gq_exp")
    SetCurveStyle(exp_chi,kAzure+6,3004,402,0.1)
    
    obs_chi=file_chi.Get("gq_obs")
    SetCurveStyle(obs_chi,kAzure,3004,402,0.1)

    canvas=TCanvas("myCanvas","myCanvas",0,0,1600,1200)

    mg=TMultiGraph()

    #exp_res.Draw()
    #obs_res.Draw("same")
    #exp_chi.Draw("same")
    #obs_chi.Draw("same")

    mg.Add(exp_res,"l")
    mg.Add(obs_res,"l")
    mg.Add(exp_chi,"l")
    mg.Add(obs_chi,"l")

    xmin=400
    xmax=6000

    ymin=0.
    ymax=1.42788
    
    mg.Draw("apl")
    mg.GetYaxis().SetRangeUser(ymin,ymax)
    mg.GetYaxis().SetTitle("g_{q}")
    mg.GetYaxis().SetTitleOffset(0.8)
    mg.GetYaxis().SetTitleSize(0.05)
    mg.GetYaxis().SetLabelSize(0.04)
    
    mg.GetXaxis().SetLimits(xmin,xmax)
    mg.GetXaxis().SetTitle("M_{Med} [GeV]")
    mg.GetXaxis().SetTitleOffset(0.95)
    mg.GetXaxis().SetTitleSize(0.05)
    mg.GetXaxis().SetLabelSize(0.04)
    
    minwidth=medWidth(ymin)
    myFunc=TF1("myFunc","pow((x-1/(12*3.141592653))*(4*3.141592653)/6,0.5)",minwidth,1)
    y2=TGaxis(xmax, ymin, xmax, ymax,"myFunc",510, "+L")
    y2.SetTitle("#Gamma/M_{Med}")
    y2.SetLabelSize(0.04)
    y2.SetTitleSize(0.05)
    y2.SetTitleOffset(0.8)
    y2.Draw()

    upper_exp_res=TGraph(0)
    upper_exp_res.SetPoint(upper_exp_res.GetN(),600,exp_res.Eval(600))
    upper_exp_res.SetPoint(upper_exp_res.GetN(),600,0.5)
    upper_exp_res.SetPoint(upper_exp_res.GetN(),3700,0.5)
    upper_exp_res.SetPoint(upper_exp_res.GetN(),3700,exp_res.Eval(3700))
    SetCurveStyle(upper_exp_res,kRed-10,3004,-402,0.1)
    #upper_exp_res.Draw()

    upper_obs_res=TGraph(0)
    upper_obs_res.SetPoint(upper_obs_res.GetN(),600,obs_res.Eval(600))
    upper_obs_res.SetPoint(upper_obs_res.GetN(),600,0.5)
    upper_obs_res.SetPoint(upper_obs_res.GetN(),3700,0.5)
    upper_obs_res.SetPoint(upper_obs_res.GetN(),3700,obs_res.Eval(3700))
    SetCurveStyle(upper_obs_res,kRed+2,3004,-402,0.1)
    #upper_obs_res.Draw("same")

    upper_exp_chi=TGraph(0)
    upper_exp_chi.SetPoint(upper_exp_chi.GetN(),2500,exp_chi.Eval(2500))
    upper_exp_chi.SetPoint(upper_exp_chi.GetN(),2500,1.5)
    #upper_exp_chi.SetPoint(upper_exp_chi.GetN(),6000,0.5)
    #upper_exp_chi.SetPoint(upper_exp_chi.GetN(),6000,exp_chi.Eval(6000))
    SetCurveStyle(upper_exp_chi,kAzure+6,3004,-402,0.1)
    #upper_exp_chi.Draw("same")

    upper_obs_chi=TGraph(0)
    upper_obs_chi.SetPoint(upper_obs_chi.GetN(),2500,obs_chi.Eval(2500))
    upper_obs_chi.SetPoint(upper_obs_chi.GetN(),2500,1.5)
    #upper_obs_chi.SetPoint(upper_obs_chi.GetN(),6000,0.5)
    #upper_obs_chi.SetPoint(upper_obs_chi.GetN(),6000,obs_chi.Eval(6000))
    SetCurveStyle(upper_obs_chi,kAzure,3004,-402,0.1)
    #upper_obs_chi.Draw("same")

    l0p5=TLine(xmin,0.4,xmax,0.4)
    l0p5.SetLineColor(kGray+1)
    l0p5.SetLineStyle(kDashed)
    l0p5.Draw("same")
    l0p5T=TLatex((xmax-xmin)*0.4+xmin,0.4+0.05,"g_{q}=0.4, #Gamma/M_{Med}=10%")
    l0p5T.SetTextSize(0.03)
    l0p5T.SetTextColor(kGray+1)
    l0p5T.Draw("same")

    l1p0=TLine(xmin,1,xmax,1)
    l1p0.SetLineColor(kGray+1)
    l1p0.SetLineStyle(kDashed)
    l1p0.Draw("same")
    l1p0T=TLatex((xmax-xmin)*0.4+xmin,1+0.05,"g_{q}=1.0, #Gamma/M_{Med}=50%")
    l1p0T.SetTextSize(0.03)
    l1p0T.SetTextColor(kGray+1)
    l1p0T.Draw("same")

    leg=TLegend(0.62,0.135,0.8,0.4,"          CMS 95% CL")
    leg.SetFillStyle(0)
    leg.SetTextSize(0.03)
    leg.AddEntry(obs_chi,"Dijet Chi Observed","fl")
    leg.AddEntry(exp_chi,"Dijet Chi Expected","fl")
    leg.AddEntry(obs_res,"Dijet Resonance Observed","fl")
    leg.AddEntry(exp_res,"Dijet Resonance Expected","fl")
    leg.Draw()


    # CMS
    #leg2=TLatex(xmin,ymax+0.03,"#bf{CMS} #it{Preliminary}")
    leg2=TLatex(xmin,ymax+0.03,"#bf{CMS} #it{Supplementary}")
    leg2.SetTextFont(42)
    leg2.SetTextSize(0.04)
    # lumi
    leg3=TLatex(xmax-1300,ymax+0.03,"35.9 fb^{-1} (13 TeV)")
    leg3.SetTextFont(42)
    leg3.SetTextSize(0.04)
    leg2.Draw("same")
    leg3.Draw("same")
    
    canvas.SaveAs("~/Desktop/dijet_combined_gq.pdf")

    
    
