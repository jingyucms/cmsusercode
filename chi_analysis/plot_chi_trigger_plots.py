import os, sys
import array
from ROOT import * 

gROOT.Reset()
gROOT.SetStyle("Plain")
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetTitleOffset(1.2,"Y")
gStyle.SetPadLeftMargin(0.18)
gStyle.SetPadBottomMargin(0.15)
gStyle.SetPadTopMargin(0.08)
gStyle.SetPadRightMargin(0.05)
gStyle.SetMarkerSize(0.5)
gStyle.SetHistLineWidth(1)
gStyle.SetStatFontSize(0.020)
gStyle.SetTitleSize(0.06, "XYZ")
gStyle.SetLabelSize(0.05, "XYZ")
gStyle.SetNdivisions(506, "XYZ")
gStyle.SetLegendBorderSize(0)

if __name__ == '__main__':

  colors=[1,2,3,4,6,7,8,9,10,11,12,13]
  styles=[1,2,3,4,5,6,7,8,9,11,12,13]

  samples=["ReRun2012A","ReRun2012B","ReRun2012C","ReRun2012D"]
  for sample in samples:
   f=TFile.Open("chi_"+sample+".root")

   canvas = TCanvas("","",0,0,200,200)
   legend=TLegend(0.5,0.7,0.95,0.90,"")
   
   bins=[500,550,600,650,700,750,800,850,900,950,1000,1100,1200,1300,1400,1500,1600,1700,1800,2000,2500,3000,5000]
   binning=array.array('d')
   for bin in bins:
       binning.append(bin)
   
   hist1=f.Get("dijet_mass_ref")
   hist1=hist1.Rebin(len(binning)-1,hist1.GetName()+"_rebin",binning)
   hist2=f.Get("dijet_mass_trig")
   hist2=hist2.Rebin(len(binning)-1,hist2.GetName()+"_rebin",binning)
   hist=TGraphAsymmErrors(hist1)
   hist.Divide(hist2,hist1,"cl=0.683 b(1,1) mode")
   hist.SetLineWidth(2)
   hist.SetTitle("")
   hist.GetXaxis().SetTitle("dijet mass")
   hist.GetYaxis().SetTitle("trigger efficiency")
   hist.GetXaxis().SetRangeUser(500,5000)
   hist.GetYaxis().SetRangeUser(0,1)
   hist.Draw("ale")

   legend.SetTextSize(0.04)
   legend.SetFillStyle(0)
   legend.Draw("same")

   canvas.SaveAs("chi_trigger_plots_"+sample+".root")
   canvas.SaveAs("chi_trigger_plots_"+sample+".pdf")
