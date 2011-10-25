import os, sys
from ROOT import * 
from CMGTools.RootTools.RootTools import *

hists=[]

colors=[1,2,3,4,6,7,8,9,10,11,12,13,14]

def plotVariable(name,formula,labelx,labely,xbins,xmin,xmax,ymin=0,fitxmin=-1):
    print 'plotVariable:', name
    global hists
    legend=TLegend(0.5,0.6,0.9,0.9,"")
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
        events.Project(name+' '+str(i),formula,weight)
	if 'normalized'==labely:
	    hist.Scale(1./hist.Integral())
	hist.SetLineColor(colors[i])
        hist.Draw(options)
	if fitxmin>0 and labelx=='jet mass' and not 'G*' in samples[i][2]:
	    fit=TF1('fit '+str(i),'exp([0]+[1]*x)',fitxmin,xmax)
	    fit.SetLineWidth(1)
	    fit.SetLineColor(colors[i])
	    hist.Fit(fit,"RQ0")
	    fit.Draw('lsame')
	elif fitxmin>0 and labelx=='jet mass' and 'G*' in samples[i][2] and not (name=="mass2" and i==0):
	    fit=TF1('fit '+str(i),'[0]+[1]*x+[2]*exp(-0.5*((x-[3])/[4])**2)',65,95)
	    fit.SetParameter(0,0)
	    fit.SetParameter(1,0)
	    fit.SetParameter(2,1)
	    fit.SetParameter(3,80)
	    fit.SetParameter(4,5)
	    fit.SetLineWidth(1)
	    fit.SetLineColor(colors[i])
	    hist.Fit(fit,"R0")
	    fit.Draw('lsame')
	elif fitxmin>0 and labelx=='m_{12}' and 'G*' in samples[i][2] and i<2:
            if '0.5 TeV' in samples[i][2]:
	        m=350
	        mmin=200
	        mmax=500
            if '1 TeV' in samples[i][2]:
	        m=1000
	        mmin=900
	        mmax=1100
	    fit=TF1('fit '+str(i),'[0]+[1]*x+[2]*exp(-0.5*((x-[3])/[4])**2)',mmin,mmax)
	    fit.SetParameter(0,0)
	    fit.SetParameter(1,0)
	    fit.SetParameter(2,1)
	    fit.SetParameter(3,m)
	    fit.SetParameter(4,(mmax-mmin)/2)
	    fit.SetLineWidth(1)
	    fit.SetLineColor(colors[i])
	    hist.Fit(fit,"R0")
	    fit.Draw('lsame')
	elif fitxmin>0 and not 'G*' in samples[i][2]:
	    fit=TF1('fit '+str(i),'[0]*pow(x,[1])',fitxmin,xmax)
	    fit.SetLineWidth(1)
	    fit.SetLineColor(colors[i])
	    hist.Fit(fit,"RQ0")
	    fit.Draw('lsame')
        hists+=[hist]
	if i==0:
            firsthist=hist
	ymax=max(ymax,hist.GetMaximum())
	if ymin>0:
            firsthist.GetYaxis().SetRangeUser(ymin,ymax*3.0)
	else:
            firsthist.GetYaxis().SetRangeUser(ymin,ymax*1.1)
        legend.AddEntry(hist,samples[i][2],"l")
    legend.SetTextSize(0.05)
    legend.SetFillStyle(0)
    legend.Draw("same")
    hists+=[legend]
    
