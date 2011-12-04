import os, sys
from ROOT import * 
from CMGTools.RootTools.RootTools import *

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
	if doSemileptonic:
            weight0tag=weight
            weight1tag=weight+'*tag1'
        else:
            weight0tag=weight+'*(!tag1tag2)'
            weight1tag=weight+'*((tag1notag2+notag1tag2)>0)'
            weight2tag=weight+'*tag1tag2'
	events=trees[i]
        hist1 = TH1F(name+' '+str(i)+'1tag',';'+labelx+';'+'efficiency',xbins,xmin,xmax)
	hist1.Sumw2()
        events.Project(name+' '+str(i)+'1tag',formula,weight1tag)
	hist1.SetLineColor(colors[i])
        hists+=[hist1]
	if not doSemileptonic:
            hist2 = TH1F(name+' '+str(i)+'2tag',';'+labelx+';'+'efficiency',xbins,xmin,xmax)
            hist2.Sumw2()
            events.Project(name+' '+str(i)+'2tag',formula,weight2tag)
            hist2.SetLineColor(colors[i])
            hist2.SetLineStyle(3)
            hists+=[hist2]
        hist1_ref = TH1F(name+' '+str(i)+'ref1',';'+labelx+';'+'efficiency',xbins,xmin,xmax)
	hist1_ref.Sumw2()
        events.Project(name+' '+str(i)+'ref1',formula,weight0tag)
        hist2_ref = TH1F(name+' '+str(i)+'ref2',';'+labelx+';'+'efficiency',xbins,xmin,xmax)
	hist2_ref.Sumw2()
        events.Project(name+' '+str(i)+'ref2',formula,weight1tag)
        hist1.Divide(hist1,hist1_ref,1,1,'B')
        options='le'
	if i>0: options+='same'
        hist1.Draw(options)
	if not doSemileptonic:
            hist2.Divide(hist2,hist2_ref,1,1,'B')
            if i==0: options+='same'
            hist2.Draw(options)
	if i==0:
            firsthist=hist1
            firsthist.GetYaxis().SetRangeUser(0,1)
        legend.AddEntry(hist1,samples[i][2]+' 1-tag',"l")
	if not doSemileptonic:
            legend.AddEntry(hist2,samples[i][2]+' 2-tag',"l")
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
	if doGenLevel:
	    if 'JHU' in samples[i][2]:# or 'H++' in samples[i][2]:
	        form=formula.replace('gen.','gen2.')
	    else:
	        form=formula.replace('gen.','gen1.')
	    if 'H++' in samples[i][2]:
	        #form=form.replace('[7]','[5]')
	        #form=form.replace('[8]','[6]')
	        form=form.replace('[9]','[14]')
	        form=form.replace('[10]','[15]')
	        form=form.replace('[11]','[17]')
	        form=form.replace('[12]','[18]')
	else:
	    form=formula
        events.Project(name+' '+str(i),form,weight)
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
    legend.SetTextSize(0.04)
    legend.SetFillStyle(0)
    legend.Draw("same")
    hists+=[legend]
    
def plotDijetKinematics():
    print 'plotDijetKinematics'

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
    plotVariable('dphi','fabs(fmod(jet.obj[0].phi()-jet.obj[1].phi()+3.0*pi,2.0*pi)-pi)', '|#phi_{1}-#phi_{2}|','normalized',20,0,3.1416)
    canvas.SaveAs(prefix + '_dijet.root')
    canvas.SaveAs(prefix + '_dijet.pdf')
    canvas.SaveAs(prefix + '_dijet.eps')
    if wait:
        os.system("ghostview "+prefix + '_dijet.eps')

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    plotVariable('eta1','jet.obj[0].eta()', '#eta 1','normalized',30,-5,5)
    canvas.cd(2)
    plotVariable('eta2','jet.obj[1].eta()', '#eta 2','normalized',30,-5,5)
    canvas.cd(3)
    plotVariable('eta3','jet.obj[2].eta()', '#eta 3','normalized',30,-5,5)
    canvas.cd(4)
    plotVariable('eta4','jet.obj[3].eta()', '#eta 4','normalized',30,-5,5)
    canvas.SaveAs(prefix + '_eta.root')
    canvas.SaveAs(prefix + '_eta.pdf')
    canvas.SaveAs(prefix + '_eta.eps')
    if wait:
        os.system("ghostview "+prefix + '_eta.eps')

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    canvas.GetPad(1).SetLogy()
    plotVariable('pT1','jet.obj[0].pt()', 'p_{T} 1 (GeV)','d#sigma / fb',100,0,1500,0.001,110)
    canvas.cd(2)
    canvas.GetPad(2).SetLogy()
    plotVariable('pT2','jet.obj[1].pt()', 'p_{T} 2 (GeV)','d#sigma / fb',100,0,1500,0.001,90)
    canvas.cd(3)
    canvas.GetPad(3).SetLogy()
    plotVariable('pT3','jet.obj[2].pt()', 'p_{T} 3 (GeV)','d#sigma / fb',100,0,1500,0.001)
    canvas.cd(4)
    canvas.GetPad(4).SetLogy()
    plotVariable('pT4','jet.obj[3].pt()', 'p_{T} 4 (GeV)','d#sigma / fb',100,0,1500,0.001)
    canvas.SaveAs(prefix + '_pT.root')
    canvas.SaveAs(prefix + '_pT.pdf')
    canvas.SaveAs(prefix + '_pT.eps')
    if wait:
        os.system("ghostview "+prefix + '_pT.eps')

