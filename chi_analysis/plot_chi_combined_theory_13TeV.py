from ROOT import *
import ROOT
import array, math
import os
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

if __name__=="__main__":

  unfoldedData=True

  massbins=[(1900,2400),
  	      (2400,3000),
  	      (3000,3600),
  	      (3600,4200),
  	      (4200,4800),
  	      (4800,13000),
  ]

  chi_bins=[(1,2,3,4,5,6,7,8,9,10,12,14,16),
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

  for massbin in [3,4,5]:
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

    gROOT.LoadMacro("CMS_lumi.C");
    iPeriod = 4;	#// 1=7TeV, 2=8TeV, 3=7+8TeV, 7=7+8+13TeV 
    iPos = 33;
    #// second parameter in example_plot is iPos, which drives the position of the CMS logo in the plot
    #// iPos=11 : top-left, left-aligned
    #// iPos=33 : top-right, right-aligned
    #// iPos=22 : center, centered
    #// mode generally : 
    #//   iPos = 10*(alignement 1/2/3) + position (1/2/3 = left/center/right)

    prefix="datacard_shapelimit13TeV"

    c = TCanvas("combined", "combined", 0, 0, 400, 400)
    c.Divide(1,1)
    new_hists=[]
    if True:
        filename="fastnlo/RunII/fnl5662i_v23_fix_CT14_ak4.root"
        print filename
        fNloQcd = TFile.Open(filename)
        new_hists+=[fNloQcd]
        histname='chi-'+str(massbins[massbin]).strip("()").replace(',',"-").replace(' ',"").replace("5400-13000","5400-6000").replace("4800-13000","4800-5400")
        print histname
        hNloQcd=fNloQcd.Get(histname)
	print "NLO QCD hist: "
        print fNloQcd
	hNloQcd=rebin(hNloQcd,len(chi_binnings[massbin])-1,chi_binnings[massbin])
    
        filename="fastnlo/RunII/DijetAngularCMS13_ewk.root"
        print filename
        fEWK = TFile.Open(filename)
        new_hists+=[fEWK]
        histname='chi-'+str(massbins[massbin]).strip("()").replace(',',"-").replace(' ',"").replace("5400-13000","5400-6000").replace("4800-13000","4800-5400")
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

        filename="datacard_shapelimit13TeV_QCD_chi.root"
        print filename
        f = TFile.Open(filename)
        new_hists+=[f]
        histname='QCD#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print histname
        h0=f.Get(histname)
        h0.SetLineColor(1)
        h0.SetLineStyle(3)

        if unfoldedData:
          filename="datacards/Unfolded_chiNtuple_PFHT800_20160530_fromCB_AK4SF_DataToMCSF_Pythia_M_1000toInf.root"
          masstext=str(massbins[massbin]).strip("()").replace(',',".0-").replace(' ',"")
          histname='dijet_mass1_chi2__projY_'+masstext+'.0_unfolded'
	else:
          filename="datacards/datacard_shapelimit13TeV_25nsData7_chi.root"
          masstext=str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")
          histname='data_obs#chi'+masstext+'_rebin1'
        print filename
        fData = TFile.Open(filename)
        new_hists+=[fData]
        print histname
        h14=fData.Get(histname)
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

        filename="datacard_shapelimit13TeV_QCD_chi.root"
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
        h2new.SetLineColor(15)
        h2new.SetFillColor(10)
        h3new.SetLineColor(15)
        h3new.SetFillColor(15)

        if massbin>=0:
          filename="datacard_shapelimit13TeV_cs_nn30nlo_0_11000_LL+_chi.root"
          histname='cs_nn30nlo_0_11000_LL+#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print filename
          f = TFile.Open(filename)
          new_hists+=[f]
          print histname
          h4=f.Get(histname)
          h4.SetLineColor(2)
          h4.SetLineWidth(2)
	  h4.Scale(1./h4.Integral())
	  for b in range(h4.GetNbinsX()):
	       h4.SetBinContent(b+1,h4.GetBinContent(b+1)/h4.GetBinWidth(b+1))

          filename="datacard_shapelimit13TeV_cs_nn30nlo_0_11000_LL-_chi.root"
          histname='cs_nn30nlo_0_11000_LL-#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print filename
          f = TFile.Open(filename)
          new_hists+=[f]
          print histname
          h4b=f.Get(histname)
          h4b.SetLineColor(32)
          h4b.SetLineStyle(7)
          h4b.SetLineWidth(4)
	  h4b.Scale(1./h4b.Integral())
	  for b in range(h4b.GetNbinsX()):
	       h4b.SetBinContent(b+1,h4b.GetBinContent(b+1)/h4b.GetBinWidth(b+1))

          filename="datacard_shapelimit13TeV_cs_nn30nlo_0_11000_VV+_chi.root"
          histname='cs_nn30nlo_0_11000_VV+#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print filename
          f = TFile.Open(filename)
          new_hists+=[f]
          print histname
          h4c=f.Get(histname)
          h4c.SetLineColor(6)
          h4c.SetLineStyle(3)
          h4c.SetLineWidth(3)
	  h4c.Scale(1./h4c.Integral())
	  for b in range(h4c.GetNbinsX()):
	       h4c.SetBinContent(b+1,h4c.GetBinContent(b+1)/h4c.GetBinWidth(b+1))

          filename="datacard_shapelimit13TeV_cs_nn30nlo_0_11000_VV-_chi.root"
          histname='cs_nn30nlo_0_11000_VV-#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
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

          filename="datacard_shapelimit13TeV_cs_nn30nlo_0_11000_AA+_chi.root"
          histname='cs_nn30nlo_0_11000_AA+#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print filename
          f = TFile.Open(filename)
          new_hists+=[f]
          print histname
          h4e=f.Get(histname)
          h4e.SetLineColor(8)
          h4e.SetLineStyle(6)
          h4e.SetLineWidth(3)
	  h4e.Scale(1./h4e.Integral())
	  for b in range(h4e.GetNbinsX()):
	       h4e.SetBinContent(b+1,h4e.GetBinContent(b+1)/h4e.GetBinWidth(b+1))

          filename="datacard_shapelimit13TeV_cs_nn30nlo_0_11000_AA-_chi.root"
          histname='cs_nn30nlo_0_11000_AA-#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print filename
          f = TFile.Open(filename)
          new_hists+=[f]
          print histname
          h4f=f.Get(histname)
          h4f.SetLineColor(9)
          h4f.SetLineStyle(7)
          h4f.SetLineWidth(3)
	  h4f.Scale(1./h4f.Integral())
	  for b in range(h4f.GetNbinsX()):
	       h4f.SetBinContent(b+1,h4f.GetBinContent(b+1)/h4f.GetBinWidth(b+1))

          filename="datacard_shapelimit13TeV_cs_nn30nlo_0_11000_V-A+_chi.root"
          histname='cs_nn30nlo_0_11000_V-A+#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print filename
          f = TFile.Open(filename)
          new_hists+=[f]
          print histname
          h4g=f.Get(histname)
          h4g.SetLineColor(11)
          h4g.SetLineStyle(4)
          h4g.SetLineWidth(3)
	  h4g.Scale(1./h4g.Integral())
	  for b in range(h4g.GetNbinsX()):
	       h4g.SetBinContent(b+1,h4g.GetBinContent(b+1)/h4g.GetBinWidth(b+1))

          filename="datacard_shapelimit13TeV_cs_nn30nlo_0_11000_V-A-_chi.root"
          histname='cs_nn30nlo_0_11000_V-A-#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print filename
          f = TFile.Open(filename)
          new_hists+=[f]
          print histname
          h4h=f.Get(histname)
          h4h.SetLineColor(12)
          h4h.SetLineStyle(8)
          h4h.SetLineWidth(4)
	  h4h.Scale(1./h4h.Integral())
	  for b in range(h4h.GetNbinsX()):
	       h4h.SetBinContent(b+1,h4h.GetBinContent(b+1)/h4h.GetBinWidth(b+1))

          filename="datacard_shapelimit13TeV_GENnp-22-v4_chi.root"
          print filename
          f = TFile.Open(filename)
          new_hists+=[f]
          histname='QCDADD10000#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print histname
          h5=f.Get(histname)
          h5.SetLineColor(4)
          h5.SetLineStyle(2)
          h5.SetLineWidth(2)
	  h5.Scale(1./h5.Integral())
	  for b in range(h5.GetNbinsX()):
	       h5.SetBinContent(b+1,h5.GetBinContent(b+1)/h5.GetBinWidth(b+1))

          filename="datacard_shapelimit13TeV_QBH_7500_6_chi_v1.root"
          print filename
          f = TFile.Open(filename)
          new_hists+=[f]
          histname='qbh_7500_6_#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print histname
          h6=f.Get(histname)
          h6=h6.Rebin(len(chi_binnings[massbin])-1,h6.GetName()+"_rebin",chi_binnings[massbin])
          h6.SetLineColor(7)
          h6.SetLineStyle(4)
          h6.SetLineWidth(2)
          h6.Scale(1./h6.Integral())
          for b in range(h6.GetNbinsX()):
              h6.SetBinContent(b+1,h6.GetBinContent(b+1)/h6.GetBinWidth(b+1))
          
        #h0.Add(TF1("offset",str(offsets[massbin]),1,16))
        #h14G.Apply(TF2("offset",str(offsets[massbin])+"+y",1,16))
        #h14Gsys.Apply(TF2("offset",str(offsets[massbin])+"+y",1,16))
        #h14Gsysstat.Apply(TF2("offset",str(offsets[massbin])+"+y",1,16))
        #h2new.Add(TF1("offset",str(offsets[massbin]),1,16))
        #h3new.Add(TF1("offset",str(offsets[massbin]),1,16))
        #if massbin>=0:
        #    h4.Add(TF1("offset",str(offsets[massbin]),1,16))
        #    h4b.Add(TF1("offset",str(offsets[massbin]),1,16))
        #    h4c.Add(TF1("offset",str(offsets[massbin]),1,16))
        #    h4d.Add(TF1("offset",str(offsets[massbin]),1,16))
        #    h5.Add(TF1("offset",str(offsets[massbin]),1,16))
        
        h0.GetYaxis().SetRangeUser(0,0.24)
        h0.GetXaxis().SetTitle("#chi_{dijet}")
        h0.GetYaxis().SetTitle("1/#sigma_{dijet} d#sigma_{dijet}/d#chi_{dijet}")
        h0.GetYaxis().SetTitleOffset(1.4)
        h0.GetXaxis().SetTitleOffset(0.8)
        h0.GetYaxis().SetTitleSize(0.05)
        h0.GetYaxis().SetLabelSize(0.04)
        h0.GetXaxis().SetTitleSize(0.05)
        h0.GetXaxis().SetLabelSize(0.04)
        h0.GetXaxis().SetTickLength(0.02)
        h0.GetYaxis().SetNdivisions(505)
        c.cd(1)

        if massbin==len(massbins)-1:
            h0.Draw("axis")
        else:
            h0.Draw("axissame")
        h3new.Draw("histsame")
        h2new.Draw("histsame")
        h0.Draw("histsame")
        if massbin>=0:
             h4.Draw("histsame")
             h4b.Draw("histsame")
             h4c.Draw("histsame")
             h4d.Draw("histsame")
             #h4e.Draw("histsame")
             #h4f.Draw("histsame")
             h4g.Draw("histsame")
             #h4h.Draw("histsame")
             h5.Draw("histsame")
             h6.Draw("histsame")
        h14G.Draw("pzesame")
        h14Gsys.Draw("||same")
        h14Gsysstat.Draw("zesame")
        h0.Draw("axissame")

        ylabel=0.50
        
        if massbin==0: title="1.9 < #font[72]{M_{jj}} < 2.4 TeV"
        if massbin==1: title="2.4 < #font[72]{M_{jj}} < 3.0 TeV"
        if massbin==2: title="3.0 < #font[72]{M_{jj}} < 3.6 TeV"
        if massbin==3: title="3.6 < #font[72]{M_{jj}} < 4.2 TeV"
        if massbin==4: title="4.2 < #font[72]{M_{jj}} < 4.8 TeV"
        if massbin==5: title=" #font[72]{M_{jj}} > 4.8 TeV"

        #title+=" TeV"
        #if offsets[massbin]==0: titleo=""
        #elif offsets[massbin]<0: titleo="("+str(offsets[massbin])+")"
        #else: titleo="(+"+str(offsets[massbin])+")"

        l=TLegend(0.6,ylabel,1.0,ylabel-0.005,title)
        l.SetTextSize(0.033)
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

    l2=TLegend(0.3,0.54,0.6,0.93,"")
    l2.SetTextSize(0.035)
    l2.AddEntry(h14G,"Data","ple")
    l2.AddEntry(h3new,"NLO QCD+EW","f")
    l2.AddEntry(h6,"M_{QBH} (ADD6) = 7.5 TeV","l")
    l2.AddEntry(h4,"#Lambda_{LL}^{#font[122]{+}} (CI) = 11 TeV","l")
    l2.AddEntry(h4b,"#Lambda_{LL}^{#font[122]{-}} (CI) = 11 TeV","l")
    l2.AddEntry(h4c,"#Lambda_{VV}^{#font[122]{+}} (CI) = 11 TeV","l")
    l2.AddEntry(h4d,"#Lambda_{VV}^{#font[122]{-}} (CI) = 11 TeV","l")
    #l2.AddEntry(h4e,"#Lambda_{AA}^{#font[122]{+}} (CI) = 11 TeV","l")
    #l2.AddEntry(h4f,"#Lambda_{AA}^{#font[122]{-}} (CI) = 11 TeV","l")
    l2.AddEntry(h4g,"#Lambda_{V-A} (CI) = 11 TeV","l")
    #l2.AddEntry(h4h,"#Lambda_{V-A}^{#font[122]{-}} (CI) = 11 TeV","l")
    l2.AddEntry(h5,"#Lambda_{T} (GRW) = 10 TeV","l")
    l2.SetFillStyle(0)
    l2.Draw("same")

    l2b=TLegend(0.3,0.54,0.6,0.93,"")
    l2b.SetTextSize(0.035)
    l2b.AddEntry(h14G," ","")
    l2b.AddEntry(h0," ","l")
    l2b.AddEntry(h4," ","")
    l2b.AddEntry(h4b," ","")
    l2b.AddEntry(h4c," ","")
    l2b.AddEntry(h4d," ","")
    #l2b.AddEntry(h4e," ","")
    #l2b.AddEntry(h4f," ","")
    l2b.AddEntry(h4g," ","")
    #l2b.AddEntry(h4h," ","")
    l2b.AddEntry(h5," ","")
    l2b.AddEntry(h6," ","")
    l2b.SetFillStyle(0)
    l2b.Draw("same")
    
    tl1=TLine(16,0,16,0.24)
    tl1.SetLineColor(1)
    tl1.SetLineStyle(1)
    tl1.SetLineWidth(1)
    tl1.Draw("same")

    #// writing the lumi information and the CMS "logo"
    CMS_lumi( c, iPeriod, iPos );

    c.SaveAs(prefix + "_combined_theory"+str(massbin)+".pdf")
    c.SaveAs(prefix + "_combined_theory"+str(massbin)+".eps")