def plotKinematics(): 
    print 'plotKinematics'

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    canvas.GetPad(1).SetLogy()
    plotVariable('mass','mjj', 'm_{jj}','N / fb',50,0,3000,0.1,240)
    canvas.cd(2)
    plotVariable('seta','jet.obj[0].eta()+jet.obj[1].eta()', '#eta_{1}+#eta_{2}','normalized',20,-5,5)
    canvas.cd(3)
    plotVariable('deta','abs(jet.obj[0].eta()-jet.obj[1].eta())', '|#eta_{1}-#eta_{2}|','normalized',20,0,5)
    canvas.cd(4)
    plotVariable('dphi','fabs(fmod(jet.obj[0].phi()-jet.obj[1].phi()+3.0*pi,2.0*pi)-pi)', '|#phi_{1}-#phi_{2}|','normalized',20,0,3.1416)
    canvas.SaveAs(prefix + '_dijet.pdf')
    canvas.SaveAs(prefix + '_dijet.eps')
    os.system("ghostview "+prefix + '_dijet.eps')

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    canvas.GetPad(1).SetLogy()
    plotVariable('mass1','jet.obj[0].mass()', 'jet mass','N / fb',60,0,200,0.01,14)
    canvas.cd(2)
    canvas.GetPad(2).SetLogy()
    plotVariable('mass2','jet.obj[1].mass()', 'jet mass','N / fb',60,0,200,0.01,12)
    canvas.cd(3)
    canvas.GetPad(3).SetLogy()
    plotVariable('mass3','jet.obj[2].mass()', 'jet mass','N / fb',60,0,200,0.01)
    canvas.cd(4)
    canvas.GetPad(4).SetLogy()
    plotVariable('mass4','jet.obj[3].mass()', 'jet mass','N / fb',60,0,200,0.01)
    canvas.SaveAs(prefix + '_mass.pdf')
    canvas.SaveAs(prefix + '_mass.eps')
    os.system("ghostview "+prefix + '_mass.eps')

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    canvas.GetPad(1).SetLogy()
    plotVariable('pT1','jet.obj[0].pt()', 'p_{T} (GeV)','N / fb',100,0,1500,0.001,110)
    canvas.cd(2)
    canvas.GetPad(2).SetLogy()
    plotVariable('pT2','jet.obj[1].pt()', 'p_{T} (GeV)','N / fb',100,0,1500,0.001,90)
    canvas.cd(3)
    canvas.GetPad(3).SetLogy()
    plotVariable('pT3','jet.obj[2].pt()', 'p_{T} (GeV)','N / fb',100,0,1500,0.001)
    canvas.cd(4)
    canvas.GetPad(4).SetLogy()
    plotVariable('pT4','jet.obj[3].pt()', 'p_{T} (GeV)','N / fb',100,0,1500,0.001)
    canvas.SaveAs(prefix + '_pT.pdf')
    canvas.SaveAs(prefix + '_pT.eps')
    os.system("ghostview "+prefix + '_pT.eps')

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    plotVariable('eta1','jet.obj[0].eta()', '#eta','normalized',30,-5,5)
    canvas.cd(2)
    plotVariable('eta2','jet.obj[1].eta()', '#eta','normalized',30,-5,5)
    canvas.cd(3)
    plotVariable('eta3','jet.obj[2].eta()', '#eta','normalized',30,-5,5)
    canvas.cd(4)
    plotVariable('eta4','jet.obj[3].eta()', '#eta','normalized',30,-5,5)
    canvas.SaveAs(prefix + '_eta.pdf')
    canvas.SaveAs(prefix + '_eta.eps')
    os.system("ghostview "+prefix + '_eta.eps')

    print 'end'

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

#jets = 'cmgPFJets_cmgPFJetSel__PAT'
jets = 'cmgBaseJets_cmgPFBaseJetSel__PAT'
cuts = '(1)'
cuts += '*(jet.obj[0].pt()>100)'
#cuts += '*(jet.obj[1].pt()>100)'
#cuts += '*(mjj>500)'
#cuts += '*(jet.obj[0].mass()>50)'
#cuts += '*(jet.obj[0].mass()<200)'
#cuts += '*(jet.obj[1].mass()>50)'

samples=[("pythia6_gravitonWW_500_tree_CMG.root",1.313e-08*1e9,'G*->WW 0.5 TeV'),
         #("pythia6_gravitonZZ_500_tree_CMG.root",1.313e-08*1e9,'G*->ZZ 0.5 TeV'),
         ("pythia6_gravitonWW_1000_tree_CMG.root",2.558e-10*1e9,'G*->WW 1 TeV'),
         #("pythia6_gravitonZZ_1000_tree_CMG.root",2.558e-10*1e9,'G*->ZZ 1 TeV'),
         #("pythia6_gravitonWW_2000_tree_CMG.root",1.827e-12*1e9,'G*->WW 2 TeV'),
         #("pythia6_gravitonZZ_2000_tree_CMG.root",1.827e-12*1e9,'G*->ZZ 2 TeV'),
         ("pythia6_WW_tree_CMG.root",2.780e-08*1e9,'WW'),
         ("pythia6_W_tree_CMG.root",7.314e-05*1e9,'W'),
         ("pythia6_QCD_tree_CMG.root",3.326e-04*1e9,'QCD'),
         ]
weights=[]
trees=[]
for sample,weight,name in samples:
    trees+=[Chain('Events', sample)]
    nevents=trees[-1].GetEntries()
    print sample,", number of events:",nevents
    weights+=[str(weight/nevents*1000)+'*'+cuts]
    trees[-1].SetAlias('jet', jets)
    trees[-1].SetAlias('mjj','sqrt(pow(jet.obj[0].energy()+jet.obj[1].energy(),2)-pow(jet.obj[0].px()+jet.obj[1].px(),2)-pow(jet.obj[0].py()+jet.obj[1].py(),2)-pow(jet.obj[0].pz()+jet.obj[1].pz(),2))')
    
prefix = "gravitonWW"

if __name__ == '__main__':
    plotKinematics()
