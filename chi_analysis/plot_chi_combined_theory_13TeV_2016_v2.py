from ROOT import *
import ROOT
import array, math
import os,sys
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

def setUpDMHists(hist,linecolor,linestyle,linewidth):
    hist.SetLineColor(linecolor)
    hist.SetLineStyle(linestyle)
    hist.SetLineWidth(linewidth)
    hist.Scale(1./hist.Integral())
    for b in range(hist.GetNbinsX()):
        hist.SetBinContent(b+1,hist.GetBinContent(b+1)/hist.GetBinWidth(b+1))
    return 

def divideAsymErrors(g1,h1,doEX):
    if not g1.GetN()==h1.GetNbinsX():
        print "divideAsymErrors Function Fails!!!"
        sys.exit()

    g=TGraphAsymmErrors()
    for b in range(h1.GetNbinsX()):
        den=h1.GetBinContent(b+1)
        if doEX:
            bwidth=h1.GetBinWidth(b+1)/2
        else:
            bwidth=0
        g.SetPoint(g.GetN(),g1.GetX()[b],g1.GetY()[b]/den)
        g.SetPointError(g.GetN()-1,bwidth,bwidth,g1.GetEYlow()[b]/den,g1.GetEYhigh()[b]/den)
        
    return g

def setupAsymErrors(g):
    g.SetMarkerStyle(20)
    g.SetMarkerSize(0.1)
    g.SetMarkerColor(1)
    g.SetLineColor(1)
    g.SetLineWidth(1)
    return

