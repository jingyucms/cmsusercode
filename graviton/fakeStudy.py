from ROOT import *
import ROOT
import array, math
import os
from CMGTools.RootTools.RootTools import *

algo="_ca8pruned2"

prefix = "plots/fakeStudy"+algo+"_v2"

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

def rebin(h,variable):
    mass_bins=[1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808, 7000]
    mass_binning=array.array('d')
    for mass_bin in mass_bins:
        mass_binning.append(mass_bin)
    if variable=="mass":
        #h.Rebin(60)
        h.Rebin(6)
        #h.Rebin(len(mass_binning)-1,h.GetName()+"_rebin",mass_binning)
    if variable=="mass1":
        h.Rebin(2)
    if variable=="pt1":
        h.Rebin(6)

def plot(samples,weights,files,variable):
    hists=[]
    colors=[1,2,3,4,6,7,8,9,10,11,12,13,14]
    
    canvas = TCanvas("","",0,0,300,300)
    canvas.Divide(2,2)
    canvas.cd(1)
    canvas.GetPad(1).SetLogy()
    legend=TLegend(0.5,0.6,0.9,0.9,"")
    same=""
    for i in range(len(samples)):
        weight=weights[i]
	try:
            h = TH1F(files[i].Get("cmgPFDiJetHistograms0tag/"+variable))
	except:
            h = TH1F(files[i].Get("cmgPFDiJetHistograms/"+variable))
	h.Scale(weight)
	rebin(h,variable)
	h.SetLineColor(colors[i])
	h.SetMarkerColor(colors[i])
	h.Draw("hist"+same)
	same="same"
	if variable=="mass":
            h.GetXaxis().SetTitle("dijet mass [GeV]")
	    h.GetXaxis().SetRangeUser(500,3500)
	if variable=="pt1":
            h.GetXaxis().SetTitle("jet 1 p_T [GeV]")
	    h.GetXaxis().SetRangeUser(0,1500)
	if variable=="mass1":
            h.GetXaxis().SetTitle("jet 1 mass [GeV]")
	    h.GetXaxis().SetRangeUser(0,200)
	h.GetYaxis().SetTitle("d#sigma [fb]")
	h.GetYaxis().SetRangeUser(1e-3,1e7)
	h.SetTitle("")
	h.GetXaxis().SetTitleOffset(1.0)
	h.GetYaxis().SetTitleOffset(1.4)
	h.GetXaxis().SetLabelSize(0.05)
	h.GetYaxis().SetLabelSize(0.05)
	h.GetXaxis().SetTitleSize(0.06)
	h.GetYaxis().SetTitleSize(0.06)
	hists+=[h]
        legend.AddEntry(h,samples[i][2]+" all","l")
        h2 = TH1F(files[i].Get("cmgPFDiJetHistograms1tag/"+variable))
	h2.Scale(weight)
	rebin(h2,variable)
	h2.SetLineColor(colors[i])
	h2.SetMarkerColor(colors[i])
	h2.SetLineStyle(2)
	h2.Draw("histsame")
	hists+=[h2]
        legend.AddEntry(h2,samples[i][2]+" 1tag","l")
        h3 = TH1F(files[i].Get("cmgPFDiJetHistograms2tag/"+variable))
	h3.Scale(weight)
	rebin(h3,variable)
	h3.SetLineColor(colors[i])
	h3.SetMarkerColor(colors[i])
	h3.SetLineStyle(3)
	h3.Draw("histsame")
	hists+=[h3]
        legend.AddEntry(h3,samples[i][2]+" 2tag","l")
        #print [h3.GetBinContent(b+1) for b in range(h3.GetXaxis().GetNbins())]
	#fit=TF1('fit '+str(i),'exp(5*[1]-1e-3*[2]*x-7e-7*[3]*[3]*x*x+1e-12*[0]*[0]*[0]*x*x*x+1e-15*[4]*[4]*[4]*[4]*x*x*x*x)',700,3500)
	fit=TF1('fit '+str(i),'pow(1.0-x/7000.0,[0])/pow(x/7000.0,[1]+[2]*log(x/7000.0))',700,3500)
	#fit=TF1('fit '+str(i),'exp(5*[1]-1e-3*[2]*x-7e-7*[3]*[3]*x*x)',700,3500)
	fit.SetParameter(0,0)
	fit.SetParameter(1,1)
	fit.SetParameter(2,1)
	fit.SetParameter(3,1)
	fit.SetParameter(4,1)
	fit.SetLineWidth(1)
	fit.SetLineColor(colors[i])
	#h2.Fit(fit,"R0")
	h3.Fit(fit,"R0")
	fit.Draw('lsame')
	#i=0
	#while i<fit.Integral(700,3500)*5:
	#    i+=1
	#    print fit.GetRandom()
	    
	print "1tag xsec", h2.Integral()
	#print "1tag xsec 1000", h2.Integral(h2.FindBin(800),h2.FindBin(1200))
	#print "1tag xsec 2000", h2.Integral(h2.FindBin(1600),h2.FindBin(2400))
	#print "1tag efficiency", h2.Integral()/h.Integral()
	#print "1tag efficiency 1000", h2.Integral(h2.FindBin(800),h2.FindBin(1200))/h.Integral(h2.FindBin(800),h2.FindBin(1200))
	#print "1tag efficiency 2000", h2.Integral(h2.FindBin(1600),h2.FindBin(2400))/h.Integral(h2.FindBin(1600),h2.FindBin(2400))
	#print "2tag xsec", h3.Integral()
	#print "2tag xsec 1000", h3.Integral(h3.FindBin(800),h3.FindBin(1200))
	#print "2tag xsec 2000", h3.Integral(h3.FindBin(1600),h3.FindBin(2400))
	#print "2tag efficiency", h3.Integral()/h.Integral()
	#print "2tag efficiency 1000", h3.Integral(h3.FindBin(800),h3.FindBin(1200))/h.Integral(h3.FindBin(800),h3.FindBin(1200))
	#print "2tag efficiency 2000", h3.Integral(h3.FindBin(1600),h3.FindBin(2400))/h.Integral(h3.FindBin(1600),h3.FindBin(2400))
    legend.SetTextSize(0.04)
    legend.SetFillStyle(0)
    legend.Draw("same")

    canvas.cd(2)
    #canvas.GetPad(2).SetLogy()
    legend2=TLegend(0.2,0.7,0.9,0.9,"")
    #same="A"
    same=""
    ratioplots=[]
    for i in range(len(samples)):
        weight=weights[i]
        try:
            href = TH1F(files[i].Get("cmgPFDiJetHistograms0tag/"+variable))
	except:
            href = TH1F(files[i].Get("cmgPFDiJetHistograms/"+variable))
	href.Scale(weight)
	rebin(href,variable)
	ratioplots+=[href]
        h2ref = TH1F(files[i].Get("cmgPFDiJetHistograms1tag/"+variable))
	h2ref.Scale(weight)
	rebin(h2ref,variable)
        #h2ref.Scale(0.5)
        h2 = TH1F(files[i].Get("cmgPFDiJetHistograms1tag/"+variable))
	h2.Scale(weight)
	rebin(h2,variable)
        #h2.Scale(0.5)
	#for b in range(h2.GetXaxis().GetNbins()):
	#    if h2.GetBinContent(b+1)>0 and h2.GetBinError(b+1)/h2.GetBinContent(b+1)>0.3:
	#        h2.SetBinContent(b+1,1)
	#        h2.SetBinError(b+1,1)
	#        href.SetBinContent(b+1,1)
	#        href.SetBinError(b+1,1)
	#h2=TGraphAsymmErrors(h2,href)
	#h2.Draw("lz"+same)
        h2.Divide(h2,href,1,1,'B')
	h2.Draw("hc"+same)
	h2.SetLineColor(colors[i])
	h2.SetMarkerColor(colors[i])
	#h2.SetFillColor(colors[i])
	h2.SetLineStyle(2)
	same="same"
	if variable=="mass":
            h2.GetXaxis().SetTitle("dijet mass [GeV]")
	    h2.GetXaxis().SetRangeUser(500,3000)
	if variable=="pt1":
            h2.GetXaxis().SetTitle("jet 1 p_T [GeV]")
	    h2.GetXaxis().SetRangeUser(0,1500)
	if variable=="mass1":
            h2.GetXaxis().SetTitle("jet 1 mass [GeV]")
	    h2.GetXaxis().SetRangeUser(0,200)
	h2.GetYaxis().SetTitle("Efficiency")
	h2.GetYaxis().SetRangeUser(0,1)
	h2.SetTitle("")
	h2.GetXaxis().SetTitleOffset(1.0)
	h2.GetYaxis().SetTitleOffset(1.4)
	h2.GetXaxis().SetLabelSize(0.05)
	h2.GetYaxis().SetLabelSize(0.05)
	h2.GetXaxis().SetTitleSize(0.06)
	h2.GetYaxis().SetTitleSize(0.06)
	hists+=[h2]
        legend2.AddEntry(h2,samples[i][2]+" 1tag / all","l")
        h3 = TH1F(files[i].Get("cmgPFDiJetHistograms2tag/"+variable))
	h3.Scale(weight)
	rebin(h3,variable)
	ratioplots+=[TH1F(h3)]
	
	h3ref=TH1F(h3)        
        h3ref.Divide(h3ref,href,1,1,'B')
        h2ref.Divide(h2ref,href,1,1,'B')
	h2ref.Add(h3ref)
        h3.Divide(h3,href,1,1,'B')
	h3.Scale(4)
	
	#for b in range(h3.GetXaxis().GetNbins()):
	#    if h3.GetBinContent(b+1)>0 and h3.GetBinError(b+1)/h3.GetBinContent(b+1)>0.3:
	#        h3.SetBinContent(b+1,1)
	#        h3.SetBinError(b+1,1)
	#        h2ref.SetBinContent(b+1,1)
	#        h2ref.SetBinError(b+1,1)
	#h3=TGraphAsymmErrors(h3,h2ref)
	#h3.Draw("lz"+same)
        h3.Divide(h3,h2ref,1,1,'B')
	
	h3.Add(h3ref,-1)
	
	h3.Draw("hc"+same)
	h3.SetLineColor(colors[i])
	h3.SetMarkerColor(colors[i])
	#h3.SetFillColor(colors[i])
	h3.SetLineStyle(3)
	h3.Draw("csame")
	hists+=[h3]
        legend2.AddEntry(h3,samples[i][2]+" 4 x 2tag/all / (1tag/all + 2tag/all) - 2tag/all","l")
        #legend2.AddEntry(h3,samples[i][2]+" 2tag / 1tag","l")
    legend2.SetTextSize(0.03)
    legend2.SetFillStyle(0)
    legend2.Draw("same")

