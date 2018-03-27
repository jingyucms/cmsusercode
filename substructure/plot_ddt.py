print "import"
import os, sys
import array
from ROOT import * 
from os import path
import subprocess
import array

#gROOT.Reset()
#gROOT.SetStyle("Plain")
#gROOT.ProcessLine('.L tdrstyle.C')
gROOT.SetBatch(True)
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetTitleOffset(1.3,"Y")
gStyle.SetTitleOffset(1.1,"Z")
gStyle.SetPadLeftMargin(0.17)
gStyle.SetPadBottomMargin(0.17)
gStyle.SetPadTopMargin(0.08)
gStyle.SetPadRightMargin(0.2)
gStyle.SetMarkerSize(0.5)
gStyle.SetHistLineWidth(1)
#gStyle.SetStatFontSize(0.020)
gStyle.SetTitleSize(0.06, "XYZ")
gStyle.SetLabelSize(0.05, "XYZ")
gStyle.SetNdivisions(506, "XYZ")
gStyle.SetLegendBorderSize(0)

TGaxis.SetMaxDigits(3)

if __name__ == '__main__':

 print "start"

 colors=[12,13,14,15,16,17,18,19]
 nbins_rho=12
 min_rho=-7
 max_rho=-1
 mass="mmdt"
 variable="n2_b1"
 #variable="n2_b2"
 
 if variable=="n2_b1":
   nmax=0.5
 if variable=="n2_b2":
   nmax=0.1

 #for wp in [0.001,0.002,0.005,0.01,0.02,0.05,0.1,0.15,0.2]:
 for wp in [0.01]:

  samples = ["root://eoscms.cern.ch//eos/cms/store/cmst3/group/exovv/precision/QCD_HT300to500_tarball.tar.xz/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/exovv/precision/QCD_HT500to700_tarball.tar.xz/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/exovv/precision/QCD_HT700to1000_tarball.tar.xz/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/exovv/precision/QCD_HT1000to1500_tarball.tar.xz/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/exovv/precision/QCD_HT1500to2000_tarball.tar.xz/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/exovv/precision/QCD_HT2000toInf_tarball.tar.xz/ntupler/",
 	     ]
  canvas = TCanvas("c1","c1",0,0,200,200)
  pts=[(200,300),(300,400),(400,500),(500,600),(600,800),(800,1000),(1000,10000)]
  ptsarray=array.array("d",[pt[0] for pt in pts]+[10000])
  hists=[]
  graphs=[]
  lookup=TH2F("lookup","lookup",nbins_rho,min_rho,max_rho,len(pts),ptsarray)
  mainhist=None
  for pt in pts:
   print pt
   pthist=None
   count=0
   for sample in samples:
     print sample
     tree=TChain("t_allpar")
     p=subprocess.Popen(["eos ls "+sample.replace("root://eoscms.cern.ch/","")],shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
     files=0
     for fn in p.stdout:
       if not ".root" in fn: continue
       tree.Add(sample+fn.replace("\n",""))
       files+=1
       #if files>10: break### only first files for testing
     hists+=[tree]
     print sample,tree.GetEntries()
     hist=TH2F("ddt"+str(pts.index(pt))+str(count),"",nbins_rho,min_rho,max_rho,100,0,nmax)
     hists+=[hist]
     tree.Project("ddt"+str(pts.index(pt))+str(count),"j_"+variable+":log(pow(j_mass_"+mass+"/j_pt,2))","(j_pt>="+str(pt[0])+")*(j_pt<"+str(pt[1])+")")
     if "300to500" in sample:
       hist.Scale(3.50e+05/1634880)
     if "500to700" in sample:
       hist.Scale(32100./2185120)
     if "700to1000" in sample:
       hist.Scale(6831./1713079)
     if "1000to1500" in sample:
       hist.Scale(1207./1362432)
     if "1500to2000" in sample:
       hist.Scale(119.9/668887)
     if "2000toInf" in sample:
       hist.Scale(25.24/689668)
     if pthist==None:
       pthist=hist
     else:
       pthist.Add(hist)
     print count,pthist.Integral()
     count+=1

   if mainhist==None:
     mainhist=pthist
   else:
     mainhist.Add(pthist)
   
   graph=TGraph()
   graphs+=[graph]
   npoints=0
   for x in range(1,pthist.GetXaxis().GetNbins()+1):
     sumy=0
     for y in range(1,pthist.GetYaxis().GetNbins()+1):
         sumy+=pthist.GetBinContent(x,y)
     partsumy=0
     for y in range(1,pthist.GetYaxis().GetNbins()+1):
         partsumy+=pthist.GetBinContent(x,y)
	 if partsumy>wp*sumy:
	    graph.Set(npoints)
	    graph.SetPoint(npoints,pthist.GetXaxis().GetBinCenter(x),pthist.GetYaxis().GetBinCenter(y))
	    lookup.SetBinContent(x,pts.index(pt)+1,pthist.GetYaxis().GetBinCenter(y))
	    npoints+=1
	    break
         	 
  mainhist.GetXaxis().SetTitle("#rho = log(m_{mMDT}^{2}/p_{T}^{2})")
  if variable=="n2_b1":
    mainhist.GetYaxis().SetTitle("N_{2}^{#beta=1}")
  if variable=="n2_b2":
    mainhist.GetYaxis().SetTitle("N_{2}^{#beta=2}")
  mainhist.GetZaxis().SetTitle("Events")
  mainhist.Draw("colz")
  for graph in graphs:
    graph.SetLineColor(colors[graphs.index(graph)])
    graph.SetLineStyle(graphs.index(graph)+1)
    #graph.SetMarkerStyle(graphs.index(graph)+20)
    graph.Draw("lsame")
  canvas.SaveAs("ddt_"+variable+"_"+str(wp)+".pdf")
  f=TFile.Open("ddt_"+variable+"_"+str(wp)+".root","RECREATE")
  lookup.Write()
  f.Close()
  