if __name__=="__main__":

  unfoldedData=True

  massbins=[#(1900,2400),
  	      (2400,3000),
  	      (3000,3600),
  	      (3600,4200),
  	      (4200,4800),
  	      (4800,5400),
  	      (5400,6000),
  	      (6000,13000),
  ]

  chi_bins=[#(1,2,3,4,5,6,7,8,9,10,12,14,16),
  	    (1,2,3,4,5,6,7,8,9,10,12,14,16),
  	    (1,2,3,4,5,6,7,8,9,10,12,14,16),
  	    (1,2,3,4,5,6,7,8,9,10,12,14,16),
  	    (1,2,3,4,5,6,7,8,9,10,12,14,16),
  	    (1,2,3,4,5,6,7,8,9,10,12,14,16),
  	    (1,2,3,4,5,6,7,8,9,10,12,14,16),
  	    (1,3,6,9,12,16),
  ]
  chi_binnings=[]
  for mass_bin in chi_bins:
      chi_binnings+=[array.array('d')]
      for chi_bin in mass_bin:
  	  chi_binnings[-1].append(chi_bin)

  for massbin in [0,1,2,3,4,5,6]:
      
    massbintext = str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")
    
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
    gStyle.SetEndErrorSize(8)

    gROOT.LoadMacro("CMS_lumi.C");
    iPeriod = 5;	#// 1=7TeV, 2=8TeV, 3=7+8TeV, 7=7+8+13TeV 
    iPos = 33;
    #// second parameter in example_plot is iPos, which drives the position of the CMS logo in the plot
    #// iPos=11 : top-left, left-aligned
    #// iPos=33 : top-right, right-aligned
    #// iPos=22 : center, centered
    #// mode generally : 
    #//   iPos = 10*(alignement 1/2/3) + position (1/2/3 = left/center/right)

    prefix="datacard_shapelimit13TeV"

    c = TCanvas("combined", "combined", 0, 0, 650, 800)
    c.Divide(1,1)
    new_hists=[]
    if True:
        if unfoldedData:
            fdir='invertMatrixOct20/'
        else:
            fdir='smearedDatacardsNov2/'
            
        if unfoldedData:  
            filename="fastnlo/RunII/fnl5662j_v23_fix_CT14nlo_allmu_ak4.root"
            print filename
            fNloQcd = TFile.Open(filename)
            new_hists+=[fNloQcd]
            histname='chi-'+str(massbins[massbin]).strip("()").replace(',',"-").replace(' ',"").replace("6000-13000","6000-6600")
            print histname
            hNloQcd=fNloQcd.Get(histname)
	    print "NLO QCD hist: "
            print fNloQcd
	    hNloQcd=rebin(hNloQcd,len(chi_binnings[massbin])-1,chi_binnings[massbin])
            hNloQcd.SetLineColor(5)
            hNloQcd.SetLineStyle(3)
            hNloQcd.SetLineWidth(2)
    
            filename="fastnlo/RunII/DijetAngularCMS13_ewk.root"
            print filename
            fEWK = TFile.Open(filename)
            new_hists+=[fEWK]
            histname='chi-'+str(massbins[massbin]).strip("()").replace(',',"-").replace(' ',"").replace("6000-13000","6000-6600")
            print histname
            hEWK=fEWK.Get(histname)
	    print "EWK hist: "
            print hEWK
            for b in range(hNloQcd.GetXaxis().GetNbins()):
	        low_bin=hEWK.FindBin(hNloQcd.GetXaxis().GetBinLowEdge(b+1))
	        up_bin=hEWK.FindBin(hNloQcd.GetXaxis().GetBinUpEdge(b+1))
	        correction=hEWK.Integral(low_bin,up_bin-1)/(up_bin-low_bin)
	        print "correction: "
                print correction
                hNloQcd.SetBinContent(b+1,hNloQcd.GetBinContent(b+1)*correction*hNloQcd.GetBinWidth(b+1))
            hNloQcd.Scale(1./hNloQcd.Integral())
            for b in range(hNloQcd.GetXaxis().GetNbins()):
	        hNloQcd.SetBinContent(b+1,hNloQcd.GetBinContent(b+1)/hNloQcd.GetBinWidth(b+1))

        else:
            filename=fdir+'datacard_shapelimit13TeV_DMAxial_Dijet_LO_Mphi_4500_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_1_chi2016.root'
            print filename
            f = TFile.Open(filename)
            new_hists+=[f]
            histname='DMAxial_Dijet_LO_Mphi_4500_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_1_ALT#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
            print filename
            f = TFile.Open(filename)
            new_hists+=[f]
            print histname
            hNloQcd=f.Get(histname)
            hNloQcd.SetLineColor(5)
            hNloQcd.SetLineStyle(3)
            hNloQcd.SetLineWidth(2)
	    hNloQcd.Scale(1./hNloQcd.Integral())
	    for b in range(hNloQcd.GetNbinsX()):
	        hNloQcd.SetBinContent(b+1,hNloQcd.GetBinContent(b+1)/hNloQcd.GetBinWidth(b+1))
            
        hNloQcdbackup=hNloQcd.Clone(hNloQcd.GetName()+"backup")    

        #filename="datacard_shapelimit13TeV_QCD_chi2016.root"
        #print filename
        #f = TFile.Open(filename)
        #new_hists+=[f]
        #histname='QCD#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        #print histname
        #h0=f.Get(histname)
        h0=hNloQcd
        h0.SetLineColor(1)
        h0.SetLineStyle(3)
        h0.SetLineWidth(4)

        filename="datacards/Unfolded_chiNtuple_dataReReco_v3_Coarse_PFHT900_fromCB_AK4SF_pythia8_Pt_170toInf_MatrixInvert.root"
        if unfoldedData:
            histname="dijet_mass_"+massbintext+"_chi_unfolded"
	else:
            histname="dijet_mass_"+massbintext+"_chi"
        print filename
        fData = TFile.Open(filename)
        new_hists+=[fData]
        print histname
        h14=fData.Get(histname)
	#if not unfoldedData:
        #  for b in range(h14.GetXaxis().GetNbins()):
        #    h14.SetBinContent(b+1,h14.GetBinContent(b+1)*h14.GetBinWidth(b+1))
        #    h14.SetBinError(b+1,h14.GetBinError(b+1)*h14.GetBinWidth(b+1))
	origh14=h14.Rebin(len(chi_binnings[massbin])-1,h14.GetName()+"rebinorig",chi_binnings[massbin])
	h14=rebin2(h14,len(chi_binnings[massbin])-1,chi_binnings[massbin])
	    
	h14G=TGraphAsymmErrors(h14.Clone(histname+"G"))
	new_hists+=[h14G]
        setupAsymErrors(h14G)
	alpha=1.-0.6827
	nevents=0
	for b in range(h14G.GetN()):
	    if unfoldedData:
	        N=origh14.GetBinContent(b+1)
	    else:
	        N=1./pow(h14.GetBinError(b+1)/h14.GetBinContent(b+1),2)
	    #print N
	    nevents+=N
	    L=0
	    if N>0:
	        L=ROOT.Math.gamma_quantile(alpha/2.,N,1.)
            U=ROOT.Math.gamma_quantile_c(alpha/2.,N+1,1.)
            h14G.SetPointEYlow(b,(N-L)/N*h14.GetBinContent(b+1))
            h14G.SetPointEYhigh(b,(U-N)/N*h14.GetBinContent(b+1))
            print N, sqrt(N)/N, origh14.GetBinError(b+1)/origh14.GetBinContent(b+1), h14.GetBinError(b+1)/h14.GetBinContent(b+1), (N-L)/N, (U-N)/N
        print "data events:", nevents
	
	h14Gsys=h14G.Clone(histname+"sys")
	new_hists+=[h14Gsys]
	h14Gsysstat=h14G.Clone(histname+"sysstat")
	new_hists+=[h14Gsysstat]

        filename="datacard_shapelimit13TeV_QCD_chi2016_backup.root"
        print filename
        fsys = TFile.Open(filename)
        new_hists+=[fsys]
        uncertaintynames=["jer","jes","pdf","scale"]
        uncertainties=[]
        for u in uncertaintynames:
            histname1='QCD#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1_"+u+"Up"
            print histname1
            histname2='QCD#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1_"+u+"Down"
            print histname2
            histname3='QCD#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
            print histname3
            up=fsys.Get(histname1)
            down=fsys.Get(histname2)
            central=fsys.Get(histname3)
            uncertainties+=[[up,down,central]]
        h2new=h14.Clone("down"+str(massbins[massbin]))
        h3new=h14.Clone("up"+str(massbins[massbin]))
	chi2=0
        for b in range(h14.GetXaxis().GetNbins()):
            if b==0:# or b==h14G.GetXaxis().GetNbins()-1:
                print massbins[massbin],b,"stat",h14G.GetErrorYlow(b)/h14G.GetY()[b],h14G.GetErrorYhigh(b)/h14G.GetY()[b]
	    exp_sumdown=0
	    exp_sumup=0
            theory_sumdown=0
            theory_sumup=0
            for up,down,central in uncertainties:
	        if b==0:# or b==h14G.GetXaxis().GetNbins()-1:
                    print massbins[massbin],b,uncertaintynames[uncertainties.index([up,down,central])],abs(up.GetBinContent(b+1)-central.GetBinContent(b+1))/central.GetBinContent(b+1),abs(down.GetBinContent(b+1)-central.GetBinContent(b+1))/central.GetBinContent(b+1)
                addup=pow(max(0,up.GetBinContent(b+1)-central.GetBinContent(b+1),down.GetBinContent(b+1)-central.GetBinContent(b+1)),2)/pow(central.GetBinContent(b+1),2)
		adddown=pow(max(0,central.GetBinContent(b+1)-up.GetBinContent(b+1),central.GetBinContent(b+1)-down.GetBinContent(b+1)),2)/pow(central.GetBinContent(b+1),2)
                if uncertaintynames[uncertainties.index([up,down,central])]=="jer" or uncertaintynames[uncertainties.index([up,down,central])]=="jes":
		    exp_sumup+=addup
                    exp_sumdown+=adddown
		else:
		    theory_sumup+=addup
                    theory_sumdown+=adddown
            exp_sumdown=sqrt(exp_sumdown)
            exp_sumup=sqrt(exp_sumup)
            theory_sumdown=sqrt(theory_sumdown)
            theory_sumup=sqrt(theory_sumup)

	    chi2+=pow(hNloQcdbackup.GetBinContent(b+1)-h14G.GetY()[b],2) / \
	           (pow(max(exp_sumdown,exp_sumup)*h14G.GetY()[b],2)+pow(max(theory_sumdown,theory_sumup)*h14G.GetY()[b],2)+pow(max(h14G.GetErrorYlow(b),h14G.GetErrorYhigh(b)),2))

            h14Gsys.SetPointEXlow(b,0)
            h14Gsys.SetPointEXhigh(b,0)
            h14Gsys.SetPointEYlow(b,exp_sumdown*h14G.GetY()[b])
            h14Gsys.SetPointEYhigh(b,exp_sumup*h14G.GetY()[b])
            h14Gsysstat.SetPointEXlow(b,0)
            h14Gsysstat.SetPointEXhigh(b,0)
            h14Gsysstat.SetPointEYlow(b,sqrt(pow(exp_sumdown*h14G.GetY()[b],2)+pow(h14G.GetErrorYlow(b),2)))
            h14Gsysstat.SetPointEYhigh(b,sqrt(pow(exp_sumup*h14G.GetY()[b],2)+pow(h14G.GetErrorYhigh(b),2)))
	    stat_up=h14G.GetErrorYhigh(b)
            stat_down=h14G.GetErrorYlow(b)
            h14G.SetPointEYlow(b,0)
            h14G.SetPointEYhigh(b,0)
            h2new.SetBinContent(b+1,hNloQcdbackup.GetBinContent(b+1)-theory_sumdown*hNloQcdbackup.GetBinContent(b+1))
            h3new.SetBinContent(b+1,hNloQcdbackup.GetBinContent(b+1)+theory_sumup*hNloQcdbackup.GetBinContent(b+1))
	    print "{0:.1f} TO {1:.1f}; {2:.4f} +{3:.4f},-{4:.4f} (DSYS=+{5:.4f},-{6:.4f})".format(h2new.GetXaxis().GetBinLowEdge(b+1),h2new.GetXaxis().GetBinUpEdge(b+1),h14G.GetY()[b],sqrt(pow(stat_up,2)),sqrt(pow(stat_down,2)),sqrt(pow(exp_sumup*h14G.GetY()[b],2)),sqrt(pow(exp_sumdown*h14G.GetY()[b],2)))
        print "chi2/ndof",chi2/h14G.GetXaxis().GetNbins()
	new_hists+=[h2new]
        new_hists+=[h3new]
        h2new.SetLineStyle(1)
        h3new.SetLineStyle(1)
        h2new.SetLineColor(kGray)
        h2new.SetFillColor(10)
        h3new.SetLineColor(kGray)
        h3new.SetFillColor(kGray)
        
        if massbin>=0:
          filename=fdir+"datacard_shapelimit13TeV_cs_ct14nlo_14000_LL+_chi2016.root"
          histname='cs_ct14nlo_14000_LL+#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print filename
          f = TFile.Open(filename)
          new_hists+=[f]
          print histname
          h4=f.Get(histname)
          h4.SetLineColor(kRed)
          h4.SetLineWidth(3)
          h4.SetLineStyle(8)
	  h4.Scale(1./h4.Integral())
	  for b in range(h4.GetNbinsX()):
	       h4.SetBinContent(b+1,h4.GetBinContent(b+1)/h4.GetBinWidth(b+1))

          filename=fdir+"datacard_shapelimit13TeV_cs_ct14nlo_14000_LL-_chi2016.root"
          histname='cs_ct14nlo_14000_LL-#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print filename
          f = TFile.Open(filename)
          new_hists+=[f]
          print histname
          h4b=f.Get(histname)
          h4b.SetLineColor(kAzure+3)
          h4b.SetLineStyle(6)
          h4b.SetLineWidth(3)
	  h4b.Scale(1./h4b.Integral())
	  for b in range(h4b.GetNbinsX()):
	       h4b.SetBinContent(b+1,h4b.GetBinContent(b+1)/h4b.GetBinWidth(b+1))

          filename=fdir+"datacard_shapelimit13TeV_cs_ct14nlo_14000_VV+_chi2016.root"
          histname='cs_ct14nlo_14000_VV+#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print filename
          f = TFile.Open(filename)
          new_hists+=[f]
          print histname
          h4c=f.Get(histname)
          h4c.SetLineColor(36)
          h4c.SetLineStyle(5)
          h4c.SetLineWidth(3)
	  h4c.Scale(1./h4c.Integral())
	  for b in range(h4c.GetNbinsX()):
	       h4c.SetBinContent(b+1,h4c.GetBinContent(b+1)/h4c.GetBinWidth(b+1))

          filename=fdir+"datacard_shapelimit13TeV_cs_ct14nlo_14000_VV-_chi2016.root"
          histname='cs_ct14nlo_14000_VV-#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print filename
          f = TFile.Open(filename)
          new_hists+=[f]
          print histname
          h4d=f.Get(histname)
          h4d.SetLineColor(28)
          h4d.SetLineStyle(5)
          h4d.SetLineWidth(3)
	  h4d.Scale(1./h4d.Integral())
	  for b in range(h4d.GetNbinsX()):
	       h4d.SetBinContent(b+1,h4d.GetBinContent(b+1)/h4d.GetBinWidth(b+1))

          filename=fdir+"datacard_shapelimit13TeV_cs_ct14nlo_14000_AA+_chi2016.root"
          histname='cs_ct14nlo_14000_AA+#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print filename
          f = TFile.Open(filename)
          new_hists+=[f]
          print histname
          h4e=f.Get(histname)
          h4e.SetLineColor(8)
          h4e.SetLineStyle(5)
          h4e.SetLineWidth(3)
	  h4e.Scale(1./h4e.Integral())
	  for b in range(h4e.GetNbinsX()):
	       h4e.SetBinContent(b+1,h4e.GetBinContent(b+1)/h4e.GetBinWidth(b+1))

          filename=fdir+"datacard_shapelimit13TeV_cs_ct14nlo_14000_AA-_chi2016.root"
          histname='cs_ct14nlo_14000_AA-#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print filename
          f = TFile.Open(filename)
          new_hists+=[f]
          print histname
          h4f=f.Get(histname)
          h4f.SetLineColor(9)
          h4f.SetLineStyle(5)
          h4f.SetLineWidth(3)
	  h4f.Scale(1./h4f.Integral())
	  for b in range(h4f.GetNbinsX()):
	       h4f.SetBinContent(b+1,h4f.GetBinContent(b+1)/h4f.GetBinWidth(b+1))

          filename=fdir+"datacard_shapelimit13TeV_cs_ct14nlo_14000_V-A+_chi2016.root"
          histname='cs_ct14nlo_14000_V-A+#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print filename
          f = TFile.Open(filename)
          new_hists+=[f]
          print histname
          h4g=f.Get(histname)
          h4g.SetLineColor(kAzure+3)
          h4g.SetLineStyle(5)
          h4g.SetLineWidth(3)
	  h4g.Scale(1./h4g.Integral())
	  for b in range(h4g.GetNbinsX()):
	       h4g.SetBinContent(b+1,h4g.GetBinContent(b+1)/h4g.GetBinWidth(b+1))

          filename=fdir+"datacard_shapelimit13TeV_cs_ct14nlo_14000_V-A-_chi2016.root"
          histname='cs_ct14nlo_14000_V-A-#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print filename
          f = TFile.Open(filename)
          new_hists+=[f]
          print histname
          h4h=f.Get(histname)
          h4h.SetLineColor(kAzure+3)
          h4h.SetLineStyle(5)
          h4h.SetLineWidth(3)
	  h4h.Scale(1./h4h.Integral())
	  for b in range(h4h.GetNbinsX()):
	       h4h.SetBinContent(b+1,h4h.GetBinContent(b+1)/h4h.GetBinWidth(b+1))

          filename=fdir+"datacard_shapelimit13TeV_GENnp-22-v5_chi2016.root"
          print filename
          f = TFile.Open(filename)
          new_hists+=[f]
          histname='QCDADD10000#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print histname
          h5=f.Get(histname)
          h5.SetLineColor(kAzure+7)
          h5.SetLineStyle(7)
          h5.SetLineWidth(4)
	  h5.Scale(1./h5.Integral())
	  for b in range(h5.GetNbinsX()):
	       h5.SetBinContent(b+1,h5.GetBinContent(b+1)/h5.GetBinWidth(b+1))
            
          coupling="1"
          filename=fdir+'datacard_shapelimit13TeV_DMAxial_Dijet_LO_Mphi_2000_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'_chi2016.root'
          histname='DMAxial_Dijet_LO_Mphi_2000_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print filename
          f7 = TFile.Open(filename)
          new_hists+=[f7]
          print histname
          h7=f7.Get(histname)
          setUpDMHists(h7,kBlue,4,2)

          filename=fdir+'datacard_shapelimit13TeV_DMAxial_Dijet_LO_Mphi_3000_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'_chi2016.root'
          histname='DMAxial_Dijet_LO_Mphi_3000_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print filename
          f7a = TFile.Open(filename)
          new_hists+=[f7a]
          print histname
          h7a=f7a.Get(histname)
          setUpDMHists(h7a,kMagenta,7,2)

          filename=fdir+'datacard_shapelimit13TeV_DMAxial_Dijet_LO_Mphi_1000_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'_chi2016.root'
          histname='DMAxial_Dijet_LO_Mphi_1000_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print filename
          f7b = TFile.Open(filename)
          new_hists+=[f7b]
          print histname
          h7b=f7b.Get(histname)
          setUpDMHists(h7b,kTeal+4,10,2)

          filename=fdir+'datacard_shapelimit13TeV_DMAxial_Dijet_LO_Mphi_5000_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'_chi2016.root'
          histname='DMAxial_Dijet_LO_Mphi_5000_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print filename
          f7c = TFile.Open(filename)
          new_hists+=[f7c]
          print histname
          h7c=f7c.Get(histname)
          setUpDMHists(h7c,kOrange+7,1,2)

          filename=fdir+'datacard_shapelimit13TeV_DMAxial_Dijet_LO_Mphi_1500_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'_chi2016.root'
          histname='DMAxial_Dijet_LO_Mphi_1500_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print filename
          f7d = TFile.Open(filename)
          new_hists+=[f7d]
          print histname
          h7d=f7d.Get(histname)
          setUpDMHists(h7d,kAzure+8,1,2)

        if massbin>3:
          if unfoldedData:  
              filename=fdir+"datacard_shapelimit13TeV_QBH_8000_6_chi_v1.root"
          else:
              filename=fdir+"datacard_shapelimit13TeV_QBH_8000_6_chi2016.root"
          print filename
          f = TFile.Open(filename)
          new_hists+=[f]
          if unfoldedData:
              histname='QCDADD6QBH8000#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          else:
              histname='QBH_8000_6#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print histname
          h6=f.Get(histname)
          h6=h6.Rebin(len(chi_binnings[massbin])-1,h6.GetName()+"_rebin",chi_binnings[massbin])
          h6.SetLineColor(kGreen+3)
          h6.SetLineStyle(5)
          h6.SetLineWidth(4)
          h6.Scale(1./h6.Integral())
          for b in range(h6.GetNbinsX()):
              h6.SetBinContent(b+1,h6.GetBinContent(b+1)/h6.GetBinWidth(b+1))

