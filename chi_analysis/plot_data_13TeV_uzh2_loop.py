import os, sys
from ROOT import * 
import array
from math import *

#gROOT.Macro( os.path.expanduser( '~/rootlogon.C' ) )
gROOT.Reset()
gROOT.SetStyle("Plain")
gROOT.SetBatch(True)
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
gStyle.SetNdivisions(506, "XYZ")
gStyle.SetLegendBorderSize(0)

doJES=False

if doJES:
  gROOT.ProcessLine(".L /shome/hinzmann/CMSSW_7_4_7_patch2/src/CondFormats/JetMETObjects/src/Utilities.cc+");
  gROOT.ProcessLine(".L /shome/hinzmann/CMSSW_7_4_7_patch2/src/CondFormats/JetMETObjects/src/JetCorrectorParameters.cc+");
  gROOT.ProcessLine(".L /shome/hinzmann/CMSSW_7_4_7_patch2/src/CondFormats/JetMETObjects/src/SimpleJetCorrectionUncertainty.cc+");
  gROOT.ProcessLine(".L /shome/hinzmann/CMSSW_7_4_7_patch2/src/CondFormats/JetMETObjects/src/JetCorrectionUncertainty.cc+");

  JECsources = ["AbsoluteScale", "AbsoluteFlavMap", "AbsoluteMPFBias", "Fragmentation",
"SinglePionECAL", "SinglePionHCAL",
"FlavorQCD", "TimeEta", "TimePt",
"RelativeJEREC1", "RelativeJEREC2", "RelativeJERHF",
"RelativePtBB","RelativePtEC1", "RelativePtEC2", "RelativePtHF", "RelativeFSR",
"RelativeStatFSR", "RelativeStatEC", "RelativeStatHF",
"PileUpDataMC", 
"PileUpPtRef", "PileUpPtBB", "PileUpPtEC1", "PileUpPtEC2", "PileUpPtHF","PileUpMuZero", "PileUpEnvelope",
#"TimeRunA", "TimeRunB", "TimeRunC",
"TimeRunD",
#"SubTotalPileUp","SubTotalRelative","SubTotalPt","SubTotalScale","SubTotalAbsolute","SubTotalMC",
"Total",
#"TotalNoFlavor","TotalNoTime","TotalNoFlavorNoTime",
#"FlavorZJet","FlavorPhotonJet","FlavorPureGluon","FlavorPureQuark","FlavorPureCharm","FlavorPureBottom"
  ]

  JESuncertainties={}
  for source in JECsources:
    p = JetCorrectorParameters("../../EXOVVNtuplizerRunII/Ntuplizer/JEC/Fall15_25nsV2_DATA_UncertaintySources_AK4PFchs.txt", source)
    JESuncertainties[source]=JetCorrectionUncertainty(p)


