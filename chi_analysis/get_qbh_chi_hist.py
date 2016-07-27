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

# init
energy = sys.argv[1]
maxNevents=sys.argv[2]

isADDQBH=True
isRS1QBH=False

if isADDQBH:
    outname="qbh_"+energy+"_6_chi_v1.root"
    qbhfile=TFile.Open("root://eoscms//eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/Jingyu/samples/DiJet/pythia_qbh_"+energy+"_6_v1.root")
    print "root://eoscms//eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/Jingyu/samples/DiJet/pythia_qbh_"+energy+"_6_v1.root"
    model="ADD6"

if isRS1QBH:
    outname="qbh_"+energy+"_RS1_chi_v1.root"
    qbhfile=TFile.Open("root://eoscms//eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/Jingyu/samples/DiJet/pythia_qbh_"+energy+"_RS1_v1.root")
    print "root://eoscms//eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/Jingyu/samples/DiJet/pythia_qbh_"+energy+"_RS1_v1.root"
    model="RS1"

massbins=[[3600,4200],[4200,4800],[4800,13000]]

##chi_bins=[(1,2,3,4,5,6,7,8,9,10,12,14,16),(1,2,3,4,5,6,7,8,9,10,12,14,16),(1,3,6,9,12,16)]
##
##chi_binnings=[]
##for mass_bin in chi_bins:
##    chi_binnings+=[array.array('d')]
##    for chi_bin in mass_bin:
##        chi_binnings[-1].append(chi_bin)

plots=[]

for massbin in massbins:
    plot = TH1F('QCD'+model+'QBH'+energy+'#chi'+str(massbin[0])+'_'+str(massbin[1]),';#chi;N',15,1,16)
    plot.Sumw2()
    plots.append(plot)

prunedgenjets_handle=Handle("std::vector<reco::GenJet>")
prunedgenjets_label="ak4GenJets"
qbhEvents=qbhfile.Get("Events")
if int(maxNevents)==-1:
    totNEvents=qbhEvents.GetEntries()
else:
    totNEvents=int(maxNevents)
print "Running on:",totNEvents
    
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

print "Selection efficiency for all massbins: ",str(event_pass/float(event_count))

out = TFile.Open(outname,"RECREATE")
print "created file:",outname

for massbin in massbins:
    plots[massbins.index(massbin)].Write()