def plotSubjetKinematics():
    print 'plotSubjetKinematics'

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    canvas.GetPad(1).SetLogy()
    plotVariable('mass1','jet.obj[0].mass()', 'jet 1 mass','d#sigma / fb',60,0,200,ymin,14)
    canvas.cd(2)
    canvas.GetPad(2).SetLogy()
    plotVariable('mass2','jet.obj[1].mass()', 'jet 2 mass','d#sigma / fb',60,0,200,ymin,12)
    canvas.cd(3)
    canvas.GetPad(3).SetLogy()
    plotVariable('mass3','prunedjet.obj[0].mass()', 'pruned jet 1 mass','d#sigma / fb',60,0,200,ymin)
    canvas.cd(4)
    canvas.GetPad(4).SetLogy()
    plotVariable('mass4','prunedjet.obj[1].mass()', 'pruned jet 2 mass','d#sigma / fb',60,0,200,ymin)
    canvas.SaveAs(prefix + '_mass.root')
    canvas.SaveAs(prefix + '_mass.pdf')
    canvas.SaveAs(prefix + '_mass.eps')
    if wait:
        os.system("ghostview "+prefix + '_mass.eps')

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    canvas.GetPad(1).SetLogy()
    plotVariable('prunedmass1','jet.obj[0].mass()-prunedjet.obj[0].mass()', 'jet 1 pruned mass','d#sigma / fb',60,0,200,ymin)
    canvas.cd(2)
    canvas.GetPad(2).SetLogy()
    plotVariable('prunedmass2','jet.obj[1].mass()-prunedjet.obj[1].mass()', 'jet 2 pruned mass','d#sigma / fb',60,0,200,ymin)
    canvas.cd(3)
    plotVariable('subjets1','nsubjets1', 'jet 1 subjets','normalized',3,-0.5,2.5)
    canvas.cd(4)
    plotVariable('subjets2','nsubjets2', 'jet 2 subjets','normalized',3,-0.5,2.5)
    canvas.SaveAs(prefix + '_subjets.root')
    canvas.SaveAs(prefix + '_subjets.pdf')
    canvas.SaveAs(prefix + '_subjets.eps')
    if wait:
        os.system("ghostview "+prefix + '_subjets.eps')

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    canvas.GetPad(1).SetLogy()
    plotVariable('subjetmass1','prunedjet.obj[0].subjets_[0].mass()', 'subjet 1 mass','d#sigma / fb',60,0,200,ymin)
    canvas.cd(2)
    canvas.GetPad(2).SetLogy()
    plotVariable('subjetmass2','prunedjet.obj[1].subjets_[0].mass()', 'subjet 2 mass','d#sigma / fb',60,0,200,ymin)
    canvas.cd(3)
    canvas.GetPad(3).SetLogy()
    plotVariable('massdrop1','massdrop1', 'jet 1 mass drop','normalized',30,0,1,ymin)
    canvas.cd(4)
    canvas.GetPad(4).SetLogy()
    plotVariable('massdrop2','massdrop2', 'jet 2 mass drop','normalized',30,0,1,ymin)
    canvas.SaveAs(prefix + '_massdrop.root')
    canvas.SaveAs(prefix + '_massdrop.pdf')
    canvas.SaveAs(prefix + '_massdrop.eps')
    if wait:
        os.system("ghostview "+prefix + '_massdrop.eps')

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    canvas.GetPad(1).SetLogy()
    plotVariable('subjet1pt1','subjet1pt1', 'subjet p_{T} 1','normalized',60,0,200,ymin)
    canvas.cd(2)
    canvas.GetPad(2).SetLogy()
    plotVariable('subjet1pt2','subjet1pt2', 'subjet p_{T} 2','normalized',60,0,200,ymin)
    canvas.cd(3)
    plotVariable('subjet1dpt','subjet1dpt', 'subjet dp_{T}','normalized',60,0,200,ymin)
    canvas.cd(4)
    plotVariable('subjet1theta','subjet1theta', 'subjet #theta','normalized',20,-3.1416,3.1416)
    canvas.SaveAs(prefix + '_subdijet.root')
    canvas.SaveAs(prefix + '_subdijet.pdf')
    canvas.SaveAs(prefix + '_subdijet.eps')
    if wait:
        os.system("ghostview "+prefix + '_subdijet.eps')

