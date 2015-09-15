import os, sys
from ROOT import * 
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
gStyle.SetNdivisions(506, "XYZ")
gStyle.SetLegendBorderSize(0)

if __name__ == '__main__':

  files=[]
  for prefix in  ["jet_mass_uzh_WZH_","jet_mass_uzh_W_"]:
    if "WZH" in prefix:    
     samples=[("W",["dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-1000_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-1200_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-1400_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-1600_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-1800_13TeV-madgraph_1.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-2000_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-2500_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-3000_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-3500_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-4000_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-4500_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-600_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-800_13TeV-madgraph_1.root",
                    ]),
            ("Z",["dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToZZToZlepZhad_narrow_M-1000_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToZZToZlepZhad_narrow_M-1200_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToZZToZlepZhad_narrow_M-1400_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToZZToZlepZhad_narrow_M-1600_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToZZToZlepZhad_narrow_M-1800_13TeV-madgraph_1.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToZZToZlepZhad_narrow_M-2000_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToZZToZlepZhad_narrow_M-2500_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToZZToZlepZhad_narrow_M-3000_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToZZToZlepZhad_narrow_M-3500_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToZZToZlepZhad_narrow_M-4000_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToZZToZlepZhad_narrow_M-4500_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToZZToZlepZhad_narrow_M-600_13TeV-madgraph_1.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToZZToZlepZhad_narrow_M-800_13TeV-madgraph_1.root",
                    ]),
            ("H",["dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravTohhTohbbhbb_narrow_M-1000_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravTohhTohbbhbb_narrow_M-1200_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravTohhTohbbhbb_narrow_M-1400_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravTohhTohbbhbb_narrow_M-1600_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravTohhTohbbhbb_narrow_M-1800_13TeV-madgraph_1.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravTohhTohbbhbb_narrow_M-2000_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravTohhTohbbhbb_narrow_M-2500_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravTohhTohbbhbb_narrow_M-3000_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravTohhTohbbhbb_narrow_M-3500_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravTohhTohbbhbb_narrow_M-4000_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravTohhTohbbhbb_narrow_M-4500_13TeV-madgraph_1.root",
                    ]),
            ("q/g",["dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_1.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_2.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_3.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_4.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_5.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_6.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_7.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_8.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_9.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_10.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_11.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_12.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_13.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_14.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_15.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_16.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_17.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_18.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_19.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_20.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_21.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_22.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_23.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_24.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_25.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_26.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_27.root",
                    ]),
            ]
     ptbins=[#(250,350),
            #(350,450),
            (450,550),
	    #(600,800),
	    #(700,1100),
            (800,1200),
	    #(1400,1600),
            #(1600,2400),
            #(2500,3500),
            #(3500,4500),
           ]

    else:
     samples=[("W",["dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-1000_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-1200_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-1400_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-1600_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-1800_13TeV-madgraph_1.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-2000_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-2500_13TeV-madgraph_1.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-3000_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-3500_13TeV-madgraph_1.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-4000_13TeV-madgraph_1.root",
                    #"dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-4500_13TeV-madgraph_1.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-600_13TeV-madgraph_1.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_BulkGravToWW_narrow_M-800_13TeV-madgraph_1.root",
                    ]),
            ("q/g",["dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_1.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_2.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_3.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_4.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_5.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_6.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_7.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_8.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_9.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_10.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_11.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_12.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_13.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_14.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_15.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_16.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_17.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_18.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_19.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_20.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_21.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_22.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_23.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_24.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_25.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_26.root",
                    "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring15/WtaggingWithPuppi/EXOVVTree_QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_27.root",
                    ]),
            ]
     ptbins=[(250,350),
            (350,450),
            (450,550),
	    #(600,800),
            (800,1200),
	    (1400,1600),
            (1600,2400),
            #(2500,3500),
            #(3500,4500),
           ]
    variables=["prunedMass","prunedMassL23Corrected","prunedMassL123Corrected",
    "softdropMass","softdropMassL23Corrected","softdropMassL123Corrected",
    "prunedMassTau21","softdropMassTau21",
    "tau21","tau21Corrected",
    "trimmedMass","trimmedMassL23Corrected","trimmedMassL123Corrected",
    "puppiPrunedMass","puppiPrunedMassL23Corrected","puppiPrunedMassL123Corrected",
    "puppiSoftdropMass","puppiSoftdropMassL23Corrected","puppiSoftdropMassL123Corrected",
    "D2","JEC"]
    
    #samples=[("W",["flatTuple.root"])]
    
    color=[1,2,4,6,7,8,9,11,40,41]
    
    plots=[]
    for sample,filenames in samples:
      for ptbin in ptbins:
        plots += [TH1F(prefix+sample+str(ptbin[0])+'#prunedMass',';pruned mass;N',50,0,250)]
        plots += [TH1F(prefix+sample+str(ptbin[0])+'#prunedMassL23Corrected',';L23-corrected pruned mass;N',50,0,250)]
        plots += [TH1F(prefix+sample+str(ptbin[0])+'#prunedMassL123Corrected',';L123-corrected pruned mass;N',50,0,250)]
        plots += [TH1F(prefix+sample+str(ptbin[0])+'#softdropMass',';softdrop mass;N',50,0,250)]
        plots += [TH1F(prefix+sample+str(ptbin[0])+'#softdropMassL23Corrected',';L23-corrected softdrop mass;N',50,0,250)]
        plots += [TH1F(prefix+sample+str(ptbin[0])+'#softdropMassL123Corrected',';L123-corrected softdrop mass;N',50,0,250)]
        plots += [TH1F(prefix+sample+str(ptbin[0])+'#prunedMassTau21',';L23-corrected pruned mass;N',50,0,250)]
        plots += [TH1F(prefix+sample+str(ptbin[0])+'#softdropMassTau21',';L23-corrected softdrop mass;N',50,0,250)]
        plots += [TH1F(prefix+sample+str(ptbin[0])+'#tau21',';#tau_{2}/#tau_{1};N',50,0,2)]
        plots += [TH1F(prefix+sample+str(ptbin[0])+'#tau21Corrected',';corrected #tau_{2}/#tau_{1};N',50,0,2)]
        plots += [TH1F(prefix+sample+str(ptbin[0])+'#trimmedMass',';trimmed mass;N',50,0,250)]
        plots += [TH1F(prefix+sample+str(ptbin[0])+'#trimmedMassL23Corrected',';L23-corrected trimmed mass;N',50,0,250)]
        plots += [TH1F(prefix+sample+str(ptbin[0])+'#trimmedMassL123Corrected',';L123-corrected trimmed mass;N',50,0,250)]
        plots += [TH1F(prefix+sample+str(ptbin[0])+'#puppiPrunedMass',';PUPPI pruned mass;N',50,0,250)]
        plots += [TH1F(prefix+sample+str(ptbin[0])+'#puppiPrunedMassL23Corrected',';PUPPI+L23-corrected pruned mass;N',50,0,250)]
        plots += [TH1F(prefix+sample+str(ptbin[0])+'#puppiPrunedMassL123Corrected',';PUPPI+L123-corrected pruned mass;N',50,0,250)]
        plots += [TH1F(prefix+sample+str(ptbin[0])+'#puppiSoftdropMass',';PUPPI softdrop mass;N',50,0,250)]
        plots += [TH1F(prefix+sample+str(ptbin[0])+'#puppiSoftdropMassL23Corrected',';PUPPI+L23-corrected softdrop mass;N',50,0,250)]
        plots += [TH1F(prefix+sample+str(ptbin[0])+'#puppiSoftdropMassL123Corrected',';PUPPI+L123-corrected softdrop mass;N',50,0,250)]
        plots += [TH1F(prefix+sample+str(ptbin[0])+'#D2',';D2;N',50,0,10)]
        plots += [TH1F(prefix+sample+str(ptbin[0])+'#JEC',';JEC;N',50,1.0,1.2)]
    for plot in plots:
        plot.Sumw2()
    for k in range(len(samples)):
      sample=samples[k][0]
      filenames=samples[k][1]
      for f in filenames[:]:
     	  print f
     	  fil=TFile.Open(f)
	  files+=[fil]
     	  events=fil.Get("ntuplizer/tree")
     	  nevents=events.GetEntries()
          event_count=0
     	  print sample,nevents
     	  for event in events:
     	    event_count+=1
	    if event_count>1000: break
     	    if event_count%10000==1: print "event",event_count
     	    if len(event.jetAK8_pt)<1 or not event.jetAK8_IDTight[0]: continue
            for j in range(len(ptbins)):
	     offsetindex=len(variables)*j+len(variables)*len(ptbins)*k
	     if event.jetAK8_pt[0]>ptbins[j][0] and event.jetAK8_pt[0]<ptbins[j][1]:
              plots[0+offsetindex].Fill(event.jetAK8_pruned_mass[0])
              plots[1+offsetindex].Fill(event.jetAK8_pruned_massCorr[0])
              plots[2+offsetindex].Fill(event.jetAK8_pruned_mass[0]*event.jetAK8_jec[0])
              plots[3+offsetindex].Fill(event.jetAK8_softdrop_mass[0])
              plots[4+offsetindex].Fill(event.jetAK8_softdrop_massCorr[0])
              plots[5+offsetindex].Fill(event.jetAK8_softdrop_mass[0]*event.jetAK8_jec[0])
	      if event.jetAK8_tau1[0]>0 and event.jetAK8_tau2[0]/event.jetAK8_tau1[0]<0.5:
                plots[6+offsetindex].Fill(event.jetAK8_pruned_massCorr[0])
                plots[7+offsetindex].Fill(event.jetAK8_softdrop_massCorr[0])
              if event.jetAK8_tau1[0]>0 and event.jetAK8_pruned_massCorr[0]>65 and event.jetAK8_pruned_massCorr[0]<95:
	        plots[8+offsetindex].Fill(event.jetAK8_tau2[0]/event.jetAK8_tau1[0])
	        plots[9+offsetindex].Fill(event.jetAK8_tau2[0]/event.jetAK8_tau1[0]*(1+5*(event.jetAK8_pruned_jec[0]-1.))) # jet pT and tau21 are correlated to with factor 5
              plots[10+offsetindex].Fill(event.jetAK10_trimmed_mass[0])
              plots[11+offsetindex].Fill(event.jetAK10_trimmed_massCorr[0])
              plots[12+offsetindex].Fill(event.jetAK10_trimmed_mass[0]*event.jetAK8_jec[0])
              plots[13+offsetindex].Fill(event.jetAK8_puppi_pruned_mass[0])
              plots[14+offsetindex].Fill(event.jetAK8_puppi_pruned_massCorr[0])
              plots[15+offsetindex].Fill(event.jetAK8_puppi_pruned_mass[0]*event.jetAK8_jec[0])
              plots[16+offsetindex].Fill(event.jetAK8_puppi_softdrop_mass[0])
              plots[17+offsetindex].Fill(event.jetAK8_puppi_softdrop_massCorr[0])
              plots[18+offsetindex].Fill(event.jetAK8_puppi_softdrop_mass[0]*event.jetAK8_jec[0])
	      if event.jetAK10_ecf2[0]>0 and event.jetAK10_trimmed_massCorr[0]>65 and event.jetAK10_trimmed_massCorr[0]<95:
                plots[19+offsetindex].Fill(event.jetAK10_ecf3[0]*pow(event.jetAK10_ecf1[0],3)/pow(event.jetAK10_ecf2[0],3))
              plots[20+offsetindex].Fill(event.jetAK8_pruned_jec[0])

    print plots
    for i in range(len(variables)):
        canvas = TCanvas(variables[i],"",0,0,200,200)
        legend1=TLegend(0.55,0.4,0.9,0.9,"sample, p_{T} [GeV], mean")
        for k in range(len(samples)):
          sample=samples[k][0]
          for j in range(len(ptbins)):
	    offsetindex=len(variables)*j+len(variables)*len(ptbins)*k
            plots[i+offsetindex].SetLineColor(color[j])
            plots[i+offsetindex].SetLineStyle(k+1)
            plots[i+offsetindex].SetLineWidth(k+1)
	    if j==0 and k==0:
              plots[i+offsetindex].Draw("he")
	      integral=plots[i+offsetindex].Integral()
	    else:
	      if plots[i+offsetindex].Integral()>0:
	        plots[i+offsetindex].Scale(integral/plots[i+offsetindex].Integral())
	      plots[i+offsetindex].Draw("hesame")
	    if (sample=="W" or sample=="Z" or sample=="H") and "ass" in variables[i]:
	     #N = 1
             #res = array.array("d", [0.]*N)
             #q = array.array("d", [0.5])
             #plots[i+offsetindex].GetQuantiles(N, res, q)
	     #mean=res[0]
	     maxbin=0
	     maxcontent=0
	     for b in range(plots[i+offsetindex].GetXaxis().GetNbins()):
	       if plots[i+offsetindex].GetXaxis().GetBinCenter(b+1)>50 and plots[i+offsetindex].GetBinContent(b+1)>maxcontent:
	          maxbin=b
		  maxcontent=plots[i+offsetindex].GetBinContent(b+1)
	     mean=plots[i+offsetindex].GetXaxis().GetBinCenter(maxbin)
	     g1 = TF1("g1","gaus", mean-15.,mean+15.)
	     plots[i+offsetindex].Fit(g1, "R0")
	     if i==1:
	      print g1.GetParameter(1)
	      print plots[i+offsetindex].Integral(plots[i+offsetindex].FindBin(65),plots[i+offsetindex].FindBin(100)),plots[i+offsetindex].Integral(plots[i+offsetindex].FindBin(60),plots[i+offsetindex].FindBin(105))
             hmed = int(g1.GetParameter(1)*100.)/100.
	    else:
	     hmed = int(plots[i+offsetindex].GetMean()*1000.)/1000.
	    entry=sample+", "+str(ptbins[j]).replace("(","").replace(")","").replace(", ","-")
	    entry+=", "+str(hmed)
            legend1.AddEntry(plots[i+offsetindex],entry,"l")
        legend1.SetTextSize(0.04)
        legend1.SetFillStyle(0)
        legend1.Draw("same")

        if "tau21" in variables[i]:
          legend2=TLegend(0.55,0.9,0.9,0.95,"65<m_{pruned,corr}<95")
          legend2.SetTextSize(0.04)
          legend2.SetFillStyle(0)
          legend2.Draw("same")

        if "Tau21" in variables[i]:
          legend2=TLegend(0.55,0.9,0.9,0.95,"#tau_{2}/#tau_{1}<0.5")
          legend2.SetTextSize(0.04)
          legend2.SetFillStyle(0)
          legend2.Draw("same")

        if "D2" in variables[i]:
          legend2=TLegend(0.55,0.9,0.9,0.95,"65<m_{trimmed,corr}<95")
          legend2.SetTextSize(0.04)
          legend2.SetFillStyle(0)
          legend2.Draw("same")

        canvas.SaveAs(prefix + variables[i] + '.pdf')
        canvas.SaveAs(prefix + variables[i] + '.eps')
