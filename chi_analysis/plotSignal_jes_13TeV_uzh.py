import os, sys
from ROOT import * 
from DataFormats.FWLite import Events,Handle
import array
from math import *

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

doJES=True

if doJES:
  gROOT.ProcessLine(".L /mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_4_7_patch2/src/CondFormats/JetMETObjects/src/Utilities.cc+");
  gROOT.ProcessLine(".L /mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_4_7_patch2/src/CondFormats/JetMETObjects/src/JetCorrectorParameters.cc+");
  gROOT.ProcessLine(".L /mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_4_7_patch2/src/CondFormats/JetMETObjects/src/SimpleJetCorrectionUncertainty.cc+");
  gROOT.ProcessLine(".L /mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_4_7_patch2/src/CondFormats/JetMETObjects/src/JetCorrectionUncertainty.cc+");

  JECsources = ["AbsoluteStat", "AbsoluteScale", "AbsoluteFlavMap", "AbsoluteMPFBias", "Fragmentation",
"SinglePionECAL", "SinglePionHCAL",
"FlavorQCD", "TimePtEta",
"RelativeJEREC1", "RelativeJEREC2", "RelativeJERHF",
"RelativePtBB","RelativePtEC1", "RelativePtEC2", "RelativePtHF", "RelativeBal", "RelativeFSR",
"RelativeStatFSR", "RelativeStatEC", "RelativeStatHF",
"PileUpPtRef", "PileUpPtBB", "PileUpPtEC1", "PileUpPtEC2", "PileUpPtHF","PileUpMuZero", "PileUpEnvelope",
#"SubTotalPileUp","SubTotalRelative","SubTotalPt","SubTotalScale","SubTotalAbsolute","SubTotalMC",
"Total",
#"TotalNoFlavor","TotalNoTime","TotalNoFlavorNoTime",
#"FlavorZJet","FlavorPhotonJet","FlavorPureGluon","FlavorPureQuark","FlavorPureCharm","FlavorPureBottom"
#"TimeRunBCD", "TimeRunEF", "TimeRunG", "TimeRunH",
  ]

  JESuncertainties={}
  for source in JECsources:
    #p = JetCorrectorParameters("/shome/hinzmann/Fall15/CMSSW_7_6_3_patch2/src/EXOVVNtuplizerRunII/Ntuplizer/JEC/Summer15_25nsV7_DATA_UncertaintySources_AK4PFchs.txt", source)
    #p = JetCorrectorParameters("/shome/hinzmann/Fall15/CMSSW_7_6_3_patch2/src/EXOVVNtuplizerRunII/Ntuplizer/JEC/Spring16_25nsV8BCD_DATA_UncertaintySources_AK4PFchs.txt", source)
    p = JetCorrectorParameters("/mnt/t3nfs01/data01/shome/hinzmann/CMSSW_8_0_21/src/EXOVVNtuplizerRunII/Ntuplizer/JEC/Summer16_23Sep2016V3_MC_UncertaintySources_AK4PFchs.txt", source)
    JESuncertainties[source]=JetCorrectionUncertainty(p)


def createPlots(sample,prefix,xsec,massbins):
    files=[]
    if sample.endswith(".txt"):
        filelist=open(sample)
	for line in filelist.readlines():
	    if ".root" in line:
	        files+=[line.strip()]
    else:
        folders=os.listdir("/pnfs/psi.ch/cms/trivcat/store/user/hinzmann/dijet_angular/")
	for folder in folders:
	  if sample in folder:
            files+=["dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/user/hinzmann/dijet_angular/"+folder+"/GEN.root"]
	    #break