def createPlotsAndTree(sample,prefix,massbins,factor,tree,HLT_isFired):
    if sample.endswith(".txt"):
        files=[]
        filelist=open(sample)
	for line in filelist.readlines():
	    if ".root" in line:
	        files+=[line.strip()]
    else:
        files=[sample]

    plots=[]
    genplots=[]
    variables=["#chi","p_{T1}","p_{T2}","y_{1}","y_{2}","y_{1}","y_{2}","y_{1}","y_{2}","y_{1}","y_{2}","y_{boost}","missing E_{T} / #sum E_{T}","#sum #vec p_{T} / #sum |p_{T}|","#Delta #phi","#Delta p_{T} / #sum p_T"]
    for massbin in massbins:
      plots += [TH1F(prefix+'#chi'+str(massbin).strip("()").replace(',',"_").replace(' ',""),';#chi;N',15,1,16)]
      genplots += [TH1F(prefix+'#genchi'+str(massbin).strip("()").replace(',',"_").replace(' ',""),';#genchi;N',15,1,16)]
      #plots += [TH1F(prefix+'y_{boost}'+str(massbin).strip("()").replace(',',"_").replace(' ',""),';y_{boost};N',20,0,2)]
    plots += [TH1F(prefix+'mass',';dijet mass;N events',1300,0,13000)]
    genplots += [TH1F(prefix+'genmass',';dijet mass;N events',1300,0,13000)]
    if doJES:
     for source in JECsources:
       for massbin in massbins:
        plots += [TH1F(prefix+'#chi'+str(massbin).strip("()").replace(',',"_").replace(' ',"")+source+"Up",';#chi;N',15,1,16)]
       for massbin in massbins:
        plots += [TH1F(prefix+'#chi'+str(massbin).strip("()").replace(',',"_").replace(' ',"")+source+"Down",';#chi;N',15,1,16)]
    
    for plot in plots:
        plot.Sumw2()
    for plot in genplots:
        plot.Sumw2()
    print len(plots),"plots to fill"

    event_count=0
    for f in files[:]:
     print f
     try:
       fil=TFile.Open(f)
       events=fil.Get("ntuplizer/tree")
       nevents=events.GetEntries()
     except:
       print "error opening", f
       continue
     print sample,nevents
     for event in events:
       #if event_count>200:break
       #if not "data" in sample and event_count>3000000:break
       
       event_count+=1
       if event_count%10000==1: print "event",event_count
       
       while len(event.jetAK4_pt)<3:
          event.jetAK4_pt.push_back(-1)
          event.jetAK4_eta.push_back(-1)
          event.jetAK4_phi.push_back(-1)
          event.jetAK4_mass.push_back(-1)
          event.jetAK4_jec.push_back(-1)       
          event.jetAK4_muf.push_back(-1)       
          event.jetAK4_muf.push_back(-1)       
          event.jetAK4_phf.push_back(-1)       
          event.jetAK4_emf.push_back(-1)       
          event.jetAK4_nhf.push_back(-1)       
          event.jetAK4_chf.push_back(-1)       
          event.jetAK4_area.push_back(-1)       
          event.jetAK4_cm.push_back(-1)       
          event.jetAK4_nm.push_back(-1)       
          event.jetAK4_che.push_back(-1)       
          event.jetAK4_ne.push_back(-1)       
          event.jetAK4_hf_hf.push_back(-1)	
          event.jetAK4_hf_emf.push_back(-1)	 
          event.jetAK4_hof.push_back(-1)       
          event.jetAK4_chm.push_back(-1)       
          event.jetAK4_neHadMult.push_back(-1)	    
          event.jetAK4_phoMult.push_back(-1)	  
          event.jetAK4_nemf.push_back(-1)       
          event.jetAK4_cemf.push_back(-1)       
          event.jetAK4_csv.push_back(-1)       
          event.jetAK4_IDTight.push_back(0)
       
       values=[event.jetAK4_pt[0],event.jetAK4_eta[0],event.jetAK4_phi[0],event.jetAK4_mass[0],
	          event.jetAK4_jec[0],event.jetAK4_muf[0],event.jetAK4_phf[0],event.jetAK4_emf[0],event.jetAK4_nhf[0],event.jetAK4_chf[0],event.jetAK4_area[0],event.jetAK4_cm[0],event.jetAK4_nm[0],event.jetAK4_hof[0],event.jetAK4_chm[0],event.jetAK4_neHadMult[0],event.jetAK4_phoMult[0],event.jetAK4_nemf[0],event.jetAK4_cemf[0],event.jetAK4_csv[0],bool(event.jetAK4_IDTight[0]),
	          event.jetAK4_pt[1],event.jetAK4_eta[1],event.jetAK4_phi[1],event.jetAK4_mass[1],
	          event.jetAK4_jec[1],event.jetAK4_muf[1],event.jetAK4_phf[1],event.jetAK4_emf[1],event.jetAK4_nhf[1],event.jetAK4_chf[1],event.jetAK4_area[1],event.jetAK4_cm[1],event.jetAK4_nm[1],event.jetAK4_hof[1],event.jetAK4_chm[1],event.jetAK4_neHadMult[1],event.jetAK4_phoMult[1],event.jetAK4_nemf[1],event.jetAK4_cemf[1],event.jetAK4_csv[1],bool(event.jetAK4_IDTight[1]),
	          event.jetAK4_pt[2],event.jetAK4_eta[2],event.jetAK4_phi[2],event.jetAK4_mass[2],
	          event.jetAK4_jec[2],event.jetAK4_muf[2],event.jetAK4_phf[2],event.jetAK4_emf[2],event.jetAK4_nhf[2],event.jetAK4_chf[2],event.jetAK4_area[2],event.jetAK4_cm[2],event.jetAK4_nm[2],event.jetAK4_hof[2],event.jetAK4_chm[2],event.jetAK4_neHadMult[2],event.jetAK4_phoMult[2],event.jetAK4_nemf[2],event.jetAK4_cemf[2],event.jetAK4_csv[2],bool(event.jetAK4_IDTight[2]),
		  event.MET_et[0],event.MET_sumEt[0],
		  event.EVENT_event,event.EVENT_run,event.EVENT_lumiBlock,
		  event.passFilter_HBHE,event.passFilter_HBHEIso,event.passFilter_EEBadSc,event.passFilter_globalTightHalo2016,event.passFilter_GoodVtx,event.passFilter_ECALDeadCell,event.passFilter_chargedHadronTrackResolution,event.passFilter_muonBadTrack,
	          ]
       if "QCD" in name:
         while len(event.genJetAK4_pt)<3:
           event.genJetAK4_pt.push_back(-1)
           event.genJetAK4_eta.push_back(-1)
           event.genJetAK4_phi.push_back(-1)
           event.genJetAK4_mass.push_back(-1)
         while len(event.jetAK4_genParton_pdgID1)<3:
           event.jetAK4_genParton_pdgID1.push_back(-1)
           event.jetAK4_genParton_pdgID2.push_back(-1)

         values+=[event.genJetAK4_pt[0],event.genJetAK4_eta[0],event.genJetAK4_phi[0],event.genJetAK4_mass[0],
                  event.jetAK4_genParton_pdgID1[0],
		  event.genJetAK4_pt[1],event.genJetAK4_eta[1],event.genJetAK4_phi[1],event.genJetAK4_mass[1],
                  event.jetAK4_genParton_pdgID2[1],
		  event.genJetAK4_pt[2],event.genJetAK4_eta[2],event.genJetAK4_phi[2],event.genJetAK4_mass[2],
                  event.jetAK4_genParton_pdgID2[2],
		  event.genWeight,
                 ]
       #print "saving",len(values),"vars"

       HLT_isFired.clear()
       for pair in event.HLT_isFired:
          HLT_isFired.insert(pair)
       tree.Fill(array.array("f",[float(value) for value in values]))

       if not event.passFilter_HBHE or not event.passFilter_CSCHalo or not event.passFilter_GoodVtx or not event.passFilter_EEBadSc: continue
       if len(event.jetAK4_pt)<2 or event.jetAK4_pt[0]<100 or event.jetAK4_pt[1]<100 or abs(event.jetAK4_eta[0])>3 or abs(event.jetAK4_eta[1])>3: continue
       if not bool(event.jetAK4_IDTight[0]) or not bool(event.jetAK4_IDTight[1]): continue

       scales=[1]
       if doJES:
          scales+=[s+"_Up" for s in JECsources]
          scales+=[s for s in JECsources]
       irec=0
       for scale in scales:
         jet1=TLorentzVector()
         jet2=TLorentzVector()
         jet1.SetPtEtaPhiM(event.jetAK4_pt[0],event.jetAK4_eta[0],event.jetAK4_phi[0],event.jetAK4_mass[0])
         jet2.SetPtEtaPhiM(event.jetAK4_pt[1],event.jetAK4_eta[1],event.jetAK4_phi[1],event.jetAK4_mass[1])
         mjj=(jet1+jet2).M()
         chi=exp(abs(jet1.Rapidity()-jet2.Rapidity()))
         yboost=abs(jet1.Rapidity()+jet2.Rapidity())/2.
         if mjj<1500 or chi>16. or yboost>1.11: continue
         if scale!=1:
           jes=JESuncertainties[scale.replace("_Up","")]
           jes.setJetPt(jet1.Pt())
           jes.setJetEta(jet1.Eta())
	   if scale[-1]=="p":
             jet1*=1.+jes.getUncertainty(True)
	   else:
             jet1*=1.-jes.getUncertainty(False)
           jes.setJetPt(jet2.Pt())
           jes.setJetEta(jet2.Eta())
	   if scale[-1]=="p":
             jet2*=1.+jes.getUncertainty(True)
	   else:
             jet2*=1.-jes.getUncertainty(False)
           mjj=(jet1+jet2).M()
         for massbin in massbins:
           if yboost<1.11 and mjj>=massbin[0] and mjj<massbin[1]:
             plots[irec].Fill(chi)
           irec+=1
         if scale==1:
           if yboost<1.11 and chi<16:
             plots[irec].Fill(mjj)
           irec+=1
       #if not "data" in sample and len(event.genJetAK4_pt)>=2:
       #  genJet1=TLorentzVector()
       #  genJet2=TLorentzVector()
       #  genJet1.SetPtEtaPhiM(event.genJetAK4_pt[0],event.genJetAK4_eta[0],event.genJetAK4_phi[0],event.genJetAK4_mass[0])
       #  genJet2.SetPtEtaPhiM(event.genJetAK4_pt[1],event.genJetAK4_eta[1],event.genJetAK4_phi[1],event.genJetAK4_mass[1])
       #  genmjj=(genJet1+genJet2).M()
       #  genchi=exp(abs(genJet1.Rapidity()-genJet2.Rapidity()))
       #  genyboost=abs(genJet1.Rapidity()+genJet2.Rapidity())/2.
       #  igen=0
       #  for massbin in massbins:
       #    if genyboost<1.11 and genmjj>=massbin[0] and genmjj<massbin[1]:
	#     genplots[igen].Fill(genchi)
  	#   igen+=1
        # if genyboost<1.11 and genchi<16:
        #   genplots[igen].Fill(genmjj)
        # igen+=1
     fil.Close()

    print "analyzed",event_count,"events"
    #if event_count>0:
    #  for plot in plots:
    #    plot.Scale(factor/event_count)
    #  for plot in genplots:
    #    plot.Scale(factor/event_count)
    return (plots,genplots,event_count)

