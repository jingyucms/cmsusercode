from ROOT import *
import ROOT,sys,os,math
from math import *
import numpy as np

#gROOT.Macro( os.path.expanduser( '~/rootlogon.C' ) )
gROOT.Reset()
gROOT.SetStyle("Plain")
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetTitleOffset(0.9,"XY")
gStyle.SetPadLeftMargin(0.1)
gStyle.SetPadBottomMargin(0.1)
gStyle.SetPadTopMargin(0.075)
gStyle.SetPadRightMargin(0.1)
gStyle.SetMarkerSize(1.5)
gStyle.SetHistLineWidth(1)
gStyle.SetStatFontSize(0.020)
gStyle.SetTitleSize(0.04, "XYZ")
gStyle.SetLabelSize(0.03, "XYZ")
gStyle.SetNdivisions(513, "Y")
gStyle.SetNdivisions(510, "X")
gStyle.SetLegendBorderSize(0)

def medWidth(gq):
  return 6*gq**2/(4*3.141592653)+1/(12*3.141592653)

if __name__=="__main__":
  
  #style="DMVector"
  style="DMAxial"

  testStat="LHC"
  version="_v2"
  
  signalCounter={}
  if style=="DMVector":
    counter=100
  else:
    counter=1100

  gs=["0p01","0p05","0p1","0p2","0p25","0p3","0p5","0p75","1","1p5","2p0","2p5","3p0"]
  mdms=["1","3000"]
  #mdms=["1"]
  #signalMasses=[1000,1500,1750,2000,2250,2500,3000,3500,4000,4500,5000,6000]
  signalMasses=[1500,1750,2000,2250,2500,3000,3500,4000,4500,5000,6000,7000]
 
  for mdm in mdms:
    for g in gs:
      signalCounter[style+"_mdm"+mdm+"_g"+g]=counter
      counter+=1
      
  #for mdm in mdms:
  for mdm in ["1"]:
    g_q_out=TFile('limits'+testStat+"_"+style+"_mdm"+mdm+version+'.root',"RECREATE")
    
    g_q=TGraph(0)
    g_q_exp=TGraph(0)
    g_q_band=TGraphAsymmErrors(0)
    g_q_band_2sigma=TGraphAsymmErrors(0)
    for signalMass in signalMasses:
      #if signalMass==6000:
      #  mdm="2990"
      print "--------------------"
      signal=style+"_Mphi"+str(signalMass)+"_mdm"+mdm

      limits=[]
      for g in gs:
        if testStat!="LEP":
          try:
            f=file("limits"+testStat+str(signalCounter[style+"_mdm"+mdm+"_g"+g])+"_"+style+"_Dijet_LO_Mphi_exp_"+str(signalMass)+"_2016"+version+".txt")
          except:
            print "can't open","limits"+testStat+str(signalCounter[style+"_mdm"+mdm+"_g"+g])+"_"+style+"_Dijet_LO_Mphi_exp_"+str(signalMass)+"_2016"+version+".txt"
	    continue
        else:
          try:
            f=file("limits"+testStat+str(signalCounter[style+"_mdm"+mdm+"_g"+g])+"_"+style+"_Dijet_LO_Mphi_"+str(signalMass)+"_2016"+version+".txt")
          except:
            print "can't open","limits"+testStat+str(signalCounter[style+"_mdm"+mdm+"_g"+g])+"_"+style+"_Dijet_LO_Mphi_"+str(signalMass)+"_2016"+version+".txt"
            continue
          
        limits+=[[]]
        for line in f.readlines():
          
          if "CLs = " in line and testStat=="LEP":
            limits[-1]=[float(g.replace('p','.')),float(line.strip().split(" ")[-3]),float(line.strip().split(" ")[-1])]
	    if limits[-1][-1]==0:
	      limits[-1][-2]=1e-6
          
          if "Observed CLs = " in line and testStat!="LEP":
            limits[-1]=[float(g.replace('p','.')),float(line.strip().split(" ")[-1]),0]
              
          if "CLb      = " in line and testStat=="LEP":
            print "observed signficance (p-value): ",ROOT.Math.normal_quantile_c((1.-float(line.strip().split(" ")[-3]))/2.,1),"(",(1.-float(line.strip().split(" ")[-3])),")"

          if "Observed CLb = " in line and testStat!="LEP":
            print "observed signficance (p-value): ",ROOT.Math.normal_quantile_c((1.-float(line.strip().split(" ")[-1]))/2.,1),"(",(1.-float(line.strip().split(" ")[-1])),")"
            
        if len(limits[-1])==0:
          limits[-1]+=[float(g.replace('p','.'))]
          limits[-1]+=[1e-6]
          limits[-1]+=[0]
          
        try:
          f=file("limits"+testStat+str(signalCounter[style+"_mdm"+mdm+"_g"+g])+"_"+style+"_Dijet_LO_Mphi_exp_"+str(signalMass)+"_2016"+version+".txt")
        except:
          print "can't open","limits"+testStat+str(signalCounter[style+"_mdm"+mdm+"_g"+g])+"_"+style+"_Dijet_LO_Mphi_exp_"+str(signalMass)+"_2016"+version+".txt"
          del limits[-1]
	  continue
        for line in f.readlines():
          if "Expected CLs" in line:
	    try:
              limits[-1]+=[float(line.strip().split(" ")[-1])]
	    except:
              print "didn't find one point"
            
        for i in range(len(limits[-1]),8):
          limits[-1]+=[0]

        for i in range(len(limits[-1])):
          if limits[-1][i]==0 and i>=3:
            limits[-1][i]=1e-6

      print limits

      canvas = TCanvas("","",0,0,300,300)
      #canvas.GetPad(0).SetLogy()
      #canvas.GetPad(0).SetLogx()
      mg=TMultiGraph()

      min_x=0.01
      max_x=3

      g=TGraph(0)
      g_exp_=TGraph(0)
      g_exp1m=TGraph(0)
      g_exp1p=TGraph(0)
      g_exp2m=TGraph(0)
      g_exp2p=TGraph(0)
      max_mass=0
      max_mass_exp=0
      max_mass_exp1m=0
      max_mass_exp1p=0
      for lim in limits:
        mass,limit,error,exp,exp1m,exp1p,exp2m,exp2p =lim
        if limit>0:
          g.SetPoint(g.GetN(),mass,log10(limit))
	  max_mass=mass
        if exp>0:
          g_exp_.SetPoint(g_exp_.GetN(),mass,log10(exp))
	  max_mass_exp=mass
        if exp1m>0:
          g_exp1m.SetPoint(g_exp1m.GetN(),mass,log10(exp1m))
	  max_mass_exp1m=mass
        if exp1p>0:
          g_exp1p.SetPoint(g_exp1p.GetN(),mass,log10(exp1p))
	  max_mass_exp1p=mass
        if exp2m>0:
          g_exp2m.SetPoint(g_exp2m.GetN(),mass,log10(exp2m))
	  max_mass_exp2m=mass
        if exp2p>0:
          g_exp2p.SetPoint(g_exp2p.GetN(),mass,log10(exp2p))
	  max_mass_exp2p=mass

      g.SetMarkerStyle(24)
      g.SetMarkerSize(0.5)
      g.SetLineColor(1)
      g.SetLineWidth(3)
      mg.Add(g)
      g_exp_.SetMarkerStyle(24)
      g_exp_.SetMarkerSize(0.5)
      g_exp_.SetLineColor(2)
      g_exp_.SetLineWidth(3)
      mg.Add(g_exp_)
      g_exp1m.SetMarkerStyle(24)
      g_exp1m.SetMarkerSize(0.5)
      g_exp1m.SetLineColor(3)
      g_exp1m.SetLineWidth(3)
      mg.Add(g_exp1m)
      g_exp1p.SetMarkerStyle(24)
      g_exp1p.SetMarkerSize(0.5)
      g_exp1p.SetLineColor(3)
      g_exp1p.SetLineWidth(3)
      mg.Add(g_exp1p)

      g_exp2m.SetMarkerStyle(24)
      g_exp2m.SetMarkerSize(0.5)
      g_exp2m.SetLineColor(5)
      g_exp2m.SetLineWidth(3)
      mg.Add(g_exp2m)
      g_exp2p.SetMarkerStyle(24)
      g_exp2p.SetMarkerSize(0.5)
      g_exp2p.SetLineColor(5)
      g_exp2p.SetLineWidth(3)
      mg.Add(g_exp2p)
  
      mg.Draw("apl")
      mg.SetTitle("")
      mg.GetXaxis().SetTitle("g_{q}")
      mg.GetYaxis().SetTitle("log_{10}(CL_{S})")
      mg.GetYaxis().SetRangeUser(-6,0)

      min_x=0.01
  
      l=TLine(min_x,log10(0.05),max_x,log10(0.05))
      l.SetLineColor(2)
      l.SetLineStyle(2)
      l.Draw("same")
      
      l1=TLatex((max_x-min_x)*0.75+min_x,log10(0.05)*1.15,"CL_{S}=0.05")
      l1.Draw("same")

      limit=0
      exp=0
      exp1m=0
      exp1p=0
      exp2m=0
      exp2p=0
      nseg=10000
      masses=np.linspace(max_x,min_x,num=nseg)
      for mass in masses:  
        if limit==0 and g.Eval(mass,0)>log10(0.05) and mass<=max_mass:
          limit=mass
        if exp==0 and g_exp_.Eval(mass,0)>log10(0.05) and mass<=max_mass_exp:
          exp=mass
          print "exp:",i,mass
        if exp1m==0 and g_exp1m.Eval(mass,0)>log10(0.05) and mass<=max_mass_exp1m:
          print "exp1m:",i,mass
          exp1m=mass
        if exp1p==0 and g_exp1p.Eval(mass,0)>log10(0.05) and mass<=max_mass_exp1p:
          exp1p=mass
          print "exp1p:",i,mass
        if exp2m==0 and g_exp2m.Eval(mass,0)>log10(0.05) and mass<=max_mass_exp2m:
          print "exp2m:",i,mass
          exp2m=mass
        if exp2p==0 and g_exp2p.Eval(mass,0)>log10(0.05) and mass<=max_mass_exp2p:
          exp2p=mass
          print "exp2p:",i,mass


      print "limit: %.6f" % (limit), "& %.6f" % (exp), "$\pm$ %.6f" % (max(exp-exp1p,exp1m-exp))

      #print "limit: %.6f," % (limit), "%.6f," % (exp), "%.6f, %.6f, 0, 0" % ((-max(exp-exp1p,exp1m-exp)+exp),(exp+max(exp-exp1p,exp1m-exp)))
      print "limit: %.6f," % (limit), "%.6f," % (exp), "%.6f, %.6f, %.6f, %.6f" % (exp-min(exp1p,exp1m),max(exp1p,exp1m)-exp, exp-min(exp2p,exp2m), max(exp2p,exp2m)-exp)
 
      g_q.SetPoint(g_q.GetN(),signalMass,limit)
      g_q_exp.SetPoint(g_q_exp.GetN(),signalMass,exp)
      g_q_band.SetPoint(g_q_band.GetN(),signalMass,exp)
      g_q_band_2sigma.SetPoint(g_q_band_2sigma.GetN(),signalMass,exp)

      #g_q_band.SetPointError(g_q_band.GetN()-1,0,0,max(exp-exp1p,exp1m-exp),max(exp-exp1p,exp1m-exp))
      g_q_band.SetPointError(g_q_band.GetN()-1,0,0,exp-min(exp1p,exp1m),max(exp1p,exp1m)-exp)
      g_q_band_2sigma.SetPointError(g_q_band_2sigma.GetN()-1,0,0,exp-min(exp2p,exp2m),max(exp2p,exp2m)-exp)
      #print "g_q_band_2sigma.GetErrorYlow(g_q_band_2sigma.GetN()-1),g_q_band.GetErrorYhigh(g_q_band_2sigma.GetN()-1):",g_q_band_2sigma.GetErrorYlow(g_q_band_2sigma.GetN()-1),g_q_band_2sigma.GetErrorYhigh(g_q_band_2sigma.GetN()-1)
  
      l2=TLine(limit,-3,limit,log10(0.05))
      l2.SetLineColor(1)
      l2.SetLineStyle(2)
      l2.Draw("same")
      
      l2a=TLine(exp,-3,exp,log10(0.05))
      l2a.SetLineColor(2)
      l2a.SetLineStyle(2)
      l2a.Draw("same")
  
      l2b=TLine(exp1m,-3,exp1m,log10(0.05))
      l2b.SetLineColor(3)
      l2b.SetLineStyle(2)
      l2b.Draw("same")
  
      l2c=TLine(exp1p,-3,exp1p,log10(0.05))
      l2c.SetLineColor(3)
      l2c.SetLineStyle(2)
      l2c.Draw("same")
  
      canvas.SaveAs('limits'+testStat+signal+version+'.pdf')

    canvas = TCanvas("","",0,0,300,300)
    mg=TMultiGraph()

    #min_x_new=signalMasses[0]
    min_x_new=2000

    ymin=0.1
    ymax=1.42788

    xs=np.linspace(6100,6500,num=20000)
    for x in xs:
      if g_q_exp.Eval(x)>=1.42788:
        max_x_new=x
        break
    #max_x_new=6000
      
    g_q_band_2sigma.SetFillStyle(1001)
    g_q_band_2sigma.SetFillColor(kOrange)
    g_q_band_2sigma.SetLineColor(1)
    g_q_band_2sigma.SetLineStyle(1)
    g_q_band_2sigma.SetLineWidth(0)
    mg.Add(g_q_band_2sigma,"3")
    g_q_band.SetFillStyle(1001)
    g_q_band.SetFillColor(kGreen-3)
    g_q_band.SetLineColor(1)
    g_q_band.SetLineStyle(1)
    g_q_band.SetLineWidth(0)
    mg.Add(g_q_band,"3")
    g_q_exp.SetLineColor(1)
    g_q_exp.SetLineWidth(3)
    g_q_exp.SetLineStyle(kDashed)
    mg.Add(g_q_exp,"l")
    g_q.SetMarkerStyle(24)
    g_q.SetMarkerSize(0)
    g_q.SetLineColor(1)
    g_q.SetLineWidth(3)
    mg.Add(g_q,"pl")

    g_q.SetName("gq_obs")
    g_q_exp.SetName("gq_exp")
    g_q.Write()
    g_q_exp.Write()
    
    mg.Draw("apl")
    mg.SetTitle("")
    mg.GetXaxis().SetTitle("M_{Med} [GeV]")
    mg.GetYaxis().SetTitle("g_{q}")
    mg.GetYaxis().SetLabelSize(0.03)
    mg.GetYaxis().SetTitleSize(0.04)
    mg.GetYaxis().SetTitleOffset(1.1)
    mg.GetXaxis().SetLimits(min_x_new,max_x_new)
    mg.GetYaxis().SetRangeUser(ymin,ymax)
    mg.GetYaxis().SetNdivisions(510)
    mg.GetXaxis().SetNdivisions(510)

    y1=TGaxis(min_x_new, ymin, min_x_new, ymax, ymin,ymax,510,"")
    y1.SetLabelSize(0)
    y1.SetTitleSize(0)
    y1.Draw()

    x2=TGaxis(min_x_new, ymax, max_x_new, ymax, min_x_new,max_x_new,510,"-")
    x2.SetLabelSize(0)
    x2.SetTitleSize(0)
    x2.Draw()

    minwidth=medWidth(ymin)
    myFunc=TF1("myFunc","pow((x-1/(12*3.141592653))*(4*3.141592653)/6,0.5)",minwidth,1)
    y2=TGaxis(max_x_new, ymin, max_x_new, ymax,"myFunc",510,"+L")
    y2.SetTitle("#Gamma/M_{Med}")
    y2.SetLabelSize(0.03)
    y2.SetTitleSize(0.04)
    y2.SetTitleOffset(1.1)
    y2.Draw()

    l0p5=TLine(min_x_new,0.5,max_x_new,0.5)
    l0p5.SetLineColor(kGray+1)
    l0p5.SetLineStyle(kDashed)
    l0p5.Draw("same")
      
    l0p5T=TLatex((max_x_new-min_x_new)*0.35+min_x_new,0.5-0.05,"g_{q}=0.5")
    l0p5T.SetTextSize(0.03)
    l0p5T.SetTextColor(kGray+1)
    l0p5T.Draw("same")

    l1p0=TLine(min_x_new,1,max_x_new,1)
    l1p0.SetLineColor(kGray+1)
    l1p0.SetLineStyle(kDashed)
    l1p0.Draw("same")
      
    l1p0T=TLatex((max_x_new-min_x_new)*0.35+min_x_new,1.0-0.05,"g_{q}=1.0")
    l1p0T.SetTextSize(0.03)
    l1p0T.SetTextColor(kGray+1)
    l1p0T.Draw("same")
    
    if style=="DMAxial":
      lt=TLatex(signalMasses[1],2.65,"#splitline{Axial-vector Mediator & Dirac DM}{ m_{DM} = "+mdm+" GeV, g_{DM} = 1.0}")
    else:
      lt=TLatex(signalMasses[1],2.65,"#splitline{Vector Mediator & Dirac DM}{ m_{DM} = "+mdm+" GeV, g_{DM} = 1.0}")
    lt.SetTextSize(0.04)
    lt.Draw("same")
    
    l=TLegend(0.15,0.66,0.575,0.9,"95% CL upper limits")
    l.SetFillColor(0)
    l.SetFillStyle(0)
    l.SetTextSize(0.03)
    l.SetShadowColor(0)
    l.AddEntry(g_q,"Observed","LP")
    l.AddEntry(g_q_exp,"Expected","LP")
    l.AddEntry(g_q_band,"Expected #pm 1#sigma","F")
    l.AddEntry(g_q_band_2sigma,"Expected #pm 2#sigma","F")
    l.Draw()
    

    # CMS
    leg2=TLatex(min_x_new,ymax+0.03,"#bf{CMS} #it{Preliminary}")
    leg2.SetTextFont(42)
    leg2.SetTextSize(0.04)
    # lumi
    leg3=TLatex(max_x_new-1500,ymax+0.03,"35.9 fb^{-1} (13 TeV)")
    leg3.SetTextFont(42)
    leg3.SetTextSize(0.04)
    leg2.Draw("same")
    leg3.Draw("same")
    
    canvas.SaveAs('limits'+testStat+"_"+style+"_mdm"+mdm+version+'.pdf')
