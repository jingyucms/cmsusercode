import os, sys
from ROOT import * 
from DataFormats.FWLite import Events,Handle
import array, math

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
gStyle.SetOptTitle(0)

isLoop=False
isMakePlot=True

# init
energy = sys.argv[1]
maxNevents=sys.argv[2]

isLoop=False
isDefaultQBH=False
isRS1QBH=True
isLowQCDScaleQBH=False

if isDefaultQBH:
    crossSectionMap=[[4000,28.65327],[4500,10.28881],[5000,3.728508],[5500,1.343979],[6000,0.4758148],[6500,0.1634881],[7000,0.05385596],[7500,0.01678352],[8000,0.004871688],[8500,0.001292072],[9000,0.0003054339],[9500,0.00006221544],[10000,0.00001040396],[10500,0.000001327101],[11000,0.0000001145733]]
    outname="datacard_shapelimit13TeV_QBH_"+energy+"_6_chi_v1.root"
    qbhfile=TFile.Open("root://eoscms//eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/Jingyu/samples/DiJet/pythia_qbh_"+energy+"_6_v1.root")
    print "root://eoscms//eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/Jingyu/samples/DiJet/pythia_qbh_"+energy+"_6_v1.root"
    signalHistFileName="qbh_"+str(energy)+"_6_chi_v1.root"
    massbins=[[3600,4200],[4200,4800],[4800,13000]]
    slopes=[0.014,0.015,0.016]
    chi_bins=[(1,2,3,4,5,6,7,8,9,10,12,14,16),(1,2,3,4,5,6,7,8,9,10,12,14,16),(1,3,6,9,12,16)]
    chi_binnings=[]
    for mass_bin in chi_bins:
        chi_binnings+=[array.array('d')]
        for chi_bin in mass_bin:
            chi_binnings[-1].append(chi_bin)
    
##     fastNloPlots=[]
##     fastNloFile=TFile.Open("/afs/cern.ch/work/z/zhangj/private/CMSSW_7_4_15/src/fnl5662i_v23_fix_CT14_ak4.root")
##     ewkFile=TFile.Open("/afs/cern.ch/work/z/zhangj/private/CMSSW_7_4_15/src/DijetAngularCMS13_ewk.root")
##     fastNloMassBins=[[4200,4800],[4800,5400],[5400,6000]]
##     for fastNloMass in fastNloMassBins:
##         fastnlo=fastNloFile.Get("chi-"+str(fastNloMass[0])+"-"+str(fastNloMass[1]))
##         ewk=ewkFile.Get("chi-"+str(fastNloMass[0])+"-"+str(fastNloMass[1]))
##         for b in range(fastnlo.GetXaxis().GetNbins()):
##             fastnlo.SetBinContent(b+1,fastnlo.GetBinContent(b+1)*fastnlo.GetBinWidth(b+1))
##             low_bin=ewk.FindBin(fastnlo.GetXaxis().GetBinLowEdge(b+1))
##             up_bin=ewk.FindBin(fastnlo.GetXaxis().GetBinUpEdge(b+1))
##             correction=ewk.Integral(low_bin,up_bin-1)/(up_bin-low_bin)
##             fastnlo.SetBinContent(b+1,fastnlo.GetBinContent(b+1)*correction)
##         fastNloPlots.append(fastnlo)
##     fastNloFinalPlots=[]
##     h1=fastNloPlots[0]
##     h2=fastNloPlots[1]
##     h3=fastNloPlots[2]
##     fastNloPlot1=h1.Clone("fastNloQCD#chi4200_4800_rebin1")
##     h2.Add(h3)
##     fastNloPlot2=h2.Clone("fastNloQCD#chi4800_13000")
##     fastNloPlot2=fastNloPlot2.Rebin(len(chi_binnings[1])-1,"fastNloQCD#chi4800_13000_rebin1",chi_binnings[1])
##     fastNloFinalPlots=[fastNloPlot1,fastNloPlot2]
##     fastNloFinalPlotsBackup=[]

    fastNloPlots=[]
    fastNloFile=TFile.Open("/afs/cern.ch/work/z/zhangj/private/CMSSW_7_4_15/src/fnl5662i_v23_fix_CT14_ak4.root")
    ewkFile=TFile.Open("/afs/cern.ch/work/z/zhangj/private/CMSSW_7_4_15/src/DijetAngularCMS13_ewk.root")
    fastNloMassBins=[[3600,4200],[4200,4800],[4800,5400],[5400,6000]]
    for fastNloMass in fastNloMassBins:
        fastnlo=fastNloFile.Get("chi-"+str(fastNloMass[0])+"-"+str(fastNloMass[1]))
        ewk=ewkFile.Get("chi-"+str(fastNloMass[0])+"-"+str(fastNloMass[1]))
        for b in range(fastnlo.GetXaxis().GetNbins()):
            fastnlo.SetBinContent(b+1,fastnlo.GetBinContent(b+1)*fastnlo.GetBinWidth(b+1))
            low_bin=ewk.FindBin(fastnlo.GetXaxis().GetBinLowEdge(b+1))
	    up_bin=ewk.FindBin(fastnlo.GetXaxis().GetBinUpEdge(b+1))
	    correction=ewk.Integral(low_bin,up_bin-1)/(up_bin-low_bin)
            fastnlo.SetBinContent(b+1,fastnlo.GetBinContent(b+1)*correction)
        fastNloPlots.append(fastnlo)
    fastNloFinalPlots=[]
    h1=fastNloPlots[0]
    h1.Scale(600.)
    h2=fastNloPlots[1]
    h2.Scale(600.)
    h3=fastNloPlots[2]
    h3.Scale(600.)
    h4=fastNloPlots[3]
    h4.Scale(600.)
    fastNloPlot1=h1.Clone("fastNloQCD#chi3600_4200_rebin1")
    fastNloPlot2=h2.Clone("fastNloQCD#chi4200_4800_rebin1")
    h3.Add(h4)
    fastNloPlot3=h3.Clone("fastNloQCD#chi4800_13000")
    fastNloPlot3=fastNloPlot3.Rebin(len(chi_binnings[2])-1,"fastNloQCD#chi4800_13000_rebin1",chi_binnings[2])
    fastNloFinalPlots=[fastNloPlot1,fastNloPlot2,fastNloPlot3]
    fastNloFinalPlotsBackup=[]   