def plotSemileptonicKinematics():
    print 'plotSemileptonicKinematics'

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    canvas.GetPad(1).SetLogy()
    plotVariable('pTW','Wpt', 'W p_{T} (GeV)','d#sigma / fb',100,0,1500,0.001)
    canvas.cd(2)
    canvas.GetPad(2).SetLogy()
    plotVariable('mTW','Wmt', 'W m_{T} (GeV)','d#sigma / fb',100,0,500,0.001)
    canvas.cd(3)
    canvas.GetPad(3).SetLogy()
    plotVariable('dptW','dptW', '|W p_{T} - jet p_{T}| (GeV)','d#sigma / fb',100,0,500,0.001)
    canvas.cd(4)
    plotVariable('dphiW','dphiW', '|#phi_{1}-#phi_{2}|','normalized',20,0,3.1416)
    canvas.SaveAs(prefix + '_Ws.root')
    canvas.SaveAs(prefix + '_Ws.pdf')
    canvas.SaveAs(prefix + '_Ws.eps')
    if wait:
        os.system("ghostview "+prefix + '_Ws.eps')

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    canvas.GetPad(1).SetLogy()
    plotVariable('pT1','jet.obj[0].pt()', 'jet 1 p_{T} (GeV)','d#sigma / fb',100,0,1500,0.001)
    canvas.cd(2)
    canvas.GetPad(2).SetLogy()
    plotVariable('pT2','jet.obj[1].pt()', 'jet 2 p_{T} (GeV)','d#sigma / fb',100,0,1500,0.001)
    canvas.cd(3)
    canvas.GetPad(3).SetLogy()
    plotVariable('pTmuon','muon.obj[0].pt()', 'muon p_{T} (GeV)','d#sigma / fb',100,0,1500,0.001)
    canvas.cd(4)
    canvas.GetPad(4).SetLogy()
    plotVariable('pTmet','met.obj[0].pt()', 'missing p_{T} (GeV)','d#sigma / fb',100,0,1500,0.001)
    canvas.SaveAs(prefix + '_pT.root')
    canvas.SaveAs(prefix + '_pT.pdf')
    canvas.SaveAs(prefix + '_pT.eps')
    if wait:
        os.system("ghostview "+prefix + '_pT.eps')

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    plotVariable('eta1','jet.obj[0].eta()', 'jet 1 #eta','normalized',30,-5,5)
    canvas.cd(2)
    plotVariable('eta2','jet.obj[1].eta()', 'jet 1 #eta','normalized',30,-5,5)
    canvas.cd(3)
    plotVariable('etamuon','muon.obj[0].eta()', 'muon #eta','normalized',30,-5,5)
    canvas.SaveAs(prefix + '_eta.root')
    canvas.SaveAs(prefix + '_eta.pdf')
    canvas.SaveAs(prefix + '_eta.eps')
    if wait:
        os.system("ghostview "+prefix + '_eta.eps')

