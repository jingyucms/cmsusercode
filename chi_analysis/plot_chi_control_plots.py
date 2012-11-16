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

   prefix="HCP"

   data=["chi_Run2012A",
         "chi_Run2012Ar",
         "chi_Run2012B",
         "chi_Run2012C1_fast",
         "chi_Run2012C2_fast",
         ]
   data2=[#"chi_Run2012A",
         #"chi_Run2012Ar",
         #"chi_Run2012B",
         #"chi_Run2012C1_fast",
         "chi_Run2012C2_fast",
         ]
   mc=[("chi_QCD_1000",204.0/13479218),
       ("chi_QCD_500",8426.0/31743483),
       ("chi_QCD_250",276000.0/26900255),
       ("chi_QCD_100",1.036e7/48365102),
       ]
   f_data=[]
   f_data2=[]
   for name in data:
      f_data+=[TFile.Open(name+".root")]
   for name in data2:
      f_data2+=[TFile.Open(name+".root")]
   f_mc=[]
   for name,xsec in mc:
      f_mc+=[TFile.Open(name+".root")]

   canvas = TCanvas("","",0,0,200,200)
   canvas.SetLogy(True)
   legend=TLegend(0.45,0.7,0.95,0.90,"#Chi<16 , y_{boost}<1.11")

   hist=f_data[0].Get("dijet_mass")
   for i in range(1,len(data)):
       hist.Add(f_data[i].Get("dijet_mass"))
   hist.SetLineWidth(2)
   hist.SetLineColor(1)
   hist.SetTitle("")
   hist.GetXaxis().SetTitle("dijet mass")
   hist.GetYaxis().SetTitle("N")
   hist.GetXaxis().SetRangeUser(1900,6000)
   hist.GetYaxis().SetRangeUser(0.5,hist.GetMaximum()*1.5)
   hist.GetXaxis().SetTitleOffset(1.1)
   hist.GetYaxis().SetTitleOffset(1.1)
   hist.GetXaxis().SetLabelSize(0.05)
   hist.GetYaxis().SetLabelSize(0.05)
   hist.GetXaxis().SetTitleSize(0.06)
   hist.GetYaxis().SetTitleSize(0.06)
   hist.Draw("le")
   legend.AddEntry(hist,"2012ABC","l")

   hist2=f_data2[0].Get("dijet_mass")
   for i in range(1,len(data2)):
       hist2.Add(f_data2[i].Get("dijet_mass"))
   hist2.Scale(hist.Integral(hist.FindBin(1900),hist.GetNbinsX())/hist2.Integral(hist2.FindBin(1900),hist2.GetNbinsX()))
   hist2.SetLineWidth(2)
   hist2.SetLineColor(4)
   hist2.Draw("lesame")
   legend.AddEntry(hist2,"2012C2","l")

   hist_mc=f_mc[0].Get("dijet_mass")
   for i in range(1,len(mc)):
       hist_mc.Add(f_mc[i].Get("dijet_mass"),mc[i][1]/mc[0][1])
   hist_mc.Scale(hist.Integral(hist.FindBin(1900),hist.GetNbinsX())/hist_mc.Integral(hist_mc.FindBin(1900),hist_mc.GetNbinsX()))
   hist_mc.SetLineWidth(2)
   hist_mc.SetLineColor(2)
   hist_mc.Draw("histsame")
   legend.AddEntry(hist_mc,"QCD MC","l")

   legend.SetTextSize(0.04)
   legend.SetFillStyle(0)
   legend.Draw("same")

   canvas.SaveAs("chi_control_plots_mass_"+prefix+".root")
   canvas.SaveAs("chi_control_plots_mass_"+prefix+".pdf")

   for var in variables:
    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    log="pt" in var or "et" in var or "dphi" in var
    legends=[]
    for mass in range(len(masses)-1):
        canvas.cd(mass+1)
        canvas.GetPad(mass+1).SetLogy(log)
        legend=TLegend(0.45,0.7,0.95,0.90,str(masses[mass])+"<m_{jj}<"+str(masses[mass+1])+" GeV")
	legends+=[legend]
    
        hist=f_data[0].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var)
        for i in range(1,len(data)):
            hist.Add(f_data[i].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var))
        hist.SetLineWidth(2)
      	hist.SetLineColor(1)
	if "metsumet" in var:
	    hist.Rebin(4)
	miny=0
	if hist.Integral()>0:
            miny=log*0.1
	hist.SetTitle("")
	hist.GetXaxis().SetTitle(label[variables.index(var)])
	hist.GetYaxis().SetTitle("N")
	hist.GetYaxis().SetRangeUser(miny,hist.GetMaximum()*(1.5+log*10))
        hist.GetXaxis().SetTitleOffset(1.1)
        hist.GetYaxis().SetTitleOffset(1.1)
        hist.GetXaxis().SetLabelSize(0.05)
        hist.GetYaxis().SetLabelSize(0.05)
        hist.GetXaxis().SetTitleSize(0.06)
        hist.GetYaxis().SetTitleSize(0.06)
        hist.Draw("le")
        legend.AddEntry(hist,"2012ABC","l")

        hist2=f_data2[0].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var)
        for i in range(1,len(data2)):
            hist2.Add(f_data2[i].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var))
	if hist2.Integral()>0:
            hist2.Scale(hist.Integral()/hist2.Integral())
        hist2.SetLineWidth(2)
      	hist2.SetLineColor(4)
	if "metsumet" in var:
	    hist2.Rebin(4)
	miny=0
	if hist2.Integral()>0:
            miny=log*0.1
	hist2.SetTitle("")
        hist2.Draw("lesame")
        legend.AddEntry(hist2,"2012C2","l")

     	hist_mc=f_mc[0].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var)
     	for i in range(1,len(mc)):
     	    hist_mc.Add(f_mc[i].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var),mc[i][1]/mc[0][1])
	if hist_mc.Integral()>0:
            hist_mc.Scale(hist.Integral()/hist_mc.Integral())
        hist_mc.SetLineWidth(2)
      	hist_mc.SetLineColor(2)
	if "metsumet" in var:
	    hist_mc.Rebin(4)
        hist_mc.Draw("histsame")
        legend.AddEntry(hist_mc,"QCD MC","l")

        legend.SetTextSize(0.04)
        legend.SetFillStyle(0)
        legend.Draw("same")

    canvas.SaveAs("chi_control_plots"+var+"_"+prefix+".root")
    canvas.SaveAs("chi_control_plots"+var+"_"+prefix+".pdf")
