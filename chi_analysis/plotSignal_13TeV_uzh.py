import os, sys
from ROOT import * 
from DataFormats.FWLite import Events,Handle
import array

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
    
    for plot in plots:
        plot.Sumw2()

    event_count=0
    events=TChain('Events')
    for f in files[:]:
      events.Add(f)
    
    nevents=events.GetEntries()
    print sample,nevents,xsec
    jets="recoGenJets_ak4GenJets__GEN.obj"
    yboost='abs('+jets+'[0].y()+'+jets+'[1].y())/2.'
    chi='exp(abs('+jets+'[0].y()-'+jets+'[1].y()))'
    mass='sqrt(pow('+jets+'[0].energy()+'+jets+'[1].energy(),2)-pow('+jets+'[0].px()+'+jets+'[1].px(),2)-pow('+jets+'[0].py()+'+jets+'[1].py(),2)-pow('+jets+'[0].pz()+'+jets+'[1].pz(),2))'
    for massbin in massbins:
      events.Project(prefix+'#chi'+str(massbin).strip("()").replace(',',"_").replace(' ',""),chi,'('+yboost+'<1.11)*('+mass+'>='+str(massbin[0])+')*('+mass+'<'+str(massbin[1])+')')
      #events.Project(prefix+'y_{boost}'+str(massbin).strip("()").replace(',',"_").replace(' ',""),yboost,'('+chi+'<16)*('+mass+'>='+str(massbin[0])+')*('+mass+'<='+str(massbin[1])+')')
    for plot in plots:
      if nevents>0:
        plot.Scale(xsec/nevents)
    return plots

