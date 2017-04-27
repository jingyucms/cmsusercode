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

    showData=True
    binByBinCorrect=False
    unfoldedData=True
    showRunI=False
    ak5Compare=False
    showSignal=True

    print "start ROOT"
    gROOT.Reset()
    gROOT.SetStyle("Plain")
    gStyle.SetOptStat(0)
    gStyle.SetOptFit(0)
    gStyle.SetTitleOffset(1.2,"Y")
    gStyle.SetPadLeftMargin(0.16)
    gStyle.SetPadBottomMargin(0.11)
    gStyle.SetPadTopMargin(0.05)
    gStyle.SetPadRightMargin(0.05)
    gStyle.SetMarkerSize(2.5)
    gStyle.SetHistLineWidth(1)
    gStyle.SetStatFontSize(0.020)
    gStyle.SetTitleSize(0.06, "XYZ")
    gStyle.SetLabelSize(0.05, "XYZ")
    gStyle.SetLegendBorderSize(0)
    gStyle.SetPadTickX(1)
    gStyle.SetPadTickY(1)
    gStyle.SetEndErrorSize(5)

    print "start CMS_lumi"

    gROOT.LoadMacro("CMS_lumi.C");
    iPeriod = 4;	#// 1=7TeV, 2=8TeV, 3=7+8TeV, 7=7+8+13TeV 
    iPos = 11;

    massbins13=[(1900,2400),
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

    offsets=[0,0,0,0,0,0,0]

    prefix="datacard_shapelimit"
    if not showData: prefix+="_nodata"
    if binByBinCorrect: prefix+="_binbybin"
    if unfoldedData: prefix+="_unfolded"
    if showRunI: prefix+="_withrun1"
    if ak5Compare: prefix+="_ak5"

    c = TCanvas("combined", "combined", 0, 0, 600, 800)
    c.Divide(1,1)
    
    pad=[]
    
    pad1=TPad("","",0,0.63,1,1)
    pad2=TPad("","",0,0.52,1,0.63)
    pad3=TPad("","",0,0.41,1,0.52)
    pad4=TPad("","",0,0.30,1,0.41)
    pad5=TPad("","",0,0.19,1,0.30)
    pad6=TPad("","",0,0.00,1,0.19)

    pad.append(pad1)
    pad.append(pad2)
    pad.append(pad3)
    pad.append(pad4)
    pad.append(pad5)
    pad.append(pad6)

    new_hists=[]
    
    for massbin in reversed(range(len(massbins13))):
      # NLO OCD plot (with EWK correction)
        if True:
            filename="fastnlo/RunII/fnl5662i_v23_fix_CT14_ak4.root"
            print filename
            fNloQcd = TFile.Open(filename)
            new_hists+=[fNloQcd]
            histname='chi-'+str(massbins13[massbin]).strip("()").replace(',',"-").replace(' ',"").replace("5400-13000","5400-6000").replace("4800-13000","4800-5400")
            print histname
            hNloQcd=fNloQcd.Get(histname)
	    print "NLO QCD hist: "
            print fNloQcd
	    hNloQcd=rebin(hNloQcd,len(chi_binnings[massbin])-1,chi_binnings[massbin])
            hNloQcd.SetLineColor(5)
            hNloQcd.SetLineStyle(3)
            hNloQcd.SetLineWidth(2)
	    hNloQcdNoEwk=hNloQcd.Clone(hNloQcd.GetName()+"noewk")
	    new_hists+=[hNloQcdNoEwk]
            hNloQcdNoEwk.Add(TF1("offset",str(offsets[massbin]),1,16))
  	    hNloQcdNoEwk.SetLineColor(6)
	    hNloQcdNoEwk.SetLineStyle(5)
	    hNloQcdNoEwk.SetLineWidth(2)
    
            filename="fastnlo/RunII/DijetAngularCMS13_ewk.root"
            print filename
            fEWK = TFile.Open(filename)
            new_hists+=[fEWK]
            histname='chi-'+str(massbins13[massbin]).strip("()").replace(',',"-").replace(' ',"").replace("5400-13000","5400-6000").replace("4800-13000","4800-5400")
            print histname
            hEWK=fEWK.Get(histname)
	    print "EWK hist: "
            print hEWK
	    if not ak5Compare:
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
            hNloQcd.Add(TF1("offset",str(offsets[massbin]),1,16))

            hNloQcd.SetTitle("")
            hNloQcd.GetXaxis().SetTitle("#chi_{dijet}")
            hNloQcd.GetYaxis().SetTitle("1/#sigma_{dijet} d#sigma_{dijet}/d#chi_{dijet}")

        # CI and ADD signal  

        if massbin>2:
            #filename="datacard_shapelimit13TeV_GENnp-2-v4_chi.root"
            filename="datacard_shapelimit13TeV_cs_nn30nlo_0_11000_LL+_chi.root"
            print filename
            f = TFile.Open(filename)
            new_hists+=[f]
            histname='cs_nn30nlo_0_11000_LL+#chi'+str(massbins13[massbin]).strip("()").replace(',',"_").replace(' ',"").replace("4800-13000","4800-5400")+"_rebin1"
            print histname
            h4=f.Get(histname)
            h4=h4.Rebin(len(chi_binnings[massbin])-1,h4.GetName()+"_rebin",chi_binnings[massbin])
            h4.SetLineColor(2)
            h4.Scale(1./h4.Integral())
            for b in range(h4.GetNbinsX()):
                h4.SetBinContent(b+1,h4.GetBinContent(b+1)/h4.GetBinWidth(b+1))
            
            filename="datacard_shapelimit13TeV_GENnp-22-v4_chi.root"
            print filename
            f = TFile.Open(filename)
            new_hists+=[f]
            histname='QCDADD10000#chi'+str(massbins13[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
            print histname
            h5=f.Get(histname)
            h5=h5.Rebin(len(chi_binnings[massbin])-1,h5.GetName()+"_rebin",chi_binnings[massbin])
            h5.SetLineColor(4)
            h5.SetLineStyle(2)
            h5.Scale(1./h5.Integral())
            for b in range(h5.GetNbinsX()):
                h5.SetBinContent(b+1,h5.GetBinContent(b+1)/h5.GetBinWidth(b+1))
            
            filename="datacard_shapelimit13TeV_QBH_7500_6_chi_v1.root"
            print filename
            f = TFile.Open(filename)
            new_hists+=[f]
            histname='qbh_7500_6_#chi'+str(massbins13[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
            print histname
            h6=f.Get(histname)
            h6=h6.Rebin(len(chi_binnings[massbin])-1,h6.GetName()+"_rebin",chi_binnings[massbin])
            h6.SetLineColor(kGreen+3)
            h6.SetLineStyle(4)
            h6.Scale(1./h6.Integral())
            for b in range(h6.GetNbinsX()):
                h6.SetBinContent(b+1,h6.GetBinContent(b+1)/h6.GetBinWidth(b+1))
            
            h4.Add(TF1("offset",str(offsets[massbin]),1,16))
            h5.Add(TF1("offset",str(offsets[massbin]),1,16))
            h6.Add(TF1("offset",str(offsets[massbin]),1,16))
            h4.SetLineWidth(2)
            h5.SetLineWidth(2)
            h6.SetLineWidth(2)

        # Unfolded data
      
        if unfoldedData:
          filename="datacards/Unfolded_chiNtuple_PFHT800_20160530_fromCB_AK4SF_DataToMCSF_Pythia_M_1000toInf.root"
          masstext=str(massbins13[massbin]).strip("()").replace(',',".0-").replace(' ',"")
          histname='dijet_mass1_chi2__projY_'+masstext+'.0_unfolded'
	else:
          filename="datacards/datacard_shapelimit13TeV_25nsData7_chi.root"
          masstext=str(massbins13[massbin]).strip("()").replace(',',"_").replace(' ',"")
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
            histname1='QCD#chi'+str(massbins13[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1_"+u+"Up"
            print histname1
            histname2='QCD#chi'+str(massbins13[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1_"+u+"Down"
            print histname2
            histname3='QCD#chi'+str(massbins13[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
            print histname3
            up=fsys.Get(histname1)
            down=fsys.Get(histname2)
            central=fsys.Get(histname3)
            uncertainties+=[[up,down,central]]
        h2new=h14.Clone("down"+str(massbins13[massbin]))
        h3new=h14.Clone("up"+str(massbins13[massbin]))
	chi2=0
        for b in range(h14.GetXaxis().GetNbins()):
            if b==0:# or b==h14G.GetXaxis().GetNbins()-1:
                print massbins13[massbin],b,"stat",h14G.GetErrorYlow(b)/h14G.GetY()[b],h14G.GetErrorYhigh(b)/h14G.GetY()[b]
	    exp_sumdown=0
	    exp_sumup=0
            theory_sumdown=0
            theory_sumup=0
            for up,down,central in uncertainties:
	        if b==0:# or b==h14G.GetXaxis().GetNbins()-1:
                    print massbins13[massbin],b,uncertaintynames[uncertainties.index([up,down,central])],abs(up.GetBinContent(b+1)-central.GetBinContent(b+1))/central.GetBinContent(b+1),abs(down.GetBinContent(b+1)-central.GetBinContent(b+1))/central.GetBinContent(b+1)
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
                  
        h14G.Apply(TF2("offset",str(offsets[massbin])+"+y",1,16))
        h14Gsys.Apply(TF2("offset",str(offsets[massbin])+"+y",1,16))
        h14Gsysstat.Apply(TF2("offset",str(offsets[massbin])+"+y",1,16))
        h2new.Add(TF1("offset",str(offsets[massbin]),1,16))
        h3new.Add(TF1("offset",str(offsets[massbin]),1,16))
        
        c.cd()
        if massbin==1 or massbin==2 or massbin==3 or massbin==4:
            pad[massbin].SetBottomMargin(0.)
            pad[massbin].SetTopMargin(0.)
        if massbin==0:
            pad[massbin].SetBottomMargin(0.)
            pad[massbin].SetTopMargin(0.14)
        if massbin==5:
            pad[massbin].SetTopMargin(0.)
            pad[massbin].SetBottomMargin(0.475)
            
        pad[5-massbin].Draw()
        
        pad[5-massbin].cd()

        if massbin==5:
            hNloQcd.GetYaxis().SetRangeUser(0.02,0.23)        
        elif massbin>=3:
            hNloQcd.GetYaxis().SetRangeUser(0.04,0.11)       
        else:
            hNloQcd.GetYaxis().SetRangeUser(0.04,0.11)          
            
        if massbin!=5:
            hNloQcd.GetYaxis().SetTitleSize(0.)
	    
	bigger=1.2

        if massbin==5:
            hNloQcd.GetYaxis().SetTitleOffset(0.65)
            hNloQcd.GetYaxis().SetTitleSize(0.096*bigger)
            hNloQcd.GetYaxis().SetLabelSize(0.074*bigger)
            hNloQcd.GetYaxis().SetLabelOffset(0.005)

        if massbin==0:
            hNloQcd.GetXaxis().SetTitleSize(0.19*bigger)
            hNloQcd.GetXaxis().SetLabelSize(0.14*bigger)
            hNloQcd.GetXaxis().SetTitleOffset(0.78)
            hNloQcd.GetYaxis().SetLabelSize(0.14*bigger)
            hNloQcd.GetYaxis().SetLabelOffset(0.005)
        
        if massbin<5 and massbin>0:
            hNloQcd.GetYaxis().SetLabelSize(0.246*bigger)
            hNloQcd.GetYaxis().SetLabelOffset(0.005)

        if massbin==0 or massbin==1 or massbin==2:
            hNloQcd.GetYaxis().SetNdivisions(503)

        if massbin==3 or massbin==4:
            hNloQcd.GetYaxis().SetNdivisions(503)

        if massbin==5:
            hNloQcd.GetYaxis().SetNdivisions(505)

        if massbin!=5 and massbin!=0:            
            hNloQcd.GetXaxis().SetTickLength(0.04)
            hNloQcd.GetYaxis().SetTickLength(0.025)
        if massbin==0:
            hNloQcd.GetXaxis().SetTickLength(0.03)
            hNloQcd.GetYaxis().SetTickLength(0.05)
        if massbin==5:
            hNloQcd.GetXaxis().SetTickLength(0.01)

        hNloQcd.GetXaxis().SetNdivisions(110)

        h14G.SetMarkerSize(1.0)
        hNloQcd.SetLineColor(1)
        
        hNloQcd.Draw("axissame")
        h3new.Draw("histsame")
        h2new.Draw("histsame")
        hNloQcd.Draw("histsame")
        #hNloQcdNoEwk.Draw("histsame")
        if massbin>2:
            h4.Draw("histsame")
            h5.Draw("histsame")
            h6.Draw("histsame")
        h14G.Draw("pzesame")
        #h14Gsys.Draw("||same")
        h14Gsysstat.Draw("zesame")
              
        if massbin==0: title="1.9 < #font[72]{M}_{jj} < 2.4 TeV"
        if massbin==1: title="2.4 < #font[72]{M}_{jj} < 3.0 TeV"
        if massbin==2: title="3.0 < #font[72]{M}_{jj} < 3.6 TeV"
        if massbin==3: title="3.6 < #font[72]{M}_{jj} < 4.2 TeV"
        if massbin==4: title="4.2 < #font[72]{M}_{jj} < 4.8 TeV"
        if massbin==5: title=" #font[72]{M}_{jj} > 4.8 TeV"

        if massbin==5:
            ylabel1=0.33
            ylabel2=0.23
            Size=0.06
        elif massbin==0:
            ylabel1=0.785
            ylabel2=0.95
            Size=0.12
        else:
            ylabel1=0.6
            ylabel2=0.95
            Size=0.21
        
        l=TLegend(0.65,ylabel1,1.0,ylabel2,title)
        l.SetTextSize(Size)
        l.SetFillStyle(0)
        l.Draw("same")
        new_hists+=[l]
        pad[5-massbin].RedrawAxis()

    pad[0].cd()
        
    h3newnew=h3new.Clone()
    h3newnew.SetLineColor(1)
    h3newnew.SetLineStyle(3)
    h3newnew.SetLineWidth(2)
    
    l2=TLegend(0.22,0.45,0.55,0.68,"")
    l2.SetTextSize(0.06)
    l2.AddEntry(h14G,"Data","ple")
    l2.AddEntry(h3newnew,"NLO QCD+EW","fl")
    #l2.AddEntry(hNloQcdNoEwk,"NLO QCD prediction","l")
    l2.SetFillStyle(0)
    l2.Draw("same")
    
    l3=TLegend(0.495,0.44,0.80,0.83,"")
    l3.SetTextSize(0.06)
    l3.AddEntry(h6,"M_{QBH} (n_{ED} = 6 ADD) = 7.5 TeV","l")
    l3.AddEntry(h4,"#Lambda_{LL}^{#font[122]{+}} (CI) = 11 TeV","l")
    l3.AddEntry(h5,"#Lambda_{T} (GRW) = 10 TeV","l")
    l3.SetFillStyle(0)
    l3.Draw("same")
    
    #// writing the lumi information and the CMS "logo"
    CMS_lumi( c, iPeriod, iPos );
    
    c.SaveAs(prefix + "_combined_RunII_25ns_v2.pdf")
    c.SaveAs(prefix + "_combined_RunII_25ns_v2.eps")