if isRS1QBH:
    crossSectionMap=[[3500,0.4288],[4000,0.1464],[4500,0.05148],[5000,0.01829],[5500,0.006472],[6000,0.002250],[6500,0.0007599],[7000,0.0002461]]
    outname="datacard_shapelimit13TeV_QBH_"+energy+"_RS1_chi_v1.root"
    qbhfile=TFile.Open("root://eoscms//eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/Jingyu/samples/DiJet/pythia_qbh_"+energy+"_RS1_v1.root")
    print "root://eoscms//eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/Jingyu/samples/DiJet/pythia_qbh_"+energy+"_RS1_v1.root"
    signalHistFileName="qbh_"+str(energy)+"_RS1_chi_v1.root"
    massbins=[[3600,4200],[4200,4800],[4800,13000]]
    slopes=[0.014,0.015,0.016]
    chi_bins=[(1,2,3,4,5,6,7,8,9,10,12,14,16),(1,2,3,4,5,6,7,8,9,10,12,14,16),(1,3,6,9,12,16)]
    chi_binnings=[]
    for mass_bin in chi_bins:
        chi_binnings+=[array.array('d')]
        for chi_bin in mass_bin:
            chi_binnings[-1].append(chi_bin)
        
    fastNloPlots=[]
    fastNloFile=TFile.Open("/afs/cern.ch/work/z/zhangj/private/CMSSW_7_4_15/src/fnl5662i_v23_fix_CT14_ak4.root")
    ewkFile=TFile.Open("/afs/cern.ch/work/z/zhangj/private/CMSSW_7_4_15/src/DijetAngularCMS13_ewk.root")
    fastNloMassBins=[[3600,4200],[4200,4800],[4800,5400],[5400,6000]]
    for fastNloMass in fastNloMassBins:
        fastnlo=fastNloFile.Get("chi-"+str(fastNloMass[0])+"-"+str(fastNloMass[1]))
        ewk=ewkFile.Get("chi-"+str(fastNloMass[0])+"-"+str(fastNloMass[1]))
        for b in range(fastnlo.GetXaxis().GetNbins()):
            fastnlo.SetBinContent(b+1,fastnlo.GetBinContent(b+1)*fastnlo.GetBinWidth(b+1))
            low_bin=ewk.FindBin(fastnlo.GetXaxis().GetBinLowEdge(b+1))
	    up_bin=ewk.FindBin(fastnlo.GetXaxis().GetBinUpEdge(b+1))
	    correction=ewk.Integral(low_bin,up_bin-1)/(up_bin-low_bin)
            fastnlo.SetBinContent(b+1,fastnlo.GetBinContent(b+1)*correction)
        fastNloPlots.append(fastnlo)
    fastNloFinalPlots=[]
    h1=fastNloPlots[0]
    h1.Scale(600.)
    h2=fastNloPlots[1]
    h2.Scale(600.)
    h3=fastNloPlots[2]
    h3.Scale(600.)
    h4=fastNloPlots[3]
    h4.Scale(600.)
    fastNloPlot1=h1.Clone("fastNloQCD#chi3600_4200_rebin1")
    fastNloPlot2=h2.Clone("fastNloQCD#chi4200_4800_rebin1")
    h3.Add(h4)
    fastNloPlot3=h3.Clone("fastNloQCD#chi4800_13000")
    fastNloPlot3=fastNloPlot3.Rebin(len(chi_binnings[2])-1,"fastNloQCD#chi4800_13000_rebin1",chi_binnings[2])
    fastNloFinalPlots=[fastNloPlot1,fastNloPlot2,fastNloPlot3]
    fastNloFinalPlotsBackup=[]   