def plotSemileptonicEfficiency():
    print 'plotSemileptonicEfficiency'

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    plotEfficiency('mass1','jet.obj[0].mass()', 'jet 1 mass','d#sigma / fb',60,0,200,ymin)
    canvas.cd(2)
    plotEfficiency('mass2','jet.obj[1].mass()', 'jet 2 mass','d#sigma / fb',60,0,200,ymin)
    canvas.cd(3)
    plotEfficiency('mass3','prunedjet.obj[0].mass()', 'pruned jet 1 mass','d#sigma / fb',60,0,200,ymin)
    canvas.cd(4)
    plotEfficiency('mass4','prunedjet.obj[1].mass()', 'pruned jet 2 mass','d#sigma / fb',60,0,200,ymin)
    canvas.SaveAs(prefix + '_eff_mass.root')
    canvas.SaveAs(prefix + '_eff_mass.pdf')
    canvas.SaveAs(prefix + '_eff_mass.eps')
    if wait:
        os.system("ghostview "+prefix + '_eff_mass.eps')

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    plotEfficiency('pTW','Wpt', 'W p_{T} (GeV)','d#sigma / fb',100,0,1500,0.001)
    canvas.cd(2)
    plotEfficiency('mTW','Wmt', 'W m_{T} (GeV)','d#sigma / fb',100,0,500,0.001)
    canvas.cd(3)
    plotEfficiency('dptW','dptW', '|W p_{T} - jet p_{T}| (GeV)','d#sigma / fb',100,0,500,0.001)
    canvas.cd(4)
    plotEfficiency('dphiW','dphiW', '|#phi_{1}-#phi_{2}|','normalized',20,0,3.1416)
    canvas.SaveAs(prefix + '_eff_Ws.root')
    canvas.SaveAs(prefix + '_eff_Ws.pdf')
    canvas.SaveAs(prefix + '_eff_Ws.eps')
    if wait:
        os.system("ghostview "+prefix + '_eff_Ws.eps')

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    plotEfficiency('pT1','jet.obj[0].pt()', 'jet 1 p_{T} (GeV)','d#sigma / fb',100,0,1500,0.001)
    canvas.cd(2)
    plotEfficiency('pT2','jet.obj[1].pt()', 'jet 2 p_{T} (GeV)','d#sigma / fb',100,0,1500,0.001)
    canvas.cd(3)
    plotEfficiency('pTmuon','muon.obj[0].pt()', 'muon p_{T} (GeV)','d#sigma / fb',100,0,1500,0.001)
    canvas.cd(4)
    plotEfficiency('pTmet','met.obj[0].pt()', 'missing p_{T} (GeV)','d#sigma / fb',100,0,1500,0.001)
    canvas.SaveAs(prefix + '_eff_pT.root')
    canvas.SaveAs(prefix + '_eff_pT.pdf')
    canvas.SaveAs(prefix + '_eff_pT.eps')
    if wait:
        os.system("ghostview "+prefix + '_eff_pT.eps')

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    plotEfficiency('eta1','jet.obj[0].eta()', 'jet 1 #eta','normalized',30,-5,5)
    canvas.cd(2)
    plotEfficiency('eta2','jet.obj[1].eta()', 'jet 1 #eta','normalized',30,-5,5)
    canvas.cd(3)
    plotEfficiency('etamuon','muon.obj[0].eta()', 'muon #eta','normalized',30,-5,5)
    canvas.SaveAs(prefix + '_eff_eta.root')
    canvas.SaveAs(prefix + '_eff_eta.pdf')
    canvas.SaveAs(prefix + '_eff_eta.eps')
    if wait:
        os.system("ghostview "+prefix + '_eff_eta.eps')

