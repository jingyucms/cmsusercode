import os, sys
import array
from ROOT import * 
from os import path
import subprocess

#gROOT.Reset()
#gROOT.SetStyle("Plain")
#gROOT.ProcessLine('.L tdrstyle.C')
gROOT.SetBatch(True)
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetTitleOffset(1.3,"Y")
gStyle.SetPadLeftMargin(0.15)
gStyle.SetPadBottomMargin(0.15)
gStyle.SetPadTopMargin(0.08)
gStyle.SetPadRightMargin(0.09)
gStyle.SetMarkerSize(0.5)
gStyle.SetHistLineWidth(1)
#gStyle.SetStatFontSize(0.020)
gStyle.SetTitleSize(0.06, "XYZ")
gStyle.SetLabelSize(0.05, "XYZ")
gStyle.SetNdivisions(506, "XYZ")
gStyle.SetLegendBorderSize(0)

TGaxis.SetMaxDigits(3)

if path.exists('rootlogon.C'):
    gROOT.Macro('rootlogon.C')  # Run ROOT logon script

if __name__ == '__main__':

 #for runSet in [36,26,20,21,22,23,24,25,27,28,30,31,32,33,34,35,37,38]:#20,21,22,23,24,25,26,27,28]:#[2,3,4,5,6,8,9,1,7]:
 #for runSet in [26,36]:
 #for runSet in [31,32,33,34,71,72,73,74,75,76]: #61,62,63,64,65,66,67,68,69
 #for runSet in [91,92,93,94,95,96]:
 #for runSet in [101,102,103,104,105,106]:
 #for runSet in [111,112,113,114,115,116]:
 #for runSet in [99]:
 #for runSet in [71,72,73,74,75,76]:
 #for runSet in [61,62,63,64,65,66,67,68,69]:
 #for runSet in [81,82,83,84,85,86]:
 #for runSet in [91,92,93,94,95,96]:
 #for runSet in [65,66,67,74,75,76,84,85,86]:
 #for runSet in [52,53,54,55,56,57,58]:
 #for runSet in [59,52,57,58]:
 #for runSet in [52,53,54,57,58,59]:
 #for runSet in [52,57,58]:
 #for runSet in [27,64,74,83,94,66,75,85,95]:
 for runSet in [162]:
  theory=0
  normalize=(runSet<20)
 
  colors=[1,2,4,6,8,1,2,4,6,8]
  styles=[1,2,3,4,5,1,2,3,4,5]
  widths=[2,2,2,2,2,3,3,3,3,3]
  sets=[""]
 
  #selection = "weight*vertexWeight*((deta<1.3)&&(abs(Jet1eta)<1.0)&&(Jet1pt>500)&&(Jet1pt<7000)&&(Jet1MassDrop<0.3))"
  selection = "((abs(j_eta[0])<2.4))"
  names = ["pt",
           "mass",
 	   "mass_mmdt",
 	   "mass_softdrop_b2",
 	   "mass_softdrop_m1",
 	   "tau21_b1",
 	   "tau21_b1_aftermass",
 	   "tau21_b2_aftermass",
 	   "c1_b0_aftermass",
 	   "c1_b1_aftermass",
 	   "c1_b2_aftermass",
 	   "c2_b1_aftermass",
 	   "c2_b2_aftermass",
 	   "d2_b1_aftermass",
 	   "d2_b2_aftermass",
 	   "d2_a1_b1_aftermass",
 	   "d2_a1_b2_aftermass",
 	   "m2_b1_aftermass",
 	   "m2_b2_aftermass",
 	   "n2_b1_aftermass",
 	   "n2_b2_aftermass",
 	   "tau21_b1_mmdt_aftermass",
 	   "tau21_b2_mmdt_aftermass",
 	   "c1_b0_mmdt_aftermass",
 	   "c1_b1_mmdt_aftermass",
 	   "c1_b2_mmdt_aftermass",
 	   "c2_b1_mmdt_aftermass",
 	   "c2_b2_mmdt_aftermass",
 	   "d2_b1_mmdt_aftermass",
 	   "d2_b2_mmdt_aftermass",
 	   "d2_a1_b1_mmdt_aftermass",
 	   "d2_a1_b2_mmdt_aftermass",
 	   "m2_b1_mmdt_aftermass",
 	   "m2_b2_mmdt_aftermass",
 	   "n2_b1_mmdt_aftermass",
 	   "n2_b2_mmdt_aftermass",
 	   ]
  plots = [("j_pt[0]",selection,"jet p_{T} (GeV)"),
           ("j_mass_prun[0]",selection,"pruned jet mass (GeV)"),
 	   ("j_mass_mmdt[0]",selection,"m_{mMDT} (GeV)"),
 	   ("j_mass_sdb2[0]",selection,"softdrop (#beta=2) jet mass (GeV)"),
 	   ("j_mass_sdm1[0]",selection,"softdrop (#beta=-1) jet mass (GeV)"),
 	   ("j_tau21_b1[0]",selection,"#tau_{2}/#tau_{1}", ),
 	   ("j_tau21_b1[0]",selection+"&&(j_mass_prun[0]>65)&&(j_mass_prun[0]<105)","#tau_{2}/#tau_{1} (#beta=1)", ),
 	   ("j_tau21_b2[0]",selection+"&&(j_mass_prun[0]>65)&&(j_mass_prun[0]<105)","#tau_{2}/#tau_{1} (#beta=2)", ),
 	   ("j_c1_b0[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","C1 (#beta=0)", ),
 	   ("j_c1_b1[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","C1 (#beta=1)", ),
 	   ("j_c1_b2[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","C1 (#beta=2)", ),
 	   ("j_c2_b1[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","C2 (#beta=1)", ),
 	   ("j_c2_b2[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","C2 (#beta=2)", ),
 	   ("j_d2_b1[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","D2 (#beta=1)", ),
 	   ("j_d2_b2[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","D2 (#beta=2)", ),
 	   ("j_d2_a1_b1[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","D2 (#alpha=1,#beta=1)", ),
 	   ("j_d2_a1_b2[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","D2 (#alpha=1,#beta=2)", ),
 	   ("j_m2_b1[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","M2 (#beta=1)", ),
 	   ("j_m2_b2[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","M2 (#beta=2)", ),
 	   ("j_n2_b1[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","N2 (#beta=1)", ),
 	   ("j_n2_b2[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","N2 (#beta=2)", ),
 	   ("j_tau21_b1_mmdt[0]",selection+"&&(j_mass_prun[0]>65)&&(j_mass_prun[0]<105)","#tau_{2}/#tau_{1} (#beta=1)", ),
 	   ("j_tau21_b2_mmdt[0]",selection+"&&(j_mass_prun[0]>65)&&(j_mass_prun[0]<105)","#tau_{2}/#tau_{1} (#beta=2)", ),
 	   ("j_c1_b0_mmdt[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","C1 (#beta=0)", ),
 	   ("j_c1_b1_mmdt[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","C1 (#beta=1)", ),
 	   ("j_c1_b2_mmdt[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","C1 (#beta=2)", ),
 	   ("j_c2_b1_mmdt[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","C2 (#beta=1)", ),
 	   ("j_c2_b2_mmdt[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","C2 (#beta=2)", ),
 	   ("j_d2_b1_mmdt[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","D2 (#beta=1)", ),
 	   ("j_d2_b2_mmdt[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","D2 (#beta=2)", ),
 	   ("j_d2_a1_b1_mmdt[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","D2 (#alpha=1,#beta=1)", ),
 	   ("j_d2_a1_b2_mmdt[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","D2 (#alpha=1,#beta=2)", ),
 	   ("j_m2_b1_mmdt[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","M2 (#beta=1)", ),
 	   ("j_m2_b2_mmdt[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","M2 (#beta=2)", ),
 	   ("j_n2_b1_mmdt[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","N2 (#beta=1)", ),
 	   ("j_n2_b2_mmdt[0]",selection+"&&(j_mass_mmdt[0]>65)&&(j_mass_mmdt[0]<105)","N2 (#beta=2)", ),
 	   ]
 
  if runSet==1:
   samples = ["../../trackObservables/processing/processed-pythia82-lhc13-WW-pt1-50k-2-no.root",
 	      "../../trackObservables/processing/processed-pythia82-lhc13-WW-pt1-50k-2-r.root",
 	      "../../trackObservables/processing/processed-pythia82-lhc13-WW-pt1-50k-2-rh.root",
 	      #"../../trackObservables/processing/processed-pythia82-lhc13-WW-pt1-50k-2-reh.root",
 	      #"../../trackObservables/processing/processed-pythia82-lhc13-WW-pt1-50k-2-ruh.root",
 	      #"../../trackObservables/processing/processed-pythia82-lhc13-WW-pt1-50k-2-rsh.root",
 	      "../../trackObservables/processing/processed-pythia82-lhc13-WW-pt1-50k-2-rth.root",
 	      "../../trackObservables/processing/processed-pythia82-lhc13-WW-pt1-50k-2-rth:p20.root",
 	      "../../trackObservables/processing/processed-pythia82-lhc13-WW-pt1-50k-2-rth:p20:i.root",
 	     ]
  if runSet==2:
   samples = ["../../trackObservables/processing/processed-pythia82-fcc100-WW-pt5-50k-2-rth:p20.root",
 	     ]
  if runSet==3:
   samples = ["../../trackObservables/processing/processed-pythia82-lhc13-WW-pt300-10k-rth:p20.root",
 	      "../../trackObservables/processing/processed-pythia82-lhc13-WW-pt500-10k-rth:p20.root",
 	      "../../trackObservables/processing/processed-pythia82-lhc13-WW-pt1-50k-2-rth:p20.root",
 	      "../../trackObservables/processing/processed-pythia82-lhc13-WW-pt3500-10k-rth:p20.root",
 	      "../../trackObservables/processing/processed-pythia82-fcc100-WW-pt5-50k-2-rth:p20.root",
 	      "../../trackObservables/processing/processed-pythia82-lhc13-qq-pt1-50k-2-rth:p20.root",
 	     ]
  if runSet==4:
   samples = ["../../trackObservables/processing/processed-pythia82-lhc13-WW-pt1-50k-2-rth:p10.root",
 	     ]
  if runSet==5:
   samples = ["../../trackObservables/processing/processed-pythia82-lhc13-qq-pt1-50k-2-rth:p10.root",
 	     ]
  if runSet==6:
   samples = ["../../trackObservables/processing/processed-pythia82-lhc13-WW-pt500-10k-rth:p20.root",
 	     ]
  if runSet==7:
   samples = ["../../trackObservables/processing/processed-pythia82-lhc13-WW-pt300-10k-no.root",
 	      "../../trackObservables/processing/processed-pythia82-lhc13-WW-pt300-10k-r.root",
 	      "../../trackObservables/processing/processed-pythia82-lhc13-WW-pt300-10k-rh.root",
 	      #"../../trackObservables/processing/processed-pythia82-lhc13-WW-pt300-10k-reh.root",
 	      #"../../trackObservables/processing/processed-pythia82-lhc13-WW-pt300-10k-ruh.root",
 	      #"../../trackObservables/processing/processed-pythia82-lhc13-WW-pt300-10k-rsh.root",
 	      "../../trackObservables/processing/processed-pythia82-lhc13-WW-pt300-10k-rth.root",
 	      "../../trackObservables/processing/processed-pythia82-lhc13-WW-pt300-10k-rth:p20.root",
 	      "../../trackObservables/processing/processed-pythia82-lhc13-WW-pt300-10k-rth:p20:i.root",
 	     ]
  if runSet==8:
   samples = ["../../trackObservables/processing/processed-pythia82-lhc13-WW-pt300-10k-rth:p20.root",
 	     ]
  if runSet==9:
   samples = ["../../trackObservables/processing/processed-pythia82-lhc13-WW-pt3500-10k-rth:p40.root",
 	     ]
  if runSet>=20:
   samples = [#"root://eoscms.cern.ch//eos/cms/store/cmst3/group/exovv/precision/WJetsToQQ_HT-600toInf_tarball.tar.xz/ntupler/",
 	     #"root://eoscms.cern.ch//eos/cms/store/cmst3/group/exovv/precision/ZJetsToQQ_HT600toInf_gridpack.tar.gz/ntupler/",
 	     #"root://eoscms.cern.ch//eos/cms/store/cmst3/group/exovv/precision/ZJetsFullyHadronic_HT180_LO_MLM_tarball.tar.xz/ntupler/",
	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-rth:W.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-rth:Z01.root",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/exovv/precision/QCD_HT300to500_tarball.tar.xz/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/exovv/precision/QCD_HT500to700_tarball.tar.xz/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/exovv/precision/QCD_HT700to1000_tarball.tar.xz/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/exovv/precision/QCD_HT1000to1500_tarball.tar.xz/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/exovv/precision/QCD_HT1500to2000_tarball.tar.xz/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/exovv/precision/QCD_HT2000toInf_tarball.tar.xz/ntupler/",
 	     ]
   if theory==3:
     samples = ["/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-rth:HS1.0:PS1.0:CS1.0.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-rth:HS1.01:PS1.0:CS1.0.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-rth:HS1.0:PS1.01:CS1.0.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-rth:HS1.0:PS1.0:CS1.01.root",
 	     ]
   if theory==1000:
     samples = ["/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-rth:TT.root",
 	     ]
   selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>500))"
   if runSet==21: selection += "&&(j_tau21_b1[0]<0.5)"
   if runSet==22: selection += "&&(j_tau21_b1[0]<0.4)"
   if runSet==23: selection += "&&(j_tau21_b1[0]<0.3)"
   if runSet==24: selection += "&&(j_tau21_b1[0]<0.2)"
   if runSet==25: selection += "&&(j_n2_b1[0]<0.3)"
   if runSet==26: selection += "&&(j_n2_b1[0]<0.25)"
   if runSet==27: selection += "&&(j_n2_b1[0]<0.2)"
   if runSet==28: selection += "&&(j_n2_b1[0]<0.15)"
   if runSet==31: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300))&&(j_n2_b1[0]<0.3)"
   if runSet==32: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300))&&(j_n2_b1[0]<0.25)"
   if runSet==33: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300))&&(j_n2_b1[0]<0.2)"
   if runSet==34: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300))&&(j_n2_b1[0]<0.15)"
   if runSet==35: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>400))&&(j_n2_b1[0]<0.3)"
   if runSet==36: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>400))&&(j_n2_b1[0]<0.25)"
   if runSet==37: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>400))&&(j_n2_b1[0]<0.2)"
   if runSet==38: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>400))&&(j_n2_b1[0]<0.15)"
   if runSet==61: selection += "&&(ddt01(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==62: selection += "&&(ddt02(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==63: selection += "&&(ddt05(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==64: selection += "&&(ddt1(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==65: selection += "&&(ddt2(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==66: selection += "&&(ddt5(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==67: selection += "&&(ddt10(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==68: selection += "&&(ddt15(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==69: selection += "&&(ddt20(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==71: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300))&&(ddt02(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==72: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300))&&(ddt05(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==73: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300))&&(ddt1(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==74: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300))&&(ddt2(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==75: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300))&&(ddt5(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==76: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300))&&(ddt10(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==81: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>400))&&(ddt02(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==82: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>400))&&(ddt05(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==83: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>400))&&(ddt1(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==84: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>400))&&(ddt2(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==85: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>400))&&(ddt5(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==86: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>400))&&(ddt10(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==91: selection += "&&(ddtb202(j_n2_b2[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==92: selection += "&&(ddtb205(j_n2_b2[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==93: selection += "&&(ddtb21(j_n2_b2[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==94: selection += "&&(ddtb22(j_n2_b2[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==95: selection += "&&(ddtb25(j_n2_b2[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==96: selection += "&&(ddtb210(j_n2_b2[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==99: pass
   if runSet==101: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300))&&(ddtb202(j_n2_b2[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==102: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300))&&(ddtb205(j_n2_b2[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==103: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300))&&(ddtb21(j_n2_b2[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==104: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300))&&(ddtb22(j_n2_b2[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==105: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300))&&(ddtb25(j_n2_b2[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==106: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300))&&(ddtb210(j_n2_b2[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==111: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>400))&&(ddtb202(j_n2_b2[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==112: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>400))&&(ddtb205(j_n2_b2[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==113: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>400))&&(ddtb21(j_n2_b2[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==114: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>400))&&(ddtb22(j_n2_b2[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==115: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>400))&&(ddtb25(j_n2_b2[0],j_pt[0],j_mass_mmdt[0])<0)"
   if runSet==116: selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>400))&&(ddtb210(j_n2_b2[0],j_pt[0],j_mass_mmdt[0])<0)"
   names = ["mass_mmdt"
 	   ]
   plots = [("j_mass_mmdt[0]",selection,"m_{mMDT} (GeV)"),
 	   ]
  if runSet==1000:
   normalize=True
   names = ["pt",
           "mass_mmdt",
 	   "n2_b1",
 	   "ddt2_n2_b1"
 	   ]
   plots = [("j_pt[0]","(abs(j_eta[0])<2.4)","jet p_{T} (GeV)"),
            ("j_mass_mmdt[0]",selection,"m_{mMDT} (GeV)"),
            ("j_n2_b1[0]",selection,"N2 (#beta=1)"),
 	    ("ddt2(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])",selection,"DDT N2 2%"),
 	   ]
  if runSet==50 or runSet==51:
   samples = ["root://eoscms.cern.ch//eos/cms/store/cmst3/group/exovv/precision/WJetsToQQ_HT-600toInf_tarball.tar.xz/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/exovv/precision/ZJetsToQQ_HT600toInf_gridpack.tar.gz/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/exovv/precision/WJetsToQQ_HT-600toInf_tarball.tar.xz/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/exovv/precision/ZJetsToQQ_HT600toInf_gridpack.tar.gz/ntupler/",
 	     ]
   selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>500))"
   normalize=True
   names = ["mass_mmdt",
 	   ]
   plots = [("j_mass_mmdt[0]",selection,"m_{mMDT} (GeV)"),
 	   ]
  if runSet==52:
   samples = ["/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:Z01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:Z01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:Z01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W:UE.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:Z:UE.root",
 	     ]
   selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300)&&(j_n2_b1[0]<0.2))"
   normalize=True
   names = ["pt",
           "eta",
           "mass_mmdt",
 	   "mass_mmdt300",
 	   "mass_mmdt350",
 	   "mass_mmdt400",
 	   "mass_mmdt450",
 	   "mass_mmdt500",
 	   "mass_mmdt550",
 	   "mass_mmdt600",
 	   "mass_mmdt700",
 	   "mass_mmdt800",
 	   ]
   plots = [("j_pt[0]",selection,"jet p_{T} (GeV)"),
            ("abs(j_eta[0])",selection,"jet |#eta|"),
            ("j_mass_mmdt[0]",selection,"m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_pt[0]>300)&&(j_pt[0]<=400)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_pt[0]>350)&&(j_pt[0]<=450)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_pt[0]>400)&&(j_pt[0]<=500)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_pt[0]>450)&&(j_pt[0]<=550)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_pt[0]>500)&&(j_pt[0]<=600)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_pt[0]>550)&&(j_pt[0]<=650)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_pt[0]>600)&&(j_pt[0]<=700)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_pt[0]>700)&&(j_pt[0]<=800)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_pt[0]>800)","m_{mMDT} (GeV)"),
 	    ]
  if runSet==53:
   samples = ["/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:Z01.root",
 	     ]
   selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300)&&(j_nbHadrons[0]>1))"
   normalize=True
   names = ["pt",
           "eta",
           "mass_mmdt5",
 	   "mass_mmdt45",
 	   "mass_mmdt4",
 	   "mass_mmdt35",
 	   "mass_mmdt3",
 	   "mass_mmdt25",
 	   "mass_mmdt2",
 	   "mass_mmdt15",
 	   "mass_mmdt1",
 	   ]
   plots = [("j_pt[0]",selection,"jet p_{T} (GeV)"),
            ("abs(j_eta[0])",selection,"jet |#eta|"),
            ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.5)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.45)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.4)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.35)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.3)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.25)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.2)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.15)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.1)","m_{mMDT} (GeV)"),
 	    ]
  if runSet==54:
   samples = ["/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:Z01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W+.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W-.root",
 	     ]
   selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300))"
   normalize=True
   names = ["pt",
           "eta",
           "mass_mmdt5",
 	   "mass_mmdt45",
 	   "mass_mmdt4",
 	   "mass_mmdt35",
 	   "mass_mmdt3",
 	   "mass_mmdt25",
 	   "mass_mmdt2",
 	   "mass_mmdt15",
 	   "mass_mmdt1",
 	   ]
   plots = [("j_pt[0]",selection,"jet p_{T} (GeV)"),
            ("abs(j_eta[0])",selection,"jet |#eta|"),
            ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.5)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.45)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.4)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.35)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.3)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.25)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.2)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.15)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.1)","m_{mMDT} (GeV)"),
 	    ]
  if runSet==55:
   samples = ["/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-rth:W.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-rthi:p200:W.root",
 	     ]
   selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300))"
   normalize=True
   names = ["mass_mmdt5",
 	   "mass_mmdt45",
 	   "mass_mmdt4",
 	   "mass_mmdt35",
 	   "mass_mmdt3",
 	   "mass_mmdt25",
 	   "mass_mmdt2",
 	   "mass_mmdt15",
 	   "mass_mmdt1",
 	   ]
   plots = [("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.5)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.45)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.4)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.35)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.3)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.25)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.2)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.15)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.1)","m_{mMDT} (GeV)"),
 	    ]
  if runSet==56:
   samples = ["/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:Z01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:Z01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:Z01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:Z01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:Z01.root",
 	     ]
   selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300))"
   normalize=True
   names = ["pt",
           "eta",
           "mass_mmdt5",
 	   "mass_mmdt45",
 	   "mass_mmdt4",
 	   "mass_mmdt35",
 	   "mass_mmdt3",
 	   "mass_mmdt25",
 	   "mass_mmdt2",
 	   "mass_mmdt15",
 	   "mass_mmdt1",
 	   ]
   plots = [("j_pt[0]",selection,"jet p_{T} (GeV)"),
            ("abs(j_eta[0])",selection,"jet |#eta|"),
            ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.5)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.45)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.4)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.35)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.3)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.25)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.2)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.15)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.1)","m_{mMDT} (GeV)"),
 	    ]
  if runSet==57:
   samples = ["/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:Z01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:Z01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:Z01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W:UE.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:Z:UE.root",
 	     ]
   selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300))"
   normalize=True
   names = ["pt",
           "eta",
           "mass_mmdt",
 	   "mass_mmdt300",
 	   "mass_mmdt350",
 	   "mass_mmdt400",
 	   "mass_mmdt450",
 	   "mass_mmdt500",
 	   "mass_mmdt550",
 	   "mass_mmdt600",
 	   "mass_mmdt700",
 	   "mass_mmdt800",
 	   ]
   plots = [("j_pt[0]",selection,"jet p_{T} (GeV)"),
            ("abs(j_eta[0])",selection,"jet |#eta|"),
            ("j_mass_mmdt[0]",selection,"m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_pt[0]>300)&&(j_pt[0]<=400)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_pt[0]>350)&&(j_pt[0]<=450)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_pt[0]>400)&&(j_pt[0]<=500)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_pt[0]>450)&&(j_pt[0]<=550)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_pt[0]>500)&&(j_pt[0]<=600)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_pt[0]>550)&&(j_pt[0]<=650)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_pt[0]>600)&&(j_pt[0]<=700)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_pt[0]>700)&&(j_pt[0]<=800)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_pt[0]>800)","m_{mMDT} (GeV)"),
 	    ]
  if runSet==58:
   samples = ["/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:Z01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:Z01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:Z01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W:UE.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:Z:UE.root",
 	     ]
   selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300))"
   normalize=True
   names = ["pt",
           "eta",
           "mass_mmdt5",
 	   "mass_mmdt45",
 	   "mass_mmdt4",
 	   "mass_mmdt35",
 	   "mass_mmdt3",
 	   "mass_mmdt25",
 	   "mass_mmdt2",
 	   "mass_mmdt15",
 	   "mass_mmdt1",
 	   ]
   plots = [("j_pt[0]",selection,"jet p_{T} (GeV)"),
            ("abs(j_eta[0])",selection,"jet |#eta|"),
            ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.5)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.45)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.4)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.35)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.3)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.25)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.2)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.15)","m_{mMDT} (GeV)"),
 	    ("j_mass_mmdt[0]",selection+"&&(j_n2_b1[0]<0.1)","m_{mMDT} (GeV)"),
 	    ]
  if runSet==59:
   samples = ["/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W:UE.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W:UE.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-rth:W.root",
 	     #"/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:Z.root",
 	     ]
   selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300))"
   normalize=True
   names = ["pt",
           "eta",
           "mass_mmdt",
 	   ]
   plots = [("j_pt[0]",selection,"jet p_{T} (GeV)"),
            ("abs(j_eta[0])",selection,"jet |#eta|"),
            ("j_mass_mmdt[0]",selection,"m_{mMDT} (GeV)"),
 	    ]

  if runSet==60:
   samples = ["/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W:UE.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W:UE.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-rth:W.root",
 	     #"/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:Z.root",
 	     ]
   selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300))"
   normalize=True
   names = ["pt",
           "eta",
           "mass_mmdt",
 	   ]
   plots = [("j_pt[0]",selection,"jet p_{T} (GeV)"),
            ("abs(j_eta[0])",selection,"jet |#eta|"),
            ("j_mass_mmdt[0]",selection,"m_{mMDT} (GeV)"),
 	    ]
  if runSet==159:
   samples = ["/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W:UE.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W:UE.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:W01.root",
 	     "/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-rth:W.root",
 	     #"/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:Z.root",
 	     ]
   selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300))"
   normalize=True
   names = ["pt",
           "eta",
           "mass_mmdt",
 	   ]
   plots = [("j_pt[0]",selection,"jet p_{T} (GeV)"),
            ("abs(j_eta[0])",selection,"jet |#eta|"),
            ("j_mass_mmdt[0]",selection,"m_{mMDT} (GeV)"),
 	    ]
  if runSet==162:
   samples = ["root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/wqq_pt150_100_tarball.tar.xz_pythia/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/wqq_pt150_100_tarball.tar.xz_herwig/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_pythia/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_herwig/ntupler/",
 	     ]
   selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300))"
   normalize=True
   names = [#"pt",
           #"eta",
           "mass_mmdt",
 	   "mass",
           "mass_trim",
 	   "mass_rsd",
 	   "mass_softdrop_b2",
 	   "mass_softdrop_m1",
 	   ]
   plots = [#("j_pt[0]",selection,"jet p_{T} (GeV)"),
            #("abs(j_eta[0])",selection,"jet |#eta|"),
            ("j_mass_mmdt[0]",selection,"m_{mMDT} (GeV)"),
 	    ("j_mass_prun[0]",selection,"pruned jet mass (GeV)"),
 	    ("j_mass_trim[0]",selection,"trimmed jet mass (GeV)"),
 	    ("j_mass_rsd[0]",selection,"r. softdrop (#beta=0) jet mass (GeV)"),
 	    ("j_mass_sdb2[0]",selection,"softdrop (#beta=2) jet mass (GeV)"),
 	    ("j_mass_sdm1[0]",selection,"softdrop (#beta=-1) jet mass (GeV)"),
 	    ]
  if runSet==163:
   samples = ["root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/wqq_pt150_100_tarball.tar.xz_pythia/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/wqq_pt150_100_tarball.tar.xz_herwig/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_pythia/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_herwig/ntupler/",
 	     ]
   selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300)&&(j_n2_b1[0]<0.2))"
   normalize=True
   names = [#"pt",
           #"eta",
           "mass_mmdt",
 	   "mass",
           "mass_trim",
 	   "mass_rsd",
 	   "mass_softdrop_b2",
 	   "mass_softdrop_m1",
 	   ]
   plots = [#("j_pt[0]",selection,"jet p_{T} (GeV)"),
            #("abs(j_eta[0])",selection,"jet |#eta|"),
            ("j_mass_mmdt[0]",selection,"m_{mMDT} (GeV)"),
 	    ("j_mass_prun[0]",selection,"pruned jet mass (GeV)"),
 	    ("j_mass_trim[0]",selection,"trimmed jet mass (GeV)"),
 	    ("j_mass_rsd[0]",selection,"r. softdrop (#beta=0) jet mass (GeV)"),
 	    ("j_mass_sdb2[0]",selection,"softdrop (#beta=2) jet mass (GeV)"),
 	    ("j_mass_sdm1[0]",selection,"softdrop (#beta=-1) jet mass (GeV)"),
 	    ]
  if runSet==164:
   samples = ["root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_pythia/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_herwig/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_pythia/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_herwig/ntupler/",
 	     ]
   selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300)&&(j_n2_b1[0]<0.2))"
   normalize=True
   names = [#"pt",
           #"eta",
           "mass_mmdt",
 	   "mass",
           "mass_trim",
 	   "mass_rsd",
 	   "mass_softdrop_b2",
 	   "mass_softdrop_m1",
 	   ]
   plots = [#("j_pt[0]",selection,"jet p_{T} (GeV)"),
            #("abs(j_eta[0])",selection,"jet |#eta|"),
            ("j_mass_mmdt[0]",selection,"m_{mMDT} (GeV)"),
 	    ("j_mass_prun[0]",selection,"pruned jet mass (GeV)"),
 	    ("j_mass_trim[0]",selection,"trimmed jet mass (GeV)"),
 	    ("j_mass_rsd[0]",selection,"r. softdrop (#beta=0) jet mass (GeV)"),
 	    ("j_mass_sdb2[0]",selection,"softdrop (#beta=2) jet mass (GeV)"),
 	    ("j_mass_sdm1[0]",selection,"softdrop (#beta=-1) jet mass (GeV)"),
 	    ]
  if runSet==165:
   samples = ["root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/wqq_pt150_100_tarball.tar.xz_pythia/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/wqq_pt150_100_tarball.tar.xz_herwig/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_pythia/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_herwig/ntupler/",
 	     #"/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:WP.root",
 	     #"/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:WH.root",
 	     #"/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:ZP.root",
 	     #"/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:ZH.root",
 	     ]
   selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300)&&(j_n2_b1[0]<0.15))"
   normalize=True
   names = [#"pt",
           #"eta",
           "mass_mmdt",
 	   "mass",
           "mass_trim",
 	   "mass_rsd",
 	   "mass_softdrop_b2",
 	   "mass_softdrop_m1",
 	   ]
   plots = [#("j_pt[0]",selection,"jet p_{T} (GeV)"),
            #("abs(j_eta[0])",selection,"jet |#eta|"),
            ("j_mass_mmdt[0]",selection,"m_{mMDT} (GeV)"),
 	    ("j_mass_prun[0]",selection,"pruned jet mass (GeV)"),
 	    ("j_mass_trim[0]",selection,"trimmed jet mass (GeV)"),
 	    ("j_mass_rsd[0]",selection,"r. softdrop (#beta=0) jet mass (GeV)"),
 	    ("j_mass_sdb2[0]",selection,"softdrop (#beta=2) jet mass (GeV)"),
 	    ("j_mass_sdm1[0]",selection,"softdrop (#beta=-1) jet mass (GeV)"),
 	    ]
  if runSet==166:
   samples = ["root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_pythia/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_herwig/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_pythia/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_herwig/ntupler/",
 	     ]
   selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300)&&(j_n2_b1[0]<0.15))"
   normalize=True
   names = [#"pt",
           #"eta",
           "mass_mmdt",
 	   "mass",
           "mass_trim",
 	   "mass_rsd",
 	   "mass_softdrop_b2",
 	   "mass_softdrop_m1",
 	   ]
   plots = [#("j_pt[0]",selection,"jet p_{T} (GeV)"),
            #("abs(j_eta[0])",selection,"jet |#eta|"),
            ("j_mass_mmdt[0]",selection,"m_{mMDT} (GeV)"),
 	    ("j_mass_prun[0]",selection,"pruned jet mass (GeV)"),
 	    ("j_mass_trim[0]",selection,"trimmed jet mass (GeV)"),
 	    ("j_mass_rsd[0]",selection,"r. softdrop (#beta=0) jet mass (GeV)"),
 	    ("j_mass_sdb2[0]",selection,"softdrop (#beta=2) jet mass (GeV)"),
 	    ("j_mass_sdm1[0]",selection,"softdrop (#beta=-1) jet mass (GeV)"),
 	    ]
  if runSet==167:
   samples = ["root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/wqq_pt150_100_tarball.tar.xz_pythia/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/wqq_pt150_100_tarball.tar.xz_herwig/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_pythia/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_herwig/ntupler/",
 	     #"/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:WP.root",
 	     #"/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:WH.root",
 	     #"/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:ZP.root",
 	     #"/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:ZH.root",
 	     ]
   selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300)&&(j_tau21_b1[0]<0.2))"
   normalize=True
   names = [#"pt",
           #"eta",
           "mass_mmdt",
 	   "mass",
           "mass_trim",
 	   "mass_rsd",
 	   "mass_softdrop_b2",
 	   "mass_softdrop_m1",
 	   ]
   plots = [#("j_pt[0]",selection,"jet p_{T} (GeV)"),
            #("abs(j_eta[0])",selection,"jet |#eta|"),
            ("j_mass_mmdt[0]",selection,"m_{mMDT} (GeV)"),
 	    ("j_mass_prun[0]",selection,"pruned jet mass (GeV)"),
 	    ("j_mass_trim[0]",selection,"trimmed jet mass (GeV)"),
 	    ("j_mass_rsd[0]",selection,"r. softdrop (#beta=0) jet mass (GeV)"),
 	    ("j_mass_sdb2[0]",selection,"softdrop (#beta=2) jet mass (GeV)"),
 	    ("j_mass_sdm1[0]",selection,"softdrop (#beta=-1) jet mass (GeV)"),
 	    ]
  if runSet==168:
   samples = ["root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_pythia/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_herwig/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_pythia/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_herwig/ntupler/",
 	     ]
   selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300)&&(j_tau21_b1[0]<0.2))"
   normalize=True
   names = [#"pt",
           #"eta",
           "mass_mmdt",
 	   "mass",
           "mass_trim",
 	   "mass_rsd",
 	   "mass_softdrop_b2",
 	   "mass_softdrop_m1",
 	   ]
   plots = [#("j_pt[0]",selection,"jet p_{T} (GeV)"),
            #("abs(j_eta[0])",selection,"jet |#eta|"),
            ("j_mass_mmdt[0]",selection,"m_{mMDT} (GeV)"),
 	    ("j_mass_prun[0]",selection,"pruned jet mass (GeV)"),
 	    ("j_mass_trim[0]",selection,"trimmed jet mass (GeV)"),
 	    ("j_mass_rsd[0]",selection,"r. softdrop (#beta=0) jet mass (GeV)"),
 	    ("j_mass_sdb2[0]",selection,"softdrop (#beta=2) jet mass (GeV)"),
 	    ("j_mass_sdm1[0]",selection,"softdrop (#beta=-1) jet mass (GeV)"),
 	    ]
  if runSet==169:
   samples = ["root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/wqq_pt150_100_tarball.tar.xz_pythia/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/wqq_pt150_100_tarball.tar.xz_herwig/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_pythia/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_herwig/ntupler/",
 	     #"/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:WP.root",
 	     #"/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:WH.root",
 	     #"/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:ZP.root",
 	     #"/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:ZH.root",
 	     ]
   selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300)&&(j_n2_b1_mmdt[0]<0.2))"
   normalize=True
   names = [#"pt",
           #"eta",
           "mass_mmdt",
 	   "mass",
           "mass_trim",
 	   "mass_rsd",
 	   "mass_softdrop_b2",
 	   "mass_softdrop_m1",
 	   ]
   plots = [#("j_pt[0]",selection,"jet p_{T} (GeV)"),
            #("abs(j_eta[0])",selection,"jet |#eta|"),
            ("j_mass_mmdt[0]",selection,"m_{mMDT} (GeV)"),
 	    ("j_mass_prun[0]",selection,"pruned jet mass (GeV)"),
 	    ("j_mass_trim[0]",selection,"trimmed jet mass (GeV)"),
 	    ("j_mass_rsd[0]",selection,"r. softdrop (#beta=0) jet mass (GeV)"),
 	    ("j_mass_sdb2[0]",selection,"softdrop (#beta=2) jet mass (GeV)"),
 	    ("j_mass_sdm1[0]",selection,"softdrop (#beta=-1) jet mass (GeV)"),
 	    ]
  if runSet==170:
   samples = ["root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_pythia/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_herwig/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_pythia/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_herwig/ntupler/",
 	     ]
   selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300)&&(j_n2_b1_mmdt[0]<0.2))"
   normalize=True
   names = [#"pt",
           #"eta",
           "mass_mmdt",
 	   "mass",
           "mass_trim",
 	   "mass_rsd",
 	   "mass_softdrop_b2",
 	   "mass_softdrop_m1",
 	   ]
   plots = [#("j_pt[0]",selection,"jet p_{T} (GeV)"),
            #("abs(j_eta[0])",selection,"jet |#eta|"),
            ("j_mass_mmdt[0]",selection,"m_{mMDT} (GeV)"),
 	    ("j_mass_prun[0]",selection,"pruned jet mass (GeV)"),
 	    ("j_mass_trim[0]",selection,"trimmed jet mass (GeV)"),
 	    ("j_mass_rsd[0]",selection,"r. softdrop (#beta=0) jet mass (GeV)"),
 	    ("j_mass_sdb2[0]",selection,"softdrop (#beta=2) jet mass (GeV)"),
 	    ("j_mass_sdm1[0]",selection,"softdrop (#beta=-1) jet mass (GeV)"),
 	    ]
  if runSet==171:
   samples = ["root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/wqq_pt150_100_tarball.tar.xz_pythia/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/wqq_pt150_100_tarball.tar.xz_herwig/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_pythia/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_herwig/ntupler/",
 	     #"/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:WP.root",
 	     #"/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:WH.root",
 	     #"/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:ZP.root",
 	     #"/afs/cern.ch/user/h/hinzmann/workspace/Wmass/trackObservables/processing/processed-output.dat-0:ZH.root",
 	     ]
   selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300)&&(j_tau21_b1_mmdt[0]<0.2))"
   normalize=True
   names = [#"pt",
           #"eta",
           "mass_mmdt",
 	   "mass",
           "mass_trim",
 	   "mass_rsd",
 	   "mass_softdrop_b2",
 	   "mass_softdrop_m1",
 	   ]
   plots = [#("j_pt[0]",selection,"jet p_{T} (GeV)"),
            #("abs(j_eta[0])",selection,"jet |#eta|"),
            ("j_mass_mmdt[0]",selection,"m_{mMDT} (GeV)"),
 	    ("j_mass_prun[0]",selection,"pruned jet mass (GeV)"),
 	    ("j_mass_trim[0]",selection,"trimmed jet mass (GeV)"),
 	    ("j_mass_rsd[0]",selection,"r. softdrop (#beta=0) jet mass (GeV)"),
 	    ("j_mass_sdb2[0]",selection,"softdrop (#beta=2) jet mass (GeV)"),
 	    ("j_mass_sdm1[0]",selection,"softdrop (#beta=-1) jet mass (GeV)"),
 	    ]
  if runSet==172:
   samples = ["root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_pythia/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_herwig/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_pythia/ntupler/",
 	     "root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/precision/zqq_pt150_100_tarball.tar.xz_herwig/ntupler/",
 	     ]
   selection = "((abs(j_eta[0])<2.4)&&(j_pt[0]>300)&&(j_tau21_b1_mmdt[0]<0.2))"
   normalize=True
   names = [#"pt",
           #"eta",
           "mass_mmdt",
 	   "mass",
           "mass_trim",
 	   "mass_rsd",
 	   "mass_softdrop_b2",
 	   "mass_softdrop_m1",
 	   ]
   plots = [#("j_pt[0]",selection,"jet p_{T} (GeV)"),
            #("abs(j_eta[0])",selection,"jet |#eta|"),
            ("j_mass_mmdt[0]",selection,"m_{mMDT} (GeV)"),
 	    ("j_mass_prun[0]",selection,"pruned jet mass (GeV)"),
 	    ("j_mass_trim[0]",selection,"trimmed jet mass (GeV)"),
 	    ("j_mass_rsd[0]",selection,"r. softdrop (#beta=0) jet mass (GeV)"),
 	    ("j_mass_sdb2[0]",selection,"softdrop (#beta=2) jet mass (GeV)"),
 	    ("j_mass_sdm1[0]",selection,"softdrop (#beta=-1) jet mass (GeV)"),
 	    ]


  results=[]
  outfile="w_jet_wmass_"+str(runSet+100*theory)+"_out.root"
  print "outfile",outfile
  fout=TFile.Open(outfile,"RECREATE")
  for plot in plots:
   if runSet>1000:
     canvas = TCanvas("c1","c1",0,0,200,260)
     canvas.Divide(1,2,0,0,0)
     canvas.GetPad(1).SetPad(0.0,0.28,1.0,1.0)
     canvas.GetPad(1).SetLeftMargin(0.15)
     canvas.GetPad(1).SetRightMargin(0.08)
     canvas.GetPad(1).SetTopMargin(0.08)
     canvas.GetPad(1).SetBottomMargin(0.05)
     canvas.GetPad(2).SetPad(0.0,0.0,1.0,0.28)
     canvas.GetPad(2).SetLeftMargin(0.15)
     canvas.GetPad(2).SetRightMargin(0.08)
     canvas.GetPad(2).SetTopMargin(0.08)
     canvas.GetPad(2).SetBottomMargin(0.45)
     canvas.cd(1)
     canvas.GetPad(1).SetLogy(False)
   else:
     canvas = TCanvas("c1","c1",0,0,200,200)
     canvas.SetLogy(False)
   if runSet>1000:
     legend=TLegend(0.55,0.7,0.85,0.9)
   else:
     legend=TLegend(0.55,0.65,0.85,0.9)
   if "mass" in plot[2] or "mMDT" in plot[2]:
     legend=TLegend(0.4,0.65,0.85,0.9)
   dataPlotted=False
   counter=0
   integral=1
   originalIntegral={}
   maximum=0
   s=0
   hists=[]
   fs=[]
   ts=[]
   firsthist=None
   for sample in samples:
    s+=1
    for gen in sets:
     if (names[plots.index(plot)]=="pt" or names[plots.index(plot)]=="eta" or names[plots.index(plot)]=="npu" or names[plots.index(plot)]=="npv" or "costheta" in names[plots.index(plot)] or "Phi" in names[plots.index(plot)] or "dR" in names[plots.index(plot)]) and gen=="Gen":
 	continue
     if names[plots.index(plot)]=="npu" and s==2:
 	continue
     if (names[plots.index(plot)]=="pt" or names[plots.index(plot)]=="eta") and gen=="lowPU":
 	continue
     print sample, gen
     
     if ".root" in sample:
       f=TFile.Open(sample)
       fs+=[f]
       tree=f.Get("t_allpar")
     else:
       tree=TChain("t_allpar")
       p=subprocess.Popen(["eos ls "+sample.replace("root://eoscms.cern.ch/","")],shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
       count=0
       for fn in p.stdout:
         if not ".root" in fn: continue
	 count+=1
	 fFile = TFile.Open(sample+fn.replace("\n",""))
         if not fFile or fFile.IsZombie():
	   print "skip broken file"
	   continue
	 fFile.Close()
	 sys.stdout.write(str(count)+",")
	 sys.stdout.flush()
         tree.Add(sample+fn.replace("\n",""))
	 #if count>10 and "QCD" in sample: break ######
	 #break #####
     print ""
     ts+=[tree]
     print sample,tree.GetEntries()
 
     signal = "Hpp" in sample or "Py6" in sample
     histname="plot"+names[plots.index(plot)]+gen+str(s)
     if plot[2]=="jet #eta":
 	hist=TH1F(histname,histname,12,-2.4,2.4);
     elif plot[2]=="jet |#eta|":
 	hist=TH1F(histname,histname,6,0,2.4);
     elif "jet p_{T}" in plot[2]:
 	hist=TH1F(histname,histname,8,300,700);
 	if runSet>1000:
 	  canvas.GetPad(1).SetLogy(True)
 	else:
 	  canvas.SetLogy(True)
     elif "pruned jet mass" in plot[2]:
 	hist=TH1F(histname,histname,30,0,150);
 	if (runSet>=162 and runSet<=172):
 	  hist=TH1F(histname,histname,40,70,110);
        elif runSet==6 or runSet==8:
 	  hist=TH1F(histname,histname,50,0,150);
 	elif runSet==9:
 	  hist=TH1F(histname,histname,25,0,150);
     elif "jet mass (GeV)" in plot[2] or "mMDT" in plot[2]:
       if "-0" in sample and "UE" in sample and (runSet==59 or runSet==60 or runSet==57 or runSet==52 or runSet==58):
 	  hist=TH1F(histname,histname,80,70,110);
       elif (runSet>=162 and runSet<=172) and "r." in plot[2]:
 	  hist=TH1F(histname,histname,40,60,100);
       elif (runSet>=162 and runSet<=172):
 	  hist=TH1F(histname,histname,40,70,110);
       elif "-0" in sample and (runSet==59 or runSet==60):
 	  hist=TH1F(histname,histname,25,70,110);
       elif "-rth" in sample and (runSet==59 or runSet==60):
 	  hist=TH1F(histname,histname,10,70,110);
       #elif "-0" in sample and s==3 and (runSet==52 or runSet==57 or runSet==58):
 	#  hist=TH1F(histname,histname,70,0,150);
       elif "-0" in sample:
 	  hist=TH1F(histname,histname,100,0,160);
       else:
 	  hist=TH1F(histname,histname,30,0,150);
     elif "#tau_{2}/#tau_{1}" in plot[2]:
 	hist=TH1F(histname,histname,20,0,1);
     elif "N2 (#beta=2)" in plot[2]:
 	hist=TH1F(histname,histname,30,0,0.1);
     elif "C1" in plot[2] or "C2" in plot[2] or "D2 (#alpha=1,#beta=2)" in plot[2] or "M2" in plot[2] or "N2" in plot[2]:
 	hist=TH1F(histname,histname,30,0,0.5);
     elif "D2" in plot[2]:
 	hist=TH1F(histname,histname,30,0,5);
     elif "#beta=" in plot[2]:
 	hist=TH1F(histname,histname,30,0,1);
     hist.Sumw2()
 
     variable,cutstring=plot[0],plot[1]

     if runSet==50 and s>2: cutstring += "&&(j_n2_b1[0]<0.25)"
     if runSet==51 and s>2: cutstring += "&&(ddt05(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])<0)"
     if runSet==52 and s==2: cutstring += "&&(j_ncHadrons[0]>0)"
     if runSet==52 and s==4: cutstring += "&&(j_nbHadrons[0]>1)"
     if runSet==52 and s==5: cutstring += "&&(j_ncHadrons[0]>1)&&(j_nbHadrons[0]<1)"
     if runSet==56 and s==2: cutstring = "(kNNLOW(j_pt[0]))*("+cutstring+")"
     if runSet==56 and s==3: cutstring = "(kNNLOW(j_pt[0]))*(1.0+d1kNLOW(j_pt[0]))*(1.0+d2kNLOW(j_pt[0]))*("+cutstring+")"
     if runSet==56 and s==4: cutstring = "(kNNLOW(j_pt[0]))*(1.0+d1kappaEWW(j_pt[0]))*(1.0+d2kappaEWW(j_pt[0]))*("+cutstring+")"
     if runSet==56 and s==5: cutstring = "(kNNLOW(j_pt[0]))*(1.0+dPDFW(j_pt[0]))*("+cutstring+")"
     if runSet==56 and s==7: cutstring = "(kNNLOZ(j_pt[0]))*("+cutstring+")"
     if runSet==56 and s==8: cutstring = "(kNNLOZ(j_pt[0]))*(1.0+d1kNLOZ(j_pt[0]))*(1.0+d2kNLOZ(j_pt[0]))*("+cutstring+")"
     if runSet==56 and s==9: cutstring = "(kNNLOZ(j_pt[0]))*(1.0+d1kappaEWZ(j_pt[0]))*(1.0+d2kappaEWZ(j_pt[0]))*("+cutstring+")"
     if runSet==56 and s==10: cutstring = "(kNNLOZ(j_pt[0]))*(1.0+dPDFZ(j_pt[0]))*("+cutstring+")"
     if runSet==57 and s==2: cutstring += "&&(j_ncHadrons[0]>0)"
     if runSet==57 and s==4: cutstring += "&&(j_nbHadrons[0]>1)"
     if runSet==57 and s==5: cutstring += "&&(j_ncHadrons[0]>1)&&(j_nbHadrons[0]<1)"
     if runSet==58 and s==2: cutstring += "&&(j_ncHadrons[0]>0)"
     if runSet==58 and s==4: cutstring += "&&(j_nbHadrons[0]>1)"
     if runSet==58 and s==5: cutstring += "&&(j_ncHadrons[0]>1)&&(j_nbHadrons[0]<1)"
     if runSet==59 and s!=1: cutstring += "&&(j_n2_b1[0]<0.2)"
     if runSet==60 and s!=3: cutstring += "&&(ddt1(j_n2_b1[0],j_pt[0],j_mass_mmdt[0])<0)"
     if runSet==159 and s!=1: cutstring += "&&(j_n2_b1[0]<0.2)"
     if runSet==159 and s==2: cutstring = "(weight_n2nonpert(j_pt[0]))*("+cutstring+")"
     if runSet==159 and s==1: cutstring = "(weight_raw(j_pt[0]))*("+cutstring+")"
     if runSet==159 and s==4: cutstring = "(weight_n2detector(j_pt[0]))*("+cutstring+")"
     if runSet==164 and s==3: cutstring += "&&(j_nbHadrons[0]>1)"
     if runSet==164 and s==4: cutstring += "&&(j_nbHadrons[0]>1)"
     if runSet==166 and s==3: cutstring += "&&(j_nbHadrons[0]>1)"
     if runSet==166 and s==4: cutstring += "&&(j_nbHadrons[0]>1)"
     if runSet==168 and s==3: cutstring += "&&(j_nbHadrons[0]>1)"
     if runSet==168 and s==4: cutstring += "&&(j_nbHadrons[0]>1)"
     if runSet==170 and s==3: cutstring += "&&(j_nbHadrons[0]>1)"
     if runSet==170 and s==4: cutstring += "&&(j_nbHadrons[0]>1)"
     if runSet==172 and s==3: cutstring += "&&(j_nbHadrons[0]>1)"
     if runSet==172 and s==4: cutstring += "&&(j_nbHadrons[0]>1)"
     if "TT" in sample: cutstring = "(-1*(event_weights<0)+1*(event_weights>0))*("+cutstring+")"

     print s,histname,variable,cutstring
     tree.Project(histname,variable,cutstring)
     fout.cd()
     hist.Write()
     if "QCD" in sample:
 	 originalIntegral[histname]=hist.Integral()
     hist.SetTitle("")
     hist.SetFillStyle(0)
     hist.SetMarkerStyle(20)
     #hist.SetMarkerSize(2)
     if runSet>1000:
       hist.GetXaxis().SetTitle("")
       hist.GetXaxis().SetLabelColor(0)
       hist.GetYaxis().SetTitle("Events")
       if "pruned jet mass" in plot[2]:
 	   hist.GetYaxis().SetTitle("Events / (3 GeV)")
     elif not normalize:
       hist.GetXaxis().SetTitle(plot[2])
       hist.GetYaxis().SetTitle("Events")
     else:
       hist.GetXaxis().SetTitle(plot[2])
       hist.GetYaxis().SetTitle("Normalized Distribution")
     if "Run" in sample:
 	 integral=hist.Integral()
     if normalize and hist.Integral()>0:
       if runSet==50 or runSet==51:
 	 hist.Scale(integral/hist.Integral(hist.GetXaxis().FindBin(65),hist.GetXaxis().FindBin(105)))
       elif (runSet==59 or runSet==60 or (runSet>=162 and runSet<=172)) and "mass" in variable:
 	 hist.Scale(integral/hist.Integral()/hist.GetXaxis().GetBinWidth(1))
       else:
 	 hist.Scale(integral/hist.Integral())
 
     print "mean",hist.GetMean()

     hists+=[hist]
     print hists
 
     hist.SetLineColor(colors[counter])
     hist.SetLineStyle(styles[counter])        
     hist.SetLineWidth(widths[counter])
     if runSet==2 or runSet==4 or runSet==5 or runSet==6 or runSet==8 or runSet==9:
       hist.SetLineStyle(2)        
       hist.SetLineWidth(4)
     
     option="histc"
     if counter==0:
       firsthist=hist
       hist.Draw(option)
     else:
       hist.Draw(option+"same")

     if hist.GetMaximum()>maximum:
       if hist.GetMaximum()>=hist.Integral():
         maximum=hist.GetBinContent(1)
       else:
 	 maximum=hist.GetMaximum()
 
     if "jet p_{T}" in plot[2]:
       firsthist.GetYaxis().SetRangeUser(maximum/50.0,maximum*2.0)
     else:
       firsthist.GetYaxis().SetRangeUser(0,maximum*1.2)
 
     if runSet>1000:
       canvas.cd(2)
       ratio=hist.Clone(hist.GetName()+"clone")
       hists+=[ratio]
       ratio.Divide(hists[0],hist)
       for b in range(hist.GetNbinsX()):
 	 if hists[0].GetBinContent(b+1)>0:
 	   ratio.SetBinError(b+1,hists[0].GetBinError(b+1)/hists[0].GetBinContent(b+1))
       ratio.GetYaxis().SetTitle("Data / Sim")
       ratio.GetYaxis().SetTitleSize(0.13)
       ratio.GetYaxis().SetTitleOffset(0.5)
       ratio.SetMarkerSize(0.1)
       ratio.GetYaxis().SetLabelSize(0.14)
       ratio.GetYaxis().SetRangeUser(0.8,1.2)
       ratio.GetYaxis().SetNdivisions(503)
       ratio.GetXaxis().SetLabelColor(1)
       ratio.GetXaxis().SetTitle(plot[2])
       ratio.GetXaxis().SetTitleSize(0.16)
       ratio.GetXaxis().SetTitleOffset(0.8)
       ratio.GetXaxis().SetLabelSize(0.14)
       if counter==0:
 	 ratio.Draw("histe")
       else:
 	 ratio.Draw("histsame")
       #line=TLine(ratio.GetXaxis().GetBinLowEdge(1),1,ratio.GetXaxis().GetBinLowEdge(ratio.GetNbinsX()+1),1)
       #hists+=[line]
       #line.Draw("same")
       canvas.cd(1)
       firsthist.GetYaxis().SetTitleOffset(1.2)
 
     if "WJets" in sample:
       entry="W+jets"
     elif "ZJets" in sample:
       entry="Z+jets"
     elif "QCD" in sample:
       entry="QCD"
     elif "WW" in sample and "pt1-" in sample and ((samples.index(sample)==0) or runSet==3):
       entry="W (pT=1 TeV)"
     elif "qq" in sample and "pt1-" in sample and (samples.index(sample)==0 or runSet==3):
       entry="q (pT=1 TeV)"
     elif "WW" in sample and "pt5-" in sample and ((samples.index(sample)==0) or runSet==3):
       entry="W (pT=5 TeV)"
     elif "WW" in sample and "pt300-" in sample and ((samples.index(sample)==0) or runSet==3):
       entry="W (pT=0.3 TeV)"
     elif "WW" in sample and "pt500-" in sample and ((samples.index(sample)==0) or runSet==3):
       entry="W (pT=0.5 TeV)"
     elif "WW" in sample and "pt3500-" in sample and ((samples.index(sample)==0) or runSet==3):
       entry="W (pT=3.5 TeV)"
     elif "-rth:p20:i" in sample:
       entry="R,Tpt,H,PU20+PP"
     elif "-rth:p20" in sample:
       entry="R,Tpt,H,PU20"
     elif "-rsh" in sample:
       entry="R,Tdr,H"
     elif "HS1.01:PS1.0:CS1.0" in sample:
       entry="hadron"
     elif "HS1.0:PS1.01:CS1.0" in sample:
       entry="photon"
     elif "HS1.0:PS1.0:CS1.01" in sample:
       entry="charged"
     elif "HS1.0:PS1.0:CS1.0" in sample:
       entry="central"
     elif ("W" in sample or "w" in sample) and (runSet==162 or runSet==163 or runSet==165 or runSet==167 or runSet==169 or runSet==171) and s==1:
       entry="W, Pythia"
     elif ("W" in sample or "w" in sample) and (runSet==162 or runSet==163 or runSet==165 or runSet==167 or runSet==169 or runSet==171) and s==2:
       entry="W, Herwig"
     elif ("Z" in sample or "z" in sample) and (runSet==162 or runSet==163 or runSet==165 or runSet==167 or runSet==169 or runSet==171) and s==3:
       entry="Z, Pythia"
     elif ("Z" in sample or "z" in sample) and (runSet==162 or runSet==163 or runSet==165 or runSet==167 or runSet==169 or runSet==171) and s==4:
       entry="Z, Herwig"
     elif ("Z" in sample or "z" in sample) and (runSet==164 or runSet==166 or runSet==168 or runSet==170 or runSet==172) and s==1:
       entry="Z, Pythia"
     elif ("Z" in sample or "z" in sample) and (runSet==164 or runSet==166 or runSet==168 or runSet==170 or runSet==172) and s==2:
       entry="Z, Herwig"
     elif ("Z" in sample or "z" in sample) and (runSet==164 or runSet==166 or runSet==168 or runSet==170 or runSet==172) and s==3:
       entry="Z #rightarrow bb, Pythia"
     elif ("Z" in sample or "z" in sample) and (runSet==164 or runSet==166 or runSet==168 or runSet==170 or runSet==172) and s==4:
       entry="Z #rightarrow bb, Herwig"
     elif "W" in sample and (runSet==59 or runSet==159) and s==1:
       entry="W, no non-pert. eff"
     elif "W" in sample and (runSet==59 or runSet==159) and s==3:
       entry="W, N_{2}^{#beta=1}<0.2"
     elif "Z" in sample and (runSet==59 or runSet==159) and s==5:
       entry="Z, N_{2}^{#beta=1}<0.2"
     elif "W" in sample and (runSet==59 or runSet==159) and s==2:
       entry="W, N_{2}^{#beta=1}<0.2, no non-pert. eff"
     elif "W" in sample and (runSet==59 or runSet==159) and s==4:
       entry="W, N_{2}^{#beta=1}<0.2, with detector"
     elif "W" in sample and (runSet==60) and s==1:
       entry="W, no non-pert. eff"
     elif "W" in sample and (runSet==60) and s==3:
       entry="W, DDT N_{2}^{#beta=1} 1%"
     elif "Z" in sample and (runSet==60) and s==5:
       entry="Z, DDT N_{2}^{#beta=1} 1%"
     elif "W" in sample and (runSet==60) and s==2:
       entry="W, DDT N_{2}^{#beta=1} 1%, no non-pert. eff"
     elif "W" in sample and (runSet==60) and s==4:
       entry="W, DDT N_{2}^{#beta=1} 1%, with detector"
     elif "W" in sample and runSet==56 and s==1:
       entry="W (LO)"
     elif "W" in sample and runSet==56 and s==2:
       entry="W (NNLO)"
     elif "W" in sample and runSet==56 and s==3:
       entry="W (NNLO+1#sigma QCD)"
     elif "W" in sample and runSet==56 and s==4:
       entry="W (NNLO+1#sigma EW)"
     elif "W" in sample and runSet==56 and s==5:
       entry="W (NNLO+1#sigma PDF)"
     elif "Z" in sample and runSet==56 and s==6:
       entry="Z (LO)"
     elif "Z" in sample and runSet==56 and s==7:
       entry="Z (NNLO)"
     elif "Z" in sample and runSet==56 and s==8:
       entry="Z (NNLO+1#sigma QCD)"
     elif "Z" in sample and runSet==56 and s==9:
       entry="Z (NNLO+1#sigma EW)"
     elif "Z" in sample and runSet==56 and s==10:
       entry="Z (NNLO+1#sigma PDF)"
     elif "W" in sample and (runSet==52 or runSet==57 or runSet==58) and s==2:
       entry="W #rightarrow cs"
     elif "Z" in sample and (runSet==52 or runSet==57 or runSet==58) and s==4:
       entry="Z #rightarrow bb"
     elif "Z" in sample and (runSet==52 or runSet==57 or runSet==58) and s==5:
       entry="Z #rightarrow cc"
     elif "W:UE" in sample:
       entry="W, no non-pert. eff"
     elif "Z:UE" in sample:
       entry="Z, no non-pert. eff"
     elif "W+" in sample:
       entry="W+"
     elif "W-" in sample:
       entry="W-"
     elif "Z" in sample:
       entry="Z"
     elif "W" in sample:
       entry="W"
     elif "-rth" in sample:
       entry="R,Tpt,H"
     elif "-ruh" in sample:
       entry="R,Teff,H"
     elif "-reh" in sample:
       entry="R,E,H"
     elif "-rh" in sample:
       entry="R,H"
     elif "-r" in sample:
       entry="R"
 
     if runSet==50 and s>2: entry += ", N2_{#beta=1}<0.25"
     if runSet==51 and s>2: entry += ", DDT N2_{#beta=1} 0.5%"
 
     if "mass" in plot[2] or "p_{T}" in plot[2] or "mMDT" in plot[2]:
       maxbin=0
       maxcontent=0
       for b in range(hist.GetXaxis().GetNbins()):
 	 if hist.GetXaxis().GetBinCenter(b+1)>65 and hist.GetBinContent(b+1)>maxcontent:
 	   maxbin=b
 	   maxcontent=hist.GetBinContent(b+1)
       mean=hist.GetXaxis().GetBinCenter(maxbin)
       print "max",mean
       fitmin=-1.0
       fitmax=1.0
       if runSet==162 or runSet==163 or runSet==164 or runSet==165 or runSet==166:
         fitmin=-1.0
	 fitmax=0.67
       g1 = TF1("g1","gaus", 0.7*mean,1.3*mean)
       hist.Fit(g1, "R0")
       mean=g1.GetParameter(1)
       sigma=g1.GetParameter(2)
       g1 = TF1("g1","gaus", mean+fitmin*sigma,mean+fitmax*sigma)
       g1.SetParameter(1,mean)
       g1.SetParameter(2,sigma)
       hist.Fit(g1, "R0")
       mean=g1.GetParameter(1)
       sigma=g1.GetParameter(2)
       g1 = TF1("g1","gaus", mean+fitmin*sigma,mean+fitmax*sigma)
       g1.SetParameter(1,mean)
       g1.SetParameter(2,sigma)
       hist.Fit(g1, "R0")
       print "gauss fit",g1.GetParameter(1)
       xq=array.array('d',[0.5])
       yq=array.array('d',[0.])
       hist.GetQuantiles(1,yq,xq)
       print "median", yq[0]
       if (g1.GetParameter(1)>65 and g1.GetParameter(1)<105) and runSet!=59 and runSet!=60:
 	 hmean = int(g1.GetParameter(1)*1000.)/1000.
 	 entry+= " "+str(hmean)+""
         hres = int(g1.GetParameter(2)/g1.GetParameter(1)*1000.)/10.
 	 entry+= " ("+str(hres)+"%)"

     legend.AddEntry(hist,entry,"l")
     counter+=1
 
   legend.SetTextSize(0.036)
   legend.SetFillStyle(0)
   legend.Draw("same")
 
   legend4=TLegend(0.23,0.85,0.5,0.9,"anti-k_{T} R=0.8")
   legend4.SetTextSize(0.03)
   legend4.SetFillStyle(0)
   #legend4.Draw("same")
 
   #legend2=TLegend(0.17,0.8,0.5,0.85,"p_{T} > 500 GeV")
   #legend2.SetTextSize(0.03)
   #legend2.SetFillStyle(0)
   #legend2.Draw("same")
 
   #if runSet==11:
   #  legend2=TLegend(0.17,0.8,0.5,0.85,"1.4 < p_{T} < 1.6 TeV")
   #  legend2.SetTextSize(0.03)
   #  legend2.SetFillStyle(0)
   #  legend2.Draw("same")
 
   legend2a=TLegend(0.24,0.8,0.5,0.85,"|#eta|<2.4")
   legend2a.SetTextSize(0.03)
   legend2a.SetFillStyle(0)
   #legend2a.Draw("same")
 
   #if runSet==2:
   #  banner = TLatex(0.27,0.93,"  CMS  	L = 19.6 fb^{-1} at #sqrt{s} = 8 TeV, dijets");
   #elif runSet==6 and theory:
   banner = TLatex(0.32,0.93,"Pythia8, #sqrt{s} = 13 TeV");
   #else:
   #  banner = TLatex(0.24,0.93,"CMS Simulation, #sqrt{s} = 8 TeV, dijets");
   banner.SetNDC()
   banner.SetTextSize(0.04)
   #banner.Draw();  
 
   if "aftermass" in names[plots.index(plot)]:
   #if False:
      #legend3=TLegend(0.17,0.7,0.5,0.75,"#tau_{2}/#tau_{1}<0.25")
      if "#tau_{2}/#tau_{1}" in plot[2]:
        legend3=TLegend(0.17,0.75,0.5,0.8,"65 < pruned jet mass < 105")
      else:
        legend3=TLegend(0.17,0.75,0.5,0.8,"65 < m_{mMDT} < 105")
      legend3.SetTextSize(0.03)
      legend3.SetFillStyle(0)
      legend3.Draw("same")
 
   canvas.SaveAs("w_jet_wmass_"+names[plots.index(plot)]+"_"+str(runSet+100*theory)+".png")
   canvas.SaveAs("w_jet_wmass_"+names[plots.index(plot)]+"_"+str(runSet+100*theory)+".pdf")
   canvas.SaveAs("w_jet_wmass_"+names[plots.index(plot)]+"_"+str(runSet+100*theory)+".root")
   canvas.SaveAs("w_jet_wmass_"+names[plots.index(plot)]+"_"+str(runSet+100*theory)+".C")
   canvas.SaveAs("w_jet_wmass_"+names[plots.index(plot)]+"_"+str(runSet+100*theory)+".eps")