if isLowQCDScaleQBH:
    crossSectionMap=[[6000,0.373],[7000,0.04143],[8000,0.003664],[9000,0.0002237]]
    outname="datacard_shapelimit13TeV_QBH_"+energy+"_6_chi_v2.root"
    qbhfile=TFile.Open("root://eoscms//eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/Jingyu/samples/DiJet/pythia_qbh_"+energy+"_6_v2.root")
    print "root://eoscms//eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/Jingyu/samples/DiJet/pythia_qbh_"+energy+"_6_v2.root"
    signalHistFileName="qbh_"+str(energy)+"_6_chi_v2.root"
    massbins=[[4200,4800],[4800,13000]]
    slopes=[0.04,0.05]
    chi_bins=[(1,2,3,4,5,6,7,8,9,10,12,14,16),(1,3,6,9,12,16)]
    chi_binnings=[]
    for mass_bin in chi_bins:
        chi_binnings+=[array.array('d')]
        for chi_bin in mass_bin:
            chi_binnings[-1].append(chi_bin)
    
    fastNloPlots=[]
    fastNloFile=TFile.Open("/afs/cern.ch/work/z/zhangj/private/CMSSW_7_4_15/src/fnl5662i_v23_fix_CT14_ak4.root")
    ewkFile=TFile.Open("/afs/cern.ch/work/z/zhangj/private/CMSSW_7_4_15/src/DijetAngularCMS13_ewk.root")
    fastNloMassBins=[[4200,4800],[4800,5400],[5400,6000]]
    for fastNloMass in fastNloMassBins:
        fastnlo=fastNloFile.Get("chi-"+str(fastNloMass[0])+"-"+str(fastNloMass[1]))
        ewk=ewkFile.Get("chi-"+str(fastNloMass[0])+"-"+str(fastNloMass[1]))
        for b in range(fastnlo.GetXaxis().GetNbins()):
            fastnlo.SetBinContent(b+1,fastnlo.GetBinContent(b+1)*fastnlo.GetBinWidth(b+1))
            low_bin=ewk.FindBin(fastnlo.GetXaxis().GetBinLowEdge(b+1))
            up_bin=ewk.FindBin(fastnlo.GetXaxis().GetBinUpEdge(b+1))
            correction=ewk.Integral(low_bin,up_bin-1)/(up_bin-low_bin)
            fastnlo.SetBinContent(b+1,fastnlo.GetBinContent(b+1)*correction)
        fastNloPlots.append(fastnlo)
    fastNloFinalPlots=[]
    h1=fastNloPlots[0]
    h2=fastNloPlots[1]
    h3=fastNloPlots[2]
    fastNloPlot1=h1.Clone("fastNloQCD#chi4200_4800_rebin1")
    h2.Add(h3)
    fastNloPlot2=h2.Clone("fastNloQCD#chi4800_13000")
    fastNloPlot2=fastNloPlot2.Rebin(len(chi_binnings[1])-1,"fastNloQCD#chi4800_13000_rebin1",chi_binnings[1])
    fastNloFinalPlots=[fastNloPlot1,fastNloPlot2]
    fastNloFinalPlotsBackup=[]

    
