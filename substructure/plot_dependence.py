from ROOT import *
import ROOT
import array, math
import os
from math import *

if __name__=="__main__":

    print "start ROOT"
    gROOT.Reset()
    gROOT.SetStyle("Plain")
    gStyle.SetOptStat(0)
    gStyle.SetOptFit(0)
    gStyle.SetTitleOffset(1.2,"Y")
    gStyle.SetPadLeftMargin(0.16)
    gStyle.SetPadBottomMargin(0.16)
    gStyle.SetPadTopMargin(0.05)
    gStyle.SetPadRightMargin(0.05)
    gStyle.SetMarkerSize(2.5)
    gStyle.SetHistLineWidth(1)
    gStyle.SetStatFontSize(0.020)
    gStyle.SetTitleSize(0.065, "XYZ")
    gStyle.SetLabelSize(0.05, "XYZ")
    gStyle.SetLegendBorderSize(0)
    gStyle.SetPadTickX(1)
    gStyle.SetPadTickY(1)
    gStyle.SetEndErrorSize(5)

    #for name in ["n2_b1_ddt","n2_b1_ddt_WZ","pt","ptgen"]:
    for name in ["n2_b1_gen","ptgen"]:
      c = TCanvas("dependence", "dependence", 0, 0, 300, 300)
      if name=="n2_b1_ddt" or name=="n2_b1_ddt_WZ":
        c.SetLogx()
      mg=TMultiGraph()
      colors=[1,2,4,6,7,8,9,15,1,2,3,4,6,7,8,9,15]
      styles=[24,25,26,27,28]
    
      l3=TLegend(0.3,0.42,0.8,0.75,"")
      l3.SetTextSize(0.05)
    
      style=0
      if name=="n2_b1_ddt":
        xs=[0.005,0.01,0.02,0.05,0.1,0.3] #0.3 corresponds to no N2 cut
        ys=[82.469,82.381,82.26,82.157,82.025,81.903]
      elif name=="n2_b1_ddt_WZ":
        xs=[0.005,0.01,0.02,0.05,0.1,0.3]
        ys=[10.348,10.454,10.601,10.813,10.923,11.022]
      elif name=="pt":
        xs=[350,450,550,650,750]
        ys=[82.27,81.75,80.99,80.48,79.14]
      elif name=="ptgen":
        xs=[300,350,400,450,500,550]
        ys=[92.469,92.105,91.995,91.643,91.556,91.534]
      elif name=="n2_b1_gen":
        xs=[0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45]
        ys=[91.662,91.909,92.150,93.158,93.676,93.779,93.543,93.280]
      
      pointsX=array.array("f",[x for x in xs])
      pointsY=array.array("f",[y for y in ys])
      g=TGraph(len(pointsX),pointsX,pointsY)
      g.SetMarkerStyle(styles[style])
      g.SetMarkerSize(1)
      g.SetLineColor(colors[style])
      g.SetLineStyle(1)
      g.SetLineWidth(2)
      mg.Add(g)
      #l3.AddEntry(g,"Vector","pl")
      #style+=1
      
      if name=="n2_b1_gen":
        l3.AddEntry(g,"Z","pl")
	style+=1
	
        xs=[0.15,0.2,0.25,0.3,0.35,0.4,0.45]
        ys=[91.878,92.291,92.565,92.803,92.725,92.751,92.720]
        pointsX=array.array("f",[x for x in xs])
        pointsY=array.array("f",[y for y in ys])
        g=TGraph(len(pointsX),pointsX,pointsY)
        g.SetMarkerStyle(styles[style])
        g.SetMarkerSize(1)
        g.SetLineColor(colors[style])
        g.SetLineStyle(1)
        g.SetLineWidth(2)
        mg.Add(g)
        l3.AddEntry(g,"Z #rightarrow b#bar{b}","pl")
        style+=1
        
	
        xs=[0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45]
        ys=[91.042,91.025,91.000,90.939,90.825,90.700,90.562,90.496]
        pointsX=array.array("f",[x for x in xs])
        pointsY=array.array("f",[y for y in ys])
        g=TGraph(len(pointsX),pointsX,pointsY)
        g.SetMarkerStyle(styles[style])
        g.SetMarkerSize(1)
        g.SetLineColor(colors[style])
        g.SetLineStyle(1)
        g.SetLineWidth(2)
        mg.Add(g)
        l3.AddEntry(g,"Z (no non-pert. eff.)","pl")
        style+=1
       
        xs=[0,1]
        ys=[91.1876,91.1876]
        pointsX=array.array("f",[x for x in xs])
        pointsY=array.array("f",[y for y in ys])
        g=TGraph(len(pointsX),pointsX,pointsY)
        g.SetMarkerStyle(1)
        g.SetMarkerSize(1)
        g.SetLineColor(15)
        g.SetLineStyle(9)
        g.SetLineWidth(2)
        mg.Add(g)
        l3.AddEntry(g,"Z (world average)","pl")
        #style+=1

	xs=[0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45]
        ys=[81.298,81.019,81.393,81.471,82.27,82.696,82.66,82.541]
        pointsX=array.array("f",[x for x in xs])
        pointsY=array.array("f",[y for y in ys])
        g=TGraph(len(pointsX),pointsX,pointsY)
        g.SetMarkerStyle(styles[style])
        g.SetMarkerSize(1)
        g.SetLineColor(colors[style])
        g.SetLineStyle(1)
        g.SetLineWidth(2)
        mg.Add(g)
        l3.AddEntry(g,"W","pl")
        style+=1
       
        xs=[0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45]
        ys=[80.321,80.321,80.293,80.262,80.209,80.039,80.010,79.995]
        pointsX=array.array("f",[x for x in xs])
        pointsY=array.array("f",[y for y in ys])
        g=TGraph(len(pointsX),pointsX,pointsY)
        g.SetMarkerStyle(styles[style])
        g.SetMarkerSize(1)
        g.SetLineColor(colors[style])
        g.SetLineStyle(1)
        g.SetLineWidth(2)
        mg.Add(g)
        l3.AddEntry(g,"W (no non-pert. eff.)","pl")
        style+=1
       
        xs=[0,1]
        ys=[80.385,80.385]
        pointsX=array.array("f",[x for x in xs])
        pointsY=array.array("f",[y for y in ys])
        g=TGraph(len(pointsX),pointsX,pointsY)
        g.SetMarkerStyle(1)
        g.SetMarkerSize(1)
        g.SetLineColor(15)
        g.SetLineStyle(9)
        g.SetLineWidth(2)
        mg.Add(g)
        l3.AddEntry(g,"W (world average)","pl")
        #style+=1

      if name=="ptgen":
        l3.AddEntry(g,"Z","pl")
	
        xs=[300,350,400,450,500,550]
        ys=[93.725,93.748,93.070,92.635,92.163,91.951]
        pointsX=array.array("f",[x for x in xs])
        pointsY=array.array("f",[y for y in ys])
        g=TGraph(len(pointsX),pointsX,pointsY)
        #g.SetMarkerStyle(styles[style])
        #g.SetMarkerSize(1)
        g.SetLineColor(colors[style])
        g.SetLineStyle(2)
        g.SetLineWidth(2)
        mg.Add(g)
        #l3.AddEntry(g,"Z, N_{2}^{#beta=1}<0.2","pl")
        style+=1
       
        xs=[300,350,400,450,500,550]
        ys=[92.568,91.991,91.758,91.674,91.342,91.506]
        pointsX=array.array("f",[x for x in xs])
        pointsY=array.array("f",[y for y in ys])
        g=TGraph(len(pointsX),pointsX,pointsY)
        g.SetMarkerStyle(styles[style])
        g.SetMarkerSize(1)
        g.SetLineColor(colors[style])
        g.SetLineStyle(1)
        g.SetLineWidth(2)
        mg.Add(g)
        l3.AddEntry(g,"Z #rightarrow b#bar{b}","pl")
        #style+=1
       
        xs=[300,350,400,450,500,550]
        ys=[93.198,92.847,92.383,91.811,91.506,91.607]
        pointsX=array.array("f",[x for x in xs])
        pointsY=array.array("f",[y for y in ys])
        g=TGraph(len(pointsX),pointsX,pointsY)
        #g.SetMarkerStyle(styles[style])
        #g.SetMarkerSize(1)
        g.SetLineColor(colors[style])
        g.SetLineStyle(2)
        g.SetLineWidth(2)
        mg.Add(g)
        #l3.AddEntry(g,"Z, b#bar{b}, N_{2}^{#beta=1}<0.2","pl")
        style+=1
       
        xs=[300,350,400,450,500,550]
        ys=[91.004,90.992,91.027,91.026,90.963,90.989]
        pointsX=array.array("f",[x for x in xs])
        pointsY=array.array("f",[y for y in ys])
        g=TGraph(len(pointsX),pointsX,pointsY)
        g.SetMarkerStyle(styles[style])
        g.SetMarkerSize(1)
        g.SetLineColor(colors[style])
        g.SetLineStyle(1)
        g.SetLineWidth(2)
        mg.Add(g)
        l3.AddEntry(g,"Z (no non-pert. eff.)","pl")
        #style+=1

        xs=[300,350,400,450,500,550]
        ys=[90.435,90.645,90.697,90.718,90.640,90.601]
        pointsX=array.array("f",[x for x in xs])
        pointsY=array.array("f",[y for y in ys])
        g=TGraph(len(pointsX),pointsX,pointsY)
        #g.SetMarkerStyle(styles[style])
        #g.SetMarkerSize(1)
        g.SetLineColor(colors[style])
        g.SetLineStyle(2)
        g.SetLineWidth(2)
        mg.Add(g)
        #l3.AddEntry(g,"Z, N_{2}^{#beta=1}<0.2, no non-pert. eff.","pl")
        style+=1
	
        xs=[0,1000]
        ys=[91.1876,91.1876]
        pointsX=array.array("f",[x for x in xs])
        pointsY=array.array("f",[y for y in ys])
        g=TGraph(len(pointsX),pointsX,pointsY)
        g.SetMarkerStyle(1)
        g.SetMarkerSize(1)
        g.SetLineColor(15)
        g.SetLineStyle(9)
        g.SetLineWidth(2)
        mg.Add(g)
        l3.AddEntry(g,"Z (world average)","pl")
        #style+=1
       
        xs=[300,350,400,450,500,550]
        ys=[81.598,81.404,81.179,81.011,80.645,80.643]
        pointsX=array.array("f",[x for x in xs])
        pointsY=array.array("f",[y for y in ys])
        g=TGraph(len(pointsX),pointsX,pointsY)
        g.SetMarkerStyle(styles[style])
        g.SetMarkerSize(1)
        g.SetLineColor(colors[style])
        g.SetLineStyle(1)
        g.SetLineWidth(2)
        mg.Add(g)
        l3.AddEntry(g,"W","pl")
        #style+=1
       
        xs=[300,350,400,450,500,550]
        ys=[82.982,82.557,82.424,81.579,80.925,80.833]
        pointsX=array.array("f",[x for x in xs])
        pointsY=array.array("f",[y for y in ys])
        g=TGraph(len(pointsX),pointsX,pointsY)
        #g.SetMarkerStyle(styles[style])
        #g.SetMarkerSize(1)
        g.SetLineColor(colors[style])
        g.SetLineStyle(2)
        g.SetLineWidth(2)
        mg.Add(g)
        #l3.AddEntry(g,"W, N_{2}^{#beta=1}<0.2","pl")
        style+=1
       
        xs=[300,350,400,450,500,550]
        ys=[80.292,80.315,80.306,80.358,80.331,80.144]
        pointsX=array.array("f",[x for x in xs])
        pointsY=array.array("f",[y for y in ys])
        g=TGraph(len(pointsX),pointsX,pointsY)
        g.SetMarkerStyle(styles[style])
        g.SetMarkerSize(1)
        g.SetLineColor(colors[style])
        g.SetLineStyle(1)
        g.SetLineWidth(2)
        mg.Add(g)
        l3.AddEntry(g,"W (no non-pert. eff.)","pl")
        #style+=1

        xs=[300,350,400,450,500,550]
        ys=[80.007,80.084,80.097,79.924,79.927,80.004]
        pointsX=array.array("f",[x for x in xs])
        pointsY=array.array("f",[y for y in ys])
        g=TGraph(len(pointsX),pointsX,pointsY)
        #g.SetMarkerStyle(styles[style])
        #g.SetMarkerSize(1)
        g.SetLineColor(colors[style])
        g.SetLineStyle(2)
        g.SetLineWidth(2)
        mg.Add(g)
        #l3.AddEntry(g,"W, N_{2}^{#beta=1}<0.2, no non-pert. eff.","pl")
        style+=1
       
        xs=[0,1000]
        ys=[80.385,80.385]
        pointsX=array.array("f",[x for x in xs])
        pointsY=array.array("f",[y for y in ys])
        g=TGraph(len(pointsX),pointsX,pointsY)
        g.SetMarkerStyle(1)
        g.SetMarkerSize(1)
        g.SetLineColor(15)
        g.SetLineStyle(9)
        g.SetLineWidth(2)
        mg.Add(g)
        l3.AddEntry(g,"W (world average)","pl")
        #style+=1
       
      mg.Draw("apl")
      mg.SetTitle("")
      
      if name=="n2_b1_ddt":
        mg.GetXaxis().SetTitle("N2 (#beta=1) DDT cut")
        mg.GetYaxis().SetTitle("m_{W} (GeV)")
        mg.GetXaxis().SetRangeUser(0.004,0.3)
        mg.GetYaxis().SetRangeUser(81.8,82.6)
      elif name=="n2_b1_ddt_WZ":
        mg.GetXaxis().SetTitle("N2 (#beta=1) DDT cut")
        mg.GetYaxis().SetTitle("m_{Z}-m_{W} (GeV)")
        mg.GetXaxis().SetRangeUser(0.004,0.3)
        mg.GetYaxis().SetRangeUser(10.3,11.1)
      elif name=="pt":
        mg.GetXaxis().SetTitle("Jet p_{T} (GeV)")
        mg.GetYaxis().SetTitle("m_{W} (GeV)")
        mg.GetXaxis().SetRangeUser(300,800)
        mg.GetYaxis().SetRangeUser(79.0,82.4)
      elif name=="ptgen":
        mg.GetXaxis().SetTitle("Jet p_{T} (GeV)")
        mg.GetYaxis().SetTitle("m_{W,Z} (GeV)")
        mg.GetXaxis().SetRangeUser(300,500)
        mg.GetYaxis().SetRangeUser(77.0,95.0)
      elif name=="n2_b1_gen":
        mg.GetXaxis().SetTitle("N2 (#beta=1) threshold")
        mg.GetYaxis().SetTitle("m_{W,Z} (GeV)")
        mg.GetXaxis().SetRangeUser(0.15,0.45)
        mg.GetYaxis().SetRangeUser(77.0,95.0)
 
      l3.SetFillStyle(0)
      l3.Draw("same")
      
      c.SaveAs(name+"dependence.pdf")
      c.SaveAs(name+"dependence.eps")
