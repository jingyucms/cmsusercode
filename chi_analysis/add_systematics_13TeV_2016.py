import os, sys
from ROOT import * 
from DataFormats.FWLite import Events,Handle
import array
from math import *
from scipy import stats

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

def rebin(h1,nbins,binning):
    for b in range(h1.GetXaxis().GetNbins()):
        h1.SetBinContent(b+1,h1.GetBinContent(b+1)*h1.GetBinWidth(b+1))
        h1.SetBinError(b+1,h1.GetBinError(b+1)*h1.GetBinWidth(b+1))
    h1=h1.Rebin(nbins,h1.GetName()+"_rebin",binning)
    for b in range(h1.GetXaxis().GetNbins()):
        h1.SetBinContent(b+1,h1.GetBinContent(b+1)/h1.GetBinWidth(b+1))
        h1.SetBinError(b+1,h1.GetBinError(b+1)/h1.GetBinWidth(b+1))
    return h1

def cloneNormalize(h1):
    h1=h1.Clone(h1.GetName()+"clone")
    for b in range(h1.GetXaxis().GetNbins()):
        h1.SetBinContent(b+1,h1.GetBinContent(b+1)/h1.GetBinWidth(b+1))
        h1.SetBinError(b+1,h1.GetBinError(b+1)/h1.GetBinWidth(b+1))
    return h1