if __name__ == '__main__':

    wait=False
 
    prefix="datacard_shapelimit13TeV_25nsData10"
    chi_bins=[(1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              ]
    massbins=[(1900,2400),
              (2400,3000),
              (3000,3600),
              (3600,4200),
              (4200,4800),
              (4800,5400),
              (5400,6000),
	      (2400,13000),
	      (3000,13000),
	      (3600,13000),
	      (4200,13000),
	      (4800,13000),
	      (5400,13000),
	      (6000,13000),
              ]
 
    samples=[("data_obs",[("JetHT_25ns_data10.txt",1.)]),
             #("QCD",[("QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6.txt",1.)])
             #("QCD",[("QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8.txt",0.000165),
             #  ("QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8.txt",0.006830),
             #  ("QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8.txt",0.114943),
             #  ("QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8.txt",0.842650),
             #  ("QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8.txt",9.4183),
             #  ("QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8.txt",32.293),
             #  ("QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8.txt",186.9),
             #  ("QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8.txt",648.2),
             #  ("QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8.txt",7823.0)],)
            ]
 
    chi_binnings=[]
    for mass_bin in chi_bins:
        chi_binnings+=[array.array('d')]
        for chi_bin in mass_bin:
            chi_binnings[-1].append(chi_bin)
        
    print prefix, samples

    nevents={}
    counter=0
    for name,files in samples:
      filelist=open(files[0][0])
      for line in filelist.readlines():

        if not ".root" in line: continue
        counter+=1
	if len(sys.argv)>1 and sys.argv[1]!=str(counter): continue
	print counter
	
	if os.path.isfile("/afs/cern.ch/user/h/hinzmann/workspace/public/chi_analysis/"+prefix + '_chi'+str(counter)+'_tree.root'):
	  print "skipping",counter,"because tree file exists"
	  continue

        plots=[]
        genplots=[]
  	outtree=TFile("/afs/cern.ch/user/h/hinzmann/workspace/public/chi_analysis/"+prefix + '_chi'+str(counter)+'_tree.root','RECREATE')
	varnames=["jetAK4_pt1","jetAK4_eta1","jetAK4_phi1","jetAK4_mass1",
	          "jetAK4_jec1","jetAK4_muf1","jetAK4_phf1","jetAK4_emf1","jetAK4_nhf1","jetAK4_chf1","jetAK4_area1","jetAK4_cm1","jetAK4_nm1","jetAK4_hof1","jetAK4_chm1","jetAK4_neHadMult1","jetAK4_phoMult1","jetAK4_nemf1","jetAK4_cemf1","jetAK4_csv1","jetAK4_IDTight1",
	          "jetAK4_pt2","jetAK4_eta2","jetAK4_phi2","jetAK4_mass2",
	          "jetAK4_jec2","jetAK4_muf2","jetAK4_phf2","jetAK4_emf2","jetAK4_nhf2","jetAK4_chf2","jetAK4_area2","jetAK4_cm2","jetAK4_nm2","jetAK4_hof2","jetAK4_chm2","jetAK4_neHadMult2","jetAK4_phoMult2","jetAK4_nemf2","jetAK4_cemf2","jetAK4_csv2","jetAK4_IDTight2",
	          "jetAK4_pt3","jetAK4_eta3","jetAK4_phi3","jetAK4_mass3",
	          "jetAK4_jec3","jetAK4_muf3","jetAK4_phf3","jetAK4_emf3","jetAK4_nhf3","jetAK4_chf3","jetAK4_area3","jetAK4_cm3","jetAK4_nm3","jetAK4_hof3","jetAK4_chm3","jetAK4_neHadMult3","jetAK4_phoMult3","jetAK4_nemf3","jetAK4_cemf3","jetAK4_csv3","jetAK4_IDTight3",
		  "MET_et","MET_sumEt",
		  "EVENT_event","EVENT_run","EVENT_lumiBlock",
		  "passFilter_HBHE","passFilter_HBHEIso","passFilter_EEBadSc","passFilter_globalTightHalo2016","passFilter_GoodVtx","passFilter_ECALDeadCell","passFilter_chargedHadronTrackResolution","passFilter_muonBadTrack",
	          ]
	if "QCD" in name:
	  varnames+=[
	          "genJetAK4_pt1","genJetAK4_eta1","genJetAK4_phi1","genJetAK4_mass1",
                  "jetAK4_genParton_pdgID1",
		  "genJetAK4_pt2","genJetAK4_eta2","genJetAK4_phi2","genJetAK4_mass2",
                  "jetAK4_genParton_pdgID2",
		  "genJetAK4_pt3","genJetAK4_eta3","genJetAK4_phi3","genJetAK4_mass3",
                  "jetAK4_genParton_pdgID3",
		  "genWeight"
	          ]
	tree=TNtuple("tree","tree",":".join(varnames))
	HLT_isFired=std.map("string","bool")()
	tree.Branch("HLT_isFired","map<string,bool>",HLT_isFired)
	print len(varnames),"vars to save"

	plots+=[[]]
  	genplots+=[[]]
  	plot,genplot,nevent=createPlotsAndTree(line.strip(),name,massbins,1.,tree,HLT_isFired)
	plots[-1]+=plot
  	genplots[-1]+=genplot
  	nevents[name]=nevent
        
	outtree.Write()
	
  	out=TFile(prefix + '_chi'+str(counter)+'.root','RECREATE')
  	#for i in range(len(samples)):
	i=0
  	for j in range(len(massbins)):
  	    print "number of "+samples[i][0]+" jet events expected in",str(massbins[j][0])+"<m_{jj}<"+str(massbins[j][1])+" GeV:",plots[i][j].Integral()
  	    print "number of "+samples[i][0]+" genjet events expected in",str(massbins[j][0])+"<m_{jj}<"+str(massbins[j][1])+" GeV:",genplots[i][j].Integral()
  	    #print "mass: number of "+samples[i][0]+" events expected in",str(massbins[j][0])+"<m_{jj}<"+str(massbins[j][1])+" GeV:",plots[i][len(massbins)].Integral(plots[i][len(massbins)].FindBin(massbins[j][0]),plots[i][len(massbins)].FindBin(massbins[j][1]))
  	    if "chi" in plots[i][j].GetName():
  	      plots[i][j]=plots[i][j].Rebin(len(chi_binnings[j])-1,plots[i][j].GetName()+"_rebin1",chi_binnings[j])
  	      clone=plots[i][j]
  	      clone.Write()
  	    if "chi" in genplots[i][j].GetName():
  	      genplots[i][j]=genplots[i][j].Rebin(len(chi_binnings[j])-1,genplots[i][j].GetName()+"_rebin1",chi_binnings[j])
  	      clone=genplots[i][j]
  	      clone.Write()
  	if doJES:
  	   for j in range(len(massbins)+1,len(massbins)+1+2*len(massbins)*len(JECsources)):
  	    if "chi" in plots[i][j].GetName():
  	      plots[i][j]=plots[i][j].Rebin(len(chi_binnings[(j-1)%len(chi_binnings)])-1,plots[i][j].GetName()+"_rebin1",chi_binnings[(j-1)%len(chi_binnings)])
  	      clone=plots[i][j]
  	      clone.Write()

  	#for i in range(len(samples)):
	i=0
  	for j in range(len(massbins)):
  	    if plots[i][j].Integral()>0:
  	      plots[i][j].Scale(1./plots[i][j].Integral())
  	    for b in range(plots[i][j].GetXaxis().GetNbins()):
  	      plots[i][j].SetBinContent(b+1,plots[i][j].GetBinContent(b+1)/plots[i][j].GetBinWidth(b+1))
  	      plots[i][j].SetBinError(b+1,plots[i][j].GetBinError(b+1)/plots[i][j].GetBinWidth(b+1))
  	    plots[i][j].GetYaxis().SetRangeUser(0,0.2)
  	    if genplots[i][j].Integral()>0:
  	      genplots[i][j].Scale(1./genplots[i][j].Integral())
  	    for b in range(genplots[i][j].GetXaxis().GetNbins()):
  	      genplots[i][j].SetBinContent(b+1,genplots[i][j].GetBinContent(b+1)/genplots[i][j].GetBinWidth(b+1))
  	      genplots[i][j].SetBinError(b+1,genplots[i][j].GetBinError(b+1)/genplots[i][j].GetBinWidth(b+1))
  	    genplots[i][j].GetYaxis().SetRangeUser(0,0.2)
  	if doJES:
  	   for j in range(len(massbins)+1,len(massbins)+1+2*len(massbins)*len(JECsources)):
  	    if plots[i][j].Integral()>0:
  	      plots[i][j].Scale(1./plots[i][j].Integral())
  	    for b in range(plots[i][j].GetXaxis().GetNbins()):
  	      plots[i][j].SetBinContent(b+1,plots[i][j].GetBinContent(b+1)/plots[i][j].GetBinWidth(b+1))
  	      plots[i][j].SetBinError(b+1,plots[i][j].GetBinError(b+1)/plots[i][j].GetBinWidth(b+1))
  	    plots[i][j].GetYaxis().SetRangeUser(0,0.2)

  	canvas = TCanvas("","",0,0,400,200)
  	canvas.Divide(2,1)
  	if len(massbins)>4:
  	  canvas = TCanvas("","",0,0,600,400)
  	  canvas.Divide(3,2)
  	elif len(massbins)>2:
  	  canvas = TCanvas("","",0,0,400,400)
  	  canvas.Divide(2,2)

  	legends=[]
  	color=[1,2,4,6,7,8,9]
  	for j in range(len(massbins)):
  	  canvas.cd(j+1)
  	  plots[0][j].Draw("he")
  	  legend1=TLegend(0.6,0.6,0.9,0.9,(str(massbins[j][0])+"<m_{jj}<"+str(massbins[j][1])+" GeV"))
  	  legends+=[legend1]
  	  legend1.AddEntry(plots[0][j],samples[0][0],"l")
  	  for i in range(1,len(samples)):
  	    plots[i][j].SetLineColor(color[i])
  	    plots[i][j].Draw("hesame")
  	    legend1.AddEntry(plots[i][j],samples[i][0],"l")
  	  legend1.SetTextSize(0.04)
  	  legend1.SetFillStyle(0)
  	  legend1.Draw("same")

  	canvas.SaveAs(prefix + '_chi'+str(counter)+'.pdf')
  	canvas.SaveAs(prefix + '_chi'+str(counter)+'.eps')
  	if wait:
  	    os.system("ghostview "+prefix + '_chi'+str(counter)+'.eps')

  	canvas = TCanvas("","",0,0,200,200)
  	canvas.SetLogy()

  	legends=[]
  	plots[0][len(massbins)].Draw("he")
  	plots[0][len(massbins)].GetXaxis().SetRangeUser(0,5000)
  	legend1=TLegend(0.6,0.6,0.9,0.9)
  	legends+=[legend1]
  	legend1.AddEntry(plots[0][len(massbins)],samples[0][0],"l")
  	for i in range(1,len(samples)):
  	  plots[i][len(massbins)].Scale(plots[0][len(massbins)].Integral()/plots[i][len(massbins)].Integral())
  	  plots[i][len(massbins)].SetLineColor(color[i])
  	  plots[i][len(massbins)].Draw("hesame")
  	  legend1.AddEntry(plots[i][len(massbins)],samples[i][0],"l")
  	legend1.SetTextSize(0.04)
  	legend1.SetFillStyle(0)
  	legend1.Draw("same")

  	canvas.SaveAs(prefix + '_mass'+str(counter)+'.pdf')
  	canvas.SaveAs(prefix + '_mass'+str(counter)+'.eps')
  	if wait:
  	    os.system("ghostview "+prefix + '_mass'+str(counter)+'.eps')

        out.Write()
        out.Close()
        outtree.Close()
