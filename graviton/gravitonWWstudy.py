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
	if 'normalized'==labely and hist.Integral()>0:
	    hist.Scale(1./hist.Integral())
	hist.SetLineColor(colors[i])
        hist.Draw(options)
	if fitxmin>0 and labelx=='jet mass' and not 'G*' in samples[i][2] and not 'WW' in samples[i][2]:
	    fit=TF1('fit '+str(i),'exp([0]+[1]*x+[2]*x*x)',fitxmin,xmax)
	    fit.SetLineWidth(1)
	    fit.SetLineColor(colors[i])
	    hist.Fit(fit,"RQ0")
	    #fit.Draw('lsame')
	elif fitxmin>0 and labelx=='jet mass' and ('G*' in samples[i][2] or 'WW' in samples[i][2]) and not (name=="mass2" and i==0):
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
	    #fit.Draw('lsame')
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

    ymin=0.001

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    canvas.GetPad(1).SetLogy()
    plotVariable('subjet1pt1','subjet1pt1', 'subjet 1 p_{T} 1','d#sigma / fb',60,0,200,ymin)
    canvas.cd(2)
    canvas.GetPad(2).SetLogy()
    plotVariable('subjet1pt2','subjet1pt2', 'subjet 1 p_{T} 2','d#sigma / fb',60,0,200,ymin)
    canvas.cd(3)
    plotVariable('subjet1seta','subjet1seta', 'subjet 1 #eta_{1}+#eta_{2}','normalized',20,-5,5)
    canvas.cd(4)
    plotVariable('subjet1deta','subjet1deta', 'subjet 1 |#eta_{1}-#eta_{2}|','normalized',20,0,5)
    canvas.SaveAs(prefix + '_subdijet.pdf')
    canvas.SaveAs(prefix + '_subdijet.eps')
    if wait:
        os.system("ghostview "+prefix + '_subdijet.eps')

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    canvas.GetPad(1).SetLogy()
    plotVariable('mass','mjj', 'm_{jj}','d#sigma / fb',50,0,3000,0.1,240)
    canvas.cd(2)
    plotVariable('seta','seta', '#eta_{1}+#eta_{2}','normalized',20,-5,5)
    canvas.cd(3)
    plotVariable('deta','deta', '|#eta_{1}-#eta_{2}|','normalized',20,0,5)
    canvas.cd(4)
    plotVariable('dphi','fabs(fmod(jet.obj['+object1+'].phi()-jet.obj['+object2+'].phi()+3.0*pi,2.0*pi)-pi)', '|#phi_{1}-#phi_{2}|','normalized',20,0,3.1416)
    canvas.SaveAs(prefix + '_dijet.pdf')
    canvas.SaveAs(prefix + '_dijet.eps')
    if wait:
        os.system("ghostview "+prefix + '_dijet.eps')

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    canvas.GetPad(1).SetLogy()
    plotVariable('subjetmass1','prunedjet.obj['+object1+'].subjets_[0].mass()', 'subjet 1 mass','d#sigma / fb',60,0,200,ymin)
    canvas.cd(2)
    canvas.GetPad(2).SetLogy()
    plotVariable('subjetmass2','prunedjet.obj['+object2+'].subjets_[0].mass()', 'subjet 2 mass','d#sigma / fb',60,0,200,ymin)
    canvas.cd(3)
    canvas.GetPad(3).SetLogy()
    plotVariable('massdrop1','massdrop1', 'jet 1 mass drop','d#sigma / fb',30,0,1,ymin)
    canvas.cd(4)
    canvas.GetPad(4).SetLogy()
    plotVariable('massdrop2','massdrop2', 'jet 2 mass drop','d#sigma / fb',30,0,1,ymin)
    canvas.SaveAs(prefix + '_massdrop.pdf')
    canvas.SaveAs(prefix + '_massdrop.eps')
    if wait:
        os.system("ghostview "+prefix + '_massdrop.eps')

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    canvas.GetPad(1).SetLogy()
    plotVariable('mass1','jet.obj['+object1+'].mass()', 'jet 1 mass','d#sigma / fb',60,0,200,ymin,14)
    canvas.cd(2)
    canvas.GetPad(2).SetLogy()
    plotVariable('mass2','jet.obj['+object2+'].mass()', 'jet 2 mass','d#sigma / fb',60,0,200,ymin,12)
    canvas.cd(3)
    canvas.GetPad(3).SetLogy()
    plotVariable('mass3','prunedjet.obj['+object1+'].mass()', 'pruned jet 1 mass','d#sigma / fb',60,0,200,ymin)
    canvas.cd(4)
    canvas.GetPad(4).SetLogy()
    plotVariable('mass4','prunedjet.obj['+object2+'].mass()', 'pruned jet 2 mass','d#sigma / fb',60,0,200,ymin)
    canvas.SaveAs(prefix + '_mass.pdf')
    canvas.SaveAs(prefix + '_mass.eps')
    if wait:
        os.system("ghostview "+prefix + '_mass.eps')

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    canvas.GetPad(1).SetLogy()
    plotVariable('prunedmass1','jet.obj['+object1+'].mass()-prunedjet.obj['+object1+'].mass()', 'jet 1 pruned mass','d#sigma / fb',60,0,200,ymin)
    canvas.cd(2)
    canvas.GetPad(2).SetLogy()
    plotVariable('prunedmass2','jet.obj['+object2+'].mass()-prunedjet.obj['+object2+'].mass()', 'jet 2 pruned mass','d#sigma / fb',60,0,200,ymin)
    canvas.cd(3)
    canvas.GetPad(3).SetLogy()
    plotVariable('subjets1','nsubjets1', 'jet 1 subjets','d#sigma / fb',3,-0.5,2.5,ymin)
    canvas.cd(4)
    canvas.GetPad(4).SetLogy()
    plotVariable('subjets2','nsubjets2', 'jet 2 subjets','d#sigma / fb',3,-0.5,2.5,ymin)
    canvas.SaveAs(prefix + '_subjets.pdf')
    canvas.SaveAs(prefix + '_subjets.eps')
    if wait:
        os.system("ghostview "+prefix + '_subjets.eps')

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    canvas.GetPad(1).SetLogy()
    plotVariable('pT1','jet.obj['+object1+'].pt()', 'p_{T} 1 (GeV)','d#sigma / fb',100,0,1500,0.001,110)
    canvas.cd(2)
    canvas.GetPad(2).SetLogy()
    plotVariable('pT2','jet.obj['+object2+'].pt()', 'p_{T} 2 (GeV)','d#sigma / fb',100,0,1500,0.001,90)
    canvas.cd(3)
    canvas.GetPad(3).SetLogy()
    plotVariable('pT3','jet.obj[2].pt()', 'p_{T} 3 (GeV)','d#sigma / fb',100,0,1500,0.001)
    canvas.cd(4)
    canvas.GetPad(4).SetLogy()
    plotVariable('pT4','jet.obj[3].pt()', 'p_{T} 4 (GeV)','d#sigma / fb',100,0,1500,0.001)
    canvas.SaveAs(prefix + '_pT.pdf')
    canvas.SaveAs(prefix + '_pT.eps')
    if wait:
        os.system("ghostview "+prefix + '_pT.eps')

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    plotVariable('eta1','jet.obj['+object1+'].eta()', '#eta 1','normalized',30,-5,5)
    canvas.cd(2)
    plotVariable('eta2','jet.obj['+object2+'].eta()', '#eta 2','normalized',30,-5,5)
    canvas.cd(3)
    plotVariable('eta3','jet.obj[2].eta()', '#eta 3','normalized',30,-5,5)
    canvas.cd(4)
    plotVariable('eta4','jet.obj[3].eta()', '#eta 4','normalized',30,-5,5)
    canvas.SaveAs(prefix + '_eta.pdf')
    canvas.SaveAs(prefix + '_eta.eps')
    if wait:
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
#jets = 'cmgBaseJets_cmgPFBaseJetSel__PAT'
#jets = 'recoGenParticles_genParticlesStatus3__PAT'
jets = 'cmgBaseJets_cmgPFBaseJetSelCA8CMG__PAT'
prunedjets = 'cmgBaseJets_cmgPFBaseJetSelCA8PrunedCMG__PAT'
object1 = '0'#'7'
object2 = '1'#'8'
cuts = '(1)'
cuts += '*(jet.obj['+object1+'].pt()>100)'
#cuts += '*(jet.obj['+object2+'].pt()>100)'
#cuts += '*(jet.obj['+object1+'].mass()>80)'
#cuts += '*(jet.obj['+object2+'].mass()>80)'
#cuts += '*(mjj>200)'
#cuts += '*(deta<1.3)'
#cuts += '*(abs(jet.obj['+object1+'].eta())<2.5)'
#cuts += '*(abs(jet.obj['+object2+'].eta())<2.5)'
#cuts += '*(prunedjet.obj['+object1+'].mass()>80)'
#cuts += '*(prunedjet.obj['+object2+'].mass()>80)'
#cuts += '*(massdrop1<0.25)'
#cuts += '*(massdrop2<0.25)'
cuts += '*(nsubjets1==2)'
cuts += '*(nsubjets2==2)'