def plotGenKinematics():
    print 'plotGenKinematics'

    numW1='7'
    numW2='8'
    numj1='9'
    numj2='10'
    numj3='11'
    numj4='12'

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    plotVariable('W1pT','gen.obj['+numW1+'].pt()', 'V 1 p_{T} (GeV)','normalized',100,0,1500,0.001)
    canvas.cd(2)
    plotVariable('W2pT','gen.obj['+numW2+'].pt()', 'V 2 p_{T} (GeV)','normalized',100,0,1500,0.001)
    canvas.cd(3)
    plotVariable('Weta1','gen.obj['+numW1+'].eta()', 'V 1 #eta','normalized',30,-5,5)
    canvas.cd(4)
    plotVariable('Weta2','gen.obj['+numW2+'].eta()', 'V 2 #eta','normalized',30,-5,5)
    canvas.SaveAs(prefix + '_gen_pT.root')
    canvas.SaveAs(prefix + '_gen_pT.pdf')
    canvas.SaveAs(prefix + '_gen_pT.eps')
    if wait:
        os.system("ghostview "+prefix + '_gen_pT.eps')

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    canvas.GetPad(1).SetLogy()
    plotVariable('WWm','sqrt(pow(gen.obj['+numW1+'].energy()+gen.obj['+numW2+'].energy(),2)-pow(gen.obj['+numW1+'].px()+gen.obj['+numW2+'].px(),2)-pow(gen.obj['+numW1+'].py()+gen.obj['+numW2+'].py(),2)-pow(gen.obj['+numW1+'].pz()+gen.obj['+numW2+'].pz(),2))', 'm(VV) (GeV)','d#sigma / fb',50,900,1100,0.001)
    canvas.cd(2)
    plotVariable('WWseta','(gen.obj['+numW1+'].eta()+gen.obj['+numW2+'].eta())', 'VV #eta_{1}+#eta_{2}','normalized',20,-5,5)
    canvas.cd(3)
    plotVariable('WWdeta','abs(gen.obj['+numW1+'].eta()-gen.obj['+numW2+'].eta())', 'VV |#eta_{1}-#eta_{2}|','normalized',20,0,5)
    canvas.cd(4)
    plotVariable('WWdphi','fabs(fmod(gen.obj['+numW1+'].phi()-gen.obj['+numW2+'].phi()+3.0*pi,2.0*pi)-pi)', 'VV |#phi_{1}-#phi_{2}|','normalized',20,0,3.1416)
    canvas.SaveAs(prefix + '_gen_dijet.root')
    canvas.SaveAs(prefix + '_gen_dijet.pdf')
    canvas.SaveAs(prefix + '_gen_dijet.eps')
    if wait:
        os.system("ghostview "+prefix + '_gen_dijet.eps')

    canvas = TCanvas("","",0,0,400,400)
    canvas.Divide(2,2)
    canvas.cd(1)
    plotVariable('j1pT','gen.obj['+numj1+'].pt()', 'jet 1 p_{T} (GeV)','normalized',100,0,1500,0.001)
    canvas.cd(2)
    plotVariable('j2pT','gen.obj['+numj2+'].pt()', 'jet 2 p_{T} (GeV)','normalized',100,0,1500,0.001)
    canvas.cd(3)
    plotVariable('j3pT','gen.obj['+numj3+'].pt()', 'jet 3 p_{T} (GeV)','normalized',100,0,1500,0.001)
    canvas.cd(4)
    plotVariable('j4pT','gen.obj['+numj4+'].pt()', 'jet 4 p_{T} (GeV)','normalized',100,0,1500,0.001)
    canvas.SaveAs(prefix + '_gen_jpT.root')
    canvas.SaveAs(prefix + '_gen_jpT.pdf')
    canvas.SaveAs(prefix + '_gen_jpT.eps')
    if wait:
        os.system("ghostview "+prefix + '_gen_jpT.eps')

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

doSemileptonic=True
doGenLevel=False
wait=True

#jets = 'cmgPFJets_cmgPFJetSel__PAT'
#jets = 'cmgBaseJets_cmgPFBaseJetSel__PAT'
#jets = 'recoGenParticles_genParticlesStatus3__PAT'
jets = 'cmgBaseJets_cmgPFBaseJetSelCA8CMG__PAT'
prunedjets = 'cmgBaseJets_cmgPFBaseJetSelCA8PrunedCMG__PAT'
muons = 'cmgMuons_cmgMuonSel__PAT'
mets = 'cmgBaseMETs_cmgPFMET__PAT'
gens1 = 'recoGenParticles_genParticlesStatus3__PAT'
gens2 = 'recoGenParticles_genParticlesStatus3__PFAOD'
cuts = '(1)'
if doGenLevel:
    pass
elif doSemileptonic:
    cuts += '*(muon.obj[0].pt()>100)'
    cuts += '*(jet.obj[0].pt()>100)'
    #cuts += '*(abs(jet.obj[0].eta())<2.5)'
    #cuts += '*(Wpt>100)'
    cuts += '*(abs(Wmt-54)<15)'
    #cuts += '*(dphiW>1.5)'
else:
    cuts += '*(jet.obj[0].pt()>100)'
    cuts += '*(abs(jet.obj[0].eta())<2.5)'
    cuts += '*(abs(jet.obj[1].eta())<2.5)'
    cuts += '*(deta<1.3)'
    #cuts += '*(jet.obj[1].pt()>100)'
    #cuts += '*(jet.obj[0].mass()>60)'
    #cuts += '*(jet.obj[1].mass()>60)'
    #cuts += '*(mjj>300)'
    #cuts += '*(prunedjet.obj[0].mass()>60)'
    #cuts += '*(prunedjet.obj[1].mass()>60)'
    #cuts += '*(massdrop1<0.25)'
    #cuts += '*(massdrop2<0.25)'
    #cuts += '*(nsubjets1==2)'
    #cuts += '*(nsubjets2==2)'