#        files=["dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/user/hinzmann/dijet_angular/jobtmp_"+sample+"-0/GEN.root"]

    prunedgenjets_handle=Handle("std::vector<reco::GenJet>")
    prunedgenjets_label="ak4GenJets"

    plots=[]
    for massbin in massbins:
      plots += [TH1F(prefix+'#chi'+str(massbin).strip("()").replace(',',"_").replace(' ',""),';#chi;N',15,1,16)]
      #plots += [TH1F(prefix+'y_{boost}'+str(massbin).strip("()").replace(',',"_").replace(' ',""),';y_{boost};N',20,0,2)]
    if doJES:
      for source in JECsources:
       for massbin in massbins:
        plots += [TH1F(prefix+'#chi'+str(massbin).strip("()").replace(',',"_").replace(' ',"")+source+"Up",';#chi;N',15,1,16)]
       for massbin in massbins:
        plots += [TH1F(prefix+'#chi'+str(massbin).strip("()").replace(',',"_").replace(' ',"")+source+"Down",';#chi;N',15,1,16)]
    
    for plot in plots:
        plot.Sumw2()

    event_count=0
    events=TChain('Events')
    for f in files[:]:
      events.Add(f)
    
    nevents=events.GetEntries()
    print sample,nevents,xsec

    for event in events:
       if event_count>10000000:break
       #if event_count>100:break
       
       event_count+=1
       if event_count%10000==1: print "event",event_count

       if len(event.recoGenJets_ak4GenJets__GEN.product())<2: continue
       if event.recoGenJets_ak4GenJets__GEN.product()[0].pt()<100 or event.recoGenJets_ak4GenJets__GEN.product()[1].pt()<100 or abs(event.recoGenJets_ak4GenJets__GEN.product()[0].eta())>3 or abs(event.recoGenJets_ak4GenJets__GEN.product()[1].eta())>3: continue
       
       scales=[1]
       if doJES:
          scales+=[s+"_Up" for s in JECsources]
          scales+=[s for s in JECsources]
       irec=0
       for scale in scales:
         jet1=TLorentzVector()
         jet2=TLorentzVector()
         jet1.SetPtEtaPhiM(event.recoGenJets_ak4GenJets__GEN.product()[0].pt(),event.recoGenJets_ak4GenJets__GEN.product()[0].eta(),event.recoGenJets_ak4GenJets__GEN.product()[0].phi(),event.recoGenJets_ak4GenJets__GEN.product()[0].mass())
         jet2.SetPtEtaPhiM(event.recoGenJets_ak4GenJets__GEN.product()[1].pt(),event.recoGenJets_ak4GenJets__GEN.product()[1].eta(),event.recoGenJets_ak4GenJets__GEN.product()[1].phi(),event.recoGenJets_ak4GenJets__GEN.product()[1].mass())
         mjj=(jet1+jet2).M()
         chi=exp(abs(jet1.Rapidity()-jet2.Rapidity()))
         yboost=abs(jet1.Rapidity()+jet2.Rapidity())/2.
         if mjj>1500 and chi<16. and yboost<1.11 and scale!=1:
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

    #jets="recoGenJets_ak4GenJets__GEN.obj"
    #yboost='abs('+jets+'[0].y()+'+jets+'[1].y())/2.'
    #chi='exp(abs('+jets+'[0].y()-'+jets+'[1].y()))'
    #mass='sqrt(pow('+jets+'[0].energy()+'+jets+'[1].energy(),2)-pow('+jets+'[0].px()+'+jets+'[1].px(),2)-pow('+jets+'[0].py()+'+jets+'[1].py(),2)-pow('+jets+'[0].pz()+'+jets+'[1].pz(),2))'
    #for massbin in massbins:
    #  events.Project(prefix+'#chi'+str(massbin).strip("()").replace(',',"_").replace(' ',""),chi,'('+yboost+'<1.11)*('+mass+'>='+str(massbin[0])+')*('+mass+'<'+str(massbin[1])+')')
    #  #events.Project(prefix+'y_{boost}'+str(massbin).strip("()").replace(',',"_").replace(' ',""),yboost,'('+chi+'<16)*('+mass+'>='+str(massbin[0])+')*('+mass+'<='+str(massbin[1])+')')
    for plot in plots:
      if nevents>0:
        plot.Scale(xsec/nevents)
    return plots

