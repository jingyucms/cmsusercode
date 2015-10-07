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
    writeExtraText = True;	 #// if extra text
    extraText  = "Preliminary";  #// default extra text is "Preliminary"
    lumi_13TeV  = "150 pb^{-1}"; #// default is "19.7 fb^{-1}"
    iPeriod = 4;	#// 1=7TeV, 2=8TeV, 3=7+8TeV, 7=7+8+13TeV 
    iPos = 1;
    #// second parameter in example_plot is iPos, which drives the position of the CMS logo in the plot
    #// iPos=11 : top-left, left-aligned
    #// iPos=33 : top-right, right-aligned
    #// iPos=22 : center, centered
    #// mode generally : 
    #//   iPos = 10*(alignement 1/2/3) + position (1/2/3 = left/center/right)

    massbins=[(1900,2400),
              (2400,3000),
              (3000,3600),
              (3600,4200),
              (4200,8000)]

    massbins13=[(1900,2400),
              (2400,3000),
              (3000,3600),
              (3600,4200),
              (4200,13000),
              #(4800,5400),
              #(5400,6000)
	      ]

    chi_bins=[(1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,3,6,9,12,16),
               (1,3,6,9,12,16),
               (1,3,6,9,12,16),
              ]
    chi_binnings=[]
    for mass_bin in chi_bins:
        chi_binnings+=[array.array('d')]
        for chi_bin in mass_bin:
            chi_binnings[-1].append(chi_bin)

    offsets=[0,0.05,0.1,0.15,0.25,0.35,0.45]

    prefix="datacard_shapelimit"

    c = TCanvas("combined", "combined", 0, 0, 400, 600)
    c.Divide(1,1)
    new_hists=[]
    for massbin in reversed(range(len(massbins13))):
      
      if massbin<5:
        filename="datacard_shapelimit_data_sys.root"
        print filename
        f = TFile.Open(filename)
        new_hists+=[f]
        histname='QCD#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print histname
        h0=f.Get(histname)
        h0.SetLineColor(1)
        h0.SetLineStyle(3)
	
	h6=h0.Clone(histname+"noEWK")
        histname='ewk-chi-'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"").replace("_","-")
        ewk=f.Get(histname)
	for b in range(h6.GetXaxis().GetNbins()):
	    low_bin=ewk.FindBin(h6.GetXaxis().GetBinLowEdge(b+1))
	    up_bin=ewk.FindBin(h6.GetXaxis().GetBinUpEdge(b+1))
	    correction=ewk.Integral(low_bin,up_bin-1)/(up_bin-low_bin)
            h6.SetBinContent(b+1,h6.GetBinContent(b+1)/correction)
	h6.SetLineColor(6)
	h6.SetLineStyle(5)
	h6.SetLineWidth(2)
	new_hists+=[h6]

        histname='Graph_from_dijet_'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"").replace("8000","7000")+"_chi_rebin1"
        print histname
        h1=f.Get(histname)
        h1.SetMarkerStyle(20)
        h1.SetMarkerSize(0.4)
	h1sys=h1.Clone(histname+"sys")
	h1sys.SetMarkerSize(0)
	new_hists+=[h1sys]
	h1sysstat=h1.Clone(histname+"sysstat")
	h1sysstat.SetMarkerSize(0)
	new_hists+=[h1sysstat]

        uncertaintynames=["jer","jes","pdf","scale"]
        uncertainties=[]
        for u in uncertaintynames:
            histname1='QCD#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1_"+u+"Up"
            print histname1
            histname2='QCD#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1_"+u+"Down"
            print histname2
            up=f.Get(histname1)
            down=f.Get(histname2)
            uncertainties+=[[up,down]]
        h2=h0.Clone("down"+str(massbins[massbin]))
        h3=h0.Clone("up"+str(massbins[massbin]))
	chi2=0
        for b in range(h0.GetXaxis().GetNbins()):
            if b==0:# or b==h0.GetXaxis().GetNbins()-1:
                print massbins[massbin],b,"stat",h1.GetErrorYlow(b)/h1.GetY()[b],h1.GetErrorYhigh(b)/h1.GetY()[b]
	    exp_sumdown=0
	    exp_sumup=0
            theory_sumdown=0
            theory_sumup=0
            for up,down in uncertainties:
	        if b==0:# or b==h0.GetXaxis().GetNbins()-1:
                    print massbins[massbin],b,uncertaintynames[uncertainties.index([up,down])],abs(up.GetBinContent(b+1)-h0.GetBinContent(b+1))/h0.GetBinContent(b+1),abs(down.GetBinContent(b+1)-h0.GetBinContent(b+1))/h0.GetBinContent(b+1)
                addup=pow(max(0,up.GetBinContent(b+1)-h0.GetBinContent(b+1),down.GetBinContent(b+1)-h0.GetBinContent(b+1)),2)
		adddown=pow(max(0,h0.GetBinContent(b+1)-up.GetBinContent(b+1),h0.GetBinContent(b+1)-down.GetBinContent(b+1)),2)
                if uncertaintynames[uncertainties.index([up,down])]=="jer" or uncertaintynames[uncertainties.index([up,down])]=="jes":
		  exp_sumup+=addup
                  exp_sumdown+=adddown
		else:
		  theory_sumup+=addup
                  theory_sumdown+=adddown
            exp_sumdown=sqrt(exp_sumdown)
            exp_sumup=sqrt(exp_sumup)
            theory_sumdown=sqrt(theory_sumdown)
            theory_sumup=sqrt(theory_sumup)

	    chi2+=pow(h0.GetBinContent(b+1)-h1.GetY()[b],2) / \
	            (pow(max(exp_sumdown,exp_sumup),2)+pow(max(theory_sumdown,theory_sumup),2)+pow(max(h1.GetErrorYlow(b),h1.GetErrorYhigh(b)),2))

            h1sys.SetPointEXlow(b,0)
            h1sys.SetPointEXhigh(b,0)
            h1sys.SetPointEYlow(b,exp_sumdown)
            h1sys.SetPointEYhigh(b,exp_sumup)
            h1sysstat.SetPointEXlow(b,0)
            h1sysstat.SetPointEXhigh(b,0)
            h1sysstat.SetPointEYlow(b,sqrt(pow(exp_sumdown,2)+pow(h1.GetErrorYlow(b),2)))
            h1sysstat.SetPointEYhigh(b,sqrt(pow(exp_sumup,2)+pow(h1.GetErrorYhigh(b),2)))
	    stat_up=h1.GetErrorYhigh(b)
            stat_down=h1.GetErrorYlow(b)
            h1.SetPointEYlow(b,0)
            h1.SetPointEYhigh(b,0)
            h2.SetBinContent(b+1,h0.GetBinContent(b+1)-theory_sumdown)
            h3.SetBinContent(b+1,h0.GetBinContent(b+1)+theory_sumup)
	    #print h2.GetXaxis().GetBinLowEdge(b+1),h2.GetXaxis().GetBinUpEdge(b+1),h1.GetY()[b],sqrt(pow(exp_sumdown,2)+pow(stat_down,2)),sqrt(pow(exp_sumup,2)+pow(stat_up,2))
	    print "{0:.1f} TO {1:.1f}; {2:.4f} +{3:.4f},-{4:.4f} (DSYS=+{5:.4f},-{6:.4f})".format(h2.GetXaxis().GetBinLowEdge(b+1),h2.GetXaxis().GetBinUpEdge(b+1),h1.GetY()[b],sqrt(pow(stat_up,2)),sqrt(pow(stat_down,2)),sqrt(pow(exp_sumup,2)),sqrt(pow(exp_sumdown,2)))
        print "chi2/ndof",chi2/h0.GetXaxis().GetNbins()
	new_hists+=[h2]
        new_hists+=[h3]
        h2.SetLineStyle(1)
        h3.SetLineStyle(1)
        h2.SetLineColor(15)
        h2.SetFillColor(10)
        h3.SetLineColor(15)
        h3.SetFillColor(15)

        if massbin>1:
          filename="datacard_shapelimit13TeV_GEN_chi.root"
          print filename
          f = TFile.Open(filename)
          new_hists+=[f]
          histname='QCDCIplusLL10000#chi'+str(massbins13[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print histname
          h4=f.Get(histname)
          h4.SetLineColor(8)
	  h4.Scale(1./h4.Integral())
	  for b in range(h4.GetNbinsX()):
	       h4.SetBinContent(b+1,h4.GetBinContent(b+1)/h4.GetBinWidth(b+1))

          filename="datacard_shapelimit_ADD_4_0_1_7000_chi.root"
          print filename
          f = TFile.Open(filename)
          new_hists+=[f]
          histname='QCDADD_4_0_1_7000#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print histname
          h5=f.Get(histname)
          h5.SetLineColor(4)
          h5.SetLineStyle(2)
	  h5.Scale(1./h5.Integral())
	  for b in range(h5.GetNbinsX()):
	       h5.SetBinContent(b+1,h5.GetBinContent(b+1)/h5.GetBinWidth(b+1))

        h0.Add(TF1("offset",str(offsets[massbin]),1,16))
        h6.Add(TF1("offset",str(offsets[massbin]),1,16))
        h1.Apply(TF2("offset",str(offsets[massbin])+"+y",1,16))
        h1sys.Apply(TF2("offset",str(offsets[massbin])+"+y",1,16))
        h1sysstat.Apply(TF2("offset",str(offsets[massbin])+"+y",1,16))
        h2.Add(TF1("offset",str(offsets[massbin]),1,16))
        h3.Add(TF1("offset",str(offsets[massbin]),1,16))
        if massbin>1:
            h4.Add(TF1("offset",str(offsets[massbin]),1,16))
            h5.Add(TF1("offset",str(offsets[massbin]),1,16))

      if massbin<5:

        h0.SetTitle("")
	h0.GetYaxis().SetRangeUser(0,0.8)
	if len(massbins13)==5:
	  h0.GetYaxis().SetRangeUser(0,0.6)
        h0.GetXaxis().SetTitle("#chi_{dijet}")
        h0.GetYaxis().SetTitle("1/#sigma_{dijet} d#sigma_{dijet}/d#chi_{dijet}")
        h0.GetYaxis().SetTitleOffset(1.4)
        h0.GetXaxis().SetTitleOffset(0.8)
        h0.GetYaxis().SetTitleSize(0.05)
        h0.GetYaxis().SetLabelSize(0.04)
        h0.GetXaxis().SetTitleSize(0.05)
        h0.GetXaxis().SetLabelSize(0.04)
        h0.GetXaxis().SetTickLength(0.02)
        c.cd(1)
        
        if massbin==4 and len(massbins13)==5:
          h0.Draw("axis")
        else:
	  h0.Draw("axissame")
        h3.Draw("histsame")
        h2.Draw("histsame")
        h6.Draw("histsame")
        h0.Draw("histsame")
        if massbin>1:
             h4.Draw("histsame")
             #h5.Draw("histsame")
        h1.Draw("pzesame")
        h1sys.Draw("||same")
        h1sysstat.Draw("zesame")


      if True:
        filename="fastnlo/RunII/fnl5622i_v23.root"
        print filename
        f13 = TFile.Open(filename)
        new_hists+=[f13]
        histname='chi-'+str(massbins13[massbin]).strip("()").replace(',',"-").replace(' ',"").replace("13000","4800")
        print histname
        h13=f13.Get(histname)
	print h13
	h13=rebin(h13,len(chi_binnings[massbin])-1,chi_binnings[massbin])
        h13.SetLineColor(4)
        h13.SetLineStyle(3)
        h13.SetLineWidth(3)
        h13.Add(TF1("offset",str(offsets[massbin]),1,16))

        h13.SetTitle("")
	h13.GetYaxis().SetRangeUser(0,0.8)
	if len(massbins13)==5:
	  h13.GetYaxis().SetRangeUser(0,0.6)
        h13.GetXaxis().SetTitle("#chi_{dijet}")
        h13.GetYaxis().SetTitle("1/#sigma_{dijet} d#sigma_{dijet}/d#chi_{dijet}")
        h13.GetYaxis().SetTitleOffset(1.4)
        h13.GetXaxis().SetTitleOffset(0.8)
        h13.GetYaxis().SetTitleSize(0.05)
        h13.GetYaxis().SetLabelSize(0.04)
        h13.GetXaxis().SetTitleSize(0.05)
        h13.GetXaxis().SetLabelSize(0.04)
        h13.GetXaxis().SetTickLength(0.02)
        c.cd(1)

        if massbin==6:
            h13.Draw("hist")
        else:
            h13.Draw("histsame")
        h13.Draw("axissame")

      if massbin<2:
        filename="datacard_shapelimit13TeV_25nsNoJEC_chi.root"
        print filename
        f13 = TFile.Open(filename)
        new_hists+=[f13]
	if massbin==1:
	   masstext="2400_8000"
        else:
           masstext=str(massbins13[massbin]).strip("()").replace(',',"_").replace(' ',"")
        histname='data_obs#chi'+masstext+'_rebin1'
        print histname
        h14=f13.Get(histname)
	print h14
	h14=rebin2(h14,len(chi_binnings[massbin])-1,chi_binnings[massbin])
        h14.SetMarkerStyle(21)
        h14.SetMarkerSize(0.4)
        h14.SetMarkerColor(4)
        h14.SetLineColor(4)
        h14.Add(TF1("offset",str(offsets[massbin]),1,16))

        h14.Draw("pzesame")

      if True:
        filename="datacard_shapelimit13TeV_25nsMC_chi.root"
        print filename
        f13a = TFile.Open(filename)
        new_hists+=[f13a]
        masstext=str(massbins13[massbin]).strip("()").replace(',',"_").replace(' ',"").replace("13000","4800")
        histname='QCD#chi'+masstext+'_rebin1'
        print histname
        h15=f13a.Get(histname)
	print h15
	h15=rebin2(h15,len(chi_binnings[massbin])-1,chi_binnings[massbin])
        h15.SetLineColor(2)
        h15.Add(TF1("offset",str(offsets[massbin]),1,16))

        h15.Draw("histsame")
	
        histname='QCD#genchi'+masstext+'_rebin1'
        print histname
        h16=f13a.Get(histname)
	print h16
	h16=rebin2(h16,len(chi_binnings[massbin])-1,chi_binnings[massbin])
        h16.SetLineColor(7)
	h16.SetLineStyle(2)
        h16.Add(TF1("offset",str(offsets[massbin]),1,16))

        h16.Draw("histsame")
	
      if True:

	if len(massbins13)==5:
  	  ylabel=offsets[massbin]*1.415+0.222
          if massbin==3: ylabel+=0.055
          if massbin==4: ylabel+=0.04
        else:
  	  ylabel=offsets[massbin]*1.063+0.2
        
        if massbin==0: title="1.9 < #font[72]{M_{jj}} < 2.4"
        if massbin==1: title="2.4 < #font[72]{M_{jj}} (< 3.0)"
        if massbin==2: title="3.0 < #font[72]{M_{jj}} < 3.6"
        if massbin==3: title="3.6 < #font[72]{M_{jj}} < 4.2"
        if massbin==4: title="4.2 < #font[72]{M_{jj}} < 4.8"
        if massbin==5: title="4.8 < #font[72]{M_{jj}} < 5.4"
        if massbin==6: title="5.4 < #font[72]{M_{jj}} < 6.0"

        title+=" TeV"
        if offsets[massbin]==0: titleo=""
        elif offsets[massbin]<0: titleo="("+str(offsets[massbin])+")"
        else: titleo="(+"+str(offsets[massbin])+")"

        l=TLegend(0.50,ylabel,1.0,ylabel-0.005,title)
        l.SetTextSize(0.033)
        l.SetFillStyle(0)
        l.Draw("same")
        new_hists+=[l]

        lo=TLegend(0.82,ylabel,1.4,ylabel+0.01,titleo)
        lo.SetTextSize(0.033)
        lo.SetFillStyle(0)
        lo.Draw("same")
        new_hists+=[lo]

    l2=TLegend(0.23,0.72,0.76,0.93,"")
    l2.SetTextSize(0.035)
    l2.AddEntry(h14,"13 TeV Data detector-level","ple")
    l2.AddEntry(h15,"13 TeV LO QCD detector-level","l")
    l2.AddEntry(h16,"13 TeV LO QCD particle-level","l")
    l2.AddEntry(h13,"13 TeV NLO QCD prediction","l")
    l2.AddEntry(h4,"13 TeV #Lambda_{LL}^{#font[122]{+}} (NLO) = 10 TeV","l")
    l2.AddEntry(h1,"8 TeV Data particle-level","ple")
    l2.AddEntry(h3,"8 TeV NLO QCD+EW prediction","f")
    l2.AddEntry(h6,"8 TeV NLO QCD prediction","l")
    #l2.AddEntry(h5,"8 TeV #Lambda_{T} (GRW) = 7 TeV","l")
    l2.SetFillStyle(0)
    l2.Draw("same")

    l2b=TLegend(0.23,0.72,0.76,0.93,"")
    l2b.SetTextSize(0.035)
    l2b.AddEntry(h14," ","")
    l2b.AddEntry(h15," ","")
    l2b.AddEntry(h16," ","")
    l2b.AddEntry(h13," ","")
    l2b.AddEntry(h4," ","")
    l2b.AddEntry(h1," ","")
    l2b.AddEntry(h0," ","l")
    l2b.AddEntry(h6," ","")
    #l2b.AddEntry(h5," ","")
    l2b.SetFillStyle(0)
    l2b.Draw("same")
    
    tl1=TLine(16,0,16,0.7)
    tl1.SetLineColor(1)
    tl1.SetLineStyle(1)
    tl1.SetLineWidth(1)
    tl1.Draw("same")

    #// writing the lumi information and the CMS "logo"
    CMS_lumi( c, iPeriod, iPos );

    c.SaveAs(prefix + "_combined_RunII_25ns.pdf")
    c.SaveAs(prefix + "_combined_RunII_25ns.eps")