from CMGTools.Production.datasetToSource import *
#sourceQCD = datasetToSource('hinzmann',
#    '/QCD_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM/PAT_CMG_Hinzmann',
#    'tree.*root')
#sourceW = datasetToSource('hinzmann',
#    '/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM/V2/PAT_CMG_Hinzmann6',
#    'tree.*root')
#sourceWW = datasetToSource('hinzmann',
#    '/WW_TuneZ2_7TeV_pythia6_tauola/Summer11-PU_S4_START42_V11-v1/AODSIM/V2/PAT_CMG_Hinzmann6',
#    'tree.*root')

samples=[#(["cmgtrees/pythia6_gravitonWW_500_tree_CMG.root"],1.313e-08*1e9,'G*->WW,0.5TeV,0.1k/M'),
         (["cmgtrees/pythia6_gravitonWW_1000_tree_CMG.root"],2.558e-10*1e9,'G*->WW,1TeV,0.1k/M'),
         #(["cmgtrees/pythia6_gravitonWW_2000_tree_CMG.root"],1.827e-12*1e9,'G*->WW 2 TeV'),
         #(["cmgtrees/herwigpp_graviton_WW_500_tree_CMG.root"],0.981*5.4*0.1/500*10000,'G*->WW,0.5TeV'),
         #(["cmgtrees/herwigpp_graviton_WW_1000_tree_CMG.root"],80.5e-03*5.4*0.1/1000*10000.,'G*->WW,1TeV'),
         #(["cmgtrees/herwigpp_graviton_ZZ_1000_tree_CMG.root"],40.3e-3,'H++ G*->ZZ,1TeV'),
         #(["cmgtrees/herwigpp_graviton_ZZ_1000_noMPI_noHAD_noSHOWER_PFAOD.root"],40.3e-3,'H++ G*->ZZ,1TeV'),
         #(["cmgtrees/pythia6_gravitonZZ_500_tree_CMG.root"],1.313e-08*1e9,'G*->ZZ 0.5 TeV,0.1k/M'),
         #(["cmgtrees/pythia6_graviton_0.01_WW_1000_tree_CMG.root"],2.573e-12*1e9,'G*->WW,1TeV,0.01k/M'),
         #(["cmgtrees/pythia6_gravitonZZ_1000_tree_CMG.root"],2.558e-10*1e9,'P6 G*->ZZ,1TeV'),
         #(["cmgtrees/pythia6_gravitonZZ_2000_tree_CMG.root"],1.827e-12*1e9,'G*->ZZ 2 TeV'),
         #(["cmgtrees/pythia6_Wprime_WZ_500_tree_CMG.root"],2.455e-09*1e9,"W'->WZ 0.5TeV"),
         #(["cmgtrees/pythia6_Wprime_WZ_1000_tree_CMG.root"],1.021e-10*1e9,"W'->WZ 1TeV"),
         #(["cmgtrees/pythia6_Wprime_WZ_2000_tree_CMG.root"],1.697e-12*1e9,"W'->WZ 2TeV"),
         #(["cmgtrees/pythia6_WW_tree_CMG.root"],2.780e-08*1e9,'WW'),
         #(["cmgtrees/pythia6_W_tree_CMG.root"],7.314e-05*1e9,'W'),
         #(["cmgtrees/pythia6_QCD_tree_CMG.root"],3.326e-04*1e9,'QCD'),
         #(sourceQCD.fileNames,3.326e-04*1e9*6e4,'QCDflat'),
         #(sourceW.fileNames,27770.0,'W'),
         #(sourceWW.fileNames,27.80,'WW'),
         #(["/tmp/hinzmann/QCD_tree.root"],3.326e-04*1e9*6e4,'QCDflat'),
         (["/tmp/hinzmann/W_tree.root"],27770.0,'W'),
         (["/tmp/hinzmann/WW_tree.root"],27.80,'WW'),
         #(["cmgtrees/LHE.root"],0.43538820803E-02,'JHU G*->ZZ,1TeV'),
         ]
