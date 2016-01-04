import os, sys
from ROOT import * 
import array

#gROOT.Macro( os.path.expanduser( '~/rootlogon.C' ) )
gROOT.Reset()
gROOT.SetStyle("Plain")
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetTitleOffset(1.2,"Y")
gStyle.SetPadLeftMargin(0.18)
gStyle.SetPadBottomMargin(0.15)
gStyle.SetPadTopMargin(0.03)
gStyle.SetPadRightMargin(0.05)
gStyle.SetMarkerSize(1.5)
gStyle.SetHistLineWidth(1)
gStyle.SetStatFontSize(0.020)
gStyle.SetTitleSize(0.06, "XYZ")
gStyle.SetLabelSize(0.05, "XYZ")
gStyle.SetNdivisions(510, "XYZ")
gStyle.SetLegendBorderSize(0)

def rebin(h1,nbins,binning):
    for b in range(h1.GetXaxis().GetNbins()):
        h1.SetBinContent(b+1,h1.GetBinContent(b+1)*h1.GetBinWidth(b+1))
        h1.SetBinError(b+1,h1.GetBinError(b+1)*h1.GetBinWidth(b+1))
    h1=h1.Rebin(nbins,h1.GetName()+"_rebin",binning)
    for b in range(h1.GetXaxis().GetNbins()):
        h1.SetBinContent(b+1,h1.GetBinContent(b+1)/h1.GetBinWidth(b+1))
        h1.SetBinError(b+1,h1.GetBinError(b+1)/h1.GetBinWidth(b+1))
    return h1

if __name__ == '__main__':

    prefixs=["datacard_shapelimit13TeV"]
 
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
    massbins=[(1900,2400),
              (2400,3000),
              (3000,3600),
              (3600,4200),
              (4200,4800),
              (4800,13000),
              #(5400,13000)
	      ]

    dataevents={}
    data={}
    for prefix in prefixs: 
      canvas = TCanvas("","",0,0,600,400)
      canvas.Divide(3,2)
      plots=[]
      legends=[]
      new_hists=[]

      for j in range(len(massbins)):
        # Pythia8 with MPI+HAD
        filename="datacard_shapelimit13TeV_GENv4_chi.root"
        print filename
        f = TFile.Open(filename)
        new_hists+=[f]
        histname='QCD#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1_backup"
        print histname
        alt1=f.Get(histname)
        alt1=alt1.Rebin(len(chi_binnings[j])-1,alt1.GetName()+"_rebin",chi_binnings[j])
	if alt1.Integral()>0:
            alt1.Scale(1./(alt1.Integral()))
        # Pythia8 without MPI+HAD
        filename="datacard_shapelimit13TeV_GENnonpertv4_chi.root"
        print filename
        f = TFile.Open(filename)
        new_hists+=[f]
        histname='QCDNonPert#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1_backup"
        print histname
        alt2=f.Get(histname)
        alt2=alt2.Rebin(len(chi_binnings[j])-1,alt2.GetName()+"_rebin",chi_binnings[j])
        alt2.SetLineColor(8)
        alt2.Scale(1./alt2.Integral())
        #for b in range(alt2.GetNbinsX()):
        #     alt2.SetBinContent(b+1,alt2.GetBinContent(b+1)/alt2.GetBinWidth(b+1))
	alt1.Divide(alt1,alt2)
        # Herwig++ without MPI+HAD
        filename="datacard_shapelimit13TeV_GENherwigv4_chi.root"
        print filename
        f = TFile.Open(filename)
        new_hists+=[f]
        histname='QCDHerwig#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1_backup"
        print histname
        alt3=f.Get(histname)
        alt3=alt3.Rebin(len(chi_binnings[j])-1,alt3.GetName()+"_rebin",chi_binnings[j])
	if alt3.Integral()>0:
    	    alt3.Scale(1./(alt3.Integral()))
        # Herwig++ without MPI+HAD
        filename="datacard_shapelimit13TeV_GENherwignonpertv4_chi.root"
        print filename
        f = TFile.Open(filename)
        new_hists+=[f]
        histname='QCDHerwigNonPert#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1_backup"
        print histname
        alt4=f.Get(histname)
        alt4=alt4.Rebin(len(chi_binnings[j])-1,alt4.GetName()+"_rebin",chi_binnings[j])
	if alt4.Integral()>0:
    	    alt4.Scale(1./(alt4.Integral()))
	alt3.Divide(alt3,alt4)
        # PLOTS
        canvas.cd(j+1)
        legend1=TLegend(0.2,0.6,0.9,0.95,(str(massbins[j][0])+"<m_{jj}<"+str(massbins[j][1])+" GeV").replace("4800<m_{jj}<13000","m_{jj}>4800"))
        legends+=[legend1]
	plots+=[alt1]
	alt1.SetLineColor(1)
	alt1.SetTitle("")
        alt1.Draw("he")
	alt1.GetYaxis().SetRangeUser(0.8,1.2)
        legend1.AddEntry(alt1,"Pythia8","le")
	plots+=[alt3]
	alt3.SetLineColor(3)
	alt3.SetTitle("")
        alt3.Draw("hesame")
        legend1.AddEntry(alt3,"Herwig++","le")
	
        legend1.SetTextSize(0.04)
        legend1.SetFillStyle(0)
        legend1.Draw("same")

      canvas.SaveAs(prefix + "_nonpert_sys.pdf")
      canvas.SaveAs(prefix + "_nonpert_sys.eps")