#    canvas.cd(3)
#    #canvas.GetPad(3).SetLogy()
#    #h2=TGraphAsymmErrors(h2,href)
#    #h2.Draw("lz"+same)
#    ratioplots[0].Rebin(20)
#    ratioplots[1].Rebin(20)
#    ratioplots[2].Rebin(20)
#    ratioplots[3].Rebin(20)
#    ratioplots[0].Divide(ratioplots[1],ratioplots[0],1,1)
#    ratioplots[2].Divide(ratioplots[3],ratioplots[2],1,1)
#    for b in range(ratioplots[0].GetXaxis().GetNbins()):
#        if ratioplots[2].GetBinContent(b+1)==0:
#            continue
#        ratioplots[0].SetBinContent(b+1,ratioplots[0].GetBinContent(b+1)/sqrt(ratioplots[2].GetBinContent(b+1)))
#        ratioplots[0].SetBinError(b+1,ratioplots[0].GetBinError(b+1)/sqrt(ratioplots[2].GetBinContent(b+1)))
#    ratioplots[0].Draw("hc")
#    ratioplots[0].SetLineColor(1)
#    ratioplots[0].SetMarkerColor(1)
#    if variable=="mass":
#        ratioplots[0].GetXaxis().SetTitle("dijet mass [GeV]")
#	ratioplots[0].GetXaxis().SetRangeUser(500,3500)
#    if variable=="pt1":
#        ratioplots[0].GetXaxis().SetTitle("jet 1 p_T [GeV]")
#	ratioplots[0].GetXaxis().SetRangeUser(0,1500)
#    if variable=="mass1":
#        ratioplots[0].GetXaxis().SetTitle("jet 1 mass [GeV]")
#	ratioplots[0].GetXaxis().SetRangeUser(0,200)
#    ratioplots[0].GetYaxis().SetTitle("S_eff/sqrt(B_eff)")
#    ratioplots[0].GetYaxis().SetRangeUser(0,5)
#    ratioplots[0].SetTitle("")
#    ratioplots[0].GetXaxis().SetTitleOffset(1.0)
#    ratioplots[0].GetYaxis().SetTitleOffset(1.4)
#    ratioplots[0].GetXaxis().SetLabelSize(0.05)
#    ratioplots[0].GetYaxis().SetLabelSize(0.05)
#    ratioplots[0].GetXaxis().SetTitleSize(0.06)
#    ratioplots[0].GetYaxis().SetTitleSize(0.06)
#    hists+=[ratioplots[0]]

    canvas.SaveAs(prefix + '_dijet'+variable+'.root')
    canvas.SaveAs(prefix + '_dijet'+variable+'.pdf')
    canvas.SaveAs(prefix + '_dijet'+variable+'.eps')
    if wait:
        os.system("ghostview "+prefix + '_dijet'+variable+'.eps')