weights=[]
trees=[]
for sample,weight,name in samples:
    trees+=[TChain('Events')]
    for f in sample[0:1000]:
        if f.startswith('/store'):
            trees[-1].Add('root://eoscms//eos/cms/'+f)
	else:
            trees[-1].Add(f)
    nevents=trees[-1].GetEntries()
    print sample,", number of events:",nevents
    weights+=[str(weight/nevents*1000)+'*'+cuts]
    if 'QCDflat' in name:
        weights[-1]+='*genweight'
    trees[-1].SetAlias('jet', jets)
    trees[-1].SetAlias('prunedjet', prunedjets)
    trees[-1].SetAlias('muon', muons)
    trees[-1].SetAlias('met', mets)
    trees[-1].SetAlias('gen1', gens1)
    trees[-1].SetAlias('gen2', gens2)
    trees[-1].SetAlias('mjj','sqrt(pow(jet.obj[0].energy()+jet.obj[1].energy(),2)-pow(jet.obj[0].px()+jet.obj[1].px(),2)-pow(jet.obj[0].py()+jet.obj[1].py(),2)-pow(jet.obj[0].pz()+jet.obj[1].pz(),2))')
    trees[-1].SetAlias('seta','(jet.obj[0].eta()+jet.obj[1].eta())')
    trees[-1].SetAlias('deta','abs(jet.obj[0].eta()-jet.obj[1].eta())')
    trees[-1].SetAlias('nsubjets1','prunedjet.obj[0].@subjets_.size()')
    trees[-1].SetAlias('nsubjets2','prunedjet.obj[1].@subjets_.size()')
    trees[-1].SetAlias('massdrop1','(max(prunedjet.obj[0].subjets_[0].mass(),prunedjet.obj[0].subjets_[1].mass())/prunedjet.obj[0].mass())')
    trees[-1].SetAlias('massdrop2','(max(prunedjet.obj[1].subjets_[0].mass(),prunedjet.obj[1].subjets_[1].mass())/prunedjet.obj[1].mass())')
    trees[-1].SetAlias('subjet1pt1','prunedjet.obj[0].subjetsBoosted_[0].pt()')
    trees[-1].SetAlias('subjet1pt2','prunedjet.obj[0].subjetsBoosted_[1].pt()')
    trees[-1].SetAlias('subjet1dpt','abs(prunedjet.obj[0].subjetsBoosted_[0].pt()-prunedjet.obj[0].subjetsBoosted_[1].pt())')
    trees[-1].SetAlias('subjet1theta','prunedjet.obj[0].subjetsBoosted_[0].theta()')
    trees[-1].SetAlias('genweight', 'GenEventInfoProduct_generator__SIM.obj.weight()')
    trees[-1].SetAlias('Wpt','sqrt(pow(muon.obj[0].px()+met.obj[0].px(),2)+pow(muon.obj[0].py()+met.obj[0].py(),2))')
    trees[-1].SetAlias('Wmt','sqrt(pow(muon.obj[0].et()+met.obj[0].et(),2)-pow(muon.obj[0].px()+met.obj[0].px(),2)-pow(muon.obj[0].py()+met.obj[0].py(),2))')
    trees[-1].SetAlias('Wphi','atan2(muon.obj[0].py()+met.obj[0].py(),muon.obj[0].px()+met.obj[0].px())')
    trees[-1].SetAlias('dptW','abs(Wpt-jet.obj[0].pt())')
    trees[-1].SetAlias('dphiW','fabs(fmod(Wphi-jet.obj[0].phi()+3.0*pi,2.0*pi)-pi)')
    trees[-1].SetAlias('tag1','(abs(jet.obj[0].mass()-90)<15)')
    trees[-1].SetAlias('tag2','(abs(jet.obj[1].mass()-90)<15)')
    trees[-1].SetAlias('tag1tag2','(tag1*tag2)')
    trees[-1].SetAlias('notag1tag2','((!tag1)*tag2)')
    trees[-1].SetAlias('tag1notag2','(tag1*(!tag2))')
    trees[-1].SetAlias('notag1notag2','((!tag1)*(!tag2))')

prefix = "plots/semileptonic111121"

if __name__ == '__main__':
    if doGenLevel:
        plotGenKinematics()
    elif doSemileptonic:
	plotSemileptonicEfficiency()
        plotSemileptonicKinematics()
        plotSubjetKinematics()
    else:
        plotDijetKinematics()
        plotSubjetKinematics()
