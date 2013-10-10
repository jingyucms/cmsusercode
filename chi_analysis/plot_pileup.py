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

   label="#chi"

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
   
   for prefix in ["data","QCD"]:
      canvas = TCanvas("jes","jes",0,0,600,400)
      canvas.Divide(3,2)
      log=False
      legends=[]
      hists=[]
      for mass in range(len(masses)-1):
        if prefix=="data":
	  mc=[("chi_EPS3",1)]
	if prefix=="QCD":
  	  mc=[("chi_QCD_1000",204.0/13479218),
              ("chi_QCD_500",8426.0/31743483),
              ("chi_QCD_250",276000.0/26900255),
     	      ("chi_QCD_100",1.036e7/48365102),
        	]
        f_mc=[]
        for name,xsec in mc:
          f_mc+=[TFile.Open(name+".root")]

        print mass, mc
	
        canvas.cd(mass+1)
        canvas.GetPad(mass+1).SetLogy(log)
        legend=TLegend(0.2,0.55,0.95,0.90,(str(masses[mass])+"<m_{jj}<"+str(masses[mass+1])+" GeV").replace("4200<m_{jj}<7000","m_{jj}>4200").replace("4200<m_{jj}<8000","m_{jj}>4200"))
	legends+=[legend]
    
        var="chi"
        hist=f_mc[0].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var)
	hist=hist.Clone(hist.GetName()+"main")
	hists+=[hist]
        for i in range(1,len(mc)):
            hist.Add(f_mc[i].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var),mc[i][1]/mc[0][1])
        hist=hist.Rebin(len(chi_binnings[mass])-1,hist.GetName()+"_rebin1",chi_binnings[mass])
        hist.SetLineWidth(2)
      	hist.SetLineColor(1)
	miny=0
	if hist.Integral()>0:
            miny=log*0.1
	histref=hist.Clone(hist.GetName()+"ref")
	hists+=[histref]
        for b in range(hist.GetNbinsX()):
	    hist.SetBinError(b+1,0)
	    hist.SetBinContent(b+1,1)
	hist.GetXaxis().SetTitle(label)
	hist.GetYaxis().SetTitle("N")
	hist.GetYaxis().SetRangeUser(0.8,1.3)
        hist.GetXaxis().SetTitleOffset(1.1)
        hist.GetYaxis().SetTitleOffset(1.1)
        hist.GetXaxis().SetLabelSize(0.05)
        hist.GetYaxis().SetLabelSize(0.05)
        hist.GetXaxis().SetTitleSize(0.06)
        hist.GetYaxis().SetTitleSize(0.06)
	hist.SetTitle("")
	hist.SetStats(False)
        hist.Draw("le")
        legend.AddEntry(hist,"with reweighting","l")
	
        var="nopu"
        hist2=f_mc[0].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var)
        for j in range(1,len(mc)):
	    print j, "dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var
            hist2.Add(f_mc[j].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var),mc[j][1]/mc[0][1])
        hist2=hist2.Rebin(len(chi_binnings[mass])-1,hist2.GetName()+"_rebin1",chi_binnings[mass])
	if hist2.Integral()>0:
            hist2.Scale(histref.Integral()/hist2.Integral())
        hist2.SetLineWidth(1)
        hist2.SetLineColor(colors[1])
        hist2.SetLineStyle(2)
        hist2.Divide(hist2,histref,1,1,"b")
        miny=0
        if hist2.Integral()>0:
            miny=log*0.1
	hist2.SetTitle("")
        hist2.SetStats(False)
	hists+=[hist2]
        hist2.Draw("histesame")
        legend.AddEntry(hist2,"no reweighting","l")

        var="pu20"
        hist3=f_mc[0].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var)
        for j in range(1,len(mc)):
            hist3.Add(f_mc[j].Get("dijet_"+str(masses[mass])+"_"+str(masses[mass+1])+"_"+var),mc[j][1]/mc[0][1])
        hist3=hist3.Rebin(len(chi_binnings[mass])-1,hist3.GetName()+"_rebin1",chi_binnings[mass])
        if hist3.Integral()>0:
            hist3.Scale(histref.Integral()/hist3.Integral())
        hist3.SetLineWidth(1)
        hist3.SetLineColor(colors[2])
        hist3.SetLineStyle(3)
        hist3.Divide(hist3,histref,1,1,"b")
        miny=0
        if hist3.Integral()>0:
            miny=log*0.1
	hist3.SetTitle("")
        hist3.SetStats(False)
	hists+=[hist3]
        #hist3.Draw("histsame")
        #legend.AddEntry(hist3,"n_{PV}>20","l")

        legend.SetTextSize(0.04)
        legend.SetFillStyle(0)
        legend.Draw("same")

      canvas.SaveAs("chi_pileup_plots_"+prefix+".root")
      canvas.SaveAs("chi_pileup_plots_"+prefix+".pdf")
