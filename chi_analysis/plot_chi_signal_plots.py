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

def rebin(h1,nbins,binning):
    for b in range(h1.GetXaxis().GetNbins()):
        h1.SetBinContent(b+1,h1.GetBinContent(b+1)*h1.GetBinWidth(b+1))
        h1.SetBinError(b+1,h1.GetBinError(b+1)*h1.GetBinWidth(b+1))
    h1=h1.Rebin(nbins,h1.GetName()+"_rebin",binning)
    for b in range(h1.GetXaxis().GetNbins()):
        h1.SetBinContent(b+1,h1.GetBinContent(b+1)/h1.GetBinWidth(b+1))
        h1.SetBinError(b+1,h1.GetBinError(b+1)/h1.GetBinWidth(b+1))
    return h1

if __name__ == '__main__':

    prefix="datacard_shapelimit"

    colors=[1,2,3,4,6,7,8,9,11,12,13]
    styles=[1,2,3,4,5,1,2,3,4,5,1,2,3,4,5]

    chi_bins=[#(1,2,3,4,5,6,7,8,9,10,12,14,16),
               #(1,2,3,4,5,6,7,8,9,10,12,14,16),
               #(1,2,3,4,5,6,7,8,9,10,12,14,16),
               #(1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,3,6,9,12,16),
              ]
          
    #chi_bins=[(1,2,3,4,5,6,7),
    #           (1,2,3,4,5,6,7),
    #           (1,2,3,4,5,6,7),
    #           (1,3,5,7),
    #          ]
    chi_binnings=[]
    for mass_bin in chi_bins:
        chi_binnings+=[array.array('d')]
        for chi_bin in mass_bin:
            chi_binnings[-1].append(chi_bin)
    #massbins=[(1900,2400),
    #          (2400,3000),
	#      (3000,4000),
	#      (4000,8000)]
    massbins=[#(1900,2400),
              #(2400,3000),
	      #(3000,3600),
	      (3600,4200),
	      (4200,8000)]
    mass_bins_nlo={}
    #mass_bins_nlo[4]=3000
    mass_bins_nlo[5]=3600
    mass_bins_nlo[6]=4000
    mass_bins_nlo[7]=4200
    mass_bins_nlo[8]=8000
    mass_bins_nlo2=[#(4,),
    	      (5,6,),
    	      (7,),
    	     ]
    mass_bins_nlo_max=7


    samples=[[("QCDCI4000",[("fileList_pythia8_ci_m2500_4000_1_0_0_May27_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_4000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI6000",[("fileList_pythia8_ci_m2500_6000_1_0_0_May27_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_6000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI8000",[("fileList_pythia8_ci_m2500_8000_1_0_0_May27_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_8000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI9000",[("fileList_pythia8_ci_m2500_9000_1_0_0_May27_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_9000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI10000",[("fileList_pythia8_ci_m2500_10000_1_0_0_May27_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_10000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI12000",[("fileList_pythia8_ci_m2500_12000_1_0_0_May27_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_12000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             #("QCDCI14000",[("fileList_pythia8_ci_m2500_14000_1_0_0_May27_grid.txt",[(3600,4200)]),
		#        ("fileList_pythia8_ci_m3700_14000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI15000",[("fileList_pythia8_ci_m2500_15000_1_0_0_May27_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_15000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI16000",[("fileList_pythia8_ci_m2500_16000_1_0_0_May27_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_16000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI18000",[("fileList_pythia8_ci_m2500_18000_1_0_0_May27_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_18000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI20000",[("fileList_pythia8_ci_m2500_20000_1_0_0_May27_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_20000_1_0_0_May27_grid.txt",[(4200,8000)])]),

             ],[("QCDCIminusLL6000",[("fileList_pythia8_ci_m2500_6000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_6000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL8000",[("fileList_pythia8_ci_m2500_8000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_8000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL9000",[("fileList_pythia8_ci_m2500_9000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_9000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL10000",[("fileList_pythia8_ci_m2500_10000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_10000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL12000",[("fileList_pythia8_ci_m2500_12000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_12000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             #("QCDCIminusLL14000",[("fileList_pythia8_ci_m2500_14000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
	#	        ("fileList_pythia8_ci_m3700_14000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL15000",[("fileList_pythia8_ci_m2500_15000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_15000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL16000",[("fileList_pythia8_ci_m2500_16000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_16000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL18000",[("fileList_pythia8_ci_m2500_18000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_18000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL20000",[("fileList_pythia8_ci_m2500_20000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_20000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),

             ],[#("QCDADD_4_0_0_2000",[("fileList_pythia8_add_m2500_2000_2000_4_0_0_Aug19_grid.txt",[(3600,4200)]),
		#        ("fileList_pythia8_add_m3700_2000_2000_4_0_0_Aug19_grid.txt",[(4200,8000)])]),
             #("QCDADD_4_0_0_3000",[("fileList_pythia8_add_m2500_3000_3000_4_0_0_Aug19_grid.txt",[(3600,4200)]),
		#        ("fileList_pythia8_add_m3700_3000_3000_4_0_0_Aug19_grid.txt",[(4200,8000)])]),
             ("QCDADD_4_0_0_4000",[("fileList_pythia8_add_m2500_4000_4000_4_0_0_Aug19_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_add_m3700_4000_4000_4_0_0_Aug19_grid.txt",[(4200,8000)])]),
             ("QCDADD_4_0_0_5000",[("fileList_pythia8_add_m2500_5000_5000_4_0_0_Aug19_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_add_m3700_5000_5000_4_0_0_Aug19_grid.txt",[(4200,8000)])]),
             ("QCDADD_4_0_0_6000",[("fileList_pythia8_add_m2500_6000_6000_4_0_0_Aug19_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_add_m3700_6000_6000_4_0_0_Aug19_grid.txt",[(4200,8000)])]),
             ("QCDADD_4_0_0_7000",[("fileList_pythia8_add_m2500_7000_7000_4_0_0_Aug19_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_add_m3700_7000_7000_4_0_0_Aug19_grid.txt",[(4200,8000)])]),
             ("QCDADD_4_0_0_8000",[("fileList_pythia8_add_m2500_8000_8000_4_0_0_Aug19_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_add_m3700_8000_8000_4_0_0_Aug19_grid.txt",[(4200,8000)])]),

             ],[("QCDADD_4_0_1_4000",[("fileList_pythia8_add_m2500_4000_0_0_0_1_Aug19_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_add_m3700_4000_0_0_0_1_Aug19_grid.txt",[(4200,8000)])]),
             ("QCDADD_4_0_1_5000",[("fileList_pythia8_add_m2500_5000_0_0_0_1_Aug19_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_add_m3700_5000_0_0_0_1_Aug19_grid.txt",[(4200,8000)])]),
             ("QCDADD_4_0_1_6000",[("fileList_pythia8_add_m2500_6000_0_0_0_1_Aug19_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_add_m3700_6000_0_0_0_1_Aug19_grid.txt",[(4200,8000)])]),
             ("QCDADD_4_0_1_6500",[("fileLists/fileList_pythia8_add_m2500_6500_0_0_0_1_Aug19_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_add_m3700_6500_0_0_0_1_Aug19_grid.txt",[(4200,8000)])]),
             ("QCDADD_4_0_1_7000",[("fileLists/fileList_pythia8_add_m2500_7000_0_0_0_1_Aug19_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_add_m3700_7000_0_0_0_1_Aug19_grid.txt",[(4200,8000)])]),
             ("QCDADD_4_0_1_7500",[("fileLists/fileList_pythia8_add_m2500_7500_0_0_0_1_Aug19_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_add_m3700_7500_0_0_0_1_Aug19_grid.txt",[(4200,8000)])]),
             ("QCDADD_4_0_1_8000",[("fileList_pythia8_add_m2500_8000_0_0_0_1_Aug19_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_add_m3700_8000_0_0_0_1_Aug19_grid.txt",[(4200,8000)])]),
             ("QCDADD_4_0_1_9000",[("fileList_pythia8_add_m2500_9000_0_0_0_1_Aug19_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_add_m3700_9000_0_0_0_1_Aug19_grid.txt",[(4200,8000)])]),
             ("QCDADD_4_0_1_10000",[("fileList_pythia8_add_m2500_10000_0_0_0_1_Aug19_grid.txt",[(3600,4200)]),
		        ("fileList_pythia8_add_m3700_10000_0_0_0_1_Aug19_grid.txt",[(4200,8000)])]),

             ],[("QCDCI_0_0_1_6000",[("fileLists/fileList_pythia8_ci_m2500_6000_0_0_1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_6000_0_0_1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_0_0_1_7000",[("fileLists/fileList_pythia8_ci_m2500_7000_0_0_1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_7000_0_0_1_Oct23_grid.txt",[(4200,8000)])]),
	     ("QCDCI_0_0_1_8000",[("fileLists/fileList_pythia8_ci_m2500_8000_0_0_1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_8000_0_0_1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_0_0_1_9000",[("fileLists/fileList_pythia8_ci_m2500_9000_0_0_1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_9000_0_0_1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_0_0_1_10000",[("fileLists/fileList_pythia8_ci_m2500_10000_0_0_1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_10000_0_0_1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_0_0_1_11000",[("fileLists/fileList_pythia8_ci_m2500_11000_0_0_1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_11000_0_0_1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_0_0_1_12000",[("fileLists/fileList_pythia8_ci_m2500_12000_0_0_1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_12000_0_0_1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_0_0_1_14000",[("fileLists/fileList_pythia8_ci_m2500_14000_0_0_1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_14000_0_0_1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_0_0_1_15000",[("fileLists/fileList_pythia8_ci_m2500_15000_0_0_1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_15000_0_0_1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_0_0_1_16000",[("fileLists/fileList_pythia8_ci_m2500_16000_0_0_1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_16000_0_0_1_Oct23_grid.txt",[(4200,8000)])]),
             #("QCDCI_0_0_1_18000",[("fileLists/fileList_pythia8_ci_m2500_18000_0_0_1_Oct23_grid.txt",[(3600,4200)]),
		#        ("fileLists/fileList_pythia8_ci_m3700_18000_0_0_1_Oct23_grid.txt",[(4200,8000)])]),
             #("QCDCI_0_0_1_20000",[("fileLists/fileList_pythia8_ci_m2500_20000_0_0_1_Oct23_grid.txt",[(3600,4200)]),
		#        ("fileLists/fileList_pythia8_ci_m3700_20000_0_0_1_Oct23_grid.txt",[(4200,8000)])]),

             ],[("QCDCI_1_1_1_8000",[("fileLists/fileList_pythia8_ci_m2500_8000_1_1_1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_8000_1_1_1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_1_1_1_9000",[("fileLists/fileList_pythia8_ci_m2500_9000_1_1_1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_9000_1_1_1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_1_1_1_10000",[("fileLists/fileList_pythia8_ci_m2500_10000_1_1_1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_10000_1_1_1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_1_1_1_11000",[("fileLists/fileList_pythia8_ci_m2500_11000_1_1_1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_11000_1_1_1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_1_1_1_12000",[("fileLists/fileList_pythia8_ci_m2500_12000_1_1_1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_12000_1_1_1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_1_1_1_14000",[("fileLists/fileList_pythia8_ci_m2500_14000_1_1_1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_14000_1_1_1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_1_1_1_15000",[("fileLists/fileList_pythia8_ci_m2500_15000_1_1_1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_15000_1_1_1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_1_1_1_16000",[("fileLists/fileList_pythia8_ci_m2500_16000_1_1_1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_16000_1_1_1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_1_1_1_18000",[("fileLists/fileList_pythia8_ci_m2500_18000_1_1_1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_18000_1_1_1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_1_1_1_20000",[("fileLists/fileList_pythia8_ci_m2500_20000_1_1_1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_20000_1_1_1_Oct23_grid.txt",[(4200,8000)])]),

             ],[("QCDCI_-1_-1_-1_8000",[("fileLists/fileList_pythia8_ci_m2500_8000_-1_-1_-1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_8000_-1_-1_-1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_-1_-1_-1_9000",[("fileLists/fileList_pythia8_ci_m2500_9000_-1_-1_-1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_9000_-1_-1_-1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_-1_-1_-1_10000",[("fileLists/fileList_pythia8_ci_m2500_10000_-1_-1_-1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_10000_-1_-1_-1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_-1_-1_-1_11000",[("fileLists/fileList_pythia8_ci_m2500_11000_-1_-1_-1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_11000_-1_-1_-1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_-1_-1_-1_12000",[("fileLists/fileList_pythia8_ci_m2500_12000_-1_-1_-1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_12000_-1_-1_-1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_-1_-1_-1_14000",[("fileLists/fileList_pythia8_ci_m2500_14000_-1_-1_-1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_14000_-1_-1_-1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_-1_-1_-1_15000",[("fileLists/fileList_pythia8_ci_m2500_15000_-1_-1_-1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_15000_-1_-1_-1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_-1_-1_-1_16000",[("fileLists/fileList_pythia8_ci_m2500_16000_-1_-1_-1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_16000_-1_-1_-1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_-1_-1_-1_18000",[("fileLists/fileList_pythia8_ci_m2500_18000_-1_-1_-1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_18000_-1_-1_-1_Oct23_grid.txt",[(4200,8000)])]),
             ("QCDCI_-1_-1_-1_20000",[("fileLists/fileList_pythia8_ci_m2500_20000_-1_-1_-1_Oct23_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_20000_-1_-1_-1_Oct23_grid.txt",[(4200,8000)])]),

             ],[("QCDLOCI5000",[]),
             ("QCDLOCI6000",[]),
             ("QCDLOCI7000",[]),
             ("QCDLOCI8000",[]),
             ("QCDLOCI9000",[]),
             ("QCDLOCI10000",[]),
             ("QCDLOCI11000",[]),
             ("QCDLOCI12000",[]),
             ("QCDLOCI13000",[]),
             ("QCDLOCI14000",[]),
             ("QCDLOCI15000",[]),
             
	     ],[("QCDNLOCI5000",[]),
             ("QCDNLOCI6000",[]),
             ("QCDNLOCI7000",[]),
             ("QCDNLOCI8000",[]),
             ("QCDNLOCI9000",[]),
             ("QCDNLOCI10000",[]),
             ("QCDNLOCI11000",[]),
             ("QCDNLOCI12000",[]),
             ("QCDNLOCI13000",[]),
             ("QCDNLOCI14000",[]),
             ("QCDNLOCI15000",[]),
             
	     ],[("QCDDLOCI5000",[]),
             ("QCDDLOCI6000",[]),
             ("QCDDLOCI7000",[]),
             ("QCDDLOCI8000",[]),
             ("QCDDLOCI9000",[]),
             ("QCDDLOCI10000",[]),
             ("QCDDLOCI11000",[]),
             ("QCDDLOCI12000",[]),
             ("QCDDLOCI13000",[]),
             ("QCDDLOCI14000",[]),
	     ("QCDDLOCI15000",[]),

             ],[("QCDDNLOCI5000",[]),
             ("QCDDNLOCI6000",[]),
             ("QCDDNLOCI7000",[]),
             ("QCDDNLOCI8000",[]),
             ("QCDDNLOCI9000",[]),
             ("QCDDNLOCI10000",[]),
             ("QCDDNLOCI11000",[]),
             ("QCDDNLOCI12000",[]),
             ("QCDDNLOCI13000",[]),
             ("QCDDNLOCI14000",[]),
             ("QCDDNLOCI15000",[]),

             ]
             ]
 
    dataevents={}
    data={}
    # signal cards
    for i in range(len(samples)):
     canvas = TCanvas("","",0,0,400,200)
     canvas.Divide(2,1)
     plots=[]
     legends={}

     for j in range(len(massbins)):
        canvas.cd(j+1)
        legend1=TLegend(0.4,0.6,0.9,0.95,(str(massbins[j][0])+"<m_{jj}<"+str(massbins[j][1])+" GeV").replace("4200<m_{jj}<7000","m_{jj}>4200").replace("4200<m_{jj}<8000","m_{jj}>4200"))
        legends[j]=legend1

     files=[]

     for l in range(len(samples[i])):
      sample=prefix + "_"+samples[i][l][0].replace("QCD","") + '_chi.root'
      print sample
      out=TFile(sample,'READ')
      files+=[out]

      # data file
      insample='chi_EPS2.root'
      print insample
      infile=TFile(insample,'READ')

      # NLO correction
      filename1nu="fastnlo/fnl3622g_ct10-nlo_aspdf.root"
      print filename1nu
      nlofile = TFile.Open(filename1nu)

      # JES uncertainty QCD
      filename1jes="chi_systematic_plotschi_QCD4.root"
      print filename1jes
      jesfile = TFile.Open(filename1jes)

      # JES uncertainty CI
      filename1jesci="chi_systematic_plotschi_CI4.root"
      print filename1jesci
      jescifile = TFile.Open(filename1jesci)

      for j in range(len(massbins)):
        # data
        histname="dijet_"+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"").replace("8000","7000")+"_chi"
        print histname
        data = TH1F(infile.Get(histname))
        data=data.Rebin(len(chi_binnings[j])-1,data.GetName()+"_rebin1",chi_binnings[j])
	dataevents[j]=data.Integral()

        # NLO
        nloqcd=None
        for k in mass_bins_nlo2[j]:
         histname="h10"
         if k<10: histname+="0"
         histname+=str(k)+"00"
         print histname
         hnlo = TH1F(nlofile.Get(histname))
         hnlo.Scale(float(mass_bins_nlo[k+1]-mass_bins_nlo[k]))
         hnlo=rebin(hnlo,len(chi_binnings[j])-1,chi_binnings[j])
	 if nloqcd:
	    nloqcd.Add(hnlo)
	 else:
	    nloqcd=hnlo
        for b in range(nloqcd.GetXaxis().GetNbins()):
            nloqcd.SetBinContent(b+1,nloqcd.GetBinContent(b+1)*nloqcd.GetBinWidth(b+1))
        nloqcdbackup=nloqcd.Clone(nloqcd.GetName()+"_backup")
	nloqcd.Scale(1./nloqcd.Integral())

        # QCD (empty background, not used in limit)
        histname='QCD#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print histname
        qcd=out.Get(histname)
        qcd=qcd.Rebin(len(chi_binnings[j])-1,qcd.GetName(),chi_binnings[j])
        f=file("xsecs.txt")
        crosssections=eval(f.readline())
        xsec_qcd=1
        for xsec in crosssections:
          if xsec[0]=="QCD" and massbins[j] in xsec[1]:
              xsec_qcd=float(xsec[2])
	qcd.Scale(1e10*xsec_qcd)
	print "k-factor", nloqcdbackup.Integral()/qcd.Integral()

        # CI (=LO CI+NLO QCD)
	histname=samples[i][l][0]+'#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1_backup"
        print histname
	if "LOCI" in samples[i][l][0]:
	  lambdamass=samples[i][l][0].split("I")[-1]
	  if "QCDDNLO" in samples[i][l][0]:
            filenamecinlo="fastnlo/cidijet_DijetChi_DILHC_2012_Lambda-"+lambdamass+"_Order-1_xmu-1.root"
          elif "QCDNLO" in samples[i][l][0]:
	    filenamecinlo="fastnlo/cidijet_DijetChi_CILHC_2012_Lambda-"+lambdamass+"_Order-1_xmu-1.root"
	  elif "QCDADLO" in samples[i][l][0]:
            filenamecinlo="fastnlo/cidijet_DijetChi_DILHC_2012_Lambda-"+lambdamass+"_Order-0_xmu-1.root"
	  elif "QCDDLO" in samples[i][l][0]:
            filenamecinlo="fastnlo/cidijet_DijetChi_DILHC_2012_Lambda-"+lambdamass+"_Order-0_xmu-1.root"
          else:
	    filenamecinlo="fastnlo/cidijet_DijetChi_CILHC_2012_Lambda-"+lambdamass+"_Order-0_xmu-1.root"
          print filenamecinlo
          cinlofile = TFile.Open(filenamecinlo)
          histname2="chi-"+str(massbins[j][0])+"-"+str(massbins[j][1])
          print histname2
  	  histname=histname.replace("_backup","")
          ci = TH1F(cinlofile.Get(histname2))
          ci=ci.Rebin(len(chi_binnings[j])-1,ci.GetName()+"_rebin1",chi_binnings[j]).Clone(histname)
	  ci.Scale(1./nloqcdbackup.Integral())
	  if "QCDADLO" in samples[i][l][0]:
	    ci.Scale(-1)
          ci.Add(nloqcd)
	else:
          cibackup=out.Get(histname)
  	  histname=cibackup.GetName().replace("_backup","")
          ci=cibackup.Clone(histname)
          ci=ci.Rebin(len(chi_binnings[j])-1,ci.GetName(),chi_binnings[j])
	  # properly normalize LO QCD+CI and LO QCD before substracting LO QCD
	  xsec_ci=0
	  for xsec in crosssections:
	    if xsec[0]==samples[i][l][0] and massbins[j] in xsec[1]:
	        xsec_ci=float(xsec[2])
	  if "QCDCI_" in samples[i][l][0]:
	    ci.Scale(qcd.Integral()/ci.Integral())
	    #ci.Scale(xsec_qcd)
          else:
	    ci.Scale(xsec_ci)
          ci.Add(qcd,-1)
	  ci.Scale(1./qcd.Integral())
          ci.Add(nloqcd)
	if ci.Integral()>0:
          ci.Scale(dataevents[j]/ci.Integral())
        for b in range(ci.GetXaxis().GetNbins()):
            ci.SetBinError(b+1,0)

        # ALT (=NLO QCD)
        histname=samples[i][l][0]+'_ALT#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print histname
	if "LOCI" in samples[i][l][0]:
    	    alt=nloqcd.Clone(histname)
	else:
            alt=out.Get(histname)
        alt=alt.Rebin(len(chi_binnings[j])-1,alt.GetName(),chi_binnings[j])
        alt.Add(alt,-1)
        alt.Add(nloqcd)
        alt.Scale(dataevents[j]/alt.Integral())
        for b in range(alt.GetXaxis().GetNbins()):
            alt.SetBinError(b+1,0)
	
        # jes uncertainty
        histname=samples[i][l][0]+'#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
	if "LOCI" in samples[i][l][0]:
    	    clone=ci.Clone(histname)
	else:
            clone=out.Get(histname)
        clone=clone.Rebin(len(chi_binnings[j])-1,clone.GetName(),chi_binnings[j])
        jesup=clone.Clone(histname+"_jesUp")
        jesdown=clone.Clone(histname+"_jesDown")
        jespad=jescifile.Get("jes")
	jes=jespad.GetListOfPrimitives()[-len(massbins)-1+j]
	for b in range(clone.GetNbinsX()):
	    jesup.SetBinContent(b+1,clone.GetBinContent(b+1)*jes.GetListOfPrimitives()[2].GetBinContent(b+1))
            jesdown.SetBinContent(b+1,clone.GetBinContent(b+1)*jes.GetListOfPrimitives()[4].GetBinContent(b+1))
        histname=samples[i][l][0]+'_ALT#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
	if "LOCI" in samples[i][l][0]:
    	    clone=alt.Clone(histname)
	else:
            clone=out.Get(histname)
        clone=clone.Rebin(len(chi_binnings[j])-1,clone.GetName(),chi_binnings[j])
        jesup=clone.Clone(histname+"_jesUp")
        jesdown=clone.Clone(histname+"_jesDown")
        jespad=jesfile.Get("jes")
	jes=jespad.GetListOfPrimitives()[-len(massbins)-1+j]
	for b in range(clone.GetNbinsX()):
	    jesup.SetBinContent(b+1,clone.GetBinContent(b+1)*jes.GetListOfPrimitives()[2].GetBinContent(b+1))
            jesdown.SetBinContent(b+1,clone.GetBinContent(b+1)*jes.GetListOfPrimitives()[4].GetBinContent(b+1))

        # NLO PDFup/down
        nloPDFupqcd=None
        for k in mass_bins_nlo2[j]:
         histname="h10"
         if k+mass_bins_nlo_max<10: histname+="0"
         histname+=str(k+mass_bins_nlo_max)+"01"
         print histname
         hnloPDFup = TH1F(nlofile.Get(histname))
         hnloPDFup=rebin(hnloPDFup,len(chi_binnings[j])-1,chi_binnings[j])
	 if nloPDFupqcd:
	    nloPDFupqcd.Add(hnloPDFup)
	 else:
	    nloPDFupqcd=hnloPDFup
        nloPDFupqcd.Scale(1./len(mass_bins_nlo2[j])) # average uncertainty when merging bins from Klaus
	nloPDFupqcd.Multiply(nloqcd)

        nloPDFdownqcd=None
        for k in mass_bins_nlo2[j]:
         histname="h10"
         if k+mass_bins_nlo_max<10: histname+="0"
         histname+=str(k+mass_bins_nlo_max)+"02"
         print histname
         hnloPDFdown = TH1F(nlofile.Get(histname))
         hnloPDFdown=rebin(hnloPDFdown,len(chi_binnings[j])-1,chi_binnings[j])
	 if nloPDFdownqcd:
	    nloPDFdownqcd.Add(hnloPDFdown)
	 else:
	    nloPDFdownqcd=hnloPDFdown
        nloPDFdownqcd.Scale(1./len(mass_bins_nlo2[j])) # average uncertainty when merging bins from Klaus
	nloPDFdownqcd.Multiply(nloqcd)

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

        # NLO Scaleup/down
        nloScaleupqcd=None
        for k in mass_bins_nlo2[j]:
         histname="h10"
         if k+mass_bins_nlo_max<10: histname+="0"
         histname+=str(k+mass_bins_nlo_max)+"08"
         print histname
         hnloScaleup = TH1F(nlofile.Get(histname))
         hnloScaleup=rebin(hnloScaleup,len(chi_binnings[j])-1,chi_binnings[j])
	 if nloScaleupqcd:
	    nloScaleupqcd.Add(hnloScaleup)
	 else:
	    nloScaleupqcd=hnloScaleup
        nloScaleupqcd.Scale(1./len(mass_bins_nlo2[j])) # average uncertainty when merging bins from Klaus
	#print [nloScaleupqcd.GetBinContent(b+1) for b in range(nloScaleupqcd.GetNbinsX())]
	nloScaleupqcd.Multiply(nloqcd)

        nloScaledownqcd=None
        for k in mass_bins_nlo2[j]:
         histname="h10"
         if k+mass_bins_nlo_max<10: histname+="0"
         histname+=str(k+mass_bins_nlo_max)+"09"
         print histname
         hnloScaledown = TH1F(nlofile.Get(histname))
         hnloScaledown=rebin(hnloScaledown,len(chi_binnings[j])-1,chi_binnings[j])
	 if nloScaledownqcd:
	    nloScaledownqcd.Add(hnloScaledown)
	 else:
	    nloScaledownqcd=hnloScaledown
        nloScaledownqcd.Scale(1./len(mass_bins_nlo2[j])) # average uncertainty when merging bins from Klaus
	nloScaledownqcd.Multiply(nloqcd)

        scaleup=alt.Clone(alt.GetName()+"_scaleUp")
        scaledown=alt.Clone(alt.GetName()+"_scaleDown")
	scaleup.Add(nloScaleupqcd,dataevents[j])
	scaledown.Add(nloScaledownqcd,dataevents[j])
        for b in range(scaleup.GetXaxis().GetNbins()):
            scaleup.SetBinError(b+1,0)
            scaledown.SetBinError(b+1,0)
            if scaleup.GetBinCenter(b+1)-8.5>0:
	       tmp=scaleup.GetBinContent(b+1)
	       scaleup.SetBinContent(b+1,scaledown.GetBinContent(b+1))
	       scaledown.SetBinContent(b+1,tmp)

	# DATA BLINDED
	#data=alt.Clone("data_blinded")
        #for b in range(data.GetXaxis().GetNbins()):
        #    data.SetBinError(b+1,sqrt(data.GetBinContent(b+1)))
        #out.cd()
      
	# FAKE SIGNAL
	#ci=alt.Clone("fake_signal")
        #out.cd()

        for p in [alt,ci]:
	   for b in range(p.GetNbinsX()):
	       p.SetBinContent(b+1,p.GetBinContent(b+1)/p.GetBinWidth(b+1))
	       p.SetBinError(b+1,p.GetBinError(b+1)/p.GetBinWidth(b+1))
      
        # PLOTS
        canvas.cd(j+1)
	if l==0:
  	 plots+=[alt]
	 alt.SetLineColor(1)
	 alt.SetTitle("")
         alt.Draw("he")
	 alt.GetYaxis().SetRangeUser(0,alt.GetMaximum()*2)
         alt.GetXaxis().SetTitle("\chi")
 	 alt.GetYaxis().SetTitle("d#sigma / d#chi_{dijet}")
         alt.GetYaxis().SetTitleOffset(1.1)
         alt.GetXaxis().SetLabelSize(0.05)
         alt.GetYaxis().SetLabelSize(0.05)
         alt.GetXaxis().SetTitleSize(0.06)
         alt.GetYaxis().SetTitleSize(0.06)
         legends[j].AddEntry(alt,"QCD","l")
	if True:
	 plots+=[ci]
	 ci.SetLineColor(colors[l])
	 ci.SetLineStyle(styles[l])
         ci.Draw("hesame")
	 if "QCDCIminusLL" in samples[i][l][0]:
             legends[j].AddEntry(ci,"#Lambda_{LL/RR}^{-} (LO) = "+samples[i][l][0].replace("QCDCIminusLL","")+" GeV","l")
	 elif "QCDCI_-1_-1_-1" in samples[i][l][0]:
             legends[j].AddEntry(ci,"#Lambda_{VV/AA}^{+} (LO) = "+samples[i][l][0].replace("QCDCI_-1_-1_-1_","")+" GeV","l")
	 elif "QCDCI_1_1_1" in samples[i][l][0]:
             legends[j].AddEntry(ci,"#Lambda_{VV/AA}^{-} (LO) = "+samples[i][l][0].replace("QCDCI_1_1_1_","")+" GeV","l")
	 elif "QCDCI_0_0_1" in samples[i][l][0]:
             legends[j].AddEntry(ci,"#Lambda_{V-A}^{+} (LO) = "+samples[i][l][0].replace("QCDCI_0_0_1_","")+" GeV","l")
	 elif "QCDCI" in samples[i][l][0]:
             legends[j].AddEntry(ci,"#Lambda_{LL/RR}^{+} (LO) = "+samples[i][l][0].replace("QCDCI","")+" GeV","l")
	 elif "QCDADD_4_0_0_" in samples[i][l][0]:
             legends[j].AddEntry(ci,"M_{D} (Fra) = "+samples[i][l][0].replace("QCDADD_4_0_0_","")+" GeV","l")
	 elif "QCDADD_4_0_1_" in samples[i][l][0]:
             legends[j].AddEntry(ci,"#Lambda_{T} (GRW) = "+samples[i][l][0].replace("QCDADD_4_0_1_","")+" GeV","l")
	 elif "QCDLOCI" in samples[i][l][0]:
             legends[j].AddEntry(ci,"#Lambda_{LL/RR}^{-} (LO) = "+samples[i][l][0].replace("QCDLOCI","")+" GeV","l")
	 elif "QCDDLOCI" in samples[i][l][0]:
             legends[j].AddEntry(ci,"#Lambda_{LL/RR}^{+} (LO) = "+samples[i][l][0].replace("QCDDLOCI","")+" GeV","l")
	 elif "QCDNLOCI" in samples[i][l][0]:
             legends[j].AddEntry(ci,"#Lambda_{LL/RR}^{-} (NLO) = "+samples[i][l][0].replace("QCDNLOCI","")+" GeV","l")
	 elif "QCDDNLOCI" in samples[i][l][0]:
             legends[j].AddEntry(ci,"#Lambda_{LL/RR}^{+} (NLO) = "+samples[i][l][0].replace("QCDDNLOCI","")+" GeV","l")

        if l==len(samples[i])-1:
         legends[j].SetTextSize(0.04)
         legends[j].SetFillStyle(0)
         legends[j].Draw("same")

     canvas.SaveAs("chi_signal_"+samples[i][l][0].replace("QCD","") + '_sys.pdf')
     canvas.SaveAs("chi_signal_"+samples[i][l][0].replace("QCD","") + '_sys.eps')
