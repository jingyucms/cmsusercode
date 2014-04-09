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
    gStyle.SetPadBottomMargin(0.10)
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

    add=(7.05, 6.77, 7.22, 6.32, 0, 0)

    results=[
            ("M_{S} (HLZ) n_{ED}=6", add[0]*8.3/7.0, add[1]*8.3/7.0, add[2]*8.3/7.0, add[3]*8.3/7.0, 0, 0),
            ("M_{S} (HLZ) n_{ED}=5", add[0]*7.7/7.0, add[1]*7.7/7.0, add[2]*7.7/7.0, add[3]*7.7/7.0, 0, 0),
            ("M_{S} (HLZ) n_{ED}=4", add[0], add[1], add[2], add[3], 0, 0),
            ("M_{S} (HLZ) n_{ED}=3", add[0]*5.9/7.0, add[1]*5.9/7.0, add[2]*5.9/7.0, add[3]*5.9/7.0, 0, 0),
            ("M_{S} (HLZ) n_{ED}=2", add[0]*7.2/7.0, add[1]*7.2/7.0, add[2]*7.2/7.0, add[3]*7.2/7.0, 0, 0),
            ("#Lambda_{T} (GRW)", add[0], add[1], add[2], add[3], 0, 0),
            ("ADD", 0,0,0,0, 0, 0),
            ("#Lambda_{(V-A)}^{-}", 8.89, 8.63, 9.81, 7.45, 0, 0),
            ("#Lambda_{(V-A)}^{+}", 8.79, 8.52, 9.64, 7.41, 0, 0),
            ("#Lambda_{AA}^{-}", 15.13, 14.49, 17.13, 11.85, 0, 0),
            ("#Lambda_{AA}^{+}", 11.37, 10.90, 12.04, 9.76, 0, 0),
            ("#Lambda_{VV}^{-}", 15.24, 14.61, 17.24, 11.98, 0, 0),
            ("#Lambda_{VV}^{+}", 11.29, 10.84, 11.97, 9.71, 0, 0),
            ("#Lambda_{LL/RR}^{-}", 11.75, 11.37, 13.20, 9.55, 0, 0),
            ("#Lambda_{LL/RR}^{+}", 8.99, 8.74, 9.55, 7.94, 0, 0),
            #("#Lambda_{LL/RR}^{-} (LO)", 12.93, 12.43, 14.64, 10.21, 0, 0),
            #("#Lambda_{LL/RR}^{+} (LO)", 10.35, 9.83, 10.88, 8.78, 0, 0),
            ("Contact interaction", 0,0,0,0, 0, 0),
            ]

    print results

    graphs=[]

    xmin=5
    xmax=18

    c1 = TCanvas("Limit summary","Limit summary",0,0,300,320)
     
    g1 = TH2F("grid", "", 20, xmin, xmax, 20, 0, len(results)+0.8)
    g1.GetXaxis().SetTitle("Lower limit [TeV]")
    g1.GetXaxis().SetNdivisions((xmax-xmin)/2)
    g1.GetXaxis().SetLabelSize(0.038)
    g1.GetXaxis().SetTitleSize(0.04)
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
        if "GRW" in results[i][0] or "HLZ" in results[i][0] or "ADD" in results[i][0]:
          l1 = TLatex(xmin+5.3,i+0.9,results[i][0])
        else:
	  l1 = TLatex(xmin+0.3,i+0.9,results[i][0])
        l1.SetTextSize(0.038)
        l1.Draw("same")
        graphs+=[l1]
    
    l5=TLegend(0.74,0.92,1.0,0.92,"CMS")
    l5.SetTextSize(0.038)
    l5.SetFillStyle(0)
    #l5.Draw("same")
     
    l3=TLegend(0.7,0.88,1.0,0.88,"#sqrt{s} = 8 TeV")
    l3.SetTextSize(0.038)
    l3.SetFillStyle(0)
    #l3.Draw("same")
     
    l=TLegend(0.7,0.84,1.0,0.84,"L = 19.7 fb^{-1}")
    l.SetTextSize(0.038)
    l.SetFillStyle(0)
    #l.Draw("same")
    
    banner=TLatex(0.3,0.96,"CMS,   L = 19.7 fb^{-1},   #sqrt{s} = 8 TeV")
    banner.SetNDC()
    banner.SetTextSize(0.035)
    banner.Draw()

    l2=TLegend(0.64,0.8,0.98,0.94,"")
    l2.SetTextSize(0.038)
    l2.AddEntry(g2,"Observed","l")
    l2.AddEntry(g3,"Expected","l")
    l2.AddEntry(g5,"Expected #pm 1#sigma","f")
    #l2.AddEntry(g4,"Expected #pm 2#sigma","f")
    l2.SetFillStyle(0)
    l2.Draw("same")

    c1.Print("limits_summary.ps")
    c1.Print("limits_summary.pdf")
    #os.system("ps2pdf limits_summary.ps limits_summary.pdf")
    c1.WaitPrimitive()