if __name__ == '__main__':
    wait=False
    name="QCD"
    #name="QCDCIplusLL10000"
    bin=6 #1-6
    prefix="datacard_shapelimit13TeV_"+name+"_JESvRerecoV3"+str(bin)
 
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
              (6000,6600),
	      (2400,13000),
	      (3000,13000),
	      (3600,13000),
	      (4200,13000),
	      (4800,13000),
	      (5400,13000),
	      (6000,13000),
	      (6600,13000),
              ]

    if bin==1 and name=="QCD": 
      samples=[("QCD",[("pythia8_ci_m4300_13000_50000_1_0_0_13TeV_Nov14",3.507e-09),
		       ]),
	    ]
    if bin==2 and name=="QCD":
      samples=[("QCD",[("pythia8_ci_m3800_4300_50000_1_0_0_13TeV_Nov14",5.867e-09),
		       ]),
	    ]
    if bin==3 and name=="QCD":
      samples=[("QCD",[("pythia8_ci_m3300_3800_50000_1_0_0_13TeV_Nov14",1.863e-08),
		       ]),
	    ]
    if bin==4 and name=="QCD":
      samples=[("QCD",[("pythia8_ci_m2800_3300_50000_1_0_0_13TeV_Nov14",6.446e-08),
		       ]),
	    ]
    if bin==5 and name=="QCD":
      samples=[("QCD",[("pythia8_ci_m2400_2800_50000_1_0_0_13TeV_Nov14",1.649e-07),
		       ]),
	    ]
    if bin==6 and name=="QCD":
      samples=[("QCD",[("pythia8_ci_m1900_2400_50000_1_0_0_13TeV_Nov14",8.836e-07),
		       ]),
	    ]
    if bin==7 and name=="QCD": 
      samples=[("QCD",[("pythia8_ci_m1500_1900_50000_1_0_0_13TeV_Nov14",3.307e-06),
		       ]),
	    ]

    if bin==1 and name=="QCDCIplusLL10000": 
      samples=[("QCDCIplusLL10000",[("pythia8_ci_m4300_13000_10000_1_0_0_13TeV_Nov14",3.507e-09),
		       ]),
	    ]
    if bin==2 and name=="QCDCIplusLL10000":
      samples=[("QCDCIplusLL10000",[("pythia8_ci_m3800_4300_10000_1_0_0_13TeV_Nov14",5.867e-09),
		       ]),
	    ]
    if bin==3 and name=="QCDCIplusLL10000":
      samples=[("QCDCIplusLL10000",[("pythia8_ci_m3300_3800_10000_1_0_0_13TeV_Nov14",1.863e-08),
		       ]),
	    ]
    if bin==4 and name=="QCDCIplusLL10000":
      samples=[("QCDCIplusLL10000",[("pythia8_ci_m2800_3300_10000_1_0_0_13TeV_Nov14",6.446e-08),
		       ]),
	    ]
    if bin==5 and name=="QCDCIplusLL10000":
      samples=[("QCDCIplusLL10000",[("pythia8_ci_m2400_2800_10000_1_0_0_13TeV_Nov14",1.649e-07),
		       ]),
	    ]
    if bin==6 and name=="QCDCIplusLL10000":
      samples=[("QCDCIplusLL10000",[("pythia8_ci_m1900_2400_10000_1_0_0_13TeV_Nov14",8.836e-07),
		       ]),
	    ]
    if bin==7 and name=="QCDCIplusLL10000": 
      samples=[("QCDCIplusLL10000",[("pythia8_ci_m1500_1900_10000_1_0_0_13TeV_Nov14",3.307e-06),
		       ]),
	    ]
    xsecs=eval(open("xsecs_13TeV.txt").readline())
    print xsecs

    chi_binnings=[]
    for mass_bin in chi_bins:
        chi_binnings+=[array.array('d')]
        for chi_bin in mass_bin:
            chi_binnings[-1].append(chi_bin)
        
    if len(sys.argv)>1:
        newsamples=[]
        for sample in samples:
          found=False
	  for arg in sys.argv:
	    if sample[0]==arg or sample[0]=="QCD":
	        newsamples+=[sample]
		break
	samples=newsamples
	if samples[-1][0]=="QCD":
            prefix+="_"+samples[-1][0]
        else:
	    prefix+="_"+samples[-1][0].replace("QCD","")
  
    print prefix, samples

    plots=[]
    for name,files in samples:
      plots+=[[]]
      i=0
      for filename,xsec in files:
        i+=1
        ps=createPlots(filename,name,float(xsecs[filename]),massbins)
        if i==1:
          plots[-1]+=ps
	else:
	  for i in range(len(plots[-1])):
            plots[-1][i].Add(ps[i])

    out=TFile(prefix + '_chi.root','RECREATE')
    for j in range(len(massbins)):
      for i in range(len(samples)):
        #if plots[i][j].Integral()>0:
        #  plots[i][j].Scale(expectedevents[j]/plots[i][j].Integral())
        plots[i][j]=plots[i][j].Rebin(len(chi_binnings[j])-1,plots[i][j].GetName()+"_rebin1",chi_binnings[j])
	if samples[i][0]=="QCD":
	   # data
	   plots[i][j].Write(plots[i][j].GetName().replace("QCD","data_obs"))
	   # ALT
	   clone=plots[i][j].Clone(plots[i][j].GetName().replace("QCD",samples[-1][0]+"_ALT"))
	   clone.Write()
	   # QCD
           plots[i][j].Scale(1e-10)
           plots[i][j].Write()
	   # QCD backup
	   clonebackup=plots[i][j].Clone(plots[i][j].GetName()+"_backup")
	   clonebackup.Write()
	else:
	   # signal
	   clone=plots[i][j]
	   clone.Write()
	   # signal backup
	   clonebackup=plots[i][j].Clone(plots[i][j].GetName()+"_backup")
	   clonebackup.Write()
    if doJES:
     for j in range(len(massbins),len(massbins)+2*len(massbins)*len(JECsources)):
      for i in range(len(samples)):
        plots[i][j]=plots[i][j].Rebin(len(chi_binnings[j%len(massbins)])-1,plots[i][j].GetName()+"_rebin1",chi_binnings[j%len(massbins)])
	if samples[i][0]=="QCD":
	   # QCD
	   clone=plots[i][j]
	   clone.Write()
	   # QCD backup
	   clonebackup=plots[i][j].Clone(plots[i][j].GetName()+"_backup")
	   clonebackup.Write()
	else:
	   # signal
	   clone=plots[i][j]
	   clone.Write()
	   # signal backup
	   clonebackup=plots[i][j].Clone(plots[i][j].GetName()+"_backup")
	   clonebackup.Write()

    for j in range(len(massbins)):
      for i in range(len(samples)):
        if plots[i][j].Integral()>0:
          plots[i][j].Scale(1./plots[i][j].Integral())
        for b in range(plots[i][j].GetXaxis().GetNbins()):
          plots[i][j].SetBinContent(b+1,plots[i][j].GetBinContent(b+1)/plots[i][j].GetBinWidth(b+1))
          plots[i][j].SetBinError(b+1,plots[i][j].GetBinError(b+1)/plots[i][j].GetBinWidth(b+1))
        plots[i][j].GetYaxis().SetRangeUser(0,0.2)

    canvas = TCanvas("","",0,0,400,200)
    canvas.Divide(2,1)
    if len(massbins)>2:
      canvas = TCanvas("","",0,0,600,400)
      canvas.Divide(3,2)

    legends=[]
    for j in range(len(massbins)):
      canvas.cd(j+1)
      plots[0][j].Draw("he")
      print "number of events passed:",plots[0][j].GetEntries()
      legend1=TLegend(0.6,0.6,0.9,0.9,(str(massbins[j][0])+"<m_{jj}<"+str(massbins[j][1])+" GeV").replace("4800<m_{jj}<13000","m_{jj}>4800"))
      legends+=[legend1]
      legend1.AddEntry(plots[0][j],samples[0][0],"l")
      for i in range(1,len(samples)):
        plots[i][j].SetLineColor(i+2)
        plots[i][j].Draw("hesame")
        legend1.AddEntry(plots[i][j],samples[i][0],"l")
      legend1.SetTextSize(0.04)
      legend1.SetFillStyle(0)
      legend1.Draw("same")

    canvas.SaveAs(prefix + '_chi.pdf')
    canvas.SaveAs(prefix + '_chi.eps')
    if wait:
        os.system("ghostview "+prefix + '_chi.eps')