#        if massbin>4:
#            h0.GetYaxis().SetRangeUser(0.02,0.22)
#        elif massbin>3:
#            h0.GetYaxis().SetRangeUser(0.045,0.14)
#        elif massbin>1:
#            h0.GetYaxis().SetRangeUser(0.045,0.12)
#        else:
#            h0.GetYaxis().SetRangeUser(0.055,0.105)

        if massbin>4:
            h0.GetYaxis().SetRangeUser(0.02,0.22)
        elif massbin>3:
            h0.GetYaxis().SetRangeUser(0.02,0.22)
        elif massbin>1:
            h0.GetYaxis().SetRangeUser(0.045,0.12)
        else:
            h0.GetYaxis().SetRangeUser(0.045,0.12)
            
        h0.GetXaxis().SetTitle("#chi_{dijet}")
        h0.GetYaxis().SetTitle("1/#sigma_{dijet} d#sigma_{dijet}/d#chi_{dijet}")
        h0.GetYaxis().SetTitleOffset(1.4)
        h0.GetXaxis().SetTitleOffset(0.8)
        h0.GetYaxis().SetTitleSize(0.05)
        h0.GetYaxis().SetLabelSize(0.04)
        h0.GetXaxis().SetTitleSize(0.05)
        h0.GetXaxis().SetLabelSize(0.04)
        h0.GetXaxis().SetTickLength(0.03)
        h0.GetYaxis().SetNdivisions(505)
        
        c.cd()

        pad1=TPad("","",0,0,1,0.3)
        pad1.SetTopMargin(0.08)
        pad1.SetBottomMargin(0.25)
        pad1.Draw()
        pad1.cd()
        
        h0Div=h0.Clone(h0.GetName()+"_ratio")
        h3newDiv=h3new.Clone(h3new.GetName()+"_ratio")
        h2newDiv=h2new.Clone(h2new.GetName()+"_ratio")

        h14GDiv=h14G.Clone(h14G.GetName()+"_ratio")
        h14GsysDiv=h14Gsys.Clone(h14Gsys.GetName()+"_ratio")
        h14GsysstatDiv=h14Gsysstat.Clone(h14Gsysstat.GetName()+"_ratio")

        h0Div.Divide(h0)
        h3newDiv.Divide(h0)
        h2newDiv.Divide(h0)
        #print h14G.GetN(),h14G.Eval(1),h14G.Eval(1.5), h14.GetBinContent(1)
        #print h14G.GetX()[0], h14G.GetY()[0]
        h14GDiv=divideAsymErrors(h14G,h0,True)
        setupAsymErrors(h14GDiv)
        h14GsysDiv=divideAsymErrors(h14Gsys,h0,False)
        setupAsymErrors(h14GsysDiv)
        h14GsysstatDiv=divideAsymErrors(h14Gsysstat,h0,True)
        setupAsymErrors(h14GsysstatDiv)