for crossSection in crossSectionMap:
    if crossSection[0]==int(energy):
        xsec=crossSection[1]
        print "energy: ",energy
        print "qbhCrossSection: ",xsec
        break

# input
qcdfile=TFile.Open("/afs/cern.ch/work/z/zhangj/private/CMSSW_7_4_15/src/datacard_shapelimit13TeV_GENnp-0-v5_chi.root")
jesfile=TFile.Open("/afs/cern.ch/work/z/zhangj/private/CMSSW_7_4_15/src/chi_systematic_plotschi_QCD4v7_13TeV.root")

plots=[]
plotsBackup=[]
plotsALT=[]
plotsData=[]
jesPlotsALTUp=[]
jerPlotsALTUp=[]
jesPlotsALTDown=[]
jerPlotsALTDown=[]
scalePlotsALTUp=[]
scalePlotsALTDown=[]
jesPlotsUp=[]
jerPlotsUp=[]
jesPlotsDown=[]
jerPlotsDown=[]
bgPlots=[]
plotsAddBackup=[]

prunedgenjets_handle=Handle("std::vector<reco::GenJet>")
prunedgenjets_label="ak4GenJets"
qbhEvents=qbhfile.Get("Events")
if int(maxNevents)==-1:
    totNEvents=qbhEvents.GetEntries()
else:
    totNEvents=int(maxNevents)
print "Running on:",totNEvents

# fill qbh chi
if isLoop==True:
    for massbin in massbins:
        plot = TH1F('qbh_'+energy+'_6_#chi'+str(massbin[0])+'_'+str(massbin[1]),';#chi;N',15,1,16)
        plot.Sumw2()
        plots.append(plot)

    event_count=0
    event_pass=0
    for qbhEvent in qbhEvents:
        event_count+=1
        if event_count%10000==1: print "event: ",str(event_count)
        jet1=TLorentzVector()
        jet2=TLorentzVector()
        jets=qbhEvent.recoGenJets_ak4GenJets__GEN.product()
        if len(jets)<2: continue
        j1=jets[0]
        j2=jets[1]
        if j1.pt()<30 or j2.pt()<30: continue
        jet1.SetPtEtaPhiM(j1.pt(),j1.eta(),j1.phi(),j1.mass())
        jet2.SetPtEtaPhiM(j2.pt(),j2.eta(),j2.phi(),j2.mass())
        mjj=(jet1+jet2).M()
        if j1.y()>=2.5 or j1.y()>=2.5: continue
        chi=math.exp(abs(j1.y()-j2.y()))
        if chi>=16: continue
        yboost=abs(j1.y()+j2.y())
        if yboost>=1.11: continue
        event_pass+=1
        for massbin in massbins:
            if mjj>=massbin[0] and mjj<massbin[1]:
                plots[massbins.index(massbin)].Fill(chi)
        if int(event_count)>=int(totNEvents): break
    print "Selection efficiency: ",str(event_pass/float(event_count))
else:
    qbhHistFile=TFile.Open(signalHistFileName)
    for massbin in massbins:
        print 'qbh_'+energy+'_6_#chi'+str(massbin[0])+'_'+str(massbin[1])
        qbhHist=qbhHistFile.Get('qbh_'+energy+'_6_#chi'+str(massbin[0])+'_'+str(massbin[1]))
        qbhHist.Sumw2()
        plots.append(qbhHist)
print plots
        
