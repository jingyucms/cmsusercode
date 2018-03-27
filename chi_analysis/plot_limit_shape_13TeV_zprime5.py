from ROOT import *
import ROOT
from math import *

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
gStyle.SetNdivisions(505, "XYZ")
gStyle.SetLegendBorderSize(0)

if __name__=="__main__":

 signalCounter={}
 counter=100
 for gq in ["0.1","0.15","0.2","0.25","0.5","0.75","1.0","1.25","1.5","1.75","2.0","2.25","2.5","2.75","3.0","3.5","4.0","6.0","8.0", "10.0"]:
   for vector in ["800"]:# ,"801"
     signalCounter["_1_"+gq+"_"+vector]=counter
     counter+=1
 for gq in ["1.0", "1.5", "2.0", "2.5", "3.0", "3.5", "4.0", "4.5", "5.0", "5.5", "6.0", "8.0", "10.0", "12.0", "15.0", "20.0"]:
   for vector in ["800"]:#"801"
     signalCounter["_1_"+gq+"_"+vector+"_zprime5"]=counter
     counter+=1

 for vector in ["800"]:#,"801"
  g_q=TGraph(0)
  g_q_exp=TGraph(0)
  g_q_band=TGraphAsymmErrors(0)
  for signalMass in [1000,1250,1500,2000]:
    signal="DM"+str(signalMass)+"_1_"+vector+"_zprime5"
    limits=[]
    #for gq in ["0.05","0.08","0.09","0.1","0.11","0.12","0.13","0.14","0.15","0.16","0.17","0.18","0.19","0.2","0.21","0.22","0.23","0.24","0.25","0.26","0.27","0.28","0.29","0.5","1.0"]:
    for gq in ["1.0", "1.5", "2.0", "2.5", "3.0", "3.5", "4.0", "4.5", "5.0", "5.5", "6.0", "8.0", "10.0", "12.0", "15.0", "20.0"]:
    #for gq in ["1.0","1.25","1.5","1.75","2.0","2.25"]:
      try:
        f=file("limits"+str(signalCounter["_1_"+gq+"_"+vector+"_zprime5"])+"_DM_"+str(signalMass)+".txt")
      except:
        print "can't open","limits"+str(signalCounter["_1_"+gq+"_"+vector+"_zprime5"])+"_DM_"+str(signalMass)+".txt"
	continue
      limits+=[[]]
      for line in f.readlines():
        if "CLs = " in line:
           limits[-1]=[float(gq),float(line.strip().split(" ")[-3]),float(line.strip().split(" ")[-1])]
	   if limits[-1][-1]==0:
	     limits[-1][-2]=1e-5
        if "CLb      = " in line:
           print "observed signficance (p-value): ",ROOT.Math.normal_quantile_c((1.-float(line.strip().split(" ")[-3]))/2.,1),"(",(1.-float(line.strip().split(" ")[-3])),")"
      if len(limits[-1])==0:
         limits[-1]+=[float(gq)]
      try:
        f=file("limits"+str(signalCounter["_1_"+gq+"_"+vector+"_zprime5"])+"_DM_exp_"+str(signalMass)+".txt")
      except:
        print "can't open","limits"+str(signalCounter["_1_"+gq+"_"+vector+"_zprime5"])+"_DM_exp_"+str(signalMass)+".txt"
        del limits[-1]
	continue
      for line in f.readlines():
        if "Expected CLs" in line:
	   try:
            limits[-1]+=[float(line.strip().split(" ")[-1])]
	   except:
            print "didn't find one point"
	   if limits[-1][-1]>=1:
	     limits[-1][-1]=1e-5
      for i in range(len(limits[-1]),8):
         limits[-1]+=[0]

    print limits

    canvas = TCanvas("","",0,0,300,300)
    #canvas.GetPad(0).SetLogy()
    mg=TMultiGraph()

    min_x=0
    max_x=20
    g0=TGraph(0)
    g0.SetPoint(0,min_x,0)
    g0.SetPoint(1,max_x,0)
    mg.Add(g0)
    
    g=TGraph(0)
    g_exp=TGraph(0)
    g_exp1m=TGraph(0)
    g_exp1p=TGraph(0)
    max_mass=0
    max_mass_exp=0
    max_mass_exp1m=0
    max_mass_exp1p=0
    for mass,limit,error,exp,exp1m,exp1p,exp2m,exp2p in limits:
      if limit>0:
        g.SetPoint(g.GetN(),mass,log10(limit))
	max_mass=mass
      if exp>0:
        g_exp.SetPoint(g_exp.GetN(),mass,log10(exp))
	max_mass_exp=mass
      if exp1m>0:
        g_exp1m.SetPoint(g_exp1m.GetN(),mass,log10(exp1m))
	max_mass_exp1m=mass
      if exp1p>0:
        g_exp1p.SetPoint(g_exp1p.GetN(),mass,log10(exp1p))
	max_mass_exp1p=mass
    g.SetMarkerStyle(24)
    g.SetMarkerSize(0.5)
    g.SetLineColor(1)
    g.SetLineWidth(3)
    mg.Add(g)
    g_exp.SetMarkerStyle(24)
    g_exp.SetMarkerSize(0.5)
    g_exp.SetLineColor(2)
    g_exp.SetLineWidth(3)
    mg.Add(g_exp)
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
    
    mg.Draw("apl")
    mg.SetTitle("")
    mg.GetXaxis().SetTitle("coupling")
    mg.GetYaxis().SetTitle("log_{10}(CL_{S})")
    mg.GetYaxis().SetRangeUser(-6,0)
    
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
    for i in reversed(range(20000)):
        mass=i*(limits[-1][0]-limits[0][0])/20000.+limits[0][0]
        if mass<min_x or mass>max_x: continue
	if limit==0 and g.Eval(mass,0)>log10(0.05) and mass<=max_mass:
	    limit=mass
	if exp==0 and g_exp.Eval(mass,0)>log10(0.05) and mass<=max_mass_exp:
	    exp=mass
	if exp1m==0 and g_exp1m.Eval(mass,0)>log10(0.05) and mass<=max_mass_exp1m:
	    exp1m=mass
	if exp1p==0 and g_exp1p.Eval(mass,0)>log10(0.05) and mass<=max_mass_exp1p:
	    exp1p=mass

    print "limit: %.2f" % (limit), "& %.2f" % (exp), "$\pm$ %.2f" % (max(exp-exp1p,exp1m-exp))

    print "limit: %.3f," % (limit), "%.3f," % (exp), "%.3f, %.3f, 0, 0" % ((-max(exp-exp1p,exp1m-exp)+exp),(exp+max(exp-exp1p,exp1m-exp)))

    g_q.SetPoint(g_q.GetN(),signalMass,limit)
    g_q_exp.SetPoint(g_q_exp.GetN(),signalMass,exp)
    g_q_band.SetPoint(g_q_band.GetN(),signalMass,exp)
    g_q_band.SetPointError(g_q_band.GetN()-1,0,0,max(exp-exp1p,exp1m-exp),max(exp-exp1p,exp1m-exp))
    
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
    
    canvas.SaveAs('limits'+signal+'.pdf')
    canvas.SaveAs('limits'+signal+'.eps')

  canvas = TCanvas("","",0,0,300,300)
  #canvas.GetPad(0).SetLogy()
  mg=TMultiGraph()

  min_x=1000
  max_x=2000
  g0=TGraph(0)
  g0.SetPoint(0,min_x,0)
  g0.SetPoint(20,max_x,0)
  mg.Add(g0,"a")
    
  g_q_band.SetFillStyle(1001)
  g_q_band.SetFillColor(3)
  g_q_band.SetLineColor(2)
  g_q_band.SetLineWidth(3)
  #mg.Add(g_q_band,"3")
  g_q_exp.SetLineColor(2)
  g_q_exp.SetLineWidth(3)
  mg.Add(g_q_exp,"l")
  g_q.SetMarkerStyle(24)
  g_q.SetMarkerSize(0.5)
  g_q.SetLineColor(1)
  g_q.SetLineWidth(3)
  mg.Add(g_q,"pl")
    
  mg.Draw("apl")
  mg.SetTitle("")
  mg.GetXaxis().SetTitle("mass [GeV]")
  mg.GetYaxis().SetTitle("g_{B}")
  mg.GetYaxis().SetRangeUser(0,20)
  
  l=TLegend(0.3,0.7,0.8,0.9,"Axial-Vector (g_{DM}=0)")
  l.SetFillColor(0)
  l.SetShadowColor(0)
  l.AddEntry(g_q,"CL_{S} Observed","LP")
  l.AddEntry(g_q_band,"CL_{S} Expected #pm 1#sigma","LF")
  l.Draw()
    
  canvas.SaveAs('limitsDM'+vector+"_zprime5"+'.pdf')
  canvas.SaveAs('limitsDM'+vector+"_zprime5"+'.eps')
  canvas.SaveAs('limitsDM'+vector+"_zprime5"+'.root')
