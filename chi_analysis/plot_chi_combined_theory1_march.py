from ROOT import *
import ROOT
import array, math
import os

if __name__=="__main__":

  for massbins in [[(3600,4200)],[(4200,8000)]]:
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
    writeExtraText = true;	 #// if extra text
    extraText  = "";  #// default extra text is "Preliminary"
    lumi_13TeV  = ""; #// default is "19.7 fb^{-1}"
    iPeriod = 2;	#// 1=7TeV, 2=8TeV, 3=7+8TeV, 7=7+8+13TeV 
    iPos = 33;
    #// second parameter in example_plot is iPos, which drives the position of the CMS logo in the plot
    #// iPos=11 : top-left, left-aligned
    #// iPos=33 : top-right, right-aligned
    #// iPos=22 : center, centered
    #// mode generally : 
    #//   iPos = 10*(alignement 1/2/3) + position (1/2/3 = left/center/right)

    offsets=[0,0.2]

    prefix="datacard_shapelimit"

    c = TCanvas("combined", "combined", 0, 0, 400, 400)
    c.Divide(1,1)
    new_hists=[]
    for massbin in reversed(range(len(massbins))):
        filename="datacard_shapelimit_data_sys.root"
        print filename
        f = TFile.Open(filename)
        new_hists+=[f]
        histname='QCD#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print histname
        h0=f.Get(histname)
        h0.SetLineColor(1)
        h0.SetLineStyle(3)

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
        for b in range(h0.GetXaxis().GetNbins()):
            if b==0 or b==h0.GetXaxis().GetNbins()-1:
                print massbins[massbin],b,"stat",h1.GetErrorYlow(b)/h1.GetY()[b],h1.GetErrorYhigh(b)/h1.GetY()[b]
	    exp_sumdown=0
	    exp_sumup=0
            theory_sumdown=0
            theory_sumup=0
            for up,down in uncertainties:
	        if b==0 or b==h0.GetXaxis().GetNbins()-1:
                    print massbins[massbin],b,uncertaintynames[uncertainties.index([up,down])],max(abs(up.GetBinContent(b+1)-h0.GetBinContent(b+1))/h0.GetBinContent(b+1),abs(down.GetBinContent(b+1)-h0.GetBinContent(b+1))/h0.GetBinContent(b+1))
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
            h1sys.SetPointEXlow(b,0)
            h1sys.SetPointEXhigh(b,0)
            h1sys.SetPointEYlow(b,exp_sumdown)
            h1sys.SetPointEYhigh(b,exp_sumup)
            h1sysstat.SetPointEXlow(b,0)
            h1sysstat.SetPointEXhigh(b,0)
            h1sysstat.SetPointEYlow(b,sqrt(pow(exp_sumdown,2)+pow(h1.GetErrorYlow(b),2)))
            h1sysstat.SetPointEYhigh(b,sqrt(pow(exp_sumup,2)+pow(h1.GetErrorYhigh(b),2)))
            h1.SetPointEYlow(b,0)
            h1.SetPointEYhigh(b,0)
            h2.SetBinContent(b+1,h0.GetBinContent(b+1)-theory_sumdown)
            h3.SetBinContent(b+1,h0.GetBinContent(b+1)+theory_sumup)
	    print h2.GetXaxis().GetBinLowEdge(b+1),h2.GetXaxis().GetBinUpEdge(b+1),h1.GetY()[b],sqrt(pow(exp_sumdown,2)+pow(h1.GetErrorYlow(b),2)),sqrt(pow(exp_sumup,2)+pow(h1.GetErrorYhigh(b),2))
        new_hists+=[h2]
        new_hists+=[h3]
        h2.SetLineStyle(1)
        h3.SetLineStyle(1)
        h2.SetLineColor(15)
        h2.SetFillColor(10)
        h3.SetLineColor(15)
        h3.SetFillColor(15)

        if massbin>=0:
          filename="datacard_shapelimit_CT10nlo_10000_LL+_chi.root"
          histname='QCDCT10nlo_10000_LL+#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
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

          filename="datacard_shapelimit_CT10nlo_10000_LL-_chi.root"
          histname='QCDCT10nlo_10000_LL-#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
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

          filename="datacard_shapelimit_CT10nlo_10000_VV+_chi.root"
          histname='QCDCT10nlo_10000_VV+#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
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

          filename="datacard_shapelimit_CT10nlo_10000_VV-_chi.root"
          histname='QCDCT10nlo_10000_VV-#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
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

          filename="datacard_shapelimit_CT10nlo_10000_AA+_chi.root"
          histname='QCDCT10nlo_10000_AA+#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
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

          filename="datacard_shapelimit_CT10nlo_10000_AA-_chi.root"
          histname='QCDCT10nlo_10000_AA-#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
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

          filename="datacard_shapelimit_CT10nlo_10000_V-A+_chi.root"
          histname='QCDCT10nlo_10000_V-A+#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
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

          filename="datacard_shapelimit_CT10nlo_10000_V-A-_chi.root"
          histname='QCDCT10nlo_10000_V-A-#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
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

          filename="datacard_shapelimit_ADD_4_0_1_7000_chi.root"
          print filename
          f = TFile.Open(filename)
          new_hists+=[f]
          histname='QCDADD_4_0_1_7000#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          print histname
          h5=f.Get(histname)
          h5.SetLineColor(4)
          h5.SetLineStyle(2)
          h5.SetLineWidth(2)
	  h5.Scale(1./h5.Integral())
	  for b in range(h5.GetNbinsX()):
	       h5.SetBinContent(b+1,h5.GetBinContent(b+1)/h5.GetBinWidth(b+1))

        h0.Add(TF1("offset",str(offsets[massbin]),1,16))
        h1.Apply(TF2("offset",str(offsets[massbin])+"+y",1,16))
        h1sys.Apply(TF2("offset",str(offsets[massbin])+"+y",1,16))
        h1sysstat.Apply(TF2("offset",str(offsets[massbin])+"+y",1,16))
        h2.Add(TF1("offset",str(offsets[massbin]),1,16))
        h3.Add(TF1("offset",str(offsets[massbin]),1,16))
        if massbin>=0:
            h4.Add(TF1("offset",str(offsets[massbin]),1,16))
            h4b.Add(TF1("offset",str(offsets[massbin]),1,16))
            h4c.Add(TF1("offset",str(offsets[massbin]),1,16))
            h4d.Add(TF1("offset",str(offsets[massbin]),1,16))
            h5.Add(TF1("offset",str(offsets[massbin]),1,16))
        
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
        h3.Draw("histsame")
        h2.Draw("histsame")
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
        h1.Draw("pzesame")
        h1sys.Draw("||same")
        h1sysstat.Draw("zesame")
        h0.Draw("axissame")

        ylabel=0.50
        
        if "3600" in str(massbins): title="3.6 < #font[72]{M_{jj}} < 4.2"
        else: title="#font[72]{M_{jj}} > 4.2"

        title+=" TeV"
        if offsets[massbin]==0: titleo=""
        elif offsets[massbin]<0: titleo="("+str(offsets[massbin])+")"
        else: titleo="(+"+str(offsets[massbin])+")"

        l=TLegend(0.6,ylabel,1.0,ylabel-0.005,title)
        l.SetTextSize(0.033)
        l.SetFillStyle(0)
        l.Draw("same")
        new_hists+=[l]

        lo=TLegend(0.82,ylabel,1.4,ylabel+0.01,titleo)
        lo.SetTextSize(0.033)
        lo.SetFillStyle(0)
        lo.Draw("same")
        new_hists+=[lo]

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
    l2.AddEntry(h1,"Data","ple")
    l2.AddEntry(h3,"NLO QCD+EW prediction","f")
    l2.AddEntry(h4,"#Lambda_{LL}^{#font[122]{+}} (NLO) = 10 TeV","l")
    l2.AddEntry(h4b,"#Lambda_{LL}^{#font[122]{-}} (NLO) = 10 TeV","l")
    l2.AddEntry(h4c,"#Lambda_{VV}^{#font[122]{+}} (NLO) = 10 TeV","l")
    l2.AddEntry(h4d,"#Lambda_{VV}^{#font[122]{-}} (NLO) = 10 TeV","l")
    #l2.AddEntry(h4e,"#Lambda_{AA}^{#font[122]{+}} (NLO) = 10 TeV","l")
    #l2.AddEntry(h4f,"#Lambda_{AA}^{#font[122]{-}} (NLO) = 10 TeV","l")
    l2.AddEntry(h4g,"#Lambda_{V-A} (NLO) = 10 TeV","l")
    #l2.AddEntry(h4h,"#Lambda_{V-A}^{#font[122]{-}} (NLO) = 10 TeV","l")
    l2.AddEntry(h5,"#Lambda_{T} (GRW) = 7 TeV","l")
    l2.SetFillStyle(0)
    l2.Draw("same")

    l2b=TLegend(0.3,0.54,0.6,0.93,"")
    l2b.SetTextSize(0.035)
    l2b.AddEntry(h1," ","")
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
    l2b.SetFillStyle(0)
    l2b.Draw("same")
    
    tl1=TLine(16,0,16,0.24)
    tl1.SetLineColor(1)
    tl1.SetLineStyle(1)
    tl1.SetLineWidth(1)
    tl1.Draw("same")

    #// writing the lumi information and the CMS "logo"
    CMS_lumi( c, iPeriod, iPos );

    c.SaveAs(prefix + "_combined_theory"+str(massbins).strip("([])").replace(",","_").replace(" ","")+".pdf")
    c.SaveAs(prefix + "_combined_theory"+str(massbins).strip("([])").replace(",","_").replace(" ","")+".eps")