for massbin in massbins:            
    plots[massbins.index(massbin)]=plots[massbins.index(massbin)].Rebin(len(chi_binnings[massbins.index(massbin)])-1,'qbh_'+energy+'_6_#chi'+str(massbin[0])+'_'+str(massbin[1])+"_rebin1",chi_binnings[massbins.index(massbin)])
    plots[massbins.index(massbin)].Sumw2()
    print "Selection efficiency: ",plots[massbins.index(massbin)].Integral()/float(totNEvents)
    plots[massbins.index(massbin)].Scale(1./totNEvents)
    plots[massbins.index(massbin)].Scale(xsec)
    plotsSave=plots[massbins.index(massbin)].Clone('qbh_'+energy+'_6_#chi'+str(massbin[0])+'_'+str(massbin[1])+"_rebin1_backup")
    plotsBackup.append(plotsSave)

    # save(copy) qcd and data
    qcdPlot=qcdfile.Get("QCDCIplusLL8000_ALT#chi"+str(massbin[0])+"_"+str(massbin[1])+"_rebin1")
    qcdPlot.Sumw2()
    qcdPlotSave=qcdPlot.Clone("qbh_"+energy+"_6_ALT#chi"+str(massbin[0])+"_"+str(massbin[1])+"_rebin1")
    plotsALT.append(qcdPlotSave)
    dataPlot=qcdfile.Get("data_obs#chi"+str(massbin[0])+"_"+str(massbin[1])+"_rebin1")
    dataPlot.Sumw2()
    dataPlotSave=dataPlot.Clone("data_obs#chi"+str(massbin[0])+"_"+str(massbin[1])+"_rebin1")
    plotsData.append(dataPlotSave)
    normfactor=dataPlot.Integral()

    # add qbh on top of qcd and norm to data
    fastNloFinalPlots[massbins.index(massbin)].Scale(1.)  #all in pb, no scale
    plots[massbins.index(massbin)].Add(fastNloFinalPlots[massbins.index(massbin)])
    plotsAddSave=plots[massbins.index(massbin)].Clone('qbh_'+energy+'_6_#chi'+str(massbin[0])+'_'+str(massbin[1])+"_rebin1_add_backup")
    plotsAddBackup.append(plotsAddSave)
    plots[massbins.index(massbin)].Scale(normfactor/plots[massbins.index(massbin)].Integral())

    # save fastnlo histogram for cross check
    fastNloFinalPlotsSave=fastNloFinalPlots[massbins.index(massbin)].Clone("fastNloQCD#chi"+str(massbin[0])+"_"+str(massbin[1])+"_rebin1_backup")
    fastNloFinalPlotsBackup.append(fastNloFinalPlotsSave)
    fastNloFinalPlots[massbins.index(massbin)].Scale(normfactor/fastNloFinalPlots[massbins.index(massbin)].Integral())

    # write(copy) qcd uncertainties to new file
    qcdJerUp=qcdfile.Get("QCDCIplusLL8000_ALT#chi"+str(massbin[0])+"_"+str(massbin[1])+"_rebin1_jerUp")
    qcdJerUpSave=qcdJerUp.Clone("qbh_"+energy+"_6_ALT#chi"+str(massbin[0])+"_"+str(massbin[1])+"_rebin1_jerUp")
    jerPlotsALTUp.append(qcdJerUpSave)
    qcdJesUp=qcdfile.Get("QCDCIplusLL8000_ALT#chi"+str(massbin[0])+"_"+str(massbin[1])+"_rebin1_jesUp")
    qcdJesUpSave=qcdJesUp.Clone("qbh_"+energy+"_6_ALT#chi"+str(massbin[0])+"_"+str(massbin[1])+"_rebin1_jesUp")
    jesPlotsALTUp.append(qcdJesUpSave)
    qcdScaleUp=qcdfile.Get("QCDCIplusLL8000_ALT#chi"+str(massbin[0])+"_"+str(massbin[1])+"_rebin1_scaleUp")
    qcdScaleUpSave=qcdScaleUp.Clone("qbh_"+energy+"_6_ALT#chi"+str(massbin[0])+"_"+str(massbin[1])+"_rebin1_scaleUp")
    scalePlotsALTUp.append(qcdScaleUpSave)
    qcdJerDown=qcdfile.Get("QCDCIplusLL8000_ALT#chi"+str(massbin[0])+"_"+str(massbin[1])+"_rebin1_jerDown")
    qcdJerDownSave=qcdJerDown.Clone("qbh_"+energy+"_6_ALT#chi"+str(massbin[0])+"_"+str(massbin[1])+"_rebin1_jerDown")
    jerPlotsALTDown.append(qcdJerDownSave)
    qcdJesDown=qcdfile.Get("QCDCIplusLL8000_ALT#chi"+str(massbin[0])+"_"+str(massbin[1])+"_rebin1_jesDown")
    qcdJesDownSave=qcdJesDown.Clone("qbh_"+energy+"_6_ALT#chi"+str(massbin[0])+"_"+str(massbin[1])+"_rebin1_jesDown")
    jesPlotsALTDown.append(qcdJesDownSave)
    qcdScaleDown=qcdfile.Get("QCDCIplusLL8000_ALT#chi"+str(massbin[0])+"_"+str(massbin[1])+"_rebin1_scaleDown")
    qcdScaleDownSave=qcdScaleDown.Clone("qbh_"+energy+"_6_ALT#chi"+str(massbin[0])+"_"+str(massbin[1])+"_rebin1_scaleDown")
    scalePlotsALTDown.append(qcdScaleDownSave)

    # write(copy) dummy background
    bgPlot=qcdfile.Get("QCD#chi"+str(massbin[0])+"_"+str(massbin[1])+"_rebin1")
    bgPlotSave=bgPlot.Clone("QCD#chi"+str(massbin[0])+"_"+str(massbin[1])+"_rebin1")
    bgPlots.append(bgPlotSave)
    
    # jer uncertainty
    jerPlotUp=plots[massbins.index(massbin)].Clone('qbh_'+energy+'_6_#chi'+str(massbin[0])+'_'+str(massbin[1])+'_rebin1_jerUp')
    jerPlotDown=plots[massbins.index(massbin)].Clone('qbh_'+energy+'_6_#chi'+str(massbin[0])+'_'+str(massbin[1])+'_rebin1_jerDown')
    for b in range(plots[massbins.index(massbin)].GetNbinsX()):
        jerPlotUp.SetBinContent(b+1,plots[massbins.index(massbin)].GetBinContent(b+1)*(1.+(plots[massbins.index(massbin)].GetBinCenter(b+1)-8.5)/7.5*slopes[massbins.index(massbin)]))
        jerPlotDown.SetBinContent(b+1,plots[massbins.index(massbin)].GetBinContent(b+1)*(1.-(plots[massbins.index(massbin)].GetBinCenter(b+1)-8.5)/7.5*slopes[massbins.index(massbin)]))
    jerPlotsUp.append(jerPlotUp)
    jerPlotsDown.append(jerPlotDown)
    
    # jes uncertainty
    jesPlotUp=plots[massbins.index(massbin)].Clone('qbh_'+energy+'_6_#chi'+str(massbin[0])+'_'+str(massbin[1])+'_rebin1_jesUp')
    jesPlotDown=plots[massbins.index(massbin)].Clone('qbh_'+energy+'_6_#chi'+str(massbin[0])+'_'+str(massbin[1])+'_rebin1_jesDown')    
    jespad=jesfile.Get("jes")
    jes=jespad.GetListOfPrimitives()[(6-len(massbins))+massbins.index(massbin)]
    for b in range(plots[massbins.index(massbin)].GetNbinsX()):
        jesPlotUp.SetBinContent(b+1,plots[massbins.index(massbin)].GetBinContent(b+1)*jes.GetListOfPrimitives()[2].GetBinContent(b+1))
        jesPlotDown.SetBinContent(b+1,plots[massbins.index(massbin)].GetBinContent(b+1)*jes.GetListOfPrimitives()[4].GetBinContent(b+1))
    jesPlotsUp.append(jesPlotUp)
    jesPlotsDown.append(jesPlotDown)

