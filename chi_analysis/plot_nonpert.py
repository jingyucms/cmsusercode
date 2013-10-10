import os, sys
from ROOT import * 
from DataFormats.FWLite import Events,Handle
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

    prefixs=["datacard_shapelimit"]
 
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
    massbins=[(1900,2400),
              (2400,3000),
	      (3000,3600),
	      (3600,4200),
	      (4200,8000)]
    samples=[("QCDHppNonPert",[("fileLists/fileList_herwigpp_qcdNonPert_m1400___Sep5_grid.txt",[(1900,2400),(2400,3000)]),
                               ("fileLists/fileList_herwigpp_qcdNonPert_m2500___Sep5_grid.txt",[(3000,3600),(3600,4200)]),
                               ("fileLists/fileList_herwigpp_qcdNonPert_m3700___Sep5_grid.txt",[(4200,8000)])]),
             ]
 
    dataevents={}
    data={}
    for prefix in prefixs: 
     ## data cards
     #sample=prefix + '_data_obs_chi.root'
     #print sample
     #out=TFile(sample,'RECREATE')

     # signal cards
     for i in range(len(samples)):
      sample=prefix + "_"+samples[i][0].replace("QCD","") + '_chi.root'
      print sample
      out=TFile(sample)

      canvas = TCanvas("","",0,0,600,400)
      canvas.Divide(3,2)
      plots=[]
      legends=[]

      for j in range(len(massbins)):
        # Pythia8 with MPI+HAD
        histname='QCD#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print histname
        alt1=out.Get(histname)
	if alt1.Integral()>0:
            alt1.Scale(1./(alt1.Integral()))
        # Pythia8 without MPI+HAD
        histname='QCDNonPert#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print histname
        alt2=out.Get(histname)
	if alt2.Integral()>0:
            alt2.Scale(1./(alt2.Integral()))
	alt1.Divide(alt1,alt2)
        # Herwig++ without MPI+HAD
        histname='QCDHpp#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print histname
        alt3=out.Get(histname)
	if alt3.Integral()>0:
    	    alt3.Scale(1./(alt3.Integral()))
        # Herwig++ without MPI+HAD
        histname='QCDHppNonPert#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print histname
        alt4=out.Get(histname)
	if alt4.Integral()>0:
    	    alt4.Scale(1./(alt4.Integral()))
	alt3.Divide(alt3,alt4)
        # PLOTS
        canvas.cd(j+1)
        legend1=TLegend(0.2,0.6,0.9,0.95,(str(massbins[j][0])+"<m_{jj}<"+str(massbins[j][1])+" GeV").replace("4200<m_{jj}<7000","m_{jj}>4200").replace("4200<m_{jj}<8000","m_{jj}>4200"))
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

      canvas.SaveAs(prefix + "_"+samples[i][0].replace("QCD","") + '_sys.pdf')
      canvas.SaveAs(prefix + "_"+samples[i][0].replace("QCD","") + '_sys.eps')