if __name__ == '__main__':

    wait=False
 
    prefix="datacard_shapelimit13TeV_GENherwigv3"
 
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
 
    samples2=[("QCD",[("pythia8_ci_m1000_1500_50000_1_0_0_13TeV_Nov14",3.769e-05),
		       ("pythia8_ci_m1500_1900_50000_1_0_0_13TeV_Nov14",3.307e-06),
		       ("pythia8_ci_m1900_2400_50000_1_0_0_13TeV_Nov14",8.836e-07),
		       ("pythia8_ci_m2400_2800_50000_1_0_0_13TeV_Nov14",1.649e-07),
		       ("pythia8_ci_m2800_3300_50000_1_0_0_13TeV_Nov14",6.446e-08),
		       ("pythia8_ci_m3300_3800_50000_1_0_0_13TeV_Nov14",1.863e-08),
		       ("pythia8_ci_m3800_4300_50000_1_0_0_13TeV_Nov14",5.867e-09),
		       ("pythia8_ci_m4300_13000_50000_1_0_0_13TeV_Nov14",3.507e-09),
		       ]),
	    ]
    samples2=[("QCDNonPert",[("pythia8_ciNonPert_m1000_1500_50000_1_0_0_13TeV_Nov14",3.769e-05),
		       ("pythia8_ciNonPert_m1500_1900_50000_1_0_0_13TeV_Nov14",3.307e-06),
		       ("pythia8_ciNonPert_m1900_2400_50000_1_0_0_13TeV_Nov14",8.836e-07),
		       ("pythia8_ciNonPert_m2400_2800_50000_1_0_0_13TeV_Nov14",1.649e-07),
		       ("pythia8_ciNonPert_m2800_3300_50000_1_0_0_13TeV_Nov14",6.446e-08),
		       ("pythia8_ciNonPert_m3300_3800_50000_1_0_0_13TeV_Nov14",1.863e-08),
		       ("pythia8_ciNonPert_m3800_4300_50000_1_0_0_13TeV_Nov14",5.867e-09),
		       ("pythia8_ciNonPert_m4300_13000_50000_1_0_0_13TeV_Nov14",3.507e-09),
		       ]),
	    ]
    samples=[("QCDHerwig",[("herwigpp_qcd_m1000_1500___13TeV_Nov28",3.769e-05),
		       ("herwigpp_qcd_m1500_1900___13TeV_Nov28",3.307e-06),
		       ("herwigpp_qcd_m1900_2400___13TeV_Nov28",8.836e-07),
		       ("herwigpp_qcd_m2400_2800___13TeV_Nov28",1.649e-07),
		       ("herwigpp_qcd_m2800_3300___13TeV_Nov28",6.446e-08),
		       ("herwigpp_qcd_m3300_3800___13TeV_Nov28",1.863e-08),
		       ("herwigpp_qcd_m3800_4300___13TeV_Nov28",5.867e-09),
		       ("herwigpp_qcd_m4300_13000___13TeV_Nov28",3.507e-09),
		       ]),
	    ]
    samples2=[("QCDHerwigNonPert",[("herwigpp_qcdNonPert_m1000_1500___13TeV_Nov28",3.769e-05),
		       ("herwigpp_qcdNonPert_m1500_1900___13TeV_Nov28",3.307e-06),
		       ("herwigpp_qcdNonPert_m1900_2400___13TeV_Nov28",8.836e-07),
		       ("herwigpp_qcdNonPert_m2400_2800___13TeV_Nov28",1.649e-07),
		       ("herwigpp_qcdNonPert_m2800_3300___13TeV_Nov28",6.446e-08),
		       ("herwigpp_qcdNonPert_m3300_3800___13TeV_Nov28",1.863e-08),
		       ("herwigpp_qcdNonPert_m3800_4300___13TeV_Nov28",5.867e-09),
		       ("herwigpp_qcdNonPert_m4300_13000___13TeV_Nov28",3.507e-09),
		       ]),
	    ]
    samples2=[("QCDCIplusLL8000",[("pythia8_ci_m1500_1900_8000_1_0_0_13TeV_Nov14",3.307e-06),
		       ("pythia8_ci_m1900_2400_8000_1_0_0_13TeV_Nov14",8.836e-07),
		       ("pythia8_ci_m2400_2800_8000_1_0_0_13TeV_Nov14",1.649e-07),
		       ("pythia8_ci_m2800_3300_8000_1_0_0_13TeV_Nov14",6.446e-08),
		       ("pythia8_ci_m3300_3800_8000_1_0_0_13TeV_Nov14",1.863e-08),
		       ("pythia8_ci_m3800_4300_8000_1_0_0_13TeV_Nov14",5.867e-09),
		       ("pythia8_ci_m4300_13000_8000_1_0_0_13TeV_Nov14",3.507e-09),
		       ]),
             ("QCDCIplusLL9000",[("pythia8_ci_m1500_1900_9000_1_0_0_13TeV_Nov14",3.307e-06),
		       ("pythia8_ci_m1900_2400_9000_1_0_0_13TeV_Nov14",8.836e-07),
		       ("pythia8_ci_m2400_2800_9000_1_0_0_13TeV_Nov14",1.649e-07),
		       ("pythia8_ci_m2800_3300_9000_1_0_0_13TeV_Nov14",6.446e-08),
		       ("pythia8_ci_m3300_3800_9000_1_0_0_13TeV_Nov14",1.863e-08),
		       ("pythia8_ci_m3800_4300_9000_1_0_0_13TeV_Nov14",5.867e-09),
		       ("pythia8_ci_m4300_13000_9000_1_0_0_13TeV_Nov14",3.507e-09),
		       ]),
             ("QCDCIplusLL10000",[("pythia8_ci_m1500_1900_10000_1_0_0_13TeV_Nov14",3.307e-06),
		       ("pythia8_ci_m1900_2400_10000_1_0_0_13TeV_Nov14",8.836e-07),
		       ("pythia8_ci_m2400_2800_10000_1_0_0_13TeV_Nov14",1.649e-07),
		       ("pythia8_ci_m2800_3300_10000_1_0_0_13TeV_Nov14",6.446e-08),
		       ("pythia8_ci_m3300_3800_10000_1_0_0_13TeV_Nov14",1.863e-08),
		       ("pythia8_ci_m3800_4300_10000_1_0_0_13TeV_Nov14",5.867e-09),
		       ("pythia8_ci_m4300_13000_10000_1_0_0_13TeV_Nov14",3.507e-09),
		       ]),
             ("QCDCIplusLL11000",[("pythia8_ci_m1500_1900_11000_1_0_0_13TeV_Nov14",3.307e-06),
		       ("pythia8_ci_m1900_2400_11000_1_0_0_13TeV_Nov14",8.836e-07),
		       ("pythia8_ci_m2400_2800_11000_1_0_0_13TeV_Nov14",1.649e-07),
		       ("pythia8_ci_m2800_3300_11000_1_0_0_13TeV_Nov14",6.446e-08),
		       ("pythia8_ci_m3300_3800_11000_1_0_0_13TeV_Nov14",1.863e-08),
		       ("pythia8_ci_m3800_4300_11000_1_0_0_13TeV_Nov14",5.867e-09),
		       ("pythia8_ci_m4300_13000_11000_1_0_0_13TeV_Nov14",3.507e-09),
		       ]),
             ("QCDCIplusLL12000",[("pythia8_ci_m1500_1900_12000_1_0_0_13TeV_Nov14",3.307e-06),
		       ("pythia8_ci_m1900_2400_12000_1_0_0_13TeV_Nov14",8.836e-07),
		       ("pythia8_ci_m2400_2800_12000_1_0_0_13TeV_Nov14",1.649e-07),
		       ("pythia8_ci_m2800_3300_12000_1_0_0_13TeV_Nov14",6.446e-08),
		       ("pythia8_ci_m3300_3800_12000_1_0_0_13TeV_Nov14",1.863e-08),
		       ("pythia8_ci_m3800_4300_12000_1_0_0_13TeV_Nov14",5.867e-09),
		       ("pythia8_ci_m4300_13000_12000_1_0_0_13TeV_Nov14",3.507e-09),
		       ]),
             ("QCDCIplusLL13000",[("pythia8_ci_m1500_1900_13000_1_0_0_13TeV_Nov14",3.307e-06),
		       ("pythia8_ci_m1900_2400_13000_1_0_0_13TeV_Nov14",8.836e-07),
		       ("pythia8_ci_m2400_2800_13000_1_0_0_13TeV_Nov14",1.649e-07),
		       ("pythia8_ci_m2800_3300_13000_1_0_0_13TeV_Nov14",6.446e-08),
		       ("pythia8_ci_m3300_3800_13000_1_0_0_13TeV_Nov14",1.863e-08),
		       ("pythia8_ci_m3800_4300_13000_1_0_0_13TeV_Nov14",5.867e-09),
		       ("pythia8_ci_m4300_13000_13000_1_0_0_13TeV_Nov14",3.507e-09),
		       ]),
             ("QCDCIplusLL14000",[("pythia8_ci_m1500_1900_14000_1_0_0_13TeV_Nov14",3.307e-06),
		       ("pythia8_ci_m1900_2400_14000_1_0_0_13TeV_Nov14",8.836e-07),
		       ("pythia8_ci_m2400_2800_14000_1_0_0_13TeV_Nov14",1.649e-07),
		       ("pythia8_ci_m2800_3300_14000_1_0_0_13TeV_Nov14",6.446e-08),
		       ("pythia8_ci_m3300_3800_14000_1_0_0_13TeV_Nov14",1.863e-08),
		       ("pythia8_ci_m3800_4300_14000_1_0_0_13TeV_Nov14",5.867e-09),
		       ("pythia8_ci_m4300_13000_14000_1_0_0_13TeV_Nov14",3.507e-09),
		       ]),
             ("QCDCIplusLL16000",[("pythia8_ci_m1500_1900_16000_1_0_0_13TeV_Nov14",3.307e-06),
		       ("pythia8_ci_m1900_2400_16000_1_0_0_13TeV_Nov14",8.836e-07),
		       ("pythia8_ci_m2400_2800_16000_1_0_0_13TeV_Nov14",1.649e-07),
		       ("pythia8_ci_m2800_3300_16000_1_0_0_13TeV_Nov14",6.446e-08),
		       ("pythia8_ci_m3300_3800_16000_1_0_0_13TeV_Nov14",1.863e-08),
		       ("pythia8_ci_m3800_4300_16000_1_0_0_13TeV_Nov14",5.867e-09),
		       ("pythia8_ci_m4300_13000_16000_1_0_0_13TeV_Nov14",3.507e-09),
		       ]),
             ("QCDCIplusLL18000",[("pythia8_ci_m1500_1900_18000_1_0_0_13TeV_Nov14",3.307e-06),
		       ("pythia8_ci_m1900_2400_18000_1_0_0_13TeV_Nov14",8.836e-07),
		       ("pythia8_ci_m2400_2800_18000_1_0_0_13TeV_Nov14",1.649e-07),
		       ("pythia8_ci_m2800_3300_18000_1_0_0_13TeV_Nov14",6.446e-08),
		       ("pythia8_ci_m3300_3800_18000_1_0_0_13TeV_Nov14",1.863e-08),
		       ("pythia8_ci_m3800_4300_18000_1_0_0_13TeV_Nov14",5.867e-09),
		       ("pythia8_ci_m4300_13000_18000_1_0_0_13TeV_Nov14",3.507e-09),
		       ]),
             ]
    samples2=[("QCDCIminusLL8000",[("pythia8_ci_m1500_1900_8000_-1_0_0_13TeV_Nov14",3.307e-06),
		       ("pythia8_ci_m1900_2400_8000_-1_0_0_13TeV_Nov14",8.836e-07),
		       ("pythia8_ci_m2400_2800_8000_-1_0_0_13TeV_Nov14",1.649e-07),
		       ("pythia8_ci_m2800_3300_8000_-1_0_0_13TeV_Nov14",6.446e-08),
		       ("pythia8_ci_m3300_3800_8000_-1_0_0_13TeV_Nov14",1.863e-08),
		       ("pythia8_ci_m3800_4300_8000_-1_0_0_13TeV_Nov14",5.867e-09),
		       ("pythia8_ci_m4300_13000_8000_-1_0_0_13TeV_Nov14",3.507e-09),
		       ]),
             ("QCDCIminusLL9000",[("pythia8_ci_m1500_1900_9000_-1_0_0_13TeV_Nov14",3.307e-06),
		       ("pythia8_ci_m1900_2400_9000_-1_0_0_13TeV_Nov14",8.836e-07),
		       ("pythia8_ci_m2400_2800_9000_-1_0_0_13TeV_Nov14",1.649e-07),
		       ("pythia8_ci_m2800_3300_9000_-1_0_0_13TeV_Nov14",6.446e-08),
		       ("pythia8_ci_m3300_3800_9000_-1_0_0_13TeV_Nov14",1.863e-08),
		       ("pythia8_ci_m3800_4300_9000_-1_0_0_13TeV_Nov14",5.867e-09),
		       ("pythia8_ci_m4300_13000_9000_-1_0_0_13TeV_Nov14",3.507e-09),
		       ]),
             ("QCDCIminusLL10000",[("pythia8_ci_m1500_1900_10000_-1_0_0_13TeV_Nov14",3.307e-06),
		       ("pythia8_ci_m1900_2400_10000_-1_0_0_13TeV_Nov14",8.836e-07),
		       ("pythia8_ci_m2400_2800_10000_-1_0_0_13TeV_Nov14",1.649e-07),
		       ("pythia8_ci_m2800_3300_10000_-1_0_0_13TeV_Nov14",6.446e-08),
		       ("pythia8_ci_m3300_3800_10000_-1_0_0_13TeV_Nov14",1.863e-08),
		       ("pythia8_ci_m3800_4300_10000_-1_0_0_13TeV_Nov14",5.867e-09),
		       ("pythia8_ci_m4300_13000_10000_-1_0_0_13TeV_Nov14",3.507e-09),
		       ]),
             ("QCDCIminusLL11000",[("pythia8_ci_m1500_1900_11000_-1_0_0_13TeV_Nov14",3.307e-06),
		       ("pythia8_ci_m1900_2400_11000_-1_0_0_13TeV_Nov14",8.836e-07),
		       ("pythia8_ci_m2400_2800_11000_-1_0_0_13TeV_Nov14",1.649e-07),
		       ("pythia8_ci_m2800_3300_11000_-1_0_0_13TeV_Nov14",6.446e-08),
		       ("pythia8_ci_m3300_3800_11000_-1_0_0_13TeV_Nov14",1.863e-08),
		       ("pythia8_ci_m3800_4300_11000_-1_0_0_13TeV_Nov14",5.867e-09),
		       ("pythia8_ci_m4300_13000_11000_-1_0_0_13TeV_Nov14",3.507e-09),
		       ]),
             ("QCDCIminusLL12000",[("pythia8_ci_m1500_1900_12000_-1_0_0_13TeV_Nov14",3.307e-06),
		       ("pythia8_ci_m1900_2400_12000_-1_0_0_13TeV_Nov14",8.836e-07),
		       ("pythia8_ci_m2400_2800_12000_-1_0_0_13TeV_Nov14",1.649e-07),
		       ("pythia8_ci_m2800_3300_12000_-1_0_0_13TeV_Nov14",6.446e-08),
		       ("pythia8_ci_m3300_3800_12000_-1_0_0_13TeV_Nov14",1.863e-08),
		       ("pythia8_ci_m3800_4300_12000_-1_0_0_13TeV_Nov14",5.867e-09),
		       ("pythia8_ci_m4300_13000_12000_-1_0_0_13TeV_Nov14",3.507e-09),
		       ]),
             ("QCDCIminusLL13000",[("pythia8_ci_m1500_1900_13000_-1_0_0_13TeV_Nov14",3.307e-06),
		       ("pythia8_ci_m1900_2400_13000_-1_0_0_13TeV_Nov14",8.836e-07),
		       ("pythia8_ci_m2400_2800_13000_-1_0_0_13TeV_Nov14",1.649e-07),
		       ("pythia8_ci_m2800_3300_13000_-1_0_0_13TeV_Nov14",6.446e-08),
		       ("pythia8_ci_m3300_3800_13000_-1_0_0_13TeV_Nov14",1.863e-08),
		       ("pythia8_ci_m3800_4300_13000_-1_0_0_13TeV_Nov14",5.867e-09),
		       ("pythia8_ci_m4300_13000_13000_-1_0_0_13TeV_Nov14",3.507e-09),
		       ]),
             ("QCDCIminusLL14000",[("pythia8_ci_m1500_1900_14000_-1_0_0_13TeV_Nov14",3.307e-06),
		       ("pythia8_ci_m1900_2400_14000_-1_0_0_13TeV_Nov14",8.836e-07),
		       ("pythia8_ci_m2400_2800_14000_-1_0_0_13TeV_Nov14",1.649e-07),
		       ("pythia8_ci_m2800_3300_14000_-1_0_0_13TeV_Nov14",6.446e-08),
		       ("pythia8_ci_m3300_3800_14000_-1_0_0_13TeV_Nov14",1.863e-08),
		       ("pythia8_ci_m3800_4300_14000_-1_0_0_13TeV_Nov14",5.867e-09),
		       ("pythia8_ci_m4300_13000_14000_-1_0_0_13TeV_Nov14",3.507e-09),
		       ]),
             ("QCDCIminusLL16000",[("pythia8_ci_m1500_1900_16000_-1_0_0_13TeV_Nov14",3.307e-06),
		       ("pythia8_ci_m1900_2400_16000_-1_0_0_13TeV_Nov14",8.836e-07),
		       ("pythia8_ci_m2400_2800_16000_-1_0_0_13TeV_Nov14",1.649e-07),
		       ("pythia8_ci_m2800_3300_16000_-1_0_0_13TeV_Nov14",6.446e-08),
		       ("pythia8_ci_m3300_3800_16000_-1_0_0_13TeV_Nov14",1.863e-08),
		       ("pythia8_ci_m3800_4300_16000_-1_0_0_13TeV_Nov14",5.867e-09),
		       ("pythia8_ci_m4300_13000_16000_-1_0_0_13TeV_Nov14",3.507e-09),
		       ]),
             ("QCDCIminusLL18000",[("pythia8_ci_m1500_1900_18000_-1_0_0_13TeV_Nov14",3.307e-06),
		       ("pythia8_ci_m1900_2400_18000_-1_0_0_13TeV_Nov14",8.836e-07),
		       ("pythia8_ci_m2400_2800_18000_-1_0_0_13TeV_Nov14",1.649e-07),
		       ("pythia8_ci_m2800_3300_18000_-1_0_0_13TeV_Nov14",6.446e-08),
		       ("pythia8_ci_m3300_3800_18000_-1_0_0_13TeV_Nov14",1.863e-08),
		       ("pythia8_ci_m3800_4300_18000_-1_0_0_13TeV_Nov14",5.867e-09),
		       ("pythia8_ci_m4300_13000_18000_-1_0_0_13TeV_Nov14",3.507e-09),
		       ]),
             ]
    samples2=[("QCDADD6000",[("pythia8_add_m1500_1900_6000_0_0_0_1_13TeV_Nov14",3.307e-06),
		       ("pythia8_add_m1900_2400_6000_0_0_0_1_13TeV_Nov14",8.836e-07),
		       ("pythia8_add_m2400_2800_6000_0_0_0_1_13TeV_Nov14",1.649e-07),
		       ("pythia8_add_m2800_3300_6000_0_0_0_1_13TeV_Nov14",6.446e-08),
		       ("pythia8_add_m3300_3800_6000_0_0_0_1_13TeV_Nov14",1.863e-08),
		       ("pythia8_add_m3800_4300_6000_0_0_0_1_13TeV_Nov14",5.867e-09),
		       ("pythia8_add_m4300_13000_6000_0_0_0_1_13TeV_Nov14",3.507e-09),
		       ]),
             ("QCDADD7000",[("pythia8_add_m1500_1900_7000_0_0_0_1_13TeV_Nov14",3.307e-06),
		       ("pythia8_add_m1900_2400_7000_0_0_0_1_13TeV_Nov14",8.836e-07),
		       ("pythia8_add_m2400_2800_7000_0_0_0_1_13TeV_Nov14",1.649e-07),
		       ("pythia8_add_m2800_3300_7000_0_0_0_1_13TeV_Nov14",6.446e-08),
		       ("pythia8_add_m3300_3800_7000_0_0_0_1_13TeV_Nov14",1.863e-08),
		       ("pythia8_add_m3800_4300_7000_0_0_0_1_13TeV_Nov14",5.867e-09),
		       ("pythia8_add_m4300_13000_7000_0_0_0_1_13TeV_Nov14",3.507e-09),
		       ]),
             ("QCDADD8000",[("pythia8_add_m1500_1900_8000_0_0_0_1_13TeV_Nov14",3.307e-06),
		       ("pythia8_add_m1900_2400_8000_0_0_0_1_13TeV_Nov14",8.836e-07),
		       ("pythia8_add_m2400_2800_8000_0_0_0_1_13TeV_Nov14",1.649e-07),
		       ("pythia8_add_m2800_3300_8000_0_0_0_1_13TeV_Nov14",6.446e-08),
		       ("pythia8_add_m3300_3800_8000_0_0_0_1_13TeV_Nov14",1.863e-08),
		       ("pythia8_add_m3800_4300_8000_0_0_0_1_13TeV_Nov14",5.867e-09),
		       ("pythia8_add_m4300_13000_8000_0_0_0_1_13TeV_Nov14",3.507e-09),
		       ]),
             ("QCDADD9000",[("pythia8_add_m1500_1900_9000_0_0_0_1_13TeV_Nov14",3.307e-06),
		       ("pythia8_add_m1900_2400_9000_0_0_0_1_13TeV_Nov14",8.836e-07),
		       ("pythia8_add_m2400_2800_9000_0_0_0_1_13TeV_Nov14",1.649e-07),
		       ("pythia8_add_m2800_3300_9000_0_0_0_1_13TeV_Nov14",6.446e-08),
		       ("pythia8_add_m3300_3800_9000_0_0_0_1_13TeV_Nov14",1.863e-08),
		       ("pythia8_add_m3800_4300_9000_0_0_0_1_13TeV_Nov14",5.867e-09),
		       ("pythia8_add_m4300_13000_9000_0_0_0_1_13TeV_Nov14",3.507e-09),
		       ]),
             ("QCDADD10000",[("pythia8_add_m1500_1900_10000_0_0_0_1_13TeV_Nov14",3.307e-06),
		       ("pythia8_add_m1900_2400_10000_0_0_0_1_13TeV_Nov14",8.836e-07),
		       ("pythia8_add_m2400_2800_10000_0_0_0_1_13TeV_Nov14",1.649e-07),
		       ("pythia8_add_m2800_3300_10000_0_0_0_1_13TeV_Nov14",6.446e-08),
		       ("pythia8_add_m3300_3800_10000_0_0_0_1_13TeV_Nov14",1.863e-08),
		       ("pythia8_add_m3800_4300_10000_0_0_0_1_13TeV_Nov14",5.867e-09),
		       ("pythia8_add_m4300_13000_10000_0_0_0_1_13TeV_Nov14",3.507e-09),
		       ]),
             ("QCDADD11000",[("pythia8_add_m1500_1900_11000_0_0_0_1_13TeV_Nov14",3.307e-06),
		       ("pythia8_add_m1900_2400_11000_0_0_0_1_13TeV_Nov14",8.836e-07),
		       ("pythia8_add_m2400_2800_11000_0_0_0_1_13TeV_Nov14",1.649e-07),
		       ("pythia8_add_m2800_3300_11000_0_0_0_1_13TeV_Nov14",6.446e-08),
		       ("pythia8_add_m3300_3800_11000_0_0_0_1_13TeV_Nov14",1.863e-08),
		       ("pythia8_add_m3800_4300_11000_0_0_0_1_13TeV_Nov14",5.867e-09),
		       ("pythia8_add_m4300_13000_11000_0_0_0_1_13TeV_Nov14",3.507e-09),
		       ]),
             ("QCDADD12000",[("pythia8_add_m1500_1900_12000_0_0_0_1_13TeV_Nov14",3.307e-06),
		       ("pythia8_add_m1900_2400_12000_0_0_0_1_13TeV_Nov14",8.836e-07),
		       ("pythia8_add_m2400_2800_12000_0_0_0_1_13TeV_Nov14",1.649e-07),
		       ("pythia8_add_m2800_3300_12000_0_0_0_1_13TeV_Nov14",6.446e-08),
		       ("pythia8_add_m3300_3800_12000_0_0_0_1_13TeV_Nov14",1.863e-08),
		       ("pythia8_add_m3800_4300_12000_0_0_0_1_13TeV_Nov14",5.867e-09),
		       ("pythia8_add_m4300_13000_12000_0_0_0_1_13TeV_Nov14",3.507e-09),
		       ]),
             ("QCDADD13000",[("pythia8_add_m1500_1900_13000_0_0_0_1_13TeV_Nov14",3.307e-06),
		       ("pythia8_add_m1900_2400_13000_0_0_0_1_13TeV_Nov14",8.836e-07),
		       ("pythia8_add_m2400_2800_13000_0_0_0_1_13TeV_Nov14",1.649e-07),
		       ("pythia8_add_m2800_3300_13000_0_0_0_1_13TeV_Nov14",6.446e-08),
		       ("pythia8_add_m3300_3800_13000_0_0_0_1_13TeV_Nov14",1.863e-08),
		       ("pythia8_add_m3800_4300_13000_0_0_0_1_13TeV_Nov14",5.867e-09),
		       ("pythia8_add_m4300_13000_13000_0_0_0_1_13TeV_Nov14",3.507e-09),
		       ]),
             ("QCDADD14000",[("pythia8_add_m1500_1900_14000_0_0_0_1_13TeV_Nov14",3.307e-06),
		       ("pythia8_add_m1900_2400_14000_0_0_0_1_13TeV_Nov14",8.836e-07),
		       ("pythia8_add_m2400_2800_14000_0_0_0_1_13TeV_Nov14",1.649e-07),
		       ("pythia8_add_m2800_3300_14000_0_0_0_1_13TeV_Nov14",6.446e-08),
		       ("pythia8_add_m3300_3800_14000_0_0_0_1_13TeV_Nov14",1.863e-08),
		       ("pythia8_add_m3800_4300_14000_0_0_0_1_13TeV_Nov14",5.867e-09),
		       ("pythia8_add_m4300_13000_14000_0_0_0_1_13TeV_Nov14",3.507e-09),
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
      legend1=TLegend(0.6,0.6,0.9,0.9,(str(massbins[j][0])+"<m_{jj}<"+str(massbins[j][1])+" GeV").replace("4200<m_{jj}<13000","m_{jj}>4200"))
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