samples=[("pythia6_gravitonWW_1000_tree_CMG.root",2.558e-10*1e9,'G*->WW,1TeV,0.1k/M'),
         #("cmgtrees/pythia6_gravitonWW_500_tree_CMG.root",1.313e-08*1e9,'G*->WW,0.5TeV,0.1k/M'),
         #("cmgtrees/pythia6_gravitonWW_1000_tree_CMG.root",2.558e-10*1e9,'G*->WW,1TeV,0.1k/M'),
         #("cmgtrees/pythia6_gravitonWW_2000_tree_CMG.root",1.827e-12*1e9,'G*->WW 2 TeV'),
         #("cmgtrees/herwigpp_graviton_WW_500_tree_CMG.root",0.981,'G*->WW,0.5TeV'),
         #("cmgtrees/herwigpp_graviton_WW_1000_tree_CMG.root",80.5e-03,'G*->WW,1TeV'),
         #("cmgtrees/pythia6_gravitonZZ_500_tree_CMG.root",1.313e-08*1e9,'G*->ZZ 0.5 TeV,0.1k/M'),
         #("cmgtrees/pythia6_graviton_0.01_WW_1000_tree_CMG.root",2.573e-12*1e9,'G*->WW,1TeV,0.01k/M'),
         #("cmgtrees/pythia6_gravitonZZ_1000_tree_CMG.root",2.558e-10*1e9,'G*->ZZ 1 TeV'),
         #("cmgtrees/pythia6_gravitonZZ_2000_tree_CMG.root",1.827e-12*1e9,'G*->ZZ 2 TeV'),
         #("cmgtrees/pythia6_Wprime_WZ_500_tree_CMG.root",2.455e-09*1e9,"W'->WZ 0.5TeV"),
         #("cmgtrees/pythia6_Wprime_WZ_1000_tree_CMG.root",1.021e-10*1e9,"W'->WZ 1TeV"),
         #("cmgtrees/pythia6_Wprime_WZ_2000_tree_CMG.root",1.697e-12*1e9,"W'->WZ 2TeV"),
         #("cmgtrees/pythia6_WW_tree_CMG.root",2.780e-08*1e9,'WW'),
         #("cmgtrees/pythia6_W_tree_CMG.root",7.314e-05*1e9,'W'),
         #("cmgtrees/pythia6_QCD_tree_CMG.root",3.326e-04*1e9,'QCD'),
         ]