out = TFile.Open(outname,"RECREATE")
print "created file:",outname
    
for massbin in massbins:
    plots[massbins.index(massbin)].Write()
    plotsBackup[massbins.index(massbin)].Write()
    jesPlotsUp[massbins.index(massbin)].Write()
    jerPlotsUp[massbins.index(massbin)].Write()
    jesPlotsDown[massbins.index(massbin)].Write()
    jerPlotsDown[massbins.index(massbin)].Write()
    plotsALT[massbins.index(massbin)].Write()
    plotsData[massbins.index(massbin)].Write()
    jesPlotsALTUp[massbins.index(massbin)].Write()
    jerPlotsALTUp[massbins.index(massbin)].Write()
    jesPlotsALTDown[massbins.index(massbin)].Write()
    jerPlotsALTDown[massbins.index(massbin)].Write()
    scalePlotsALTUp[massbins.index(massbin)].Write()
    scalePlotsALTDown[massbins.index(massbin)].Write()
    bgPlots[massbins.index(massbin)].Write()
    fastNloFinalPlots[massbins.index(massbin)].Write()
    fastNloFinalPlotsBackup[massbins.index(massbin)].Write()
    plotsAddBackup[massbins.index(massbin)].Write()
    
if isMakePlot:
    if len(massbins)==2:
        canvas = TCanvas("MyCanvas","Limit Input",0,0,1200,600)
        canvas.Draw()
        pad1=TPad("","",0, 0, 0.5, 1)
        pad2=TPad("","",0.5, 0, 1, 1)
        pad=[pad1,pad2]

    if len(massbins)==3:
        canvas = TCanvas("MyCanvas","Limit Input",0,0,1800,600)
        canvas.Draw()
        pad1=TPad("","",0.01, 0, 0.34, 1)
        pad2=TPad("","",0.34, 0, 0.67, 1)
        pad3=TPad("","",0.67, 0, 1, 1)
        pad=[pad1,pad2,pad3]

    legends=[]
    for massbin in massbins:
        legend=TLegend(0.25,0.65,0.6,0.95,str(massbin[0])+"<m_{jj}<"+str(massbin[1])+" GeV")
        legend.AddEntry(plotsData[massbins.index(massbin)],"Unfolded data","lep")
        legend.AddEntry(plots[massbins.index(massbin)],str(energy)+" GeV (ADD6) QBH", "l")
        legend.AddEntry(plotsALT[massbins.index(massbin)],"NLO QCD", "l")
        legend.AddEntry(jesPlotsALTUp[massbins.index(massbin)],"JES","l")
        legend.AddEntry(jerPlotsALTUp[massbins.index(massbin)],"JER","l")
        legend.AddEntry(scalePlotsALTDown[massbins.index(massbin)],"scale","l")
        legend.SetFillStyle(0)
        legends.append(legend)
    
    for massbin in massbins:
        canvas.cd()
        pad[massbins.index(massbin)].Draw()
        pad[massbins.index(massbin)].cd()
        plotsData[massbins.index(massbin)].Draw()
        plotsData[massbins.index(massbin)].SetMarkerStyle(4)
        plotsData[massbins.index(massbin)].SetMaximum(200)
        plotsData[massbins.index(massbin)].GetYaxis().SetTitle("N")
        plotsData[massbins.index(massbin)].GetXaxis().SetTitle("#chi")
        plots[massbins.index(massbin)].Draw("samehist")
        plots[massbins.index(massbin)].SetLineColor(1)
        plotsALT[massbins.index(massbin)].Draw("samehist")
        plotsALT[massbins.index(massbin)].SetLineColor(2)
        jesPlotsALTUp[massbins.index(massbin)].Draw("samehist")
        jesPlotsALTUp[massbins.index(massbin)].SetLineColor(4)
        jesPlotsALTUp[massbins.index(massbin)].SetLineStyle(2)
        jesPlotsALTDown[massbins.index(massbin)].Draw("samehist")
        jesPlotsALTDown[massbins.index(massbin)].SetLineColor(4)
        jesPlotsALTDown[massbins.index(massbin)].SetLineStyle(2)
        jerPlotsALTUp[massbins.index(massbin)].Draw("samehist")
        jerPlotsALTUp[massbins.index(massbin)].SetLineColor(3)
        jerPlotsALTUp[massbins.index(massbin)].SetLineStyle(2)
        jerPlotsALTDown[massbins.index(massbin)].Draw("samehist")
        jerPlotsALTDown[massbins.index(massbin)].SetLineColor(3)
        jerPlotsALTDown[massbins.index(massbin)].SetLineStyle(2)
        scalePlotsALTUp[massbins.index(massbin)].Draw("samehist")
        scalePlotsALTUp[massbins.index(massbin)].SetLineColor(6)
        scalePlotsALTUp[massbins.index(massbin)].SetLineStyle(2)
        scalePlotsALTDown[massbins.index(massbin)].Draw("samehist")
        scalePlotsALTDown[massbins.index(massbin)].SetLineColor(6)
        scalePlotsALTDown[massbins.index(massbin)].SetLineStyle(2)
 
        legends[massbins.index(massbin)].Draw()
        canvas.Update()

    canvas.SaveAs("limit_input_QBH_"+str(energy)+"_RS1.gif")
        
        
        
        
        
    
