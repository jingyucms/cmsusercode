from ROOT import TH1,gROOT,gStyle,TCanvas,TPad,TFile,TGraphAsymmErrors,TGraph,TColor,TColorWheel,TAttLine,kRed,kMagenta,kAzure,kOrange,TLegend,TH1D
import ROOT,array,os,sys
from math import sqrt
import pdb

gROOT.Reset()
gROOT.SetStyle("Plain")
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetTitleOffset(1.2,"Y")
gStyle.SetPadLeftMargin(0.11)
gStyle.SetPadBottomMargin(0.1)
gStyle.SetPadTopMargin(0.02)
gStyle.SetPadRightMargin(0.02)
gStyle.SetMarkerSize(1.5)
gStyle.SetHistLineWidth(1)
gStyle.SetStatFontSize(0.020)
gStyle.SetTitleSize(0.06, "XYZ")
gStyle.SetLabelSize(0.05, "XYZ")
gStyle.SetNdivisions(510, "XYZ")
gStyle.SetLegendBorderSize(0)
gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)

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
    

if __name__=="__main__":

    unfoldedData=True
    
    coupling="0p75"
    
    style="Axial"
    #style="Vector"

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
  
    #gROOT.LoadMacro("CMS_lumi.C");
    #iPeriod = 5;        #// 1=7TeV, 2=8TeV, 3=7+8TeV, 7=7+8+13TeV 
    #iPos = 33;
    
    prefix="datacard_shapelimit13TeV"
    
    h3news=[]
    h2news=[]
    h4zs=[]
    h4ys=[]
    h4xs=[]
    h4s=[]
    h4bs=[]
    h4cs=[]
    h4ds=[]
    h4es=[]
    h4fs=[]
    h4gs=[]
    h4hs=[]
    h4is=[]
    h14Gs=[]
    h14Gsysstats=[]
    hNloQcds=[]
    ls=[]
    h4={}

    new_hists=[]
    for massbin in range(0,7):

        ### NLOQCD+EWK
        
        filename="fastnlo/RunII/fnl5662j_cs_ct14nlo_30000_LL+.root"
        print filename
        fNloQcd = TFile.Open(filename)
        new_hists+=[fNloQcd]
        histname='chi-'+str(massbins[massbin]).strip("()").replace(',',"-").replace(' ',"").replace("6000-13000","6000-6600")
        print histname
        hNloQcd=fNloQcd.Get(histname)
	print "NLO QCD hist: "
        print fNloQcd
	hNloQcd=rebin2(hNloQcd,len(chi_binnings[massbin])-1,chi_binnings[massbin])
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

        hNloQcdbackup=hNloQcd.Clone(hNloQcd.GetName()+"backup")    

        ### Data
        
        if unfoldedData:
          filename="Unfolded_chiNtuple_dataReReco_v3_Coarse_PFHT900_fromCB_AK4SF_pythia8_Pt_170toInf.root"
          masstext=str(massbins[massbin]).strip("()").replace(',',".0-").replace(' ',"")
          #histname="dijet_mass2_chi1_unfolded;"+str(massbin+1)
          histname="dijet_mass_"+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_chi_unfolded;1"
	else:
          filename="datacards/datacard_shapelimit13TeV_25nsData11combi_chi2016.root"
          masstext=str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")
          histname='data_obs#chi'+masstext+'_rebin1'
        print filename
        fData = TFile.Open(filename)
        new_hists+=[fData]
        print histname
        h14=fData.Get(histname)
	if not unfoldedData:
          for b in range(h14.GetXaxis().GetNbins()):
            h14.SetBinContent(b+1,h14.GetBinContent(b+1)*h14.GetBinWidth(b+1))
            h14.SetBinError(b+1,h14.GetBinError(b+1)*h14.GetBinWidth(b+1))
	origh14=h14.Rebin(len(chi_binnings[massbin])-1,h14.GetName()+"rebinorig",chi_binnings[massbin])
	h14=rebin2(h14,len(chi_binnings[massbin])-1,chi_binnings[massbin])
	    
	h14G=TGraphAsymmErrors(h14.Clone(histname+"G"))
        new_hists+=[h14G]
        h14G.SetMarkerStyle(21)
        h14G.SetMarkerSize(0.4)
        h14G.SetMarkerColor(1)
        h14G.SetLineColor(1)
	alpha=1.-0.6827
	nevents=0
	for b in range(h14G.GetN()):
	    if unfoldedData:
	        N=origh14.GetBinContent(b+1)
	    else:
	        N=1./pow(h14.GetBinError(b+1)/h14.GetBinContent(b+1),2)
	    print N
	    nevents+=N
	    L=0
	    if N>0:
	        L=ROOT.Math.gamma_quantile(alpha/2.,N,1.)
            U=ROOT.Math.gamma_quantile_c(alpha/2.,N+1,1.)
            h14G.SetPointEYlow(b,(N-L)/N*h14.GetBinContent(b+1))
            h14G.SetPointEYhigh(b,(U-N)/N*h14.GetBinContent(b+1))
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
        #uncertaintynames=["jer","jes","scale"]
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
        h2new.SetLineColor(10)
        h2new.SetFillColor(10)
        h3new.SetLineColor(10)
        h3new.SetFillColor(15)
        #h3new.SetFillStyle(3003)

        ##### Signals

        if style=="Axial":  
            filename='datacard_shapelimit13TeV_DMAxial_Dijet_LO_Mphi_1000_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'_chi2016.root'
            histname='DMAxial_Dijet_LO_Mphi_1000_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        elif style=="Vector":
            filename='datacard_shapelimit13TeV_DMVector_Dijet_LO_Mphi_1000_1_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_'+coupling+'_ga_0_chi2016.root'
            histname='DMVector_Dijet_LO_Mphi_1000_1_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_'+coupling+'_ga_0#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print filename
        f4z = TFile.Open(filename)
        new_hists+=[f4z]
        print histname
        h4z=f4z.Get(histname)

        if style=="Axial": 
            filename='datacard_shapelimit13TeV_DMAxial_Dijet_LO_Mphi_1500_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'_chi2016.root'
            histname='DMAxial_Dijet_LO_Mphi_1500_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        elif style=="Vector":
            filename='datacard_shapelimit13TeV_DMVector_Dijet_LO_Mphi_1500_1_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_'+coupling+'_ga_0_chi2016.root'
            histname='DMVector_Dijet_LO_Mphi_1500_1_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_'+coupling+'_ga_0#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print filename
        f4y = TFile.Open(filename)
        new_hists+=[f4y]
        print histname
        h4y=f4y.Get(histname)

        if style=="Axial":    
            filename='datacard_shapelimit13TeV_DMAxial_Dijet_LO_Mphi_1750_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'_chi2016.root'
            histname='DMAxial_Dijet_LO_Mphi_1750_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        elif style=="Vector":
            filename='datacard_shapelimit13TeV_DMVector_Dijet_LO_Mphi_1750_1_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_'+coupling+'_ga_0_chi2016.root'
            histname='DMVector_Dijet_LO_Mphi_1750_1_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_'+coupling+'_ga_0#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print filename
        f4x = TFile.Open(filename)
        new_hists+=[f4x]
        print histname
        h4x=f4x.Get(histname)

        if style=="Axial":
            filename='datacard_shapelimit13TeV_DMAxial_Dijet_LO_Mphi_2000_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'_chi2016.root'
            histname='DMAxial_Dijet_LO_Mphi_2000_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        elif style=="Vector":
            filename='datacard_shapelimit13TeV_DMVector_Dijet_LO_Mphi_2000_1_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_'+coupling+'_ga_0_chi2016.root'
            histname='DMVector_Dijet_LO_Mphi_2000_1_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_'+coupling+'_ga_0#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print filename
        f4 = TFile.Open(filename)
        new_hists+=[f4]
        print histname
        h4=f4.Get(histname)

        if style=="Axial":    
            filename='datacard_shapelimit13TeV_DMAxial_Dijet_LO_Mphi_2250_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'_chi2016.root'
            histname='DMAxial_Dijet_LO_Mphi_2250_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        elif style=="Vector":
            filename='datacard_shapelimit13TeV_DMVector_Dijet_LO_Mphi_2250_1_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_'+coupling+'_ga_0_chi2016.root'
            histname='DMVector_Dijet_LO_Mphi_2250_1_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_'+coupling+'_ga_0#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print filename
        f4b = TFile.Open(filename)
        new_hists+=[f4b]
        print histname
        h4b=f4b.Get(histname)

        if style=="Axial":     
            filename='datacard_shapelimit13TeV_DMAxial_Dijet_LO_Mphi_2500_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'_chi2016.root'
            histname='DMAxial_Dijet_LO_Mphi_2500_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        elif style=="Vector":
            filename='datacard_shapelimit13TeV_DMVector_Dijet_LO_Mphi_2500_1_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_'+coupling+'_ga_0_chi2016.root'
            histname='DMVector_Dijet_LO_Mphi_2500_1_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_'+coupling+'_ga_0#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print filename
        f4c = TFile.Open(filename)
        new_hists+=[f4c]
        print histname
        h4c=f4c.Get(histname)

        if style=="Axial":   
            filename='datacard_shapelimit13TeV_DMAxial_Dijet_LO_Mphi_3000_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'_chi2016.root'
            histname='DMAxial_Dijet_LO_Mphi_3000_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        elif style=="Vector":
            filename='datacard_shapelimit13TeV_DMVector_Dijet_LO_Mphi_3000_1_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_'+coupling+'_ga_0_chi2016.root'
            histname='DMVector_Dijet_LO_Mphi_3000_1_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_'+coupling+'_ga_0#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print filename
        f4d = TFile.Open(filename)
        new_hists+=[f4d]
        print histname
        h4d=f4d.Get(histname)

        if style=="Axial":    
            filename='datacard_shapelimit13TeV_DMAxial_Dijet_LO_Mphi_3500_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'_chi2016.root'
            histname='DMAxial_Dijet_LO_Mphi_3500_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        elif style=="Vector":
            filename='datacard_shapelimit13TeV_DMVector_Dijet_LO_Mphi_3500_1_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_'+coupling+'_ga_0_chi2016.root'
            histname='DMVector_Dijet_LO_Mphi_3500_1_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_'+coupling+'_ga_0#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print filename
        f4e = TFile.Open(filename)
        new_hists+=[f4e]
        print histname
        h4e=f4e.Get(histname)

        if style=="Axial":    
            filename="datacard_shapelimit13TeV_DMAxial_Dijet_LO_Mphi_4000_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_"+coupling+"_chi2016.root"
            histname='DMAxial_Dijet_LO_Mphi_4000_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        elif style=="Vector":
            filename='datacard_shapelimit13TeV_DMVector_Dijet_LO_Mphi_4000_1_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_'+coupling+'_ga_0_chi2016.root'
            histname='DMVector_Dijet_LO_Mphi_4000_1_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_'+coupling+'_ga_0#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print filename
        f4f = TFile.Open(filename)
        new_hists+=[f4f]
        print histname
        h4f=f4f.Get(histname)

        if style=="Axial":     
            filename='datacard_shapelimit13TeV_DMAxial_Dijet_LO_Mphi_4500_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'_chi2016.root'
            histname='DMAxial_Dijet_LO_Mphi_4500_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        elif style=="Vector":
            filename='datacard_shapelimit13TeV_DMVector_Dijet_LO_Mphi_4500_1_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_'+coupling+'_ga_0_chi2016.root'
            histname='DMVector_Dijet_LO_Mphi_4500_1_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_'+coupling+'_ga_0#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print filename
        f4g = TFile.Open(filename)
        new_hists+=[f4g]
        print histname
        h4g=f4g.Get(histname)

        if style=="Axial":  
            filename='datacard_shapelimit13TeV_DMAxial_Dijet_LO_Mphi_5000_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'_chi2016.root'
            histname='DMAxial_Dijet_LO_Mphi_5000_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        elif style=="Vector":
            filename='datacard_shapelimit13TeV_DMVector_Dijet_LO_Mphi_5000_1_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_'+coupling+'_ga_0_chi2016.root'
            histname='DMVector_Dijet_LO_Mphi_5000_1_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_'+coupling+'_ga_0#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print filename
        f4h = TFile.Open(filename)
        new_hists+=[f4h]
        print histname
        h4h=f4h.Get(histname)

        if style=="Axial":  
            filename='datacard_shapelimit13TeV_DMAxial_Dijet_LO_Mphi_6000_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'_chi2016.root'
            histname='DMAxial_Dijet_LO_Mphi_6000_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_'+coupling+'#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        elif style=="Vector":
            filename='datacard_shapelimit13TeV_DMVector_Dijet_LO_Mphi_6000_1_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_'+coupling+'_ga_0_chi2016.root'
            histname='DMVector_Dijet_LO_Mphi_6000_1_1p5_1p0_Mar5_gdmv_1p0_gdma_0_gv_'+coupling+'_ga_0#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print filename
        f4i = TFile.Open(filename)
        new_hists+=[f4i]
        print histname
        h4i=f4i.Get(histname)
        
        ### Customize Histograms
        
        hNloQcd.GetYaxis().SetRangeUser(0.03,0.13)
        hNloQcd.GetXaxis().SetTitle("#chi_{dijet}")
        hNloQcd.GetYaxis().SetTitle("1/#sigma_{dijet} d#sigma_{dijet}/d#chi_{dijet}")
        hNloQcd.GetYaxis().SetTitleOffset(0.9)
        hNloQcd.GetXaxis().SetTitleOffset(0.65)
        hNloQcd.GetYaxis().SetTitleSize(0.06)
        hNloQcd.GetYaxis().SetLabelSize(0.05)
        hNloQcd.GetXaxis().SetTitleSize(0.05)
        hNloQcd.GetXaxis().SetLabelSize(0.04)
        hNloQcd.GetXaxis().SetTickLength(0.04)
        hNloQcd.GetYaxis().SetTickLength(0.03)
        hNloQcd.GetYaxis().SetNdivisions(505)
        hNloQcd.SetLineColor(10)

        setUpDMHists(h4z,8,1,2)
        setUpDMHists(h4y,4,1,2)
        setUpDMHists(h4x,5,1,2)
        setUpDMHists(h4,28,5,2)
        setUpDMHists(h4b,32,7,2)
        setUpDMHists(h4c,6,3,2)
        setUpDMHists(h4d,kRed,1,2)
        setUpDMHists(h4e,8,6,2)
        setUpDMHists(h4f,kMagenta+3,7,2)
        setUpDMHists(h4g,kAzure+8,4,2)
        setUpDMHists(h4h,12,8,2)
        setUpDMHists(h4i,kOrange+7,8,2)
        
        h3news.append(h3new)
        h2news.append(h2new)
        h4zs.append(h4z)
        h4ys.append(h4y)
        h4xs.append(h4x)
        h4s.append(h4)
        h4bs.append(h4b)
        h4cs.append(h4c)
        h4ds.append(h4d)
        h4es.append(h4e)
        h4fs.append(h4f)
        h4gs.append(h4g)
        h4hs.append(h4h)
        h4is.append(h4i)
        h14Gs.append(h14G)
        #h14Gsyss.append(h14Gsys)
        h14Gsysstats.append(h14Gsysstat)
        hNloQcds.append(hNloQcd)
        
        ylabel=0.8
        #if massbin==0: title="1.9 < #font[72]{M_{jj}} < 2.4 TeV"
        if massbin==0: title="2.4 < #font[72]{M_{jj}} < 3.0 TeV"
        if massbin==1: title="3.0 < #font[72]{M_{jj}} < 3.6 TeV"
        if massbin==2: title="3.6 < #font[72]{M_{jj}} < 4.2 TeV"
        if massbin==3: title="4.2 < #font[72]{M_{jj}} < 4.8 TeV"
        if massbin==4: title="4.8 < #font[72]{M_{jj}} < 5.4 TeV"
        if massbin==5: title="5.4 < #font[72]{M_{jj}} < 6.0 TeV"
        if massbin==6: title=" #font[72]{M_{jj}} > 6.0 TeV"

        l=TLegend(0.6,ylabel,1.0,ylabel-0.005,title)
        l.SetTextSize(0.055)
        l.SetFillStyle(0)
        ls.append(l)

    h4={}
    h4["1000"]=h4zs
    h4["1500"]=h4ys
    h4["1750"]=h4xs
    h4["2000"]=h4s
    h4["2250"]=h4bs
    h4["2500"]=h4cs
    h4["3000"]=h4ds
    h4["3500"]=h4es
    h4["4000"]=h4fs
    h4["4500"]=h4gs
    h4["5000"]=h4hs
    h4["6000"]=h4is

    #sys.exit()

    c = TCanvas("combined", "combined", 0, 0, 1500, 900)
    c.Divide(3,3)
    for massbin in range(0,8):
        if massbin==0:
            c.cd(8)
            pad2=TPad("","",0, 0, 1, 1)
            pad2.Draw()
            pad2.cd()
            hNloQcds[massbin].Draw("axissame")
            h3news[massbin].Draw("histsame")
            h2news[massbin].Draw("histsame")
            
            #h4["1000"][massbin].Draw("histsame")
            #h4["1500"][massbin].Draw("histsame")
            #h4["1750"][massbin].Draw("histsame")
            #h4["2000"][massbin].Draw("histsame")
            #h4["2250"][massbin].Draw("histsame")
            h4["2500"][massbin].Draw("histsame")
            h4["3000"][massbin].Draw("histsame")
            h4["3500"][massbin].Draw("histsame")
            h4["4000"][massbin].Draw("histsame")
            h4["4500"][massbin].Draw("histsame")            
            h4["5000"][massbin].Draw("histsame")
            #h4["6000"][massbin].Draw("histsame")
            
            h14Gs[massbin].Draw("pzesame")
            #h14Gsyss[massbin].Draw("||same")
            h14Gsysstats[massbin].Draw("zesame")
            hNloQcds[massbin].Draw("histsame")
            hNloQcds[massbin].Draw("axissame")
            ls[massbin].Draw("same")
        elif massbin==1:
            c.cd(7)
            pad2=TPad("","",0, 0, 1, 1)
            pad2.Draw()
            pad2.cd()
            hNloQcds[massbin].Draw("axissame")
            h3news[massbin].Draw("histsame")
            h2news[massbin].Draw("histsame")
            
            #h4["1000"][massbin].Draw("histsame")
            #h4["1500"][massbin].Draw("histsame")
            #h4["1750"][massbin].Draw("histsame")
            #h4["2000"][massbin].Draw("histsame")
            #h4["2250"][massbin].Draw("histsame")
            h4["2500"][massbin].Draw("histsame")
            h4["3000"][massbin].Draw("histsame")
            h4["3500"][massbin].Draw("histsame")
            h4["4000"][massbin].Draw("histsame")
            h4["4500"][massbin].Draw("histsame")            
            h4["5000"][massbin].Draw("histsame")
            h4["6000"][massbin].Draw("histsame")
            
            h14Gs[massbin].Draw("pzesame")
            #h14Gsyss[massbin].Draw("||same")
            h14Gsysstats[massbin].Draw("zesame")
            hNloQcds[massbin].Draw("histsame")
            hNloQcds[massbin].Draw("axissame")
            ls[massbin].Draw("same")
        elif massbin==2:
            c.cd(6)
            pad2=TPad("","",0, 0, 1, 1)
            pad2.Draw()
            pad2.cd()
            hNloQcds[massbin].Draw("axissame")
            h3news[massbin].Draw("histsame")
            h2news[massbin].Draw("histsame")
            
            #h4["1000"][massbin].Draw("histsame")
            #h4["1500"][massbin].Draw("histsame")
            #h4["1750"][massbin].Draw("histsame")
            #h4["2000"][massbin].Draw("histsame")
            #h4["2250"][massbin].Draw("histsame")
            h4["2500"][massbin].Draw("histsame")
            h4["3000"][massbin].Draw("histsame")
            h4["3500"][massbin].Draw("histsame")
            h4["4000"][massbin].Draw("histsame")
            h4["4500"][massbin].Draw("histsame")            
            h4["5000"][massbin].Draw("histsame")
            h4["6000"][massbin].Draw("histsame")
            
            h14Gs[massbin].Draw("pzesame")
            #h14Gsyss[massbin].Draw("||same")
            h14Gsysstats[massbin].Draw("zesame")
            hNloQcds[massbin].Draw("histsame")
            hNloQcds[massbin].Draw("axissame")
            ls[massbin].Draw("same")
        elif massbin==3:
            c.cd(5)
            pad2=TPad("","",0, 0, 1, 1)
            pad2.Draw()
            pad2.cd()
            hNloQcds[massbin].Draw("axissame")
            h3news[massbin].Draw("histsame")
            h2news[massbin].Draw("histsame")
            
            #h4["1000"][massbin].Draw("histsame")
            #h4["1500"][massbin].Draw("histsame")
            #h4["1750"][massbin].Draw("histsame")
            #h4["2000"][massbin].Draw("histsame")
            #h4["2250"][massbin].Draw("histsame")
            #h4["2500"][massbin].Draw("histsame")
            h4["3000"][massbin].Draw("histsame")
            h4["3500"][massbin].Draw("histsame")
            h4["4000"][massbin].Draw("histsame")
            h4["4500"][massbin].Draw("histsame")            
            h4["5000"][massbin].Draw("histsame")
            h4["6000"][massbin].Draw("histsame")
            
            h14Gs[massbin].Draw("pzesame")
            #h14Gsyss[massbin].Draw("||same")
            h14Gsysstats[massbin].Draw("zesame")
            hNloQcds[massbin].Draw("histsame")
            hNloQcds[massbin].Draw("axissame")
            ls[massbin].Draw("same")
        elif massbin==4:
            c.cd(4)
            pad2=TPad("","",0, 0, 1, 1)
            pad2.Draw()
            pad2.cd()
            hNloQcds[massbin].Draw("axissame")
            h3news[massbin].Draw("histsame")
            h2news[massbin].Draw("histsame")
            
            #h4["1000"][massbin].Draw("histsame")
            #h4["1500"][massbin].Draw("histsame")
            #h4["1750"][massbin].Draw("histsame")
            #h4["2000"][massbin].Draw("histsame")
            #h4["2250"][massbin].Draw("histsame")
            #h4["2500"][massbin].Draw("histsame")
            #h4["3000"][massbin].Draw("histsame")
            h4["3500"][massbin].Draw("histsame")
            h4["4000"][massbin].Draw("histsame")
            h4["4500"][massbin].Draw("histsame")            
            h4["5000"][massbin].Draw("histsame")
            h4["6000"][massbin].Draw("histsame")
            
            h14Gs[massbin].Draw("pzesame")
            #h14Gsyss[massbin].Draw("||same")
            h14Gsysstats[massbin].Draw("zesame")
            hNloQcds[massbin].Draw("histsame")
            hNloQcds[massbin].Draw("axissame")
            ls[massbin].Draw("same")
        elif massbin==5:
            c.cd(3)
            pad2=TPad("","",0, 0, 1, 1)
            pad2.Draw()
            pad2.cd()
            hNloQcds[massbin].Draw("axissame")
            h3news[massbin].Draw("histsame")
            h2news[massbin].Draw("histsame")
            
            #h4["1000"][massbin].Draw("histsame")
            #h4["1500"][massbin].Draw("histsame")
            #h4["1750"][massbin].Draw("histsame")
            #h4["2000"][massbin].Draw("histsame")
            #h4["2250"][massbin].Draw("histsame")
            #h4["2500"][massbin].Draw("histsame")
            #h4["3000"][massbin].Draw("histsame")
            #h4["3500"][massbin].Draw("histsame")
            h4["4000"][massbin].Draw("histsame")
            h4["4500"][massbin].Draw("histsame")            
            h4["5000"][massbin].Draw("histsame")
            h4["6000"][massbin].Draw("histsame")
            
            h14Gs[massbin].Draw("pzesame")
            #h14Gsyss[massbin].Draw("||same")
            h14Gsysstats[massbin].Draw("zesame")
            hNloQcds[massbin].Draw("histsame")
            hNloQcds[massbin].Draw("axissame")
            ls[massbin].Draw("same")
        elif massbin==6:
            c.cd(2)
            pad2=TPad("","",0, 0, 1, 1)
            pad2.Draw()
            pad2.cd()
            hNloQcds[massbin].Draw("axissame")
            h3news[massbin].Draw("histsame")
            h2news[massbin].Draw("histsame")
            
            #h4["1000"][massbin].Draw("histsame")
            #h4["1500"][massbin].Draw("histsame")
            #h4["1750"][massbin].Draw("histsame")
            #h4["2000"][massbin].Draw("histsame")
            #h4["2250"][massbin].Draw("histsame")
            #h4["2500"][massbin].Draw("histsame")
            #h4["3000"][massbin].Draw("histsame")
            #h4["3500"][massbin].Draw("histsame")
            #h4["4000"][massbin].Draw("histsame")
            h4["4500"][massbin].Draw("histsame")            
            h4["5000"][massbin].Draw("histsame")
            h4["6000"][massbin].Draw("histsame")
            
            h14Gs[massbin].Draw("pzesame")
            #h14Gsyss[massbin].Draw("||same")
            h14Gsysstats[massbin].Draw("zesame")
            hNloQcds[massbin].Draw("histsame")
            hNloQcds[massbin].Draw("axissame")
            ls[massbin].Draw("same")
        elif massbin==7:
            #c.Update()
            c.cd(1)
            pad2=TPad("","",0, 0, 1, 1)
            pad2.Draw()
            pad2.cd()
            hNloQcds[6].Draw("axissame")
            #hNloQcds[6].SetLineColor(10)

        c.Update()
        
        h3newnew=h3news[6].Clone()
        h3newnew.SetLineColor(10)
        h3newnew.SetLineStyle(3)
        h3newnew.SetLineWidth(2)
        
        c.cd(1)
        l2=TLegend(0.3,0.15,0.6,0.93,"")
        l2.SetTextSize(0.045)
        l2.AddEntry(h14Gs[6],"Data","ple")
        l2.AddEntry(h3newnew,"NLO QCD+EW","fl")
        #l2.AddEntry(h4["1000"][6],"M_{Med} = 1.0 TeV","l")
        #l2.AddEntry(h4["1500"][6],"M_{Med} = 1.5 TeV","l")
        #l2.AddEntry(h4["1750"][6],"M_{Med} = 1.75 TeV","l")
        #l2.AddEntry(h4["2000"][6],"M_{Med} = 2.0 TeV","l")
        #l2.AddEntry(h4["2250"][6],"M_{Med} = 2.25 TeV","l")
        l2.AddEntry(h4["2500"][6],"M_{Med} = 2.5 TeV","l")
        l2.AddEntry(h4["3000"][6],"M_{Med} = 3.0 TeV","l")
        l2.AddEntry(h4["3500"][6],"M_{Med} = 3.5 TeV","l")
        l2.AddEntry(h4["4000"][6],"M_{Med} = 4.0 TeV","l")
        l2.AddEntry(h4["4500"][6],"M_{Med} = 4.5 TeV","l")
        l2.AddEntry(h4["5000"][6],"M_{Med} = 5.0 TeV","l")
        l2.AddEntry(h4["6000"][6],"M_{Med} = 6.0 TeV","l")
        l2.SetFillStyle(0)
        l2.Draw("same")
        xlow=11
        if style=="Axial":
            Mediator="Axial"
            #leg1=TLatex(xlow,0.08,"#splitline{#bf{"+Mediator+"-vector}}{#bf{mediator}}")
            leg1=TLegend(0.65,0.55,0.95,0.9,"#splitline{#bf{"+Mediator+"-vector}}{#bf{mediator}}")
        elif style=="Vector":
            #leg1=TLatex(xlow,0.08,"#splitline{#bf{Vector}}{#bf{mediator}}")
            leg1=TLegend(0.65,0.55,0.95,0.9,"#splitline{#bf{Vector}}{#bf{mediator}}")
        leg1.SetFillStyle(0)
        if coupling=="1":
            vcoupling="1.0"
        else:
            vcoupling=coupling.replace("p",".")
        #leg4=TLatex(xlow,0.06,"#splitline{#it{g_{q} = "+vcoupling+"}}{#it{g_{DM} = 1.0}}")
        leg4=TLegend(0.65,0.15,0.95,0.55,"#splitline{#it{g_{q} = "+vcoupling+"}}{#it{g_{DM} = 1.0}}")
        leg4.SetFillStyle(0)
        leg1.SetTextFont(42)
        leg4.SetTextFont(42)
        #leg5.SetTextFont(42)
        leg1.SetTextSize(0.060)
        leg4.SetTextSize(0.060)
        #leg5.SetTextSize(0.040)
        #leg4.Draw("same")
        #leg5.Draw("same")
        #leg1.Draw("same")
        leg4.Draw("same")
        #leg1.Draw("same")
        c.Update()
    #ans = raw_input('\npress return to continue, q to quit...')
    #if ans=='q':
    #    sys.exit()
  
    #// writing the lumi information and the CMS "logo"
    #CMS_lumi( c, iPeriod, iPos );
    
    #c.SaveAs(prefix + "_combined_theory"+str(massbin)+"_dm_"+style+"_"+coupling+"_2016.pdf")
    c.SaveAs(prefix + "_combined_theory_dm_"+style+"_"+coupling+"_2016.pdf")
