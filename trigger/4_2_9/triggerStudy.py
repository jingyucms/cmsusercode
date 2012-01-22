import os, sys
from ROOT import * 

hists=[]
colors=[1,2,3,4,6,7,8,9,10,11,12,13,14]
ymin=0.001

def plotEfficiency(name,formula,labelx,labely,xbins,xmin,xmax,ymin=0):
    print 'plotEfficiency:', name
    global hists
    legend=TLegend(0.7,0.6,0.9,0.9,"")
    firsthist=None
    ymax=0
    for i in range(len(samples)):
        print i
        weight=str(weights[i])
        weight0tag=weight
        weight1tag=weight+'*trigger'
	events=trees[i]
        hist1 = TH1F(name+' '+str(i)+'1tag',';'+labelx+';'+'efficiency',xbins,xmin,xmax)
	hist1.Sumw2()
        events.Project(name+' '+str(i)+'1tag',formula,weight1tag)
	hist1.SetLineColor(colors[i])
        hists+=[hist1]
        hist1_ref = TH1F(name+' '+str(i)+'ref1',';'+labelx+';'+'efficiency',xbins,xmin,xmax)
	hist1_ref.Sumw2()
        events.Project(name+' '+str(i)+'ref1',formula,weight0tag)
        hist1.Divide(hist1,hist1_ref,1,1,'B')
        options='le'
	if i>0: options+='same'
        hist1.Draw(options)
	if i==0:
            firsthist=hist1
            firsthist.GetYaxis().SetRangeUser(0,1)
        legend.AddEntry(hist1,samples[i][2]+' trigger',"l")
    legend.SetTextSize(0.04)
    legend.SetFillStyle(0)
    legend.Draw("same")
    hists+=[legend]
    
def plotVariable(name,formula,labelx,labely,xbins,xmin,xmax,ymin=0,fitxmin=-1):
    print 'plotVariable:', name
    global hists
    legend=TLegend(0.7,0.6,0.9,0.9,"")
    firsthist=None
    ymax=0
    for i in range(len(samples)):
        print i
        weight=str(weights[i])
	events=trees[i]
        options='le'
	if i>0: options+='same'
        hist = TH1F(name+' '+str(i),';'+labelx+';'+labely,xbins,xmin,xmax)
	hist.Sumw2()
        form=formula
        events.Project(name+' '+str(i),form,weight)
	if 'normalized'==labely and hist.Integral()>0:
	    hist.Scale(1./hist.Integral())
	hist.SetLineColor(colors[i])
        hist.Draw(options)
        hists+=[hist]
	if i==0:
            firsthist=hist
	ymax=max(ymax,hist.GetMaximum())
	if ymin>0:
            firsthist.GetYaxis().SetRangeUser(ymin,ymax*3.0)
	else:
            firsthist.GetYaxis().SetRangeUser(ymin,ymax*1.1)
        legend.AddEntry(hist,samples[i][2],"l")
    legend.SetTextSize(0.04)
    legend.SetFillStyle(0)
    legend.Draw("same")
    hists+=[legend]
    
def plotTriggerEfficiency():
    print 'plotTriggerEfficiency'

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    plotVariable('pt','tau.obj[0].pt()', 'tau pt','N',50,0,100)
    canvas.cd(2)
    plotEfficiency('pteff','tau.obj[0].pt()', 'tau pt','N',50,0,100)
    canvas.cd(3)
    canvas.cd(4)
    canvas.SaveAs(prefix + '_pt.root')
    canvas.SaveAs(prefix + '_pt.pdf')
    canvas.SaveAs(prefix + '_pt.eps')
    if wait:
        os.system("ghostview "+prefix + '_pt.eps')

gROOT.Macro( os.path.expanduser( '~/rootlogon.C' ) )
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

wait=True

taus = 'recoPFTaus_offlineSelectedPFTausLooseIsoTrackFinding__TEST'
cuts = '(1)'
trigger = '(1)'

samples=[(["trigger_study.root"],1,'CMSSW_4_2_9_HLT3_hltpatch2/RelValZTT/GEN-SIM-RECO/START42_V15B_PU_E7TeV_Ave18p4_50ns_special_111004-v1'),
         ]
trees=[]
weights=[]
for sample,weight,name in samples:
    trees+=[TChain('Events')]
    for f in sample:
        trees[-1].Add(f)
    nevents=trees[-1].GetEntries()
    print sample,", number of events:",nevents
    weights+=[str(weight/nevents)+'*'+cuts]
    trees[-1].SetAlias('tau', taus)
    trees[-1].SetAlias('trigger', trigger)

prefix = "plots/tau_isolation"

if __name__ == '__main__':
    plotTriggerEfficiency()