weights=[]
trees=[]
wait=True
for sample,weight,name in samples:
    trees+=[Chain('Events', sample)]
    nevents=trees[-1].GetEntries()
    print sample,", number of events:",nevents
    weights+=[str(weight/nevents*1000)+'*'+cuts]
    trees[-1].SetAlias('jet', jets)
    trees[-1].SetAlias('prunedjet', prunedjets)
    trees[-1].SetAlias('mjj','sqrt(pow(jet.obj['+object1+'].energy()+jet.obj['+object2+'].energy(),2)-pow(jet.obj['+object1+'].px()+jet.obj['+object2+'].px(),2)-pow(jet.obj['+object1+'].py()+jet.obj['+object2+'].py(),2)-pow(jet.obj['+object1+'].pz()+jet.obj['+object2+'].pz(),2))')
    trees[-1].SetAlias('nsubjets1','prunedjet.obj['+object1+'].@subjets_.size()')
    trees[-1].SetAlias('nsubjets2','prunedjet.obj['+object2+'].@subjets_.size()')
    trees[-1].SetAlias('massdrop1','(prunedjet.obj['+object1+'].subjets_[0].mass()/prunedjet.obj['+object1+'].mass())')
    trees[-1].SetAlias('massdrop2','(prunedjet.obj['+object2+'].subjets_[0].mass()/prunedjet.obj['+object2+'].mass())')
    trees[-1].SetAlias('seta','(jet.obj['+object1+'].eta()+jet.obj['+object2+'].eta())')
    trees[-1].SetAlias('deta','abs(jet.obj['+object1+'].eta()-jet.obj['+object2+'].eta())')
    trees[-1].SetAlias('subjet1pt1','prunedjet.obj['+object1+'].subjetsBoosted_[0].pt()')
    trees[-1].SetAlias('subjet1pt2','prunedjet.obj['+object1+'].subjetsBoosted_[1].pt()')
    trees[-1].SetAlias('subjet1seta','(prunedjet.obj['+object1+'].subjetsBoosted_[0].eta()+prunedjet.obj['+object1+'].subjetsBoosted_[1].eta())')
    trees[-1].SetAlias('subjet1deta','abs(prunedjet.obj['+object1+'].subjetsBoosted_[0].eta()-prunedjet.obj['+object1+'].subjetsBoosted_[1].eta())')

prefix = "plots/feasibility111109_gravitonWW_nsubjets2"

if __name__ == '__main__':
    plotKinematics()
