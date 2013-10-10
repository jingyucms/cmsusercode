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

def createPlots(sample,prefix,massbins):
    if sample.endswith(".txt"):
        files=[]
        filelist=open(sample)
	for line in filelist.readlines():
	    if ".root" in line:
	        files+=[line.strip()]
    else:
        files=[sample]
    prunedgenjets_handle=Handle("std::vector<reco::GenJet>")
    prunedgenjets_label="ak5GenJets"

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
    print sample,nevents
    jets="recoGenJets_ak5GenJets__PFAOD.obj"
    yboost='abs('+jets+'[0].y()+'+jets+'[1].y())/2.'
    chi='exp(abs('+jets+'[0].y()-'+jets+'[1].y()))'
    mass='sqrt(pow('+jets+'[0].energy()+'+jets+'[1].energy(),2)-pow('+jets+'[0].px()+'+jets+'[1].px(),2)-pow('+jets+'[0].py()+'+jets+'[1].py(),2)-pow('+jets+'[0].pz()+'+jets+'[1].pz(),2))'
    for massbin in massbins:
      events.Project(prefix+'#chi'+str(massbin).strip("()").replace(',',"_").replace(' ',""),chi,'('+yboost+'<1.11)*('+mass+'>='+str(massbin[0])+')*('+mass+'<'+str(massbin[1])+')')
      #events.Project(prefix+'y_{boost}'+str(massbin).strip("()").replace(',',"_").replace(' ',""),yboost,'('+chi+'<16)*('+mass+'>='+str(massbin[0])+')*('+mass+'<='+str(massbin[1])+')')
    for plot in plots:
      if nevents>0:
        plot.Scale(1./nevents)
    return plots

