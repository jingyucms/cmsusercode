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

   variables=["chi","pt1","pt2","y1","y2","yboost","metsumet","mptsumpt","dphi","dpt"]
   label=["#chi","p_{T1}","p_{T2}","y_{1}","y_{2}","y_{boost}","missing E_{T} / #sum E_{T}","#sum #vec p_{T} / #sum |p_{T}|","#Delta #phi","#Delta p_{T} / #sum p_T"]

   masses=[1900,2400,3000,3600,4200,7000]

   colors=[1,2,3,4,6,7,8,9,10,11,12,13]
   styles=[1,2,3,4,5,6,7,8,9,11,12,13]

   chi_bins=[(1,2,3,4,5,6,7,8,9,10,12,14,16),
             (1,2,3,4,5,6,7,8,9,10,12,14,16),
             (1,2,3,4,5,6,7,8,9,10,12,14,16),
             (1,2,3,4,5,6,7,8,9,10,12,14,16),
             (1,3,5,7,10,12,14,16),
             ]
   chi_binnings=[]
   for mass_bin in chi_bins:
        chi_binnings+=[array.array('d')]
        for chi_bin in mass_bin:
            chi_binnings[-1].append(chi_bin)
   
   prefix="2012"

   data=["chi_EPS3",
         ]
   data2=["chi_ReRun2012D",
         ]
   mc=[("chi_QCD_1000",204.0/13479218),
       ("chi_QCD_500",8426.0/31743483),
       ("chi_QCD_250",276000.0/26900255),
       ("chi_QCD_100",1.036e7/48365102),
       ]
   mc2=[("chi_QCDHerwig",1.0),]
   mc3=[("chi_QCDPythia8170",37974.99/800046),
        ("chi_QCDPythia8300",1938.868/490042),
        ("chi_QCDPythia8470",124.8942/500051),
        ("chi_QCDPythia8600",29.55049/492988),
        ("chi_QCDPythia8800",3.871308/400059),
        ("chi_QCDPythia81000",0.8031018/400050),
        ("chi_QCDPythia81400",0.03637225/200070),
        ("chi_QCDPythia81800",0.00197726/194313),
         ]
   f_data=[]
   f_data2=[]
   for name in data:
      f_data+=[TFile.Open(name+".root")]
   for name in data2:
      f_data2+=[TFile.Open(name+".root")]
   f_mc=[]
   f_mc2=[]
   f_mc3=[]
   for name,xsec in mc:
      f_mc+=[TFile.Open(name+".root")]
   for name,xsec in mc2:
      f_mc2+=[TFile.Open(name+".root")]
   for name,xsec in mc3:
      f_mc3+=[TFile.Open(name+".root")]

   canvas = TCanvas("","",0,0,200,260)
   canvas.Divide(1,2,0,0,0)
   canvas.GetPad(1).SetPad(0.0,0.28,1.0,1.0)
   canvas.GetPad(1).SetLeftMargin(0.15)
   canvas.GetPad(1).SetRightMargin(0.08)
   canvas.GetPad(1).SetTopMargin(0.08)
   canvas.GetPad(1).SetBottomMargin(0.05)
   canvas.GetPad(2).SetPad(0.0,0.0,1.0,0.28)
   canvas.GetPad(2).SetLeftMargin(0.15)
   canvas.GetPad(2).SetRightMargin(0.08)
   canvas.GetPad(2).SetTopMargin(0.08)
   canvas.GetPad(2).SetBottomMargin(0.45)
   canvas.cd(1)
   canvas.GetPad(1).SetLogy(True)
   legend=TLegend(0.45,0.7,0.95,0.90,"#Chi<16 , y_{boost}<1.11")

   hist=f_data[0].Get("dijet_mass")
   for i in range(1,len(data)):
       hist.Add(f_data[i].Get("dijet_mass"))
   hist.SetLineColor(1)
   hist.SetMarkerStyle(24)
   hist.SetMarkerSize(0.2)
   hist.SetTitle("")
   #hist.GetXaxis().SetTitle("dijet mass")
   hist.GetXaxis().SetLabelColor(0)
   hist.GetYaxis().SetTitle("N")
   hist.GetXaxis().SetRangeUser(1900,6000)
   hist.GetYaxis().SetRangeUser(0.5,hist.GetMaximum()*1.5)
   hist.GetXaxis().SetTitleOffset(1.1)
   hist.GetYaxis().SetTitleOffset(1.1)
   hist.GetXaxis().SetLabelSize(0.05)
   hist.GetYaxis().SetLabelSize(0.05)
   hist.GetXaxis().SetTitleSize(0.06)
   hist.GetYaxis().SetTitleSize(0.06)
   hist.SetStats(False)
   hist.Draw("pe")
   legend.AddEntry(hist,"2012ABCD","l")

   hist2=f_data2[0].Get("dijet_mass")
   for i in range(1,len(data2)):
       hist2.Add(f_data2[i].Get("dijet_mass"))
   hist2.SetLineColor(4)
   hist2.SetMarkerStyle(25)
   hist2.SetMarkerSize(0.2)
   hist2.SetStats(False)
   #hist2.Draw("pesame")
   #legend.AddEntry(hist2,"2012D","l")

   hist_mc=f_mc[0].Get("dijet_mass")
   for i in range(1,len(mc)):
       hist_mc.Add(f_mc[i].Get("dijet_mass"),mc[i][1]/mc[0][1])
   hist_mc.Scale(hist.Integral(hist.FindBin(1900),hist.GetNbinsX())/hist_mc.Integral(hist_mc.FindBin(1900),hist_mc.GetNbinsX()))
   hist_mc.SetLineColor(2)
   hist_mc.SetStats(False)
   hist_mc.Draw("histsame")
   legend.AddEntry(hist_mc,"MG+Pythia6 QCD","l")

   hist_mc3=f_mc3[0].Get("dijet_mass")
   for i in range(1,len(mc3)):
       hist_mc3.Add(f_mc3[i].Get("dijet_mass"),mc3[i][1]/mc3[0][1])
   hist_mc3.Scale(hist.Integral(hist.FindBin(1900),hist.GetNbinsX())/hist_mc3.Integral(hist_mc3.FindBin(1900),hist_mc3.GetNbinsX()))
   hist_mc3.SetLineColor(4)
   hist_mc3.SetStats(False)
   hist_mc3.Draw("histsame")
   legend.AddEntry(hist_mc3,"Pythia8 QCD","l")

   hist_mc2=f_mc2[0].Get("dijet_mass")
   for i in range(1,len(mc2)):
       hist_mc2.Add(f_mc2[i].Get("dijet_mass"),mc2[i][1]/mc2[0][1])
   hist_mc2.Scale(hist.Integral(hist.FindBin(1900),hist.GetNbinsX())/hist_mc2.Integral(hist_mc2.FindBin(1900),hist_mc2.GetNbinsX()))
   hist_mc2.SetLineColor(6)
   hist_mc2.SetStats(False)
   hist_mc2.Draw("histsame")
   legend.AddEntry(hist_mc2,"Herwig++ QCD","l")

   #hist2.Draw("pesame")
   hist.Draw("pesame")

   legend.SetTextSize(0.04)
   legend.SetFillStyle(0)
   legend.Draw("same")

   canvas.cd(2)
   ratio=hist.Clone(hist.GetName()+"clone")
   ratio.Divide(hist,hist)
   for b in range(hist.GetNbinsX()):
     if hist.GetBinContent(b+1)>0:
       ratio.SetBinError(b+1,hist.GetBinError(b+1)/hist.GetBinContent(b+1))
   ratio.SetTitle("")
   ratio.GetYaxis().SetTitle("Data / Sim")
   ratio.GetYaxis().SetTitleSize(0.13)
   ratio.GetYaxis().SetTitleOffset(0.5)
   ratio.SetMarkerSize(0.1)
   ratio.GetYaxis().SetLabelSize(0.14)
   ratio.GetYaxis().SetRangeUser(0,2)
   ratio.GetXaxis().SetNdivisions(506)
   ratio.GetYaxis().SetNdivisions(503)
   ratio.GetXaxis().SetLabelColor(1)
   ratio.GetXaxis().SetTitle("dijet mass")
   ratio.GetXaxis().SetTitleSize(0.16)
   ratio.GetXaxis().SetTitleOffset(1.1)
   ratio.GetXaxis().SetLabelSize(0.14)
   ratio.Draw("histe")
   ratio_mc=hist_mc.Clone(hist_mc.GetName()+"clone")
   ratio_mc.Divide(hist_mc,hist)
   for b in range(hist.GetNbinsX()):
     if hist.GetBinContent(b+1)>0:
       ratio_mc.SetBinError(b+1,hist.GetBinError(b+1)/hist.GetBinContent(b+1))
   ratio_mc.Draw("histsame")
   ratio_mc2=hist_mc2.Clone(hist_mc2.GetName()+"clone")
   ratio_mc2.Divide(hist_mc2,hist)
   for b in range(hist.GetNbinsX()):
     if hist.GetBinContent(b+1)>0:
       ratio_mc2.SetBinError(b+1,hist.GetBinError(b+1)/hist.GetBinContent(b+1))
   ratio_mc2.Draw("histsame")
   ratio_mc3=hist_mc3.Clone(hist_mc3.GetName()+"clone")
   ratio_mc3.Divide(hist_mc3,hist)
   for b in range(hist.GetNbinsX()):
     if hist.GetBinContent(b+1)>0:
       ratio_mc3.SetBinError(b+1,hist.GetBinError(b+1)/hist.GetBinContent(b+1))
   ratio_mc3.Draw("histsame")
   canvas.cd(1)
   hist.GetYaxis().SetTitleOffset(1.2)

   canvas.SaveAs("chi_control_plots_mass_"+prefix+".root")
   canvas.SaveAs("chi_control_plots_mass_"+prefix+".pdf")

   for var in variables:
    log="pt" in var or "et" in var or "dphi" in var
    legends=[]
    for mass in range(len(masses)-1):
        canvas = TCanvas("","",0,0,200,260)
        canvas.Divide(1,2,0,0,0)
        canvas.GetPad(1).SetPad(0.0,0.28,1.0,1.0)
        canvas.GetPad(1).SetLeftMargin(0.15)
        canvas.GetPad(1).SetRightMargin(0.08)
        canvas.GetPad(1).SetTopMargin(0.08)
        canvas.GetPad(1).SetBottomMargin(0.05)
        canvas.GetPad(2).SetPad(0.0,0.0,1.0,0.28)
        canvas.GetPad(2).SetLeftMargin(0.15)
        canvas.GetPad(2).SetRightMargin(0.08)
        canvas.GetPad(2).SetTopMargin(0.08)
        canvas.GetPad(2).SetBottomMargin(0.45)
        canvas.cd(1)
        canvas.GetPad(1).SetLogy(log)
        legend=TLegend(0.45,0.7,0.95,0.90,(str(masses[mass])+"<m_{jj}<"+str(masses[mass+1])+" GeV").replace("4200<m_{jj}<7000","m_{jj}>4200").replace("4200<m_{jj}<8000","m_{jj}>4200"))
	legends+=[legend]
    
        hist=f_data[0].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var)
        for i in range(1,len(data)):
            hist.Add(f_data[i].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var))
	if var=="chi":
            hist=hist.Rebin(len(chi_binnings[mass])-1,hist.GetName()+"_rebin1",chi_binnings[mass])
      	hist.SetLineColor(1)
        hist.SetMarkerStyle(24)
        hist.SetMarkerSize(0.2)
	if "metsumet" in var:
	    hist.Rebin(4)
	miny=0
	if hist.Integral()>0:
            miny=log*0.1
	hist.SetTitle("")
	#hist.GetXaxis().SetTitle(label[variables.index(var)])
        hist.GetXaxis().SetLabelColor(0)
	hist.GetYaxis().SetTitle("N")
	hist.GetYaxis().SetRangeUser(miny,hist.GetMaximum()*(1.5+log*10))
        #hist.GetXaxis().SetTitleOffset(1.1)
        hist.GetYaxis().SetTitleOffset(1.1)
        hist.GetXaxis().SetLabelSize(0.05)
        hist.GetYaxis().SetLabelSize(0.05)
        hist.GetXaxis().SetTitleSize(0.06)
        hist.GetYaxis().SetTitleSize(0.06)
        hist.SetStats(False)
        hist.Draw("le")
        legend.AddEntry(hist,"2012ABCD","l")

        hist2=f_data2[0].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var)
        for i in range(1,len(data2)):
            hist2.Add(f_data2[i].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var))
	if var=="chi":
            hist2=hist2.Rebin(len(chi_binnings[mass])-1,hist2.GetName()+"_rebin1",chi_binnings[mass])
      	hist2.SetLineColor(4)
        hist2.SetMarkerStyle(25)
        hist2.SetMarkerSize(0.2)
	if "metsumet" in var:
	    hist2.Rebin(4)
	miny=0
	if hist2.Integral()>0:
            miny=log*0.1
	hist2.SetTitle("")
        hist2.SetStats(False)
        #hist2.Draw("lesame")
        #legend.AddEntry(hist2,"2012D","l")

     	hist_mc=f_mc[0].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var)
     	for i in range(1,len(mc)):
     	    hist_mc.Add(f_mc[i].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var),mc[i][1]/mc[0][1])
	if var=="chi":
            hist_mc=hist_mc.Rebin(len(chi_binnings[mass])-1,hist_mc.GetName()+"_rebin1",chi_binnings[mass])
	if hist_mc.Integral()>0:
            hist_mc.Scale(hist.Integral()/hist_mc.Integral())
      	hist_mc.SetLineColor(2)
	if "metsumet" in var:
	    hist_mc.Rebin(4)
        hist_mc.SetStats(False)
        hist_mc.Draw("histsame")
        legend.AddEntry(hist_mc,"MG+Pythia6 QCD","l")

     	hist_mc3=f_mc3[0].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var)
     	for i in range(1,len(mc3)):
     	    hist_mc3.Add(f_mc3[i].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var),mc3[i][1]/mc3[0][1])
	if var=="chi":
            hist_mc3=hist_mc3.Rebin(len(chi_binnings[mass])-1,hist_mc3.GetName()+"_rebin1",chi_binnings[mass])
	if hist_mc3.Integral()>0:
            hist_mc3.Scale(hist.Integral()/hist_mc3.Integral())
      	hist_mc3.SetLineColor(4)
	if "metsumet" in var:
	    hist_mc3.Rebin(4)
        hist_mc3.SetStats(False)
        hist_mc3.Draw("histsame")
        legend.AddEntry(hist_mc3,"Pythia8 QCD","l")

     	hist_mc2=f_mc2[0].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var)
     	for i in range(1,len(mc2)):
     	    hist_mc2.Add(f_mc2[i].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var),mc2[i][1]/mc2[0][1])
	if var=="chi":
            hist_mc2=hist_mc2.Rebin(len(chi_binnings[mass])-1,hist_mc2.GetName()+"_rebin1",chi_binnings[mass])
	if hist_mc2.Integral()>0:
            hist_mc2.Scale(hist.Integral()/hist_mc2.Integral())
      	hist_mc2.SetLineColor(6)
	if "metsumet" in var:
	    hist_mc2.Rebin(4)
        hist_mc2.SetStats(False)
        hist_mc2.Draw("histsame")
        legend.AddEntry(hist_mc2,"Herwig++ QCD","l")

        #hist2.Draw("lesame")
        hist.Draw("lesame")

        legend.SetTextSize(0.04)
        legend.SetFillStyle(0)
        legend.Draw("same")

        canvas.cd(2)
        ratio=hist.Clone(hist.GetName()+"clone")
        ratio.Divide(hist,hist)
        for b in range(hist.GetNbinsX()):
          if hist.GetBinContent(b+1)>0:
            ratio.SetBinError(b+1,hist.GetBinError(b+1)/hist.GetBinContent(b+1))
        ratio.SetTitle("")
        ratio.GetYaxis().SetTitle("Data / Sim")
        ratio.GetYaxis().SetTitleSize(0.13)
        ratio.GetYaxis().SetTitleOffset(0.5)
        ratio.SetMarkerSize(0.1)
        ratio.GetYaxis().SetLabelSize(0.14)
        ratio.GetYaxis().SetRangeUser(0,2)
        ratio.GetXaxis().SetNdivisions(506)
        ratio.GetYaxis().SetNdivisions(503)
        ratio.GetXaxis().SetLabelColor(1)
        ratio.GetXaxis().SetTitle(label[variables.index(var)])
        ratio.GetXaxis().SetTitleSize(0.16)
        ratio.GetXaxis().SetTitleOffset(1.1)
        ratio.GetXaxis().SetLabelSize(0.14)
        ratio.Draw("histe")
        ratio_mc=hist_mc.Clone(hist_mc.GetName()+"clone")
        ratio_mc.Divide(hist_mc,hist)
        for b in range(hist.GetNbinsX()):
          if hist.GetBinContent(b+1)>0:
            ratio_mc.SetBinError(b+1,hist.GetBinError(b+1)/hist.GetBinContent(b+1))
        ratio_mc.Draw("histsame")
        ratio_mc2=hist_mc2.Clone(hist_mc2.GetName()+"clone")
        ratio_mc2.Divide(hist_mc2,hist)
        for b in range(hist.GetNbinsX()):
          if hist.GetBinContent(b+1)>0:
            ratio_mc2.SetBinError(b+1,hist.GetBinError(b+1)/hist.GetBinContent(b+1))
        ratio_mc2.Draw("histsame")
        ratio_mc3=hist_mc3.Clone(hist_mc3.GetName()+"clone")
        ratio_mc3.Divide(hist_mc3,hist)
        for b in range(hist.GetNbinsX()):
          if hist.GetBinContent(b+1)>0:
            ratio_mc3.SetBinError(b+1,hist.GetBinError(b+1)/hist.GetBinContent(b+1))
        ratio_mc3.Draw("histsame")
        canvas.cd(1)
        hist.GetYaxis().SetTitleOffset(1.2)

        canvas.SaveAs("chi_control_plots_"+var+"_"+str(mass)+"_"+prefix+".root")
        canvas.SaveAs("chi_control_plots_"+var+"_"+str(mass)+"_"+prefix+".pdf")