if __name__ == '__main__':

    wait=True

    samples=[
             #("diJetAnalysis"+algo+"_Histograms_WW.root",27.80,'WW'),
             ("diJetAnalysis"+algo+"_Histograms_QCD.root",3.326e-04*1e9*6e4,'QCD'),
             ("diJetAnalysis"+algo+"_Histograms_W1Jet.root",4480.,'W1jet'),
             #("diJetAnalysis"+algo+"_Histograms_graviton-ZZ-1000.root",40.3e-3*5.4,'G*->ZZ,1TeV'),
             #("diJetAnalysis"+algo+"_Histograms_graviton-WW-1000.root",80.5e-3*5.4,'G*->WW,1TeV'),
             #("diJetAnalysis"+algo+"_Histograms_graviton-ZZ-2000.root",1.16e-3*5.4/2.0,'G*->ZZ 2TeV'),
             #("diJetAnalysis"+algo+"_Histograms_graviton-WW-2000.root",2.34e-3*5.4/2.0,'G*->WW 2TeV'),
             #("diJetAnalysis"+algo+"_Histograms_Wprime-WZ-1000.root",1.021e-10*1e9,"W'->WZ 1TeV"),
             #("diJetAnalysis"+algo+"_Histograms_Wprime-WZ-2000.root",1.697e-12*1e9,"W'->WZ 2TeV"),
             #("diJetAnalysis"+algo+"_Histograms_qStar-qW-1000.root",1.696e-08*1e9,"q*->qW 1TeV"),
             #("diJetAnalysis"+algo+"_Histograms_qStar-qW-2000.root",1.653e-10*1e9,"q*->qW 2TeV"),
             #("diJetAnalysis"+algo+"_Histograms_qStar-qZ-1000.root",6.045e-09*1e9,"q*->qZ 1TeV"),
             #("diJetAnalysis"+algo+"_Histograms_qStar-qZ-2000.root",5.775e-11*1e9,"q*->qZ 2TeV"),
             #("diJetAnalysis"+algo+"_Histograms_Wfast.root",7.314e-05*1e9,'W'),
             #("diJetAnalysis"+algo+"_Histograms_QCDfast.root",3.326e-04*1e9,'QCD'),
             #("diJetAnalysis"+algo+"_Histograms_graviton-ZZ-1000.root",1.28e-10*1e9,'G*->ZZ,1TeV'),
             #("diJetAnalysis"+algo+"_Histograms_graviton-WW-1000.root",2.558e-10*1e9,'G*->WW,1TeV'),
             #("diJetAnalysis"+algo+"_Histograms_graviton-ZZ-2000.root",9.22e-13*1e9,'G*->ZZ 2TeV'),
             #("diJetAnalysis"+algo+"_Histograms_graviton-WW-2000.root",1.827e-12*1e9,'G*->WW 2TeV'),
         #("cmgtrees/pythia6_gravitonWW_500_tree_CMG.root",1.313e-08*1e9,'G*->WW,0.5TeV,0.1k/M'),
         #("cmgtrees/herwigpp_graviton_WW_500_tree_CMG.root",0.981*5.4*0.1/500*10000,'G*->WW,0.5TeV'),
         #("cmgtrees/herwigpp_graviton_WW_1000_tree_CMG.root",80.5e-03*5.4*0.1/1000*10000.,'G*->WW,1TeV'),
         #("cmgtrees/herwigpp_graviton_ZZ_1000_tree_CMG.root",40.3e-3,'H++ G*->ZZ,1TeV'),
         #("cmgtrees/herwigpp_graviton_ZZ_1000_noMPI_noHAD_noSHOWER_PFAOD.root",40.3e-3,'H++ G*->ZZ,1TeV'),
         #("cmgtrees/pythia6_gravitonZZ_500_tree_CMG.root",1.313e-08*1e9,'G*->ZZ 0.5 TeV,0.1k/M'),
         #("cmgtrees/pythia6_graviton_0.01_WW_1000_tree_CMG.root",2.573e-12*1e9,'G*->WW,1TeV,0.01k/M'),
         #("cmgtrees/pythia6_Wprime_WZ_500_tree_CMG.root",2.455e-09*1e9,"W'->WZ 0.5TeV"),
         #("cmgtrees/pythia6_Wprime_WZ_1000_tree_CMG.root",1.021e-10*1e9,"W'->WZ 1TeV"),
         #("cmgtrees/pythia6_Wprime_WZ_2000_tree_CMG.root",1.697e-12*1e9,"W'->WZ 2TeV"),
         #("cmgtrees/pythia6_WW_tree_CMG.root",2.780e-08*1e9,'WW'),
         #(sourceQCD.fileNames,3.326e-04*1e9*6e4,'QCDflat'),
         #(sourceW.fileNames,27770.0,'W'),
         #(sourceWW.fileNames,27.80,'WW'),
         #("/tmp/hinzmann/W_tree.root",27770.0,'W'),
         #("cmgtrees/LHE.root",0.43538820803E-02,'JHU G*->ZZ,1TeV'),
         ]
    weights=[]
    files=[]
    for sample,weight,name in samples:
        files+=[TFile.Open(sample)]
        nevents=files[-1].Get("baseMETHistograms/met").GetEntries()
        print sample,", number of events:",nevents
	weights+=[1000*weight/nevents] #/fb
        print [key.GetName() for key in files[-1].GetListOfKeys()]
	try:
            print [key.GetName() for key in files[-1].GetDirectory("cmgPFDiJetHistograms0tag").GetListOfKeys()]
        except:
            print [key.GetName() for key in files[-1].GetDirectory("cmgPFDiJetHistograms").GetListOfKeys()]

    plot(samples,weights,files,"mass")
    #plot(samples,weights,files,"mass1")
    #plot(samples,weights,files,"pt1")
