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
    
    for plot in plots:
        plot.Sumw2()

    event_count=0
    events=TChain('Events')
    for f in files:
      events.Add(f)
    
    print sample,events.GetEntries()
    jets="recoGenJets_ak5GenJets__PFAOD.obj"
    yboost='abs('+jets+'[0].y()+'+jets+'[1].y())'
    chi='exp(abs('+jets+'[0].y()-'+jets+'[1].y()))'
    mass='sqrt(pow('+jets+'[0].energy()+'+jets+'[1].energy(),2)-pow('+jets+'[0].px()+'+jets+'[1].px(),2)-pow('+jets+'[0].py()+'+jets+'[1].py(),2)-pow('+jets+'[0].pz()+'+jets+'[1].pz(),2))'
    for massbin in massbins:
      events.Project(prefix+'#chi'+str(massbin).strip("()").replace(',',"_").replace(' ',""),chi,'('+yboost+'<1.11)*('+mass+'>='+str(massbin[0])+')*('+mass+'<='+str(massbin[1])+')')
    return plots

if __name__ == '__main__':

    wait=True
 
    prefix="datacard_test"
 
    chi_bins=[(1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,3,5,7,10,12,14,16),
               (1,3,5,7,10,12,14,16),
              ]
          
    chi_bins=[(1,2,3,4,5,6,7),
               (1,2,3,4,5,6,7),
               (1,2,3,4,5,6,7),
               (1,3,5,7),
              ]
    massbins=[(1900,2400),
              (2400,3000),
	      (3000,4000),
	      (4000,8000)]
    expectedevents=[89179*2,14448*2,1990*2,54*2] #chi<16
    #expectedevents=[58586*2,9453*2,1312*2,31*2] #chi<10
    #expectedevents=[34961*2,5601*2,838*2,12*2] #chi<6
    #expectedevents=[75720*2,13487*2,1962*2,55*2] #061
    #expectedevents=[89317*2,14449*2,1990*2,55*2] #161
    #expectedevents=[113938*2,18504*2,2512*2,69*2] #100
    #expectedevents=[52706*2,8532*2,1182*2,27*2] #135
    #expectedevents=[29294*2,4755*2,705*2,8*2] #160
    
    samples=[("QCD",[("fileList_pythia8_qcd_m1500___Nov15_grid.txt",[(1900,2400)]),
                     ("fileList_pythia8_qcd_m2000___Nov15_grid.txt",[(2400,3000)]),
		     ("fileList_pythia8_qcd_m2500___Nov15_grid.txt",[(3000,4000),(4000,8000)])]),
             ("QCDCI4000",[("fileList_pythia8_ci_m1500_4000_1_0_0_Nov15_grid.txt",[(1900,2400)]),
                        ("fileList_pythia8_ci_m2000_4000_1_0_0_Nov15_grid.txt",[(2400,3000)]),
		        ("fileList_pythia8_ci_m2500_4000_1_0_0_Nov15_grid.txt",[(3000,4000),(4000,8000)])]),
             ("QCDCI6000",[("fileList_pythia8_ci_m1500_6000_1_0_0_Nov15_grid.txt",[(1900,2400)]),
                        ("fileList_pythia8_ci_m2000_6000_1_0_0_Nov15_grid.txt",[(2400,3000)]),
		        ("fileList_pythia8_ci_m2500_6000_1_0_0_Nov15_grid.txt",[(3000,4000),(4000,8000)])]),
             ("QCDCI8000",[("fileList_pythia8_ci_m1500_8000_1_0_0_Nov15_grid.txt",[(1900,2400)]),
                        ("fileList_pythia8_ci_m2000_8000_1_0_0_Nov15_grid.txt",[(2400,3000)]),
		        ("fileList_pythia8_ci_m2500_8000_1_0_0_Nov15_grid.txt",[(3000,4000),(4000,8000)])]),
             ("QCDCI10000",[("fileList_pythia8_ci_m1500_10000_1_0_0_Nov15_grid.txt",[(1900,2400)]),
                        ("fileList_pythia8_ci_m2000_10000_1_0_0_Nov15_grid.txt",[(2400,3000)]),
		        ("fileList_pythia8_ci_m2500_10000_1_0_0_Nov15_grid.txt",[(3000,4000),(4000,8000)])]),
             ("QCDCI12000",[("fileList_pythia8_ci_m1500_12000_1_0_0_Nov15_grid.txt",[(1900,2400)]),
                        ("fileList_pythia8_ci_m2000_12000_1_0_0_Nov15_grid.txt",[(2400,3000)]),
		        ("fileList_pythia8_ci_m2500_12000_1_0_0_Nov15_grid.txt",[(3000,4000),(4000,8000)])]),
             ("QCDCI14000",[("fileList_pythia8_ci_m1500_14000_1_0_0_Nov15_grid.txt",[(1900,2400)]),
                        ("fileList_pythia8_ci_m2000_14000_1_0_0_Nov15_grid.txt",[(2400,3000)]),
		        ("fileList_pythia8_ci_m2500_14000_1_0_0_Nov15_grid.txt",[(3000,4000),(4000,8000)])]),
             ("QCDCI16000",[("fileList_pythia8_ci_m1500_16000_1_0_0_Nov15_grid.txt",[(1900,2400)]),
                        ("fileList_pythia8_ci_m2000_16000_1_0_0_Nov15_grid.txt",[(2400,3000)]),
		        ("fileList_pythia8_ci_m2500_16000_1_0_0_Nov15_grid.txt",[(3000,4000),(4000,8000)])]),
             ("QCDCI18000",[("fileList_pythia8_ci_m1500_18000_1_0_0_Nov15_grid.txt",[(1900,2400)]),
                        ("fileList_pythia8_ci_m2000_18000_1_0_0_Nov15_grid.txt",[(2400,3000)]),
		        ("fileList_pythia8_ci_m2500_18000_1_0_0_Nov15_grid.txt",[(3000,4000),(4000,8000)])]),
             ("QCDCI20000",[("fileList_pythia8_ci_m1500_20000_1_0_0_Nov15_grid.txt",[(1900,2400)]),
                        ("fileList_pythia8_ci_m2000_20000_1_0_0_Nov15_grid.txt",[(2400,3000)]),
		        ("fileList_pythia8_ci_m2500_20000_1_0_0_Nov15_grid.txt",[(3000,4000),(4000,8000)])]),
             ]
    """
    chi_bins=[(1,2,3,4,5,6,7),
               (1,2,3,4,5,6,7),
               (1,2,3,4,5,6,7),
               (1,3,5,7),
               (1,3,5,7),
              ]
    massbins=[(1900,2400),
              (2400,3000),
	      (3000,3600),
	      (3600,4200),
	      (4200,8000)]
    expectedevents=[89179*2,14448*2,1814*2,196*2,35*2]
 
    samples=[("QCD",[("fileList_pythia8_qcd_m1500___Nov15_grid.txt",[(1900,2400)]),
                     ("fileList_pythia8_qcd_m2000___Nov15_grid.txt",[(2400,3000)]),
		     ("fileList_pythia8_qcd_m2500___Nov15_grid.txt",[(3000,3600),(3600,4200),(4200,8000)])]),
             ("QCDCI4000",[("fileList_pythia8_ci_m1500_4000_1_0_0_Nov15_grid.txt",[(1900,2400)]),
                        ("fileList_pythia8_ci_m2000_4000_1_0_0_Nov15_grid.txt",[(2400,3000)]),
		        ("fileList_pythia8_ci_m2500_4000_1_0_0_Nov15_grid.txt",[(3000,3600),(3600,4200),(4200,8000)])]),
             ("QCDCI6000",[("fileList_pythia8_ci_m1500_6000_1_0_0_Nov15_grid.txt",[(1900,2400)]),
                        ("fileList_pythia8_ci_m2000_6000_1_0_0_Nov15_grid.txt",[(2400,3000)]),
		        ("fileList_pythia8_ci_m2500_6000_1_0_0_Nov15_grid.txt",[(3000,3600),(3600,4200),(4200,8000)])]),
             ("QCDCI8000",[("fileList_pythia8_ci_m1500_8000_1_0_0_Nov15_grid.txt",[(1900,2400)]),
                        ("fileList_pythia8_ci_m2000_8000_1_0_0_Nov15_grid.txt",[(2400,3000)]),
		        ("fileList_pythia8_ci_m2500_8000_1_0_0_Nov15_grid.txt",[(3000,3600),(3600,4200),(4200,8000)])]),
             ("QCDCI10000",[("fileList_pythia8_ci_m1500_10000_1_0_0_Nov15_grid.txt",[(1900,2400)]),
                        ("fileList_pythia8_ci_m2000_10000_1_0_0_Nov15_grid.txt",[(2400,3000)]),
		        ("fileList_pythia8_ci_m2500_10000_1_0_0_Nov15_grid.txt",[(3000,3600),(3600,4200),(4200,8000)])]),
             ("QCDCI12000",[("fileList_pythia8_ci_m1500_12000_1_0_0_Nov15_grid.txt",[(1900,2400)]),
                        ("fileList_pythia8_ci_m2000_12000_1_0_0_Nov15_grid.txt",[(2400,3000)]),
		        ("fileList_pythia8_ci_m2500_12000_1_0_0_Nov15_grid.txt",[(3000,3600),(3600,4200),(4200,8000)])]),
             ("QCDCI14000",[("fileList_pythia8_ci_m1500_14000_1_0_0_Nov15_grid.txt",[(1900,2400)]),
                        ("fileList_pythia8_ci_m2000_14000_1_0_0_Nov15_grid.txt",[(2400,3000)]),
		        ("fileList_pythia8_ci_m2500_14000_1_0_0_Nov15_grid.txt",[(3000,3600),(3600,4200),(4200,8000)])]),
             ("QCDCI16000",[("fileList_pythia8_ci_m1500_16000_1_0_0_Nov15_grid.txt",[(1900,2400)]),
                        ("fileList_pythia8_ci_m2000_16000_1_0_0_Nov15_grid.txt",[(2400,3000)]),
		        ("fileList_pythia8_ci_m2500_16000_1_0_0_Nov15_grid.txt",[(3000,3600),(3600,4200),(4200,8000)])]),
             ("QCDCI18000",[("fileList_pythia8_ci_m1500_18000_1_0_0_Nov15_grid.txt",[(1900,2400)]),
                        ("fileList_pythia8_ci_m2000_18000_1_0_0_Nov15_grid.txt",[(2400,3000)]),
		        ("fileList_pythia8_ci_m2500_18000_1_0_0_Nov15_grid.txt",[(3000,3600),(3600,4200),(4200,8000)])]),
             ("QCDCI20000",[("fileList_pythia8_ci_m1500_20000_1_0_0_Nov15_grid.txt",[(1900,2400)]),
                        ("fileList_pythia8_ci_m2000_20000_1_0_0_Nov15_grid.txt",[(2400,3000)]),
		        ("fileList_pythia8_ci_m2500_20000_1_0_0_Nov15_grid.txt",[(3000,3600),(3600,4200),(4200,8000)])]),
             ]
    """
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
	prefix+="_"+samples[-1][0].replace("QCDCI","CI")
  
    print prefix, samples

    plots=[]
    for name,files in samples:
      plots+=[[]]
      for filename,mbs in files:
        plots[-1]+=createPlots(filename,name,mbs)

    out=TFile(prefix + '_chi.root','RECREATE')
    for j in range(len(massbins)):
      for i in range(len(samples)):
        if plots[i][j].Integral()>0:
          plots[i][j].Scale(expectedevents[j]/plots[i][j].Integral())
        plots[i][j]=plots[i][j].Rebin(len(chi_binnings[j])-1,plots[i][j].GetName()+"_rebin1",chi_binnings[j])
        plots[i][j].Write()
        jesup=plots[i][j].Clone(plots[i][j].GetName()+"_jesUp")
        jesdown=plots[i][j].Clone(plots[i][j].GetName()+"_jesDown")
	for b in range(plots[i][j].GetNbinsX()):
	    jesup.SetBinContent(b+1,plots[i][j].GetBinContent(b+1)*(1+(8.5-plots[i][j].GetBinCenter(b+1))/7.5*0.2))
	    jesdown.SetBinContent(b+1,plots[i][j].GetBinContent(b+1)*(1-(8.5-plots[i][j].GetBinCenter(b+1))/7.5*0.2))
	jesup.Write()
	jesdown.Write()
	if samples[i][0]=="QCD":
	   plots[i][j].Write(plots[i][j].GetName().replace("QCD","data_obs"))
	else:
	   clone=plots[i][j].Clone(plots[i][j].GetName().replace("QCDCI","CI"))
	   clone.Add(plots[0][j],-1)
	   for b in range(clone.GetNbinsX()):
                if clone.GetBinContent(b+1)-clone.GetBinError(b+1)<0:
		    clone.SetBinContent(b+1,0)
	   clone.Write()
           jesup=clone.Clone(clone.GetName()+"_jesUp")
           jesdown=clone.Clone(clone.GetName()+"_jesDown")
	   for b in range(clone.GetNbinsX()):
	       jesup.SetBinContent(b+1,clone.GetBinContent(b+1)*(1+(8.5-clone.GetBinCenter(b+1))/7.5*0.2))
               jesdown.SetBinContent(b+1,clone.GetBinContent(b+1)*(1-(8.5-clone.GetBinCenter(b+1))/7.5*0.2))
	   for b in range(jesup.GetNbinsX()):
                if jesup.GetBinContent(b+1)-jesup.GetBinError(b+1)<0:
		    jesup.SetBinContent(b+1,0)
                if jesdown.GetBinContent(b+1)-jesdown.GetBinError(b+1)<0:
		    jesdown.SetBinContent(b+1,0)
           jesup.Write()
           jesdown.Write()

    for j in range(len(massbins)):
      for i in range(len(samples)):
        if plots[i][j].Integral()>0:
          plots[i][j].Scale(1./plots[i][j].Integral())
        for b in range(plots[i][j].GetXaxis().GetNbins()):
          plots[i][j].SetBinContent(b+1,plots[i][j].GetBinContent(b+1)/plots[i][j].GetBinWidth(b+1))
          plots[i][j].SetBinError(b+1,plots[i][j].GetBinError(b+1)/plots[i][j].GetBinWidth(b+1))
        plots[i][j].GetYaxis().SetRangeUser(0,0.2)

    canvas = TCanvas("","",0,0,600,400)
    canvas.Divide(3,2)

    legends=[]
    for j in range(len(massbins)):
      canvas.cd(j+1)
      plots[0][j].Draw("he")
      print "number of events passed:",plots[0][j].GetEntries()
      legend1=TLegend(0.6,0.6,0.9,0.9,"")
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
