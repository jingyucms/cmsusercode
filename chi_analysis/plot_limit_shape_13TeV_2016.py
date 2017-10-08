from ROOT import *
import ROOT
from math import log10

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

 models=[3]
 #models+=[10,11]
 models+=[60,61,62,63,64,65,66,67,68,69]
 #models+=[70,71,72,73,74,75,76,77]
 #models+=[78,79,80,81,82,83,84,85,86,87]
 #models+=[30,31,32,33,34,35,36,37,38]
 #models+=[40,41,42,43,44,45,46,47,48]
 #models=[88,89]
 #models=[60,61]
 models=[10,11]
 
 testStat="LHC"
 asym="a" #asymptotic CLS

 for model in models:

    if model==1:
       signal="CIplusLL"    
    if model==2:
       signal="CIminusLL"    
    if model==3:
       signal="ADD"    
    if model==4:
       signal="cs_nn30nlo_0_"    
    if model==5:
       signal="cs_nn30nlo_0_"    
    if model==6:
       signal="cs_nn30nlo_0_"    
    if model==7:
       signal="cs_nn30nlo_0_"    
    if model==8:
       signal="cs_nn30nlo_0_"    
    if model==9:
       signal="cs_nn30nlo_0_"    
    if model==10:
       signal="QBH_"    
    if model==11:
       signal="QBH_"    

    if model>=18 and model<20:
       signal="cs_ct14nlo_"
    if model>=20 and model<30:
       signal="cs_nn30nlo_0_"
    if model>=30 and model<40:
       signal="cs_ct14nlo_"
    if model>=40 and model<50:
       signal="AntiCIplusLL"
    if model>=60 and model<70:
       signal="cs_ct14nlo_"
    if model>=70 and model<90:
       signal="cs_ct14nlo_"

    print signal,model

    f=file("limits"+testStat+asym+str(model)+"_"+signal+"_2016.txt")
    limits=eval(f.readline())
    #print limits

    canvas = TCanvas("","",0,0,300,300)
    #canvas.GetPad(0).SetLogy()
    mg=TMultiGraph()

    min_x=5000
    max_x=20000
    g0=TGraph(0)
    g0.SetPoint(0,min_x,0)
    g0.SetPoint(1,max_x,0)
    mg.Add(g0)
    
    g=TGraph(0)
    g_exp=TGraph(0)
    g_exp1m=TGraph(0)
    g_exp1p=TGraph(0)
    for mass,limit,error,exp,exp1m,exp1p,exp2m,exp2p in limits:
      if limit==0: limit=1e-5
      if not testStat=="LHC":
       if exp>=1: exp=1e-5
       if exp1m>=1: exp1m=1e-5
       if exp1p>=1: exp1p=1e-5
       if exp2m>=1: exp2m=1e-5
       if exp2p>=1: exp2p=1e-5
      if limit>0:
        g.SetPoint(g.GetN(),mass,log10(limit))
      if exp>0:
        g_exp.SetPoint(g_exp.GetN(),mass,log10(exp))
      if exp1m>0:
        g_exp1m.SetPoint(g_exp1m.GetN(),mass,log10(exp1m))
      if exp1p>0:
        g_exp1p.SetPoint(g_exp1p.GetN(),mass,log10(exp1p))
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
    mg.GetXaxis().SetTitle("scale [GeV]")
    if testStat=="LHC":
      mg.GetYaxis().SetTitle("log_{10}(signal strength)")
      miny=-1
      maxy=1
    else:
      mg.GetYaxis().SetTitle("log_{10}(CL_{S})")
      miny=-3
      maxy=0
    mg.GetYaxis().SetRangeUser(miny,maxy)
    
    if testStat=="LHC":
      cut=1
    else:
      cut=0.05
    l=TLine(min_x,log10(cut),max_x,log10(cut))
    l.SetLineColor(2)
    l.SetLineStyle(2)
    l.Draw("same")
    if testStat=="LHC":
      l1=TLatex((max_x-min_x)*0.5+min_x,log10(cut)*1,"signal strength = 1")
    else:
      l1=TLatex((max_x-min_x)*0.5+min_x,log10(cut)*1,"CL_{S}=0.05")
    l1.Draw("same")

    limit=0
    exp=0
    exp1m=0
    exp1p=0
    for i in range(20000):
        mass=i*(max_x-limits[0][0])/20000.+limits[0][0]
        if mass<min_x or mass>max_x: continue
	if limit==0 and g.Eval(mass,0)>log10(cut):
	    limit=mass
	if exp==0 and g_exp.Eval(mass,0)>log10(cut):
	    exp=mass
	if exp1m==0 and g_exp1m.Eval(mass,0)>log10(cut):
	    exp1m=mass
	if exp1p==0 and g_exp1p.Eval(mass,0)>log10(cut):
	    exp1p=mass

    err=0
    if exp1m>0: err=exp-exp1m
    if exp1p>0 and exp1p-exp>exp-exp1m: err=exp1p-exp

    print "limit: %.1f" % (limit/1000.), "& %.1f" % (exp/1000.), "$\pm$ %.1f" % (err/1000.)

    print "limit: %.2f," % (limit/1000.), "%.2f," % (exp/1000.), "%.2f, %.2f, 0, 0" % ((exp1m)/1000.,(exp1p)/1000.)
    
    l2=TLine(limit,miny,limit,log10(cut))
    l2.SetLineColor(1)
    l2.SetLineStyle(2)
    l2.Draw("same")
    
    l2a=TLine(exp,miny,exp,log10(cut))
    l2a.SetLineColor(2)
    l2a.SetLineStyle(2)
    l2a.Draw("same")
    
    l2b=TLine(exp1m,miny,exp1m,log10(cut))
    l2b.SetLineColor(3)
    l2b.SetLineStyle(2)
    l2b.Draw("same")
    
    l2c=TLine(exp1p,miny,exp1p,log10(cut))
    l2c.SetLineColor(3)
    l2c.SetLineStyle(2)
    l2c.Draw("same")
    
    canvas.SaveAs('limits'+testStat+asym+str(model)+signal+'_2016.pdf')
    canvas.SaveAs('limits'+testStat+asym+str(model)+signal+'_2016.eps')
    
