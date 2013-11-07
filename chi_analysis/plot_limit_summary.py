from ROOT import *
import ROOT
import array
import os

if __name__ == "__main__":
    prefix="dijet1fb"

    print "*** init root"    
    gROOT.Reset()
    gROOT.SetStyle("Plain")
    gStyle.SetOptStat(0)
    gStyle.SetOptFit(0)
    gStyle.SetTitleOffset(1.1,"X")
    gStyle.SetTitleOffset(1.3,"Y")
    gStyle.SetPadLeftMargin(0.05)
    gStyle.SetPadBottomMargin(0.15)
    gStyle.SetPadTopMargin(0.05)
    gStyle.SetPadRightMargin(0.05)
    gStyle.SetMarkerSize(1.5)
    gStyle.SetHistLineWidth(1)
    gStyle.SetStatFontSize(0.025)
    gStyle.SetTitleFontSize(0.05)
    gStyle.SetTitleSize(0.06, "XYZ")
    gStyle.SetLabelSize(0.05, "XYZ")
    gStyle.SetNdivisions(510, "XYZ")
    gStyle.SetNdivisions(503, "Y")
    gStyle.SetLegendBorderSize(0)
    gStyle.SetErrorX(1)

    results=[
            ("ADD M_{S} (HLZ) n_{ED}=2", 6.97*7.2/7.0, 6.99*7.2/7.0, 7.67*7.2/7.0, 6.32*7.2/7.0, 0, 0),
            ("ADD M_{S} (HLZ) n_{ED}=3", 6.97*5.9/7.0, 6.99*5.9/7.0, 7.67*5.9/7.0, 6.32*5.9/7.0, 0, 0),
            ("ADD M_{S} (HLZ) n_{ED}=4", 6.97, 6.99, 7.67, 6.32, 0, 0),
            ("ADD M_{S} (HLZ) n_{ED}=5", 6.97*7.7/7.0, 6.99*7.7/7.0, 7.67*7.7/7.0, 6.32*7.7/7.0, 0, 0),
            ("ADD M_{S} (HLZ) n_{ED}=6", 6.97*8.3/7.0, 6.99*8.3/7.0, 7.67*8.3/7.0, 6.32*8.3/7.0, 0, 0),
            ("ADD #Lambda_{T} (GRW)", 6.97, 6.99, 7.67, 6.32, 0, 0),
            ("", 0,0,0,0, 0, 0),
            ("#Lambda_{(V-A)}^{#pm} (LO)", 8.64, 8.96, 8.96+0.8, 8.96-0.8, 0, 0),
            ("#Lambda_{VV/AA}^{-} (LO)", 15.51, 16.30, 19.00, 13.60, 0, 0),
            ("#Lambda_{VV/AA}^{+} (LO)", 11.60, 11.66, 12.99, 10.33, 0, 0),
            ("#Lambda_{LL/RR}^{-} (LO)", 11.91, 12.52, 14.56, 10.48, 0, 0),
            ("#Lambda_{LL/RR}^{+} (LO)", 9.80, 9.83, 10.71, 8.95, 0, 0),
            ("#Lambda_{LL/RR}^{-} (NLO)", 10.87, 11.37, 13.21, 9.53, 0, 0),
            ("#Lambda_{LL/RR}^{+} (NLO)", 8.76, 8.83, 9.64, 8.03, 0, 0),
            ]

    graphs=[]

    xmin=3
    xmax=20

    c1 = TCanvas("Limit summary","Limit summary",0,0,300,300)
     
    g1 = TH2F("grid", "", 20, xmin, xmax, 20, 0, len(results)+0.8)
    g1.GetXaxis().SetTitle("Lower limit on energy scale [TeV]")
    g1.GetXaxis().SetNdivisions(xmax-xmin)
    g1.GetYaxis().SetLabelColor(0)
    g1.GetYaxis().SetNdivisions(1)
    g1.Draw()
    graphs+=[g1]

    for x in range(xmin+1,xmax):
      l4 = TLine(x,0.2,x,len(results)+0.8)
      l4.SetLineColor(16)
      l4.SetLineWidth(1)
      l4.SetLineStyle(3)
      l4.Draw("same")
      graphs+=[l4]

    for i in range(len(results)):
        g4 = TPave(results[i][5],i+0.9,results[i][6],i+1.1)
        g4.SetFillColor(17)
        g4.Draw("same")
        graphs+=[g4]
    
    for i in range(len(results)):
        g5 = TPave(results[i][3],i+0.85,results[i][4],i+1.15)
        g5.SetFillColor(15)
        g5.Draw("same")
        graphs+=[g5]
    
    for i in range(len(results)):
        g3 = TLine(results[i][2],i+0.7,results[i][2],i+1.3)
        g3.SetLineColor(1)
        g3.SetLineWidth(3)
        g3.SetLineStyle(2)
        g3.Draw("same")
        graphs+=[g3]
    
    for i in range(len(results)):
        g2 = TLine(results[i][1],i+0.7,results[i][1],i+1.3)
        g2.SetLineColor(2)
        g2.SetLineWidth(3)
        g2.SetLineStyle(1)
        g2.Draw("same")
        graphs+=[g2]
    
    for i in range(len(results)):
        if "ADD" in results[i][0]:
          l1 = TLatex(xmin+8.3,i+0.9,results[i][0])
        else:
	  l1 = TLatex(xmin+0.3,i+0.9,results[i][0])
        l1.SetTextSize(0.05)
        l1.Draw("same")
        graphs+=[l1]
    
    c1.Print("limits_summary.ps")
    os.system("ps2pdf limits_summary.ps limits_summary.pdf")
    c1.WaitPrimitive()
