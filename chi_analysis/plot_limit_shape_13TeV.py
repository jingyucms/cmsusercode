from ROOT import *
import ROOT

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

 models=[1,2,3,4,5,6,7]

 for model in models:

    if model==1:
       signal="CIplusLL"    
    if model==2:
       signal="CIminusLL"    
    if model==3:
       signal="ADD"    
    if model==4:
       signal="CIplusLL"    
    if model==5:
       signal="CIplusLL"    

    print signal

    f=file("limits"+str(model)+"_"+signal+".txt")
    limits=eval(f.readline())
    #print limits

    canvas = TCanvas("","",0,0,300,300)
    #canvas.GetPad(0).SetLogy()
    mg=TMultiGraph()

    min_x=7000
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
    mg.GetYaxis().SetTitle("log_{10}(CL_{S})")
    mg.GetYaxis().SetRangeUser(-3,0)
    
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
    for i in range(20000):
        mass=i*(limits[-1][0]-limits[0][0])/20000.+limits[0][0]
        if mass<min_x or mass>max_x: continue
	if limit==0 and g.Eval(mass,0)>log10(0.05):
	    limit=mass
	if exp==0 and g_exp.Eval(mass,0)>log10(0.05):
	    exp=mass
	if exp1m==0 and g_exp1m.Eval(mass,0)>log10(0.05):
	    exp1m=mass
	if exp1p==0 and g_exp1p.Eval(mass,0)>log10(0.05):
	    exp1p=mass

    print "limit: %.1f" % (limit/1000.), "& %.1f" % (exp/1000.), "$\pm$ %.1f" % (max(exp-exp1m,exp1p-exp)/1000.)

    print "limit: %.2f," % (limit/1000.), "%.2f," % (exp/1000.), "%.2f, %.2f, 0, 0" % ((max(exp-exp1m,exp1p-exp)+exp)/1000.,(exp-max(exp-exp1m,exp1p-exp))/1000.)
    
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
    
    canvas.SaveAs('limits'+str(model)+signal+'.pdf')
    canvas.SaveAs('limits'+str(model)+signal+'.eps')
    
