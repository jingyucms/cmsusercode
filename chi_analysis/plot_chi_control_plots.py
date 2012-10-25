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
gStyle.SetNdivisions(510, "XYZ")
gStyle.SetLegendBorderSize(0)

if __name__ == '__main__':

   variables=["chi","pt1","pt2","y1","y2","yboost","metsumet","mptsumpt","dphi"]
   label=["#chi","p_{T1}","p_{T2}","y_{1}","y_{2}","y_{boost}","missing E_{T} / #sum E_{T}","#sum #vec p_{T} / #sum |p_{T}|","#Delta #phi"]

   masses=[1900,2400,3000,4000,5000]

   colors=[1,2,3,4,6,7,8,9,10,11,12,13]
   styles=[1,2,3,4,5,6,7,8,9,11,12,13]

   #data="5fb_5TeV"
   #data="8fb_5TeV"
   data="11_9fb"
   f=TFile.Open("data_"+data+".root")

   canvas = TCanvas("","",0,0,200,200)
   canvas.SetLogy(True)
   hist=f.Get("dijet_mass")
   hist.SetLineWidth(2)
   hist.SetTitle("")
   hist.GetXaxis().SetTitle("dijet mass")
   hist.GetYaxis().SetRangeUser(0.5,hist.GetMaximum()*1.5)
   hist.Draw("he")
   canvas.SaveAs("chi_control_plots_mass_"+data+".root")
   canvas.SaveAs("chi_control_plots_mass_"+data+".pdf")

   for var in variables:
    canvas = TCanvas("","",0,0,200,200)
    log="pt" in var or "et" in var or "dphi" in var
    canvas.SetLogy(log)
    index=0
    legend=TLegend(0.5,0.7,0.95,0.90,"")
    
    for mass in range(len(masses)-1):
        hist=f.Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var)
        hist.SetLineColor(colors[index])
        hist.SetLineStyle(styles[index])
        hist.SetLineWidth(2)
	if "metsumet" in var:
	    hist.Rebin(4)
	miny=0
	if hist.Integral()>0:
            miny=log/hist.Integral()
            hist.Scale(1./hist.Integral())
	hist.SetTitle("")
	hist.GetXaxis().SetTitle(label[variables.index(var)])
	hist.GetYaxis().SetRangeUser(miny,hist.GetMaximum()*1.5)
	if index==0:
            hist.Draw("he")
        else:	
            hist.Draw("hesame")
	index+=1
        legend.AddEntry(hist,str(masses[mass])+"<m_{jj}<"+str(masses[mass+1])+" GeV","l")

    legend.SetTextSize(0.04)
    legend.SetFillStyle(0)
    legend.Draw("same")

    canvas.SaveAs("chi_control_plots"+var+"_"+data+".root")
    canvas.SaveAs("chi_control_plots"+var+"_"+data+".pdf")