#        if massbin>4:
#            h0Div.GetYaxis().SetRangeUser(0.,2.)
#        elif massbin>3:
#            h0Div.GetYaxis().SetRangeUser(0.4,1.6)
#        elif massbin>1:
#            h0Div.GetYaxis().SetRangeUser(0.7,1.3)
#        else:
#            h0Div.GetYaxis().SetRangeUser(0.8,1.2)

        if massbin>4:
            h0Div.GetYaxis().SetRangeUser(0.,2.)
        elif massbin>3:
            h0Div.GetYaxis().SetRangeUser(0.,2.)
        elif massbin>1:
            h0Div.GetYaxis().SetRangeUser(0.7,1.3)
        else:
            h0Div.GetYaxis().SetRangeUser(0.7,1.3)
        h0Div.GetYaxis().SetTitle("#frac{Data}{NLO QCD + EW}")
        h0Div.GetXaxis().SetTitle("#chi_{dijet}")
        h0Div.GetYaxis().SetTitleOffset(0.65)
        h0Div.GetYaxis().SetTitleSize(0.1)
        h0Div.GetYaxis().SetLabelSize(0.095)
        h0Div.GetXaxis().SetTitleSize(0.12)
        h0Div.GetXaxis().SetLabelSize(0.095)
        h0Div.GetYaxis().SetTickLength(0.04)
        h0Div.GetXaxis().SetTickLength(0.08)
        
        h0Div.Draw("axis")
        h3newDiv.Draw("histsame")
        h2newDiv.Draw("histsame")
        h0Div.Draw("histsame")
        #h14GDiv.Draw("pzesame")
        h14GsysDiv.Draw("||same")
        h14GsysstatDiv.Draw("zesame")
        h0Div.Draw("axissame")
        h14GDiv.SetMarkerSize(0.8)
        h14GDiv.Draw("pzesame")

        c.cd()

        pad2=TPad("","",0,0.3,1,1)
        pad2.SetBottomMargin(0.001)
        pad2.SetTopMargin(0.07)
        pad2.Draw()
        pad2.cd()
        
        if massbin==len(massbins)-1:
            h0.Draw("axis")
        else:
            h0.Draw("axissame")
        h3new.Draw("histsame")
        h2new.Draw("histsame")
        h0.Draw("histsame")
        if massbin>=2:
            h4.Draw("histsame")
            h4b.Draw("histsame")
            #h4c.Draw("histsame")
            #h4d.Draw("histsame")
            #h4e.Draw("histsame")
            #h4f.Draw("histsame")
            #h4g.Draw("histsame")
            #h4h.Draw("histsame")
        if massbin>2:
            h5.Draw("histsame")
        if massbin>3:
            h6.Draw("histsame")
        if massbin == 0:
            h7.Draw("histsame")
            h7a.Draw("histsame")
            #h7b.Draw("histsame")
            h7c.Draw("histsame")
            #h7d.Draw("histsame")
        if massbin == 1:
            #h7.Draw("histsame")
            h7a.Draw("histsame")
            #h7b.Draw("histsame")
            h7c.Draw("histsame")
            #h7d.Draw("histsame")
        if massbin == 2:
            #h7.Draw("histsame")
            #h7a.Draw("histsame")
            #h7b.Draw("histsame")
            h7c.Draw("histsame")
            #h7d.Draw("histsame")
        if massbin == 3:
            #h7.Draw("histsame")
            #h7a.Draw("histsame")
            #h7b.Draw("histsame")
            h7c.Draw("histsame")
            #h7d.Draw("histsame")
        if massbin == 4:
            #h7.Draw("histsame")
            #h7a.Draw("histsame")
            #h7b.Draw("histsame")
            h7c.Draw("histsame")
            #h7d.Draw("histsame")
        if massbin == 5:
            #h7.Draw("histsame")
            #h7a.Draw("histsame")
            #h7b.Draw("histsame")
            h7c.Draw("histsame")
            #h7d.Draw("histsame")
        #if massbin == 6:
            #h7.Draw("histsame")
            #h7a.Draw("histsame")
            #h7b.Draw("histsame")
            #h7c.Draw("histsame")
            #h7d.Draw("histsame")
        #h14G.Draw("pzesame")
        h14Gsys.Draw("||same")
        h14Gsysstat.Draw("zesame")
        h14G.SetMarkerSize(0.8)
        h14G.Draw("pzesame")
        h0.Draw("axissame")
        #h14G.Print()
        #h14Gsys.Print()
        #h14Gsysstat.Print()

        if massbin>=4:
            ylabel=0.35
        else:
            ylabel=0.4
        
        #if massbin==0: title="1.9 < #font[72]{M_{jj}} < 2.4 TeV"
        if massbin==0: title="2.4 < #font[72]{M_{jj}} < 3.0 TeV"
        if massbin==1: title="3.0 < #font[72]{M_{jj}} < 3.6 TeV"
        if massbin==2: title="3.6 < #font[72]{M_{jj}} < 4.2 TeV"
        if massbin==3: title="4.2 < #font[72]{M_{jj}} < 4.8 TeV"
        if massbin==4: title="4.8 < #font[72]{M_{jj}} < 5.4 TeV"
        if massbin==5: title="5.4 < #font[72]{M_{jj}} < 6.0 TeV"
        if massbin==6: title=" #font[72]{M_{jj}} > 6.0 TeV"

        #title+=" TeV"
        #if offsets[massbin]==0: titleo=""
        #elif offsets[massbin]<0: titleo="("+str(offsets[massbin])+")"
        #else: titleo="(+"+str(offsets[massbin])+")"

        l=TLegend(0.6,ylabel,1.0,ylabel+0.005,title)
        l.SetTextSize(0.035)
        l.SetFillStyle(0)
        l.Draw("same")
        new_hists+=[l]

        #lo=TLegend(0.82,ylabel,1.4,ylabel+0.01,titleo)
        #lo.SetTextSize(0.033)
        #lo.SetFillStyle(0)
        #lo.Draw("same")
        #new_hists+=[lo]

    l5=TLegend(0.74,0.92,1.0,0.92,"CMS")
    l5.SetTextSize(0.035)
    l5.SetFillStyle(0)
    #l5.Draw("same")
    new_hists+=[l5]
     
    l5=TLegend(0.7,0.88,1.0,0.88,"#sqrt{s} = 8 TeV")
    l5.SetTextSize(0.035)
    l5.SetFillStyle(0)
    #l5.Draw("same")
    new_hists+=[l5]
     
    l=TLegend(0.7,0.82,1.0,0.82,"L = 19.7 fb^{-1}")
    l.SetTextSize(0.035)
    l.SetFillStyle(0)
    #l.Draw("same")
    new_hists+=[l]
    
    banner=TLatex(0.33,0.96,"CMS,   L = 19.7 fb^{-1},   #sqrt{s} = 8 TeV")
    banner.SetNDC()
    banner.SetTextSize(0.035)
    #banner.Draw()

    h3newnew=h3new.Clone()
    h3newnew.SetLineColor(1)
    h3newnew.SetLineStyle(3)
    h3newnew.SetLineWidth(4)

    if massbin>=4:
        l2=TLegend(0.3,0.45,0.6,0.91,"")
    elif massbin>=1:
        l2=TLegend(0.3,0.55,0.6,0.91,"")
    else:
        l2=TLegend(0.3,0.55,0.6,0.91,"")
    l2.SetTextSize(0.033)
    l2.SetMargin(0.33)
    l2.AddEntry(h14G,"Data","ple")
    l2.AddEntry(h3newnew,"NLO QCD + EW","fl")
    if massbin>=2:
        l2.AddEntry(h4,"#Lambda_{LL}^{#font[122]{+}} (CI) = 14 TeV","l")
        l2.AddEntry(h4b,"#Lambda_{LL}^{#font[122]{-}} (CI) = 14 TeV","l")
        #l2.AddEntry(h4c,"#Lambda_{VV}^{#font[122]{+}} (CI) = 14 TeV","l")
        #l2.AddEntry(h4d,"#Lambda_{VV}^{#font[122]{-}} (CI) = 14 TeV","l")
        #l2.AddEntry(h4e,"#Lambda_{AA}^{#font[122]{+}} (CI) = 14 TeV","l")
        #l2.AddEntry(h4f,"#Lambda_{AA}^{#font[122]{-}} (CI) = 14 TeV","l")
        #l2.AddEntry(h4g,"#Lambda_{V-A} (CI) = 14 TeV","l")
        #l2.AddEntry(h4h,"#Lambda_{V-A}^{#font[122]{-}} (CI) = 14 TeV","l")
    if massbin > 2:
        l2.AddEntry(h5,"#Lambda_{T} (GRW) = 10 TeV","l")
    if massbin > 3:
        l2.AddEntry(h6,"M_{QBH} (n_{ED} = 6 ADD) = 8 TeV","l")
    if massbin == 0:
        #l2.AddEntry(h7b,"M_{Med} (DM g_{q} = 1.0) = 1 TeV","l")
        #l2.AddEntry(h7d,"M_{Med} (DM g_{q} = 1.0) = 1.5 TeV","l")
        l2.AddEntry(h7,"M_{Med} (DM g_{q} = 1.0) = 2 TeV","l")
        l2.AddEntry(h7a,"M_{Med} (DM g_{q} = 1.0) = 3 TeV","l")
        l2.AddEntry(h7c,"M_{Med} (DM g_{q} = 1.0) = 5 TeV","l")
    if massbin == 1:
        #l2.AddEntry(h7,"M_{Med} (DM g_{q} = 1.0) = 2.0 TeV","l")
        l2.AddEntry(h7a,"M_{Med} (DM g_{q} = 1.0) = 3 TeV","l")
        #l2.AddEntry(h7b,"M_{Med} (DM g_{q} = 1.0) = 4.0 TeV","l")
        l2.AddEntry(h7c,"M_{Med} (DM g_{q} = 1.0) = 5 TeV","l")
        #l2.AddEntry(h7d,"M_{Med} (DM g_{q} = 1.0) = 6.0 TeV","l")
    if massbin == 2:
        #l2.AddEntry(h7,"M_{Med} (DM g_{q} = 1.0) = 2.0 TeV","l")
        #l2.AddEntry(h7a,"M_{Med} (DM g_{q} = 1.0) = 3.0 TeV","l")
        #l2.AddEntry(h7b,"M_{Med} (DM g_{q} = 1.0) = 4.0 TeV","l")
        l2.AddEntry(h7c,"M_{Med} (DM g_{q} = 1.0) = 5 TeV","l")
        #l2.AddEntry(h7d,"M_{Med} (DM g_{q} = 1.0) = 6.0 TeV","l")
    if massbin == 3:
        #l2.AddEntry(h7,"M_{Med} (DM g_{q} = 1.0) = 2.0 TeV","l")
        #l2.AddEntry(h7a,"M_{Med} (DM g_{q} = 1.0) = 3.0 TeV","l")
        #l2.AddEntry(h7b,"M_{Med} (DM g_{q} = 1.0) = 4.0 TeV","l")
        l2.AddEntry(h7c,"M_{Med} (DM g_{q} = 1.0) = 5 TeV","l")
        #l2.AddEntry(h7d,"M_{Med} (DM g_{q} = 1.0) = 6.0 TeV","l")
    if massbin == 4:
        #l2.AddEntry(h7,"M_{Med} (DM g_{q} = 1.0) = 2.0 TeV","l")
        #l2.AddEntry(h7a,"M_{Med} (DM g_{q} = 1.0) = 3.0 TeV","l")
        #l2.AddEntry(h7b,"M_{Med} (DM g_{q} = 1.0) = 4.0 TeV","l")
        l2.AddEntry(h7c,"M_{Med} (DM g_{q} = 1.0) = 5 TeV","l")
        #l2.AddEntry(h7d,"M_{Med} (DM g_{q} = 1.0) = 6.0 TeV","l")
    if massbin == 5:
        #l2.AddEntry(h7,"M_{Med} (DM g_{q} = 1.0) = 2.0 TeV","l")
        #l2.AddEntry(h7a,"M_{Med} (DM g_{q} = 1.0) = 3.0 TeV","l")
        #l2.AddEntry(h7b,"M_{Med} (DM g_{q} = 1.0) = 4.0 TeV","l")
        l2.AddEntry(h7c,"M_{Med} (DM g_{q} = 1.0) = 5 TeV","l")
        #l2.AddEntry(h7d,"M_{Med} (DM g_{q} = 1.0) = 6.0 TeV","l")
    #if massbin == 6:
        #l2.AddEntry(h7,"M_{Med} (DM g_{q} = 1.0) = 2.0 TeV","l")
        #l2.AddEntry(h7a,"M_{Med} (DM g_{q} = 1.0) = 3.0 TeV","l")
        #l2.AddEntry(h7b,"M_{Med} (DM g_{q} = 1.0) = 4.0 TeV","l")
        #l2.AddEntry(h7c,"M_{Med} (DM g_{q} = 1.0) = 5.0 TeV","l")
        #l2.AddEntry(h7d,"M_{Med} (DM g_{q} = 1.0) = 6.0 TeV","l")
    l2.SetFillStyle(0)
    l2.Draw("same")