if __name__ == '__main__':

    wait=False
 
    prefix="datacard_shapelimit"
    chi_bins=[(1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,3,5,7,10,12,14,16),
              ]
    massbins=[(3600,4200),
	      (4200,8000)]
    #expectedevents=[1814*2,196*2,35*2]#89179*2,14448*2,
    #expectedevents=[3070,355,50]#23948
 
    if "QCD" in sys.argv[1]:
      chi_bins=[(1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,3,5,7,10,12,14,16),
              ]
      massbins=[(1900,2400),
              (2400,3000),
	      (3000,3600),
	      (3600,4200),
	      (4200,8000)]
 
    samples=[("QCD",[("fileLists/fileList_pythia8_qcd_m1400___Sep4_grid.txt",[(1900,2400),(2400,3000)]),
		     ("fileLists/fileList_pythia8_qcd_m2500___Sep4_grid.txt",[(3000,3600),(3600,4200)]),
		     ("fileLists/fileList_pythia8_qcd_m3700___Sep4_grid.txt",[(4200,8000)])]),
             
	     ("QCDNonPert",[("fileLists/fileList_pythia8_qcdNonPert_m1400___Sep4_grid.txt",[(1900,2400),(2400,3000)]),
                            ("fileLists/fileList_pythia8_qcdNonPert_m2500___Sep4_grid.txt",[(3000,3600),(3600,4200)]),
                            ("fileLists/fileList_pythia8_qcdNonPert_m3700___Sep4_grid.txt",[(4200,8000)])]),
	     ("QCDHpp",[("fileLists/fileList_herwigpp_qcd_m1400___Sep4_grid.txt",[(1900,2400),(2400,3000)]),
                        ("fileLists/fileList_herwigpp_qcd_m2500___Sep4_grid.txt",[(3000,3600),(3600,4200)]),
                        ("fileLists/fileList_herwigpp_qcd_m3700___Sep4_grid.txt",[(4200,8000)])]),
	     ("QCDHppNonPert",[("fileLists/fileList_herwigpp_qcdNonPert_m1400___Sep5_grid.txt",[(1900,2400),(2400,3000)]),
                               ("fileLists/fileList_herwigpp_qcdNonPert_m2500___Sep5_grid.txt",[(3000,3600),(3600,4200)]),
                               ("fileLists/fileList_herwigpp_qcdNonPert_m3700___Sep5_grid.txt",[(4200,8000)])]),
             
	     ("QCDCI4000",[("fileLists/fileList_pythia8_ci_m2500_4000_1_0_0_May27_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_4000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI6000",[("fileLists/fileList_pythia8_ci_m2500_6000_1_0_0_May27_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_6000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI8000",[("fileLists/fileList_pythia8_ci_m2500_8000_1_0_0_May27_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_8000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI9000",[("fileLists/fileList_pythia8_ci_m2500_9000_1_0_0_May27_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_9000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI10000",[("fileLists/fileList_pythia8_ci_m2500_10000_1_0_0_May27_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_10000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI12000",[("fileLists/fileList_pythia8_ci_m2500_12000_1_0_0_May27_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_12000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI14000",[("fileLists/fileList_pythia8_ci_m2500_14000_1_0_0_May27_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_14000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI15000",[("fileLists/fileList_pythia8_ci_m2500_15000_1_0_0_May27_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_15000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI16000",[("fileLists/fileList_pythia8_ci_m2500_16000_1_0_0_May27_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_16000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI18000",[("fileLists/fileList_pythia8_ci_m2500_18000_1_0_0_May27_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_18000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI20000",[("fileLists/fileList_pythia8_ci_m2500_20000_1_0_0_May27_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_20000_1_0_0_May27_grid.txt",[(4200,8000)])]),

             ("QCDCIminusLL6000",[("fileLists/fileList_pythia8_ci_m2500_6000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_6000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL8000",[("fileLists/fileList_pythia8_ci_m2500_8000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_8000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL9000",[("fileLists/fileList_pythia8_ci_m2500_9000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_9000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL10000",[("fileLists/fileList_pythia8_ci_m2500_10000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_10000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL12000",[("fileLists/fileList_pythia8_ci_m2500_12000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_12000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL14000",[("fileLists/fileList_pythia8_ci_m2500_14000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_14000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL15000",[("fileLists/fileList_pythia8_ci_m2500_15000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_15000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL16000",[("fileLists/fileList_pythia8_ci_m2500_16000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_16000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL18000",[("fileLists/fileList_pythia8_ci_m2500_18000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_18000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),
             ("QCDCIminusLL20000",[("fileLists/fileList_pythia8_ci_m2500_20000_-1_0_0_Aug24_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_ci_m3700_20000_-1_0_0_Aug24_grid.txt",[(4200,8000)])]),

             #("QCDADD_4_0_0_2000",[("fileLists/fileList_pythia8_add_m2500_2000_2000_4_0_0_Aug19_grid.txt",[(3600,4200)]),
		#        ("fileLists/fileList_pythia8_add_m3700_2000_2000_4_0_0_Aug19_grid.txt",[(4200,8000)])]),
             #("QCDADD_4_0_0_3000",[("fileLists/fileList_pythia8_add_m2500_3000_3000_4_0_0_Aug19_grid.txt",[(3600,4200)]),
		#        ("fileLists/fileList_pythia8_add_m3700_3000_3000_4_0_0_Aug19_grid.txt",[(4200,8000)])]),
             ("QCDADD_4_0_0_4000",[("fileLists/fileList_pythia8_add_m2500_4000_4000_4_0_0_Aug19_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_add_m3700_4000_4000_4_0_0_Aug19_grid.txt",[(4200,8000)])]),
             ("QCDADD_4_0_0_5000",[("fileLists/fileList_pythia8_add_m2500_5000_5000_4_0_0_Aug19_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_add_m3700_5000_5000_4_0_0_Aug19_grid.txt",[(4200,8000)])]),
             ("QCDADD_4_0_0_6000",[("fileLists/fileList_pythia8_add_m2500_6000_6000_4_0_0_Aug19_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_add_m3700_6000_6000_4_0_0_Aug19_grid.txt",[(4200,8000)])]),
             ("QCDADD_4_0_0_7000",[("fileLists/fileList_pythia8_add_m2500_7000_7000_4_0_0_Aug19_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_add_m3700_7000_7000_4_0_0_Aug19_grid.txt",[(4200,8000)])]),
             ("QCDADD_4_0_0_8000",[("fileLists/fileList_pythia8_add_m2500_8000_8000_4_0_0_Aug19_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_add_m3700_8000_8000_4_0_0_Aug19_grid.txt",[(4200,8000)])]),

             ("QCDADD_4_0_1_4000",[("fileLists/fileList_pythia8_add_m2500_4000_0_0_0_1_Aug19_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_add_m3700_4000_0_0_0_1_Aug19_grid.txt",[(4200,8000)])]),
             ("QCDADD_4_0_1_5000",[("fileLists/fileList_pythia8_add_m2500_5000_0_0_0_1_Aug19_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_add_m3700_5000_0_0_0_1_Aug19_grid.txt",[(4200,8000)])]),
             ("QCDADD_4_0_1_6000",[("fileLists/fileList_pythia8_add_m2500_6000_0_0_0_1_Aug19_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_add_m3700_6000_0_0_0_1_Aug19_grid.txt",[(4200,8000)])]),
             ("QCDADD_4_0_1_7000",[("fileLists/fileList_pythia8_add_m2500_7000_0_0_0_1_Aug19_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_add_m3700_7000_0_0_0_1_Aug19_grid.txt",[(4200,8000)])]),
             ("QCDADD_4_0_1_8000",[("fileLists/fileList_pythia8_add_m2500_8000_0_0_0_1_Aug19_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_add_m3700_8000_0_0_0_1_Aug19_grid.txt",[(4200,8000)])]),
             ("QCDADD_4_0_1_9000",[("fileLists/fileList_pythia8_add_m2500_9000_0_0_0_1_Aug19_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_add_m3700_9000_0_0_0_1_Aug19_grid.txt",[(4200,8000)])]),
             ("QCDADD_4_0_1_10000",[("fileLists/fileList_pythia8_add_m2500_10000_0_0_0_1_Aug19_grid.txt",[(3600,4200)]),
		        ("fileLists/fileList_pythia8_add_m3700_10000_0_0_0_1_Aug19_grid.txt",[(4200,8000)])]),
             ]

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
      for filename,mbs in files:
        plots[-1]+=createPlots(filename,name,mbs)

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
      legend1=TLegend(0.6,0.6,0.9,0.9,(str(massbins[j][0])+"<m_{jj}<"+str(massbins[j][1])+" GeV").replace("4200<m_{jj}<7000","m_{jj}>4200").replace("4200<m_{jj}<8000","m_{jj}>4200"))
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

