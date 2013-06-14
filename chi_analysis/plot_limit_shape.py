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
gStyle.SetNdivisions(510, "XYZ")
gStyle.SetLegendBorderSize(0)

if __name__=="__main__":

    model=2

    if model==0:
    	signal="CI"    
    if model==1:
    	signal="ADD_4_0_0_"
    if model==2:
    	signal="ADD_4_0_1_"

    f=file("limits"+signal+".txt")
    limits=eval(f.readline())
    print limits

    canvas = TCanvas("","",0,0,300,300)
    #canvas.GetPad(0).SetLogy()
    mg=TMultiGraph()

    g=TGraph(1)
    g_exp=TGraph(1)
    g_exp1m=TGraph(1)
    g_exp1p=TGraph(1)
    i=0
    for mass,limit,error,exp,exp1m,exp1p,exp2m,exp2p in limits:
        g.SetPoint(i,mass,limit)
        g_exp.SetPoint(i,mass,exp)
        g_exp1m.SetPoint(i,mass,exp1m)
        g_exp1p.SetPoint(i,mass,exp1p)
	i+=1
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
    mg.GetXaxis().SetTitle("contact interaction scale [GeV]")
    mg.GetYaxis().SetTitle("CLs")
    mg.GetYaxis().SetRangeUser(0,1)
    
    l=TLine(limits[0][0],0.05,limits[-1][0],0.05)
    l.SetLineColor(2)
    l.SetLineStyle(2)
    l.Draw("same")
    
    limit=0
    exp=0
    exp1m=0
    exp1p=0
    for i in reversed(range(10000)):
        mass=i*(limits[-1][0]-limits[0][0])/10000.+limits[0][0]
	if limit==0 and g.Eval(mass,0)<0.05:
	    limit=mass
	if exp==0 and g_exp.Eval(mass,0)<0.05:
	    exp=mass
	if exp1m==0 and g_exp1m.Eval(mass,0)<0.05:
	    exp1m=mass
	if exp1p==0 and g_exp1p.Eval(mass,0)<0.05:
	    exp1p=mass

    print "limit",limit,"exp",exp,"-",exp-exp1m,"+",exp1p-exp
    
    l2=TLine(limit,0,limit,0.05)
    l2.SetLineColor(2)
    l2.SetLineStyle(2)
    l2.Draw("same")
    
    canvas.SaveAs('limits'+signal+'.pdf')
    canvas.SaveAs('limits'+signal+'.eps')
    