#    l2b=TLegend(0.3,0.54,0.6,0.93,"")
#    l2b.SetTextSize(0.035)
#    l2b.AddEntry(h14G," ","")
#    l2b.AddEntry(h0," ","l")
#    #l2b.AddEntry(h6," ","")
#    l2b.AddEntry(h4," ","")
#    l2b.AddEntry(h4b," ","")
#    l2b.AddEntry(h4c," ","")
#    l2b.AddEntry(h4d," ","")
#    #l2b.AddEntry(h4e," ","")
#    #l2b.AddEntry(h4f," ","")
#    l2b.AddEntry(h4g," ","")
#    #l2b.AddEntry(h4h," ","")
#    l2b.AddEntry(h5," ","")
#    l2b.SetFillStyle(0)
#    #l2b.Draw("same")
    
    #tl1=TLine(16,0,16,0.24)
    #tl1.SetLineColor(1)
    #tl1.SetLineStyle(1)
    #tl1.SetLineWidth(1)
    #tl1.Draw("same")

    #// writing the lumi information and the CMS "logo"
    CMS_lumi( c, iPeriod, iPos );

    #c.SaveAs(prefix + "_combined_theory"+str(massbin)+"_2016.pdf")
    #c.SaveAs(prefix + "_combined_theory"+str(massbin)+"_2016.eps")