if __name__ == '__main__':

    useLensData=False
    useUnfoldedData=True
    injectSignal=False

    prefixs=["datacard_shapelimit13TeV"]
 
    #negligible jes source commented out
    jessources = ["AbsoluteStat", 
#"AbsoluteScale", 
#"AbsoluteFlavMap", 
"AbsoluteMPFBias", 
"Fragmentation",
#"SinglePionECAL", 
"SinglePionHCAL",
#"FlavorQCD", 
"TimePtEta",
"RelativeJEREC1",
#"RelativeJEREC2",
"RelativeJERHF",
#"RelativePtBB",
"RelativePtEC1",
"RelativePtEC2",
#"RelativePtHF",
"RelativeBal",
"RelativeFSR",
"RelativeStatFSR", 
#"RelativeStatEC", 
#"RelativeStatHF",
"PileUpPtRef", 
#"PileUpPtBB", 
"PileUpPtEC1", 
"PileUpPtEC2", 
#"PileUpPtHF",
"PileUpMuZero", 
#"PileUpEnvelope",
"SumInQuadrature" ]
    print len(jessources)-1,"jes sources"

 
    chi_bins=[(1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,3,6,9,12,16),
              ]
    massbins=[(1900,2400),
              (2400,3000),
              (3000,3600),
              (3600,4200),
              (4200,4800),
              (4800,5400),
              (5400,6000),
              (6000,13000)]
    mass_bins_nlo3={}
    mass_bins_nlo3[2]=1900
    mass_bins_nlo3[3]=2400
    mass_bins_nlo3[4]=3000
    mass_bins_nlo3[5]=3600
    mass_bins_nlo3[6]=4200
    mass_bins_nlo3[7]=4800
    mass_bins_nlo3[8]=5400
    mass_bins_nlo3[9]=6000
    mass_bins_nlo3[10]=6600
    mass_bins_nlo3[11]=13000
    mass_bins_nlo_list=[(2,),
                  (3,),
                  (4,),
                  (5,),
                  (6,),
              (7,),
              (8,),
              (9,10,),
                 ]
    if useUnfoldedData:
       massbins=massbins[1:]
       mass_bins_nlo_list=mass_bins_nlo_list[1:]
       chi_bins=chi_bins[1:]
    chi_binnings=[]
    for mass_bin in chi_bins:
        chi_binnings+=[array.array('d')]
        for chi_bin in mass_bin:
            chi_binnings[-1].append(chi_bin)

    samples=[]
    samples2=[]
    samples3=[]

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
    samples2+=[("QCDCIminusLL8000",[("pythia8_ci_m1500_1900_8000_-1_0_0_13TeV_Nov14",3.307e-06),
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
    samples2+=[("QCDADD6000",[("pythia8_add_m1500_1900_6000_0_0_0_1_13TeV_Nov14",3.307e-06),
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
             ("QCDADD15000",[("pythia8_add_m1500_1900_15000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m1900_2400_15000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m2400_2800_15000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m2800_3300_15000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m3300_3800_15000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m3800_4300_15000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m4300_5200_15000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m5200_13000_15000_0_0_0_1_13TeV_Nov14",1),
                       ]),
             ("QCDADD16000",[("pythia8_add_m1500_1900_16000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m1900_2400_16000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m2400_2800_16000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m2800_3300_16000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m3300_3800_16000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m3800_4300_16000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m4300_5200_16000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m5200_13000_16000_0_0_0_1_13TeV_Nov14",1),
                       ]),
             ("QCDADD17000",[("pythia8_add_m1500_1900_17000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m1900_2400_17000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m2400_2800_17000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m2800_3300_17000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m3300_3800_17000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m3800_4300_17000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m4300_5200_17000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m5200_13000_17000_0_0_0_1_13TeV_Nov14",1),
                       ]),
             ("QCDADD18000",[("pythia8_add_m1500_1900_18000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m1900_2400_18000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m2400_2800_18000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m2800_3300_18000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m3300_3800_18000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m3800_4300_18000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m4300_5200_18000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m5200_13000_18000_0_0_0_1_13TeV_Nov14",1),
                       ]),
             ("QCDADD19000",[("pythia8_add_m1500_1900_19000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m1900_2400_19000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m2400_2800_19000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m2800_3300_19000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m3300_3800_19000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m3800_4300_19000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m4300_5200_19000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m5200_13000_19000_0_0_0_1_13TeV_Nov14",1),
                       ]),
             ("QCDADD20000",[("pythia8_add_m1500_1900_20000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m1900_2400_20000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m2400_2800_20000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m2800_3300_20000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m3300_3800_20000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m3800_4300_20000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m4300_5200_20000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m5200_13000_20000_0_0_0_1_13TeV_Nov14",1),
                       ]),
             ("QCDADD21000",[("pythia8_add_m1500_1900_21000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m1900_2400_21000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m2400_2800_21000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m2800_3300_21000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m3300_3800_21000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m3800_4300_21000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m4300_5200_21000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m5200_13000_21000_0_0_0_1_13TeV_Nov14",1),
                       ]),
             ("QCDADD22000",[("pythia8_add_m1500_1900_22000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m1900_2400_22000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m2400_2800_22000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m2800_3300_22000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m3300_3800_22000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m3800_4300_22000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m4300_5200_22000_0_0_0_1_13TeV_Nov14",1),
                       ("pythia8_add_m5200_13000_22000_0_0_0_1_13TeV_Nov14",1),
                       ]),
             ]
    samples+=[("QCD",[("pythia8_ci_m1000_1500_50000_1_0_0_13TeV_Nov14",3.769e-05),
                       ("pythia8_ci_m1500_1900_50000_1_0_0_13TeV_Nov14",3.307e-06),
                       ("pythia8_ci_m1900_2400_50000_1_0_0_13TeV_Nov14",8.836e-07),
                       ("pythia8_ci_m2400_2800_50000_1_0_0_13TeV_Nov14",1.649e-07),
                       ("pythia8_ci_m2800_3300_50000_1_0_0_13TeV_Nov14",6.446e-08),
                       ("pythia8_ci_m3300_3800_50000_1_0_0_13TeV_Nov14",1.863e-08),
                       ("pythia8_ci_m3800_4300_50000_1_0_0_13TeV_Nov14",5.867e-09),
                       ("pythia8_ci_m4300_13000_50000_1_0_0_13TeV_Nov14",3.507e-09),
                       ]),
            ]
    samples2+=[("QCDAntiCIplusLL12000",[("pythia8_ci_m1500_1900_12000_1_0_0_13TeV_Nov14",3.307e-06),
                       ("pythia8_ci_m1900_2400_12000_1_0_0_13TeV_Nov14",8.836e-07),
                       ("pythia8_ci_m2400_2800_12000_1_0_0_13TeV_Nov14",1.649e-07),
                       ("pythia8_ci_m2800_3300_12000_1_0_0_13TeV_Nov14",6.446e-08),
                       ("pythia8_ci_m3300_3800_12000_1_0_0_13TeV_Nov14",1.863e-08),
                       ("pythia8_ci_m3800_4300_12000_1_0_0_13TeV_Nov14",5.867e-09),
                       ("pythia8_ci_m4300_13000_12000_1_0_0_13TeV_Nov14",3.507e-09),
                       ]),
             ]
    samples2+=[("QCDCIplusLL12000",[("pythia8_ci_m1500_1900_12000_1_0_0_13TeV_Nov14",3.307e-06),
                       ("pythia8_ci_m1900_2400_12000_1_0_0_13TeV_Nov14",8.836e-07),
                       ("pythia8_ci_m2400_2800_12000_1_0_0_13TeV_Nov14",1.649e-07),
                       ("pythia8_ci_m2800_3300_12000_1_0_0_13TeV_Nov14",6.446e-08),
                       ("pythia8_ci_m3300_3800_12000_1_0_0_13TeV_Nov14",1.863e-08),
                       ("pythia8_ci_m3800_4300_12000_1_0_0_13TeV_Nov14",5.867e-09),
                       ("pythia8_ci_m4300_13000_12000_1_0_0_13TeV_Nov14",3.507e-09),
                       ]),
             ]

    for m in range(5,31):
    #for m in range(29,31):
       samples2+=[#("cs_ct14nlo_"+str(m*1000)+"_LL+",[]),
               #("cs_ct14nlo_"+str(m*1000)+"_LL-",[]),
               #("cs_ct14nlo_"+str(m*1000)+"_RR+",[]),
               #("cs_ct14nlo_"+str(m*1000)+"_RR-",[]),
               #("cs_ct14nlo_"+str(m*1000)+"_VV+",[]),
               #("cs_ct14nlo_"+str(m*1000)+"_VV-",[]),
               #("cs_ct14nlo_"+str(m*1000)+"_AA+",[]),
               #("cs_ct14nlo_"+str(m*1000)+"_AA-",[]),
               #("cs_ct14nlo_"+str(m*1000)+"_V-A+",[]),
               ("cs_ct14nlo_"+str(m*1000)+"_V-A-",[]),
               ]

    for mass in [1700,2000,2300,2600,2900,3200,3500,3800,4100,4400,4700,5000,5300,5600,5900,6200,6500,6800,7100]:
     for xsec in [5e-5,1e-4,2e-4,5e-4,1e-3,2e-3,5e-3,1e-2,2e-2,5e-2,1e-2]:
      for width in ["kMG1439","kMG2035","kMG2493","kMG3218"]:
        for decay in ["GluonGluon","QuarkQuark"]:
          samples2+=[("wide"+str(mass)+"_"+str(xsec)+"_"+decay+"_"+width,["wide"+str(mass)+"_"+str(xsec)+"_"+decay+"_"+width,1])]

    #xsecs={}
    #for l in open("xsecs_13TeV_dm.txt").readlines():
    #  xsecs[l.split("     ")[0]]=eval(l.split("     ")[1])
    #for mass in [1000,1500,1750,2000,2250,2500,3000,3500,4000,4500,5000,6000]:
    #for mass in [2000,2250,2500,3000,3500,4000,4500,5000,6000]:
    for mass in [6000]:
     if mass==6000:
       mDMs=[1,2990]
     elif mass==7000:
       mDMs=[1,4000]
     elif mass==8000:
       mDMs=[1,3990]
     else:
       mDMs=[1,3000]
     mDMs=[1]
     for mDM in mDMs:
      for weight in ['gdmv_1p0_gdma_0_gv_0p01_ga_0', 'gdmv_1p0_gdma_0_gv_0p05_ga_0', 'gdmv_1p0_gdma_0_gv_0p1_ga_0', 'gdmv_1p0_gdma_0_gv_0p2_ga_0', 'gdmv_1p0_gdma_0_gv_0p25_ga_0', 'gdmv_1p0_gdma_0_gv_0p3_ga_0', 'gdmv_1p0_gdma_0_gv_0p5_ga_0', 'gdmv_1p0_gdma_0_gv_0p75_ga_0', 'gdmv_1p0_gdma_0_gv_1_ga_0', 'gdmv_1p0_gdma_0_gv_1p5_ga_0', 'gdmv_1p0_gdma_0_gv_2p0_ga_0', 'gdmv_1p0_gdma_0_gv_2p5_ga_0', 'gdmv_1p0_gdma_0_gv_3p0_ga_0']:
         samples2+=[("DMVector_Dijet_LO_Mphi_"+str(mass)+"_"+str(mDM)+"_1p0_1p0_Mar5_"+weight,[("DMVector_Dijet_LO_Mphi_"+str(mass)+"_"+str(mDM)+"_1p0_1p0_Mar5_"+weight,0)]),
             ]
      for weight in ['gdmv_0_gdma_1p0_gv_0_ga_0p01', 'gdmv_0_gdma_1p0_gv_0_ga_0p05', 'gdmv_0_gdma_1p0_gv_0_ga_0p1', 'gdmv_0_gdma_1p0_gv_0_ga_0p2', 'gdmv_0_gdma_1p0_gv_0_ga_0p25', 'gdmv_0_gdma_1p0_gv_0_ga_0p3', 'gdmv_0_gdma_1p0_gv_0_ga_0p5', 'gdmv_0_gdma_1p0_gv_0_ga_0p75', 'gdmv_0_gdma_1p0_gv_0_ga_1', 'gdmv_0_gdma_1p0_gv_0_ga_1p5', 'gdmv_0_gdma_1p0_gv_0_ga_2p0', 'gdmv_0_gdma_1p0_gv_0_ga_2p5', 'gdmv_0_gdma_1p0_gv_0_ga_3p0']:
      #for weight in ['gdmv_0_gdma_1p0_gv_0_ga_0p5']:
         samples2+=[("DMAxial_Dijet_LO_Mphi_"+str(mass)+"_"+str(mDM)+"_1p0_1p0_Mar5_"+weight,[("DMAxial_Dijet_LO_Mphi_"+str(mass)+"_"+str(mDM)+"_1p0_1p0_Mar5_"+weight,0)]),
             ]

    for m in [[7500,0.01678352],[8000,0.004871688],[8500,0.001292072],[9000,0.0003054339],[9500,0.00006221544],[10000,0.00001040396],[10500,0.000001327101],[11000,0.0000001145733]]:
        samples3+=[("QBH_"+str(m[0])+"_6",[("QBH_"+str(m[0])+"_6",m[1])]),]

    for m in [[4500,0.05148],[5000,0.01829],[5500,0.006472],[6000,0.002250],[6500,0.0007599],[7000,0.0002461]]:
        samples3+=[("QBH_"+str(m[0])+"_RS1",[("QBH_"+str(m[0])+"_RS1",m[1])]),]

    #samples=samples3

    print samples
    #sys.exit()
    dataevents={}
    datahist={}
    data=None
    dataplot={}
    qcdnorm={}
    cinorm={}
    for prefix in prefixs: 
     # signal cards
     for i in range(len(samples)):
      if samples[i][0]=="QCDCIplusLL8000":
        sample=prefix + '_GENnp-0-v4_chi2016.root'
      elif samples[i][0]=="QCDCIplusLL9000":
        sample=prefix + '_GENnp-1-v4_chi2016.root'
      elif samples[i][0]=="QCDCIplusLL10000":
        sample=prefix + '_GENnp-2-v4_chi2016.root'
      elif samples[i][0]=="QCDCIplusLL11000":
        sample=prefix + '_GENnp-3-v4_chi2016.root'
      elif samples[i][0]=="QCDCIplusLL12000":
        sample=prefix + '_GENnp-4-v4_chi2016.root'
      elif samples[i][0]=="QCDCIplusLL13000":
        sample=prefix + '_GENnp-5-v4_chi2016.root'
      elif samples[i][0]=="QCDCIplusLL14000":
        sample=prefix + '_GENnp-6-v4_chi2016.root'
      elif samples[i][0]=="QCDCIplusLL16000":
        sample=prefix + '_GENnp-7-v4_chi2016.root'
      elif samples[i][0]=="QCDCIplusLL18000":
        sample=prefix + '_GENnp-8-v4_chi2016.root'
      elif samples[i][0]=="QCDCIminusLL8000":
        sample=prefix + '_GENnp-9-v4_chi2016.root'
      elif samples[i][0]=="QCDCIminusLL9000":
        sample=prefix + '_GENnp-10-v4_chi2016.root'
      elif samples[i][0]=="QCDCIminusLL10000":
        sample=prefix + '_GENnp-11-v4_chi2016.root'
      elif samples[i][0]=="QCDCIminusLL11000":
        sample=prefix + '_GENnp-12-v4_chi2016.root'
      elif samples[i][0]=="QCDCIminusLL12000":
        sample=prefix + '_GENnp-13-v4_chi2016.root'
      elif samples[i][0]=="QCDCIminusLL13000":
        sample=prefix + '_GENnp-14-v4_chi2016.root'
      elif samples[i][0]=="QCDCIminusLL14000":
        sample=prefix + '_GENnp-15-v4_chi2016.root'
      elif samples[i][0]=="QCDCIminusLL16000":
        sample=prefix + '_GENnp-16-v4_chi2016.root'
      elif samples[i][0]=="QCDCIminusLL18000":
        sample=prefix + '_GENnp-17-v4_chi2016.root'
      elif samples[i][0]=="QCDADD6000":
        sample=prefix + '_GENnp-18-v5_chi2016.root'
      elif samples[i][0]=="QCDADD7000":
        sample=prefix + '_GENnp-19-v5_chi2016.root'
      elif samples[i][0]=="QCDADD8000":
        sample=prefix + '_GENnp-20-v5_chi2016.root'
      elif samples[i][0]=="QCDADD9000":
        sample=prefix + '_GENnp-21-v5_chi2016.root'
      elif samples[i][0]=="QCDADD10000":
        sample=prefix + '_GENnp-22-v5_chi2016.root'
      elif samples[i][0]=="QCDADD11000":
        sample=prefix + '_GENnp-23-v5_chi2016.root'
      elif samples[i][0]=="QCDADD12000":
        sample=prefix + '_GENnp-24-v5_chi2016.root'
      elif samples[i][0]=="QCDADD13000":
        sample=prefix + '_GENnp-25-v5_chi2016.root'
      elif samples[i][0]=="QCDADD14000":
        sample=prefix + '_GENnp-26-v5_chi2016.root'
      elif samples[i][0]=="QCDADD15000":
        sample=prefix + '_GENnp-27-v5_chi2016.root'
      elif samples[i][0]=="QCDADD16000":
        sample=prefix + '_GENnp-28-v5_chi2016.root'
      elif samples[i][0]=="QCDADD17000":
        sample=prefix + '_GENnp-29-v5_chi2016.root'
      elif samples[i][0]=="QCDADD18000":
        sample=prefix + '_GENnp-30-v5_chi2016.root'
      elif samples[i][0]=="QCDADD19000":
        sample=prefix + '_GENnp-31-v5_chi2016.root'
      elif samples[i][0]=="QCDADD20000":
        sample=prefix + '_GENnp-32-v5_chi2016.root'
      elif samples[i][0]=="QCDADD21000":
        sample=prefix + '_GENnp-33-v5_chi2016.root'
      elif samples[i][0]=="QCDADD22000":
        sample=prefix + '_GENnp-34-v5_chi2016.root'
      elif samples[i][0]=="QCDAntiCIplusLL12000":
        sample=prefix + '_GENnp-antici-v4_chi2016.root'
      elif samples[i][0]=="QCD":
        sample=prefix + '_QCD_chi2016.root'
      elif "DM" in samples[i][0] or "ll" in samples[i][0] or "cs" in samples[i][0] or "wide" in samples[i][0] or "QBH" in samples[i][0]:
        sample=prefix + "_" + samples[i][0] + '_chi2016.root'
      #if "ADD" in samples[i][0]:
      #  sample=prefix + '_GENaddv3_chi2016.root'
      #elif "CIplus" in samples[i][0]:
      #  sample=prefix + '_GENciv3_chi2016.root'
      #elif "CIminus" in samples[i][0]:
      #  sample=prefix + '_GENciminusv3_chi2016.root'
      else:
        sample="datacards/"+prefix + '_GENv4_chi.root'
      print sample
  
      out=TFile(sample,'UPDATE')
      closefiles=[out]
      
      # LO QCD file
      sample2="datacards/"+prefix + '_GENv4_chi.root'
      print sample2
      in2=TFile(sample2,'READ')

      # data file
      insample='datacards/chiHist_dataReReco_v3_PFHT900.root'
      #insample='datacards/datacard_shapelimit13TeV_25nsData13combi_chi.root' # buggy data
      print insample
      infile=TFile(insample,'READ')

      # unfolded data file
      #unfoldsample='datacards/Unfolded_chiNtuple_dataReReco_v3_Coarse_PFHT900_fromCB_AK4SF_pythia8_Pt_170toInf.root'
      unfoldsample='datacards/Unfolded_chiNtuple_dataReReco_v3_Coarse_PFHT900_fromCB_AK4SF_pythia8_Pt_170toInf_MatrixInvert.root'
      print unfoldsample
      unfoldfile=TFile(unfoldsample,'READ')

      # NLO correction
      filename1nu2="fastnlo/RunII/fnl5662j_v23_fix_CT14nlo_allmu_ak4.root"
      print filename1nu2
      nlofile2 = TFile.Open(filename1nu2)
      closefiles+=[nlofile2]

      # NLO uncertainties
      #filename1nu3="fastnlo/RunII/fnl5662j_cs_ct14nlo_30000_LL+.root"
      filename1nu3="fastnlo/RunII/InclusiveNJetEvents_fnl5662j_v23_fix_CT14nlo_allmu_norm.root"
      print filename1nu3
      nlofile3 = TFile.Open(filename1nu3)
      closefiles+=[nlofile3]

      # NLO uncertainties
      #filename1nu3="fastnlo/RunII/fnl5662j_cs_ct14nlo_30000_LL+.root"
      filename1nu4="fastnlo/RunII/InclusiveNJetEvents_fnl5662j_v23_fix_CT14nlo_allmem_norm.root"
      print filename1nu4
      nlofile4 = TFile.Open(filename1nu4)
      closefiles+=[nlofile4]
      
       # DM uncertainties
      filename1dmpdf="datacards/chi_dm_pdf_plots6000_13TeV_2016.root"
      print filename1dmpdf
      dmpdffile = TFile.Open(filename1dmpdf)
      closefiles+=[dmpdffile]

      # EWK correction
      filename1ewk="fastnlo/RunII/DijetAngularCMS13_ewk.root"
      print filename1ewk
      ewkfile = TFile.Open(filename1ewk)
      closefiles+=[ewkfile]

      # JES uncertainty QCD
      jesfiles=[]
      for n in range(5):
        filename1jes="datacards/chi_systematic_plotschi_QCD"+str(n)+"RerecoV3_13TeV_2016.root"
        print filename1jes
        jesfiles += [TFile.Open(filename1jes)]
        closefiles+=[jesfiles[-1]]
      jeshists={}
      for j in range(len(massbins)):
        for source in jessources:
          jeshists[str(j)+source]=[]
	  for jesfile in jesfiles:
	    jespad=jesfile.Get("jes")
            jes=jespad.GetListOfPrimitives()[j+useUnfoldedData*1]
            jeshists[str(j)+source]+=[a for a in jes.GetListOfPrimitives() if source in str(a)]
          if len(jeshists[str(j)+source])!=2:
	    print "JES source not found", jesname
	    error

      # JES uncertainty CI
      jescifiles=[]
      for n in range(5):
        filename1jesci="datacards/chi_systematic_plotschi_QCD"+str(n)+"RerecoV3_13TeV_2016.root"
        print filename1jesci
        jescifiles += [TFile.Open(filename1jesci)]
        closefiles+=[jescifiles[-1]]
      jescihists={}
      for j in range(len(massbins)):
        for source in jessources:
          jescihists[str(j)+source]=[]
	  for jescifile in jescifiles:
	    jespad=jescifile.Get("jes")
            jes=jespad.GetListOfPrimitives()[j+useUnfoldedData*1]
            jescihists[str(j)+source]+=[a for a in jes.GetListOfPrimitives() if source in str(a)]
          if len(jescihists[str(j)+source])!=2:
	    print "JES source not found", jesname
	    error

      canvas = TCanvas("","",0,0,600,600)
      canvas.Divide(3,3)
      plots=[]
      legends=[]

      for j in range(len(massbins)):
        #if not "LO" in sample and j<2 and not "EWK" in sample:
        #   continue
        # data
        histname="dijet_"+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_chi"
        print histname
        if useLensData:
          if "13000" in str(massbins[j]):
            histname2="dijet_m_chi_2__projY_"+str(massbins[j]).strip("()").replace(',',"-").replace(' ',"")
          else:
            histname2="dijet_m_chi_2__projY_"+str(massbins[j]).strip("()").replace(',',"-").replace(' ',"")
          print histname2
          data = TH1D(unfoldfile.Get(histname2))
          data.SetName(histname)
        elif useUnfoldedData:
          histname2="dijet_mass_"+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_chi_unfolded"
          print histname2
          data = TH1F(unfoldfile.Get(histname2))
          data.SetName(histname)
        else:
          histname2="dijet_"+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_chi"
          print histname2
          data = TH1F(infile.Get(histname2))
          #data = TH1F(infile.Get("Data13#chi"+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1")) # buggy data
          #for b in range(data.GetXaxis().GetNbins()):
          #   data.SetBinContent(b+1,data.GetBinContent(b+1)*data.GetBinWidth(b+1))
          #   data.SetBinError(b+1,data.GetBinError(b+1)*data.GetBinWidth(b+1))
          data.SetName(histname)
        data=data.Rebin(len(chi_binnings[j])-1,data.GetName()+"_rebin1",chi_binnings[j])
        dataevents[j]=data.Integral()
        print dataevents[j]
        out.cd()
        if not injectSignal:
         histname='data_obs#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
         for k in range(0,200):
             out.Delete(histname+";"+str(k))
         data.Write(histname)

        # NLO
        nloqcd=None
        for k in mass_bins_nlo_list[j]:
         histname='chi-'+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])
         print histname
         hnlo = TH1F(nlofile2.Get(histname))
         hnlo.Scale(float(mass_bins_nlo3[k+1]-mass_bins_nlo3[k]))
         hnlo=rebin(hnlo,len(chi_binnings[j])-1,chi_binnings[j])
         if nloqcd:
            nloqcd.Add(hnlo)
         else:
            nloqcd=hnlo
        for b in range(nloqcd.GetXaxis().GetNbins()):
           nloqcd.SetBinContent(b+1,nloqcd.GetBinContent(b+1)*nloqcd.GetBinWidth(b+1))
        nloqcdbackup=nloqcd.Clone(nloqcd.GetName()+"_backup")
	print "NLO integral:", nloqcdbackup.Integral()

        # NLO normalized
        nloqcdnorm=None
        for k in mass_bins_nlo_list[j]:
         histname='chi-'+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"backup"
         print histname
         hnlo = TH1F(nlofile3.Get(histname))
         hnlo.Scale(float(mass_bins_nlo3[k+1]-mass_bins_nlo3[k]))
         hnlo=rebin(hnlo,len(chi_binnings[j])-1,chi_binnings[j])
         if nloqcdnorm:
            nloqcdnorm.Add(hnlo)
         else:
            nloqcdnorm=hnlo

        # EWK corrections
        histname='chi-'+str(massbins[j]).strip("()").replace(',',"-").replace(' ',"").replace("6000-13000","6000-6600")
        print histname
        ewk=ewkfile.Get(histname)
        for b in range(nloqcd.GetXaxis().GetNbins()):
            low_bin=ewk.FindBin(nloqcd.GetXaxis().GetBinLowEdge(b+1))
            up_bin=ewk.FindBin(nloqcd.GetXaxis().GetBinUpEdge(b+1))
            correction=ewk.Integral(low_bin,up_bin-1)/(up_bin-low_bin)
            if not "EWK" in samples[i][0]:
               nloqcd.SetBinContent(b+1,nloqcd.GetBinContent(b+1)*correction)
        nloqcd.Scale(1./nloqcd.Integral())
        ewk.SetName("ewk-"+histname)

        # QCD (empty background, not used in limit)
        histname='QCD#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1_backup"
        print histname
        qcd=in2.Get(histname)
        out.cd()
        for k in range(0,200):
            out.Delete(histname.replace("_backup","")+";"+str(k))
        qcd.Write(histname.replace("_backup",""))
        qcd=qcd.Rebin(len(chi_binnings[j])-1,histname,chi_binnings[j])
        qcd.Scale(1e10*1e9) #mb -> pb and factor 1e-10 for backup
        if j in qcdnorm.keys():
           qcd.Scale(qcdnorm[j]/qcd.Integral())
        else:
           qcdnorm[j]=qcd.Integral()
        print "k-factor", nloqcdbackup.Integral()/qcd.Integral()

        # CI (=LO CI+NLO QCD)
        histname=samples[i][0].replace("Anti","")+'#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1_backup"
        print histname
        if "EWK" in samples[i][0]:
          histname=histname.replace("_backup","")
          ci=nloqcdbackup.Clone(histname)
          for b in range(ci.GetXaxis().GetNbins()):
            low_bin=ewk.FindBin(ci.GetXaxis().GetBinLowEdge(b+1))
            up_bin=ewk.FindBin(ci.GetXaxis().GetBinUpEdge(b+1))
            correction=ewk.Integral(low_bin,up_bin-1)/(up_bin-low_bin)
            ci.SetBinContent(b+1,ci.GetBinContent(b+1)*correction)
          ci.Scale(1./ci.Integral())
        elif "lo" in samples[i][0] or "cteq66" in samples[i][0] or "cteq6ll" in samples[i][0]:
          filenamecinlo="fastnlo/RunII/fnl5662j_"+samples[i][0].replace("QCD","")+".root" # calcTheoryUncert.py from Jingyu already gives normalized signals
          print filenamecinlo
          cinlofile = TFile.Open(filenamecinlo)
          closefiles+=[cinlofile]
          ci=None
          for k in mass_bins_nlo_list[j]:
            histname2='chi-'+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])
            print histname2
            hci = TH1F(cinlofile.Get(histname2))
            #hci=rebin(hci,len(chi_binnings[j])-1,chi_binnings[j])
            hci=hci.Rebin(len(chi_binnings[j])-1,histname.replace("_backup",""),chi_binnings[j])
            if ci:
               ci.Add(hci)
            else:
               ci=hci
          cibackup=ci.Clone(ci.GetName()+"_backup")
          # apply EWK corrections
          ci.Scale(nloqcdbackup.Integral()/nloqcd.Integral())
          ci.Add(nloqcdbackup,-1)
          ci.Scale(nloqcd.Integral()/nloqcdbackup.Integral())
          ci.Add(nloqcd,+1)
          histname=histname.replace("_backup","")
          #   ci.Scale(nloqcd.Integral()/ci.Integral()/5.) # fake signal size for lower mass bins
        elif "LOCI" in samples[i][0]:
          lambdamass=samples[i][0].split("I")[-1]
          if "QCDDNLO" in samples[i][0]:
            filenamecinlo="fastnlo/cidijet_DijetChi_DILHC_2012_Lambda-"+lambdamass+"_Order-1_xmu-1.root"
          elif "QCDNLO" in samples[i][0]:
            filenamecinlo="fastnlo/cidijet_DijetChi_CILHC_2012_Lambda-"+lambdamass+"_Order-1_xmu-1.root"
          elif "QCDADLO" in samples[i][0]:
            filenamecinlo="fastnlo/cidijet_DijetChi_DILHC_2012_Lambda-"+lambdamass+"_Order-0_xmu-1.root"
          elif "QCDDLO" in samples[i][0]:
            filenamecinlo="fastnlo/cidijet_DijetChi_DILHC_2012_Lambda-"+lambdamass+"_Order-0_xmu-1.root"
          else:
            filenamecinlo="fastnlo/cidijet_DijetChi_CILHC_2012_Lambda-"+lambdamass+"_Order-0_xmu-1.root"
          print filenamecinlo
          cinlofile = TFile.Open(filenamecinlo)
          closefiles+=[cinlofile]
          histname2="chi-"+str(massbinsci[0])+"-"+str(massbinsci[1])
          print histname2
          histname=histname.replace("_backup","")
          ci = TH1F(cinlofile.Get(histname2))
          ci=ci.Rebin(len(chi_binnings[j])-1,histname.replace("_backup",""),chi_binnings[j])
          if "QCDADLO" in samples[i][0]:
            ci.Scale(-1)
          if j>=2:
             ci.Scale(1./nloqcdbackup.Integral())
          else:
             ci.Scale(nloqcd.Integral()/ci.Integral()/5.) # fake signal size for lower mass bins
          ci.Add(nloqcd)
        elif "DM" in samples[i][0]:
          cibackup=out.Get(histname)
          try:
             histname=cibackup.GetName().replace("_backup","")
          except:
            print "problem reading", histname
            break
          ci=cibackup.Clone(histname)
          ci=ci.Rebin(len(chi_binnings[j])-1,ci.GetName(),chi_binnings[j])
          ci.Scale(1./nloqcdbackup.Integral())
          #if not "zprime" in samples[i][0]:
          #  ci.Scale(5./4.) #to bug fix xsec from Phil
	  print histname,"signal fraction in first bin", ci.GetBinContent(1)/nloqcd.GetBinContent(1)
          ci.Add(nloqcd)
        elif "QBH" in samples[i][0]:
            histname=samples[i][0]+'#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
            if j<3:
                ci=nloqcd.Clone(histname)
            else:
                if samples[i][0].split("_")[2]=='6':
                    histnamein='QCDADD'+samples[i][0].split("_")[2]+samples[i][0].split("_")[0]+samples[i][0].split("_")[1]+'#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")
                else:
                    histnamein='QCD'+samples[i][0].split("_")[2]+samples[i][0].split("_")[0]+samples[i][0].split("_")[1]+'#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")
                cibackup=out.Get(histnamein)
                ci=cibackup.Clone(histname)
                ci=ci.Rebin(len(chi_binnings[j])-1,ci.GetName(),chi_binnings[j])
                ci.Scale(samples[i][1][0][1]/1000000)
                ci.Scale(1./nloqcdbackup.Integral())
                ci.Add(nloqcd)
        elif "wide" in samples[i][0]:
          cibackup=out.Get(histname)
          try:
              histname=cibackup.GetName().replace("_backup","")
          except:
            print "problem reading", histname
            break
          ci=cibackup.Clone(histname)
          ci=ci.Rebin(len(chi_binnings[j])-1,ci.GetName(),chi_binnings[j])
          ci.Scale(10./nloqcdbackup.Integral()) # make in units if 10pb
          ci.Add(nloqcd)
        elif "CIplus" in samples[i][0]:
          print "CREATE FAKE SIGNAL"
          if j<=3: # fake signal for signficances
            histnamealt=samples[i][0].replace("Anti","")+'#chi'+str((4800,5400)).strip("()").replace(',',"_").replace(' ',"")+"_rebin1_backup"
          else:
            histnamealt=histname
          cibackup=out.Get(histnamealt).Clone(histname)
          histname=cibackup.GetName().replace("_backup","")
          ci=cibackup.Clone(histname)
          ci=ci.Rebin(len(chi_binnings[j])-1,ci.GetName(),chi_binnings[j])
          ci.Scale(1e9) #mb -> pb
          cinorm[j]=ci.Integral()
          #print "BBB", qcdnorm[0],cinorm[0],qcdnorm[j]/dataevents[j]*26000.,cinorm[j]/dataevents[j]*26000.,nloqcdbackup.Integral()/dataevents[j]*26000.
          # CORRECT FORMULAT
          #ci.Scale(qcdnorm[0]/cinorm[0])
          # APPROXIMATE FORMULAT
          ci.Scale(qcdnorm[j]/cinorm[j])
          ci.Add(qcd,-1.)
          #ci.Scale(cinorm[0]/qcdnorm[0]) # trusting the QCD+CI LO prediction in mb (10^9) for the LO cross section
          #print "AAA",histname,ci.Integral()/qcdnorm[j], ci.Integral()/qcdnorm[0]*cinorm[0]/nloqcdbackup.Integral()*1e6, qcdnorm[j], nloqcdbackup.Integral()/1e6
          if "Anti" in samples[i][0]:
            ci.Scale(-1.)
            histname=histname.replace("CI","AntiCI")
            ci.SetName(histname)
          #if j>5:
          #  # APPROXIMATE FORMULA
          #  #ci.Scale(1./qcdnorm[j])
          #  # CORRECT FORMULA
          #   ci.Scale(1./nloqcdbackup.Integral())
          #else:
          #  # APPROXIMATE FORMULA
          #  #ci.Scale(nloqcd.Integral()/qcdnorm[j]/5.)
          #  # CORRECT FORMULA
          ci.Scale(nloqcd.Integral()/nloqcdbackup.Integral()) # fake signal for signficances
          scalesignal=abs(3*data.GetBinError(1)*nloqcd.Integral()/data.Integral()/ci.GetBinContent(1)) # find 2 sigma deviation
          ci.Scale(scalesignal)
          ci.Add(nloqcd)
        else:
          cibackup=out.Get(histname)
          histname=cibackup.GetName().replace("_backup","")
          ci=cibackup.Clone(histname)
          ci=ci.Rebin(len(chi_binnings[j])-1,ci.GetName(),chi_binnings[j])
          ci.Scale(1e9) #mb -> pb
          #cinorm[j]=ci.Integral()
          #print "BBB", qcdnorm[0],cinorm[0],qcdnorm[j]/dataevents[j]*26000.,cinorm[j]/dataevents[j]*26000.,nloqcdbackup.Integral()/dataevents[j]*26000.
          # CORRECT FORMULAT
          #ci.Scale(qcdnorm[0]/cinorm[0])
          # APPROXIMATE FORMULAT
          #ci.Scale(qcdnorm[j]/cinorm[j])
          ci.Add(qcd,-1.)
          #ci.Scale(cinorm[0]/qcdnorm[0]) # trusting the QCD+CI LO prediction in mb (10^9) for the LO cross section
          #print "AAA",histname,ci.Integral()/qcdnorm[j], ci.Integral()/qcdnorm[0]*cinorm[0]/nloqcdbackup.Integral()*1e6, qcdnorm[j], nloqcdbackup.Integral()/1e6
          #if "Anti" in samples[i][0]:
          #  ci.Scale(-1.)
          #  histname=histname.replace("CI","AntiCI")
          #if j>=2:
          #  # APPROXIMATE FORMULA
          #  #ci.Scale(1./qcdnorm[j])
          #  # CORRECT FORMULA
          ci.Scale(1./nloqcdbackup.Integral())
          #else:
          #  # APPROXIMATE FORMULA
          #  #ci.Scale(nloqcd.Integral()/qcdnorm[j]/5.)
          #  # CORRECT FORMULA
          #ci.Scale(nloqcd.Integral()/nloqcdbackup.Integral()/5.)
          ci.Add(nloqcd)
        if ci.Integral()!=0:
          ci.Scale(dataevents[j]/ci.Integral())
        for b in range(ci.GetXaxis().GetNbins()):
            ci.SetBinError(b+1,0)
        out.cd()
        for k in range(0,200):
            out.Delete(histname+";"+str(k))
        ci.Write(histname)

        # ALT (=NLO QCD)
        histname=samples[i][0].replace("Anti","")+'#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print histname
        if "LOCI" in samples[i][0] or "CT10" in samples[i][0] or "cteq" in samples[i][0] or "EWK" in samples[i][0]:
            alt=nloqcd.Clone(histname)
        else:
            alt=out.Get(histname)
        alt=alt.Rebin(len(chi_binnings[j])-1,alt.GetName(),chi_binnings[j])
        alt.Add(alt,-1)
        alt.Add(nloqcd)
        alt.Scale(dataevents[j]/alt.Integral())
        for b in range(alt.GetXaxis().GetNbins()):
            alt.SetBinError(b+1,0)
        out.cd()
        histname=samples[i][0]+'_ALT#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        alt.SetName(histname)
        alt.SetLineColor(2)
        alt.SetTitle("")
        alt.GetYaxis().SetTitle("dN/d#chi")
        for k in range(0,200):
            out.Delete(histname+";"+str(k))
        alt.Write(histname)
        
        if injectSignal:
         data.Add(ci,1)
         data.Add(alt,-1)
         histname='data_obs#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
         for k in range(0,200):
             out.Delete(histname+";"+str(k))
         data.Write(histname)

        # JER uncertainty
        histname=samples[i][0]+'#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        clone=ci.Clone(histname)
        clone=clone.Rebin(len(chi_binnings[j])-1,clone.GetName(),chi_binnings[j])
        cijerup=clone.Clone(histname+"_jerUp")
        cijerdown=clone.Clone(histname+"_jerDown")
        slopes={}
        slopes[1900]=0.018
        slopes[2400]=0.018 
        slopes[3000]=0.020 
        slopes[3600]=0.020
        slopes[4200]=0.034
        slopes[4800]=0.034
        slopes[5400]=0.026
        slopes[6000]=0.026
        for b in range(clone.GetNbinsX()):
            cijerup.SetBinContent(b+1,clone.GetBinContent(b+1)*(1.+(clone.GetBinCenter(b+1)-8.5)/7.5*slopes[massbins[j][0]]))
            cijerdown.SetBinContent(b+1,clone.GetBinContent(b+1)*(1.-(clone.GetBinCenter(b+1)-8.5)/7.5*slopes[massbins[j][0]]))
        #cijerup.Scale(dataevents[j]/cijerup.Integral())
        #cijerdown.Scale(dataevents[j]/cijerdown.Integral())
        cijerup.SetLineColor(3)
        cijerup.SetLineStyle(2)
        cijerdown.SetLineColor(3)
        cijerdown.SetLineStyle(3)
        out.cd()
        for k in range(0,200):
            out.Delete(histname+"_jerUp"+";"+str(k))
            out.Delete(histname+"_jerDown"+";"+str(k))
        cijerup.Write()
        cijerdown.Write()

        histname=samples[i][0]+'_ALT#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        clone=alt.Clone(histname)
        clone=clone.Rebin(len(chi_binnings[j])-1,clone.GetName(),chi_binnings[j])
        jerup=clone.Clone(histname+"_jerUp")
        jerdown=clone.Clone(histname+"_jerDown")
        for b in range(clone.GetNbinsX()):
            jerup.SetBinContent(b+1,clone.GetBinContent(b+1)*(1.+(clone.GetBinCenter(b+1)-8.5)/7.5*slopes[massbins[j][0]]))
            jerdown.SetBinContent(b+1,clone.GetBinContent(b+1)*(1.-(clone.GetBinCenter(b+1)-8.5)/7.5*slopes[massbins[j][0]]))
        #jerup.Scale(dataevents[j]/jerup.Integral())
        #jerdown.Scale(dataevents[j]/jerdown.Integral())
        jerup.SetLineColor(3)
        jerup.SetLineStyle(2)
        jerdown.SetLineColor(3)
        jerdown.SetLineStyle(3)
        out.cd()
        for k in range(0,200):
            out.Delete(histname+"_jerUp"+";"+str(k))
            out.Delete(histname+"_jerDown"+";"+str(k))
        jerup.Write()
        jerdown.Write()

        # jes uncertainty
        for source in jessources:
	  if source=="SumInQuadrature":
	    jesname=""
	  else:
	    jesname=str(jessources.index(source)+1)
          histname=samples[i][0]+'#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          clone=ci.Clone(histname)
          clone=clone.Rebin(len(chi_binnings[j])-1,clone.GetName(),chi_binnings[j])
          cijesup=clone.Clone(histname+"_jes"+jesname+"Up")
          cijesdown=clone.Clone(histname+"_jes"+jesname+"Down")
          for b in range(clone.GetNbinsX()):
              cijesup.SetBinContent(b+1,clone.GetBinContent(b+1)*jescihists[str(j)+source][0].GetBinContent(b+1))
              cijesdown.SetBinContent(b+1,clone.GetBinContent(b+1)*jescihists[str(j)+source][1].GetBinContent(b+1))
          #cijesup.Scale(dataevents[j]/cijesup.Integral())
          #cijesdown.Scale(dataevents[j]/cijesdown.Integral())
          #print histname, "jes down", cijesdown.GetBinContent(1)/ci.GetBinContent(1)
          #print histname, "jes up", cijesup.GetBinContent(1)/ci.GetBinContent(1)
          cijesup.SetLineColor(4)
          cijesup.SetLineStyle(2)
          cijesdown.SetLineColor(4)
          cijesdown.SetLineStyle(3)
          out.cd()
          for k in range(0,200):
              out.Delete(histname+"_jes"+jesname+"Up"+";"+str(k))
              out.Delete(histname+"_jes"+jesname+"Down"+";"+str(k))
          cijesup.Write()
          cijesdown.Write()

          histname=samples[i][0]+'_ALT#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
          clone=alt.Clone(histname)
          clone=clone.Rebin(len(chi_binnings[j])-1,clone.GetName(),chi_binnings[j])
          jesup=clone.Clone(histname+"_jes"+jesname+"Up")
          jesdown=clone.Clone(histname+"_jes"+jesname+"Down")
	  for b in range(clone.GetNbinsX()):
              jesup.SetBinContent(b+1,clone.GetBinContent(b+1)*jeshists[str(j)+source][0].GetBinContent(b+1))
              jesdown.SetBinContent(b+1,clone.GetBinContent(b+1)*jeshists[str(j)+source][1].GetBinContent(b+1))
          #jesup.Scale(dataevents[j]/jesup.Integral())
          #jesdown.Scale(dataevents[j]/jesdown.Integral())
          jesup.SetLineColor(4)
          jesup.SetLineStyle(2)
          jesdown.SetLineColor(4)
          jesdown.SetLineStyle(3)
          out.cd()
          for k in range(0,200):
              out.Delete(histname+"_jes"+jesname+"Up"+";"+str(k))
              out.Delete(histname+"_jes"+jesname+"Down"+";"+str(k))
          jesup.Write()
          jesdown.Write()

        # NLO PDFup/down
        nloPDFupqcd=None
        for k in mass_bins_nlo_list[j]:
         histname='chi-'+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"PDFUp"
         print histname
         hnloPDFup = TH1F(nlofile4.Get(histname))
         hnloPDFup.Scale(float(mass_bins_nlo3[k+1]-mass_bins_nlo3[k]))
         hnloPDFup=rebin(hnloPDFup,len(chi_binnings[j])-1,chi_binnings[j])
         if nloPDFupqcd:
            nloPDFupqcd.Add(hnloPDFup)
         else:
            nloPDFupqcd=hnloPDFup
        nloPDFupqcd.Add(nloqcdnorm,-1)
        nloPDFupqcd.Scale(1./nloqcdnorm.Integral())

        nloPDFdownqcd=None
        for k in mass_bins_nlo_list[j]:
         histname='chi-'+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"PDFDown"
         print histname
         hnloPDFdown = TH1F(nlofile4.Get(histname))
         hnloPDFdown.Scale(float(mass_bins_nlo3[k+1]-mass_bins_nlo3[k]))
         hnloPDFdown=rebin(hnloPDFdown,len(chi_binnings[j])-1,chi_binnings[j])
         if nloPDFdownqcd:
            nloPDFdownqcd.Add(hnloPDFdown)
         else:
            nloPDFdownqcd=hnloPDFdown
        nloPDFdownqcd.Add(nloqcdnorm,-1)
        nloPDFdownqcd.Scale(1./nloqcdnorm.Integral())

        pdfup=alt.Clone(alt.GetName()+"_pdfUp")
        pdfdown=alt.Clone(alt.GetName()+"_pdfDown")
        pdfup.Add(nloPDFupqcd,dataevents[j])
        pdfdown.Add(nloPDFdownqcd,dataevents[j])
        for b in range(pdfup.GetXaxis().GetNbins()):
            pdfup.SetBinError(b+1,0)
            pdfdown.SetBinError(b+1,0)
            if pdfup.GetBinCenter(b+1)-8.5>0:
               tmp=pdfup.GetBinContent(b+1)
               pdfup.SetBinContent(b+1,pdfdown.GetBinContent(b+1))
               pdfdown.SetBinContent(b+1,tmp)
        #pdfup.Scale(dataevents[j]/pdfup.Integral())
        #pdfdown.Scale(dataevents[j]/pdfdown.Integral())
        pdfup.SetLineColor(6)
        pdfup.SetLineStyle(2)
        pdfdown.SetLineColor(6)
        pdfdown.SetLineStyle(3)
        out.cd()
        for k in range(0,200):
            out.Delete(alt.GetName()+"_pdfUp"+";"+str(k))
            out.Delete(alt.GetName()+"_pdfDown"+";"+str(k))
        pdfup.Write()
        pdfdown.Write()

        if "lo" in samples[i][0] or "cteq66" in samples[i][0] or "cteq6ll" in samples[i][0]:
           nloPDFupci=None
           for k in mass_bins_nlo_list[j]:
            histname='chi-'+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"PDFUp"
            print histname
            hnloPDFup = TH1F(cinlofile.Get(histname))
            hnloPDFup=hnloPDFup.Rebin(len(chi_binnings[j])-1,histname.replace("_backup",""),chi_binnings[j])
            if nloPDFupci:
               nloPDFupci.Add(hnloPDFup)
            else:
               nloPDFupci=hnloPDFup
           nloPDFupci.Add(cibackup,-1)
           nloPDFupci.Scale(1./cibackup.Integral())

           nloPDFdownci=None
           for k in mass_bins_nlo_list[j]:
            histname='chi-'+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"PDFDown"
            print histname
            hnloPDFdown = TH1F(cinlofile.Get(histname))
            hnloPDFdown=hnloPDFdown.Rebin(len(chi_binnings[j])-1,histname.replace("_backup",""),chi_binnings[j])
            if nloPDFdownci:
              nloPDFdownci.Add(hnloPDFdown)
            else:
              nloPDFdownci=hnloPDFdown
           nloPDFdownci.Add(cibackup,-1)
           nloPDFdownci.Scale(1./cibackup.Integral())
        elif "DM" in samples[i][0] and "Mphi_6000" in samples[i][0]:
           nloPDFdownci=nloPDFdownqcd.Clone("DM_pdf_down")
           nloPDFupci=nloPDFupqcd.Clone("DM_pdf_up")
	   dmpdfcanvas=dmpdffile.Get("pdf")
	   dmpdfplot=dmpdfcanvas.GetListOfPrimitives()[j+useUnfoldedData*1]
	   dmpdfhist=[a for a in dmpdfplot.GetListOfPrimitives() if "mean" in str(a)][0]
	   for b in range(nloPDFupci.GetNbinsX()):
	     slope=(ci.GetBinContent(b+1)/dataevents[j]-nloqcd.GetBinContent(b+1))*dmpdfhist.GetBinError(1)/dmpdfhist.GetBinContent(1)
             nloPDFupci.SetBinContent(b+1,sqrt(pow((nloPDFupci.GetBinCenter(b+1)-8.5)/7.5*slope,2)+pow(nloPDFupqcd.GetBinContent(b+1),2)))
             nloPDFdownci.SetBinContent(b+1,-sqrt(pow((nloPDFdownci.GetBinCenter(b+1)-8.5)/7.5*slope,2)+pow(nloPDFdownqcd.GetBinContent(b+1),2)))
	else:
           nloPDFdownci=nloPDFdownqcd
           nloPDFupci=nloPDFupqcd

        cipdfup=ci.Clone(ci.GetName()+"_pdfUp")
        cipdfdown=ci.Clone(ci.GetName()+"_pdfDown")
        cipdfup.Add(nloPDFupci,dataevents[j])
        cipdfdown.Add(nloPDFdownci,dataevents[j])
        for b in range(cipdfup.GetXaxis().GetNbins()):
            cipdfup.SetBinError(b+1,0)
            cipdfdown.SetBinError(b+1,0)
            if cipdfup.GetBinCenter(b+1)-8.5>0:
               tmp=cipdfup.GetBinContent(b+1)
               cipdfup.SetBinContent(b+1,cipdfdown.GetBinContent(b+1))
               cipdfdown.SetBinContent(b+1,tmp)
        #cipdfup.Scale(dataevents[j]/cipdfup.Integral())
        #cipdfdown.Scale(dataevents[j]/cipdfdown.Integral())
        cipdfup.SetLineColor(6)
        cipdfup.SetLineStyle(2)
        cipdfdown.SetLineColor(6)
        cipdfdown.SetLineStyle(3)
        out.cd()
        for k in range(0,200):
          out.Delete(ci.GetName()+"_pdfUp"+";"+str(k))
          out.Delete(ci.GetName()+"_pdfDown"+";"+str(k))
        cipdfup.Write()
        cipdfdown.Write()

        # NLO Scaleup/down
	#for scaleVariation in ["MuR","MuF",""]:
        for scaleVariation in [""]:
          nloScaleupqcd=None
          for k in mass_bins_nlo_list[j]:
           histname='chi-'+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"scale"+scaleVariation+"Up"
           print histname
	   if scaleVariation=="":
             hnloScaleup = TH1F(nlofile3.Get(histname))
           elif scaleVariation=="MuR":
             hnloScaleup = TH1F(nlofile3.Get("CIJET_fnl5662j_cs_001_ct14nlo_0_56_30000_LL+_mu_qcd_chi-"+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"scale-2.0-1.0_addmu")).Clone(histname)
	   elif scaleVariation=="MuF":
             hnloScaleup = TH1F(nlofile3.Get("CIJET_fnl5662j_cs_001_ct14nlo_0_56_30000_LL+_mu_qcd_chi-"+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"scale-1.0-2.0_addmu")).Clone(histname)
	   hnloScaleup.Scale(float(mass_bins_nlo3[k+1]-mass_bins_nlo3[k]))
           hnloScaleup=rebin(hnloScaleup,len(chi_binnings[j])-1,chi_binnings[j])
           if nloScaleupqcd:
              nloScaleupqcd.Add(hnloScaleup)
           else:
              nloScaleupqcd=hnloScaleup
          nloScaleupqcd.Add(nloqcdnorm,-1)
          nloScaleupqcd.Scale(1./nloqcdnorm.Integral())

          nloScaledownqcd=None
          for k in mass_bins_nlo_list[j]:
           histname='chi-'+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"scale"+scaleVariation+"Down"
           print histname
           if scaleVariation=="":
             hnloScaledown = TH1F(nlofile3.Get(histname))
           elif scaleVariation=="MuR":
             hnloScaledown = TH1F(nlofile3.Get("CIJET_fnl5662j_cs_001_ct14nlo_0_56_30000_LL+_mu_qcd_chi-"+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"scale-0.5-1.0_addmu")).Clone(histname)
	   elif scaleVariation=="MuF":
             hnloScaledown = TH1F(nlofile3.Get("CIJET_fnl5662j_cs_001_ct14nlo_0_56_30000_LL+_mu_qcd_chi-"+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"scale-1.0-0.5_addmu")).Clone(histname)
	   hnloScaledown.Scale(float(mass_bins_nlo3[k+1]-mass_bins_nlo3[k]))
           hnloScaledown=rebin(hnloScaledown,len(chi_binnings[j])-1,chi_binnings[j])
           if nloScaledownqcd:
              nloScaledownqcd.Add(hnloScaledown)
           else:
              nloScaledownqcd=hnloScaledown
          nloScaledownqcd.Add(nloqcdnorm,-1)
          nloScaledownqcd.Scale(1./nloqcdnorm.Integral())

          scaleup=alt.Clone(alt.GetName()+"_scale"+scaleVariation+"Up")
          scaledown=alt.Clone(alt.GetName()+"_scale"+scaleVariation+"Down")
          scaleup.Add(nloScaleupqcd,dataevents[j])
          scaledown.Add(nloScaledownqcd,dataevents[j])
          for b in range(scaleup.GetXaxis().GetNbins()):
              scaleup.SetBinError(b+1,0)
              scaledown.SetBinError(b+1,0)
              if scaleVariation=="" and scaleup.GetBinCenter(b+1)-8.5>0:
         	 tmp=scaleup.GetBinContent(b+1)
         	 scaleup.SetBinContent(b+1,scaledown.GetBinContent(b+1))
         	 scaledown.SetBinContent(b+1,tmp)
          #scaleup.Scale(dataevents[j]/scaleup.Integral())
          #scaledown.Scale(dataevents[j]/scaledown.Integral())
          scaleup.SetLineColor(7)
          scaleup.SetLineStyle(2)
          scaledown.SetLineColor(7)
          scaledown.SetLineStyle(3)
          out.cd()
          for k in range(0,200):
              out.Delete(alt.GetName()+"_scale"+scaleVariation+"Up"+";"+str(k))
              out.Delete(alt.GetName()+"_scale"+scaleVariation+"Down"+";"+str(k))
          scaleup.Write()
          scaledown.Write()
          
          if "lo" in samples[i][0] or "cteq66" in samples[i][0] or "cteq6ll" in samples[i][0]:
             signalmassname="_".join(samples[i][0].split("_")[2:4])
	     nloScaleupci=None
             for k in mass_bins_nlo_list[j]:
              histname='chi-'+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"scale"+scaleVariation+"Up"
              print histname
              if scaleVariation=="":
                hnloScaleup = TH1F(cinlofile.Get(histname))
              elif scaleVariation=="MuR":
                hnloScaleup = TH1F(cinlofile.Get("CIJET_fnl5662j_cs_001_ct14nlo_0_56_"+signalmassname+"_mu_qcd_chi-"+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"scale-2.0-1.0_addmu")).Clone(histname)
	      elif scaleVariation=="MuF":
                hnloScaleup = TH1F(cinlofile.Get("CIJET_fnl5662j_cs_001_ct14nlo_0_56_"+signalmassname+"_mu_qcd_chi-"+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"scale-1.0-2.0_addmu")).Clone(histname)
              hnloScaleup=hnloScaleup.Rebin(len(chi_binnings[j])-1,histname.replace("_backup",""),chi_binnings[j])
              if nloScaleupci:
         	 nloScaleupci.Add(hnloScaleup)
              else:
         	 nloScaleupci=hnloScaleup
             nloScaleupci.Add(cibackup,-1)
             nloScaleupci.Scale(1./cibackup.Integral())

             nloScaledownci=None
             for k in mass_bins_nlo_list[j]:
              histname='chi-'+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"scale"+scaleVariation+"Down"
              print histname
              if scaleVariation=="":
                hnloScaledown = TH1F(cinlofile.Get(histname))
              elif scaleVariation=="MuR":
                hnloScaledown = TH1F(cinlofile.Get("CIJET_fnl5662j_cs_001_ct14nlo_0_56_"+signalmassname+"_mu_qcd_chi-"+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"scale-0.5-1.0_addmu")).Clone(histname)
	      elif scaleVariation=="MuF":
                hnloScaledown = TH1F(cinlofile.Get("CIJET_fnl5662j_cs_001_ct14nlo_0_56_"+signalmassname+"_mu_qcd_chi-"+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"scale-1.0-0.5_addmu")).Clone(histname)
	      hnloScaledown=hnloScaledown.Rebin(len(chi_binnings[j])-1,histname.replace("_backup",""),chi_binnings[j])
              if nloScaledownci:
         	nloScaledownci.Add(hnloScaledown)
              else:
         	nloScaledownci=hnloScaledown
             nloScaledownci.Add(cibackup,-1)
             nloScaledownci.Scale(1./cibackup.Integral())
          else:
             nloScaledownci=nloScaledownqcd
             nloScaleupci=nloScaleupqcd

          ciscaleup=ci.Clone(ci.GetName()+"_scale"+scaleVariation+"Up")
          ciscaledown=ci.Clone(ci.GetName()+"_scale"+scaleVariation+"Down")
          ciscaleup.Add(nloScaleupci,dataevents[j])
          ciscaledown.Add(nloScaledownci,dataevents[j])
          for b in range(ciscaleup.GetXaxis().GetNbins()):
              ciscaleup.SetBinError(b+1,0)
              ciscaledown.SetBinError(b+1,0)
              if scaleVariation=="" and ciscaleup.GetBinCenter(b+1)-8.5>0:
                 tmp=ciscaleup.GetBinContent(b+1)
                 ciscaleup.SetBinContent(b+1,ciscaledown.GetBinContent(b+1))
                 ciscaledown.SetBinContent(b+1,tmp)
          #ciscaleup.Scale(dataevents[j]/ciscaleup.Integral())
          #ciscaledown.Scale(dataevents[j]/ciscaledown.Integral())
          ciscaleup.SetLineColor(7)
          ciscaleup.SetLineStyle(2)
          ciscaledown.SetLineColor(7)
          ciscaledown.SetLineStyle(3)
          out.cd()
          for k in range(0,200):
            out.Delete(ci.GetName()+"_scale"+scaleVariation+"Up"+";"+str(k))
            out.Delete(ci.GetName()+"_scale"+scaleVariation+"Down"+";"+str(k))
          ciscaleup.Write()
          ciscaledown.Write()
        
        # DATA BLINDED
        #data=alt.Clone("data_blinded")
        #for b in range(data.GetXaxis().GetNbins()):
        #    data.SetBinError(b+1,sqrt(data.GetBinContent(b+1)))
        #out.cd()
        #for k in range(0,200):
        #    out.Delete('data_obs#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"+";"+str(k))
        #data.Write('data_obs#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1")
      
        # FAKE SIGNAL
        #ci=alt.Clone("fake_signal")
        #out.cd()
        #for k in range(0,200):
        #    out.Delete(samples[i][0]+'chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"+";"+str(k))
        #ci.Write(samples[i][0]+'#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1")
      
        # PLOTS
        #if j<3:
        #   continue
        canvas.cd(j+1)#j-2
        legend1=TLegend(0.2,0.6,0.9,0.95,(str(massbins[j][0])+"<m_{jj}<"+str(massbins[j][1])+" GeV").replace("4800<m_{jj}<7000","m_{jj}>4800").replace("4800<m_{jj}<13000","m_{jj}>4800"))
        legends+=[legend1]
        legend1.AddEntry(data,"data","lpe")
        alt=cloneNormalize(alt)
        plots+=[alt]
        alt.Draw("he")
        alt.GetYaxis().SetRangeUser(alt.GetMinimum()*0.8,(alt.GetMaximum()-alt.GetMinimum())*2.+alt.GetMinimum())
        legend1.AddEntry(alt,"QCD","l")
        
        # background uncertainties
        jerup=cloneNormalize(jerup)
        plots+=[jerup]
        jerup.Draw("hesame")
        legend1.AddEntry(jerup,"JER","l")
        jerdown=cloneNormalize(jerdown)
        plots+=[jerdown]
        jerdown.Draw("hesame")
        jesup=cloneNormalize(jesup)
        plots+=[jesup]
        jesup.Draw("hesame")
        legend1.AddEntry(jesup,"JES","l")
        jesdown=cloneNormalize(jesdown)
        plots+=[jesdown]
        jesdown.Draw("hesame")
        pdfup=cloneNormalize(pdfup)
        plots+=[pdfup]
        pdfup.Draw("hesame")
        legend1.AddEntry(pdfup,"PDF","l")
        pdfdown=cloneNormalize(pdfdown)
        plots+=[pdfdown]
        pdfdown.Draw("hesame")
        scaleup=cloneNormalize(scaleup)
        plots+=[scaleup]
        scaleup.Draw("hesame")
        legend1.AddEntry(scaleup,"scale","l")
        scaledown=cloneNormalize(scaledown)
        plots+=[scaledown]
        scaledown.Draw("hesame")
        
        ci=cloneNormalize(ci)
        plots+=[ci]
        ci.Draw("hesame")
        legend1.AddEntry(ci,"New Physics","l")
        
        # signal uncertainties
        cijerup=cloneNormalize(cijerup)
        plots+=[cijerup]
        cijerup.Draw("hesame")
        cijerdown=cloneNormalize(cijerdown)
        plots+=[cijerdown]
        cijerdown.Draw("hesame")
        cijesup=cloneNormalize(cijesup)
        plots+=[cijesup]
        cijesup.Draw("hesame")
        cijesdown=cloneNormalize(cijesdown)
        plots+=[cijesdown]
        cijesdown.Draw("hesame")
        cipdfup=cloneNormalize(cipdfup)
        plots+=[cipdfup]
        cipdfup.Draw("hesame")
        cipdfdown=cloneNormalize(cipdfdown)
        plots+=[cipdfdown]
        cipdfdown.Draw("hesame")
        ciscaleup=cloneNormalize(ciscaleup)
        plots+=[ciscaleup]
        ciscaleup.Draw("hesame")
        ciscaledown=cloneNormalize(ciscaledown)
        plots+=[ciscaledown]
        ciscaledown.Draw("hesame")
 
        origdata=data
	datahist[j]=data
        dataplot[j]=TGraphAsymmErrors(cloneNormalize(data))
        plots+=[dataplot[j]]
        alpha=1.-0.6827
        for b in range(dataplot[j].GetN()):
            if useUnfoldedData:
              N=1./pow(origdata.GetBinError(b+1)/origdata.GetBinContent(b+1),2)
            else:
              N=origdata.GetBinContent(b+1)
            L=0
            if N>0:
              L=ROOT.Math.gamma_quantile(alpha/2.,N,1.)
            U=ROOT.Math.gamma_quantile_c(alpha/2.,N+1,1.)
            dataplot[j].SetPointEYlow(b,(N-L)/origdata.GetBinWidth(b+1))
            dataplot[j].SetPointEYhigh(b,(U-N)/origdata.GetBinWidth(b+1))
        dataplot[j].SetLineColor(1)
        dataplot[j].SetMarkerStyle(24)
        dataplot[j].SetMarkerSize(0.5)
        dataplot[j].Draw("pe0zsame")
        
        legend1.SetTextSize(0.04)
        legend1.SetFillStyle(0)
        legend1.Draw("same")

      canvas.SaveAs(prefix + "_"+samples[i][0].replace("QCD","") + '_sys2016.pdf')
      canvas.SaveAs(prefix + "_"+samples[i][0].replace("QCD","") + '_sys2016.eps')
      
      if not useUnfoldedData:
        canvas = TCanvas("","",0,0,600,600)
        canvas.Divide(3,3)
	print "Applying response matrix"
        matrix=TFile("datacards/responseMatrices.root",'READ')
        matrix1=matrix.Get("TMatrixT<double>;2") #low mass chi binning
        matrix2=matrix.Get("TMatrixT<double>;3") #highest mass chi binning
        matrixMassBins=[1000,1200,1500,1900,2400,3000,3600,4200,4800,5400,6000,13000]
        #print (len(matrixMassBins)-1)*(len(chi_bins[0])-1)
        #matrix1.Print()
        #print (len(matrixMassBins)-1)*(len(chi_bins[-1])-1)
        #matrix2.Print()

        # modify histograms
        histogram_names=[
          (samples[i][0]+'_ALT#chi',"_rebin1"),
          (samples[i][0]+'#chi',"_rebin1"),
        ]
        for pre,post in histogram_names:
          althists=[]
          althistsclones=[]
          for j in range(len(massbins)):
            histname=pre+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+post
	    print histname
            althists+=[out.Get(histname)]
            althistsclones+=[althists[-1].Clone(althists[-1].GetName()+"original")]
            althists[-1].Scale(0)
          countgen=0
          for j1 in range(len(massbins)):
            for b1 in range(althists[j1].GetNbinsX()):
              for j2 in range(len(massbins)):
                for b2 in range(althists[j2].GetNbinsX()):
		  #if abs(j1-j2)>1 or j2<j1: continue #don't take elements too far from the diagonal to avoid statistical fluctuations
                  response=0
                  if j1==(len(massbins)-1) and j2==(len(massbins)-1):
                    # both in highest mass bin
                    response=matrix2[(j2+3)+b2*(len(matrixMassBins)-1)][(j1+3)+b1*(len(matrixMassBins)-1)]
                  elif j1!=(len(massbins)-1) and j2!=(len(massbins)-1):
                    # both in lower mass bins
                    response=matrix1[(j2+3)+b2*(len(matrixMassBins)-1)][(j1+3)+b1*(len(matrixMassBins)-1)]
                  elif j1==(len(massbins)-1):
                    # one in highest, one in lower mass bin
		    for bin1 in range(althists[0].GetNbinsX()):
                      if althists[0].GetBinCenter(bin1+1)>althists[j1].GetXaxis().GetBinLowEdge(b1+1) and\
                         althists[0].GetBinCenter(bin1+1)<althists[j1].GetXaxis().GetBinUpEdge(b1+1):
                        response+=matrix1[(j2+3)+b2*(len(matrixMassBins)-1)][(j1+3)+bin1*(len(matrixMassBins)-1)]
                  elif j2==(len(massbins)-1):
                    # one in highest, one in lower mass bin
		    for bin2 in range(althists[0].GetNbinsX()):
                      if althists[0].GetBinCenter(bin2+1)>althists[j2].GetXaxis().GetBinLowEdge(b2+1) and\
                         althists[0].GetBinCenter(bin2+1)<althists[j2].GetXaxis().GetBinUpEdge(b2+1):
                        response+=matrix1[(j2+3)+bin2*(len(matrixMassBins)-1)][(j1+3)+b1*(len(matrixMassBins)-1)]
		  #response=((b1==b2) and (j1==j2))
		  althists[j2].Fill(althists[j2].GetBinCenter(b2+1),althistsclones[j1].GetBinContent(b1+1)*response)
          for j in range(len(massbins)):
            print dataevents[j],althists[j].Integral()
            althists[j].Scale(dataevents[j]/althists[j].Integral())
	    for b in range(althists[j].GetXaxis().GetNbins()):
	      althists[j].SetBinError(b+1,0)
            #print althists[j].GetBinContent(1),althistsclones[j].GetBinContent(1)
          out.cd()
          for hist in althists:
            for k in range(0,200):
              out.Delete(hist.GetName()+";"+str(k))
            hist.Write()
 	  for j in range(len(massbins)):
            canvas.cd(j+1)#j-2
            alt=cloneNormalize(althists[j])
	    if "ALT" in pre:
	      alt.Draw("he")
              alt.GetYaxis().SetRangeUser(alt.GetMinimum()*0.8,(alt.GetMaximum()-alt.GetMinimum())*2.+alt.GetMinimum())
            else:
	      alt.Draw("hesame")
            plots+=[alt]
	  syshists={}
	  for j in range(len(massbins)):
	    syss=["jer","pdf"]
	    #syss+=["jes"]
	    for n in range(len(jessources)-1):
	      syss+=["jes"+str(n+1)]
	    syss+=["scale"]
            #syss+=["scaleMuR","scaleMuF"]
	    for sys in syss:
	      for shift in ["Up","Down"]:
	        histname=althists[j].GetName()+"_"+sys+shift
		#print histname
 	        sysHist=out.Get(histname)
	        sysNorm=sysHist.Integral()
	        for b in range(sysHist.GetNbinsX()):
	          sysHist.SetBinContent(b+1,sysHist.GetBinContent(b+1)/althistsclones[j].GetBinContent(b+1)*althists[j].GetBinContent(b+1))
                sysHist.Scale(sysNorm/althistsclones[j].Integral()*althists[j].Integral()/sysHist.Integral())
	        #sysHist.Scale(dataevents[j]/sysHist.Integral())
                for k in range(0,200):
                  out.Delete(sysHist.GetName()+";"+str(k))
	        sysHist.Write()
		syshists[sys+shift]=sysHist
                canvas.cd(j+1)#j-2
                alt=cloneNormalize(sysHist)
                alt.Draw("hesame")
                plots+=[alt]
            dataplot[j].Draw("pe0zsame")
	    legend=legend1.Clone()
	    legend.SetHeader((str(massbins[j][0])+"<m_{jj}<"+str(massbins[j][1])+" GeV").replace("4800<m_{jj}<7000","m_{jj}>4800").replace("4800<m_{jj}<13000","m_{jj}>4800"))
	    legend.Draw("same")
	    plots+=[legend]
	    chi2=0
	    for b in range(datahist[j].GetNbinsX()):
	      unc2=max(pow(dataplot[j].GetErrorYlow(b),2),pow(dataplot[j].GetErrorYhigh(b),2))
	      print "stat",sqrt(unc2)/datahist[j].GetBinContent(b+1)
	      for sys in syss:
	        unc2+=max(pow(syshists[sys+"Up"].GetBinContent(b+1)-althists[j].GetBinContent(b+1),2),pow(syshists[sys+"Down"].GetBinContent(b+1)-althists[j].GetBinContent(b+1),2))
	      print "stat+sys",sqrt(unc2)/datahist[j].GetBinContent(b+1)
	      chi2+=pow(datahist[j].GetBinContent(b+1)-althists[j].GetBinContent(b+1),2)/unc2
	    pvalue=stats.chisqprob(chi2, datahist[j].GetNbinsX())
            sign=-stats.norm.ppf(pvalue)
	    print "sign",sign,"chi2/ndof",chi2/datahist[j].GetNbinsX()
        canvas.SaveAs(prefix + "_"+samples[i][0].replace("QCD","") + '_sys2016_smear.pdf')
        canvas.SaveAs(prefix + "_"+samples[i][0].replace("QCD","") + '_sys2016_smear.eps')

      for closefile in closefiles:
          closefile.Close()
