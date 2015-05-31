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
gStyle.SetNdivisions(506, "XYZ")
gStyle.SetLegendBorderSize(0)

def createPlots(sample,prefix,massbins,factor):
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
    plots += [TH1F(prefix+'mass',';dijet mass;N events for 1/fb of data',130,0,13000)]
    
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
    events.Project(prefix+'mass',mass,'('+chi+'<16)*('+yboost+'<1.11)')
    for plot in plots:
      if nevents>0:
        plot.Scale(factor/nevents)
    return (plots,nevents)

if __name__ == '__main__':

    wait=False
 
    prefix="datacard_shapelimit13TeVhigh"
    chi_bins=[(1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              ]
    massbins=[(4800,13000),
	      #(5000,13000),
	      #(5200,13000),
	      (5400,13000),
	      #(5600,13000),
	      ]
 
    samples=[("QCD",[("/opt2/chi_analysis/pythia8_ci_m4500_50000_1_0_0_13TeV_Nov7.root",massbins)],2.162e-9*1e12),
	     ("CI12000",[("/opt2/chi_analysis/pythia8_ci_m4500_12000_1_0_0_13TeV_Nov7.root",massbins)],2.154e-9*1e12),
             ("CI13000",[("/opt2/chi_analysis/pythia8_ci_m4500_13000_1_0_0_13TeV_Nov7.root",massbins)],2.150e-9*1e12),
             ("CI14000",[("/opt2/chi_analysis/pythia8_ci_m4500_14000_1_0_0_13TeV_Nov7.root",massbins)],2.147e-9*1e12),
             ("CI16000",[("/opt2/chi_analysis/pythia8_ci_m4500_16000_1_0_0_13TeV_Nov7.root",massbins)],2.149e-9*1e12),
             ("CI18000",[("/opt2/chi_analysis/pythia8_ci_m4500_18000_1_0_0_13TeV_Nov7.root",massbins)],2.148e-9*1e12),
            ]
 
    if "high" in prefix:
      massbins=[(6000,13000),
                (7000,13000),
	      ]
 
      samples=[("QCD",[("/opt2/chi_analysis/pythia8_ci_m5000_50000_1_0_0_13TeV_Nov7.root",massbins)],7.540e-10*1e12),
	     #("CI12000",[("/opt2/chi_analysis/pythia8_ci_m5000_12000_1_0_0_13TeV_Nov7.root",massbins)],7.559e-10*1e12),
             #("CI13000",[("/opt2/chi_analysis/pythia8_ci_m5000_13000_1_0_0_13TeV_Nov7.root",massbins)],7.400e-10*1e12),
             ("CI14000",[("/opt2/chi_analysis/pythia8_ci_m5000_14000_1_0_0_13TeV_Nov7.root",massbins)],7.471e-10*1e12),
             ("CI16000",[("/opt2/chi_analysis/pythia8_ci_m5000_16000_1_0_0_13TeV_Nov7.root",massbins)],7.477e-10*1e12),
             ("CI18000",[("/opt2/chi_analysis/pythia8_ci_m5000_18000_1_0_0_13TeV_Nov7.root",massbins)],7.483e-10*1e12),
             ("CI20000",[("/opt2/chi_analysis/pythia8_ci_m5000_20000_1_0_0_13TeV_Nov7.root",massbins)],7.483e-10*1e12),
             ("CI22000",[("/opt2/chi_analysis/pythia8_ci_m5000_22000_1_0_0_13TeV_Nov7.root",massbins)],7.483e-10*1e12),
            ]

    if "8" in prefix:
      massbins=[(3600,4200),
	      (4200,8000),
	      ]
      samples=[("QCD",[("/opt2/chi_analysis/pythia8_ci_m3500_50000_1_0_0_8TeV_Nov7.root",massbins)],6.045e-10*1e12),
	     ("CI8000",[("/opt2/chi_analysis/pythia8_ci_m3500_8000_1_0_0_8TeV_Nov7.root",massbins)],6.024e-10*1e12),
	     ("CI10000",[("/opt2/chi_analysis/pythia8_ci_m3500_10000_1_0_0_8TeV_Nov7.root",massbins)],5.977e-10*1e12),
             ("CI12000",[("/opt2/chi_analysis/pythia8_ci_m3500_12000_1_0_0_8TeV_Nov7.root",massbins)],5.994e-10*1e12),
             #("CI14000",[("/opt2/chi_analysis/pythia8_ci_m3500_14000_1_0_0_8TeV_Nov7.root",massbins)],5.991e-10*1e12),
            ]
 
    
             
    chi_binnings=[]
    for mass_bin in chi_bins:
        chi_binnings+=[array.array('d')]
        for chi_bin in mass_bin:
            chi_binnings[-1].append(chi_bin)
        
    print prefix, samples

    plots=[]
    nevents={}
    for name,files,xsec in samples:
      plots+=[[]]
      for filename,mbs in files:
        plot,nevent=createPlots(filename,name,mbs,xsec/1.3)# factor 1.3 to fix to 8 TeV data observation of 50 events at >4200
        plots[-1]+=plot
	nevents[name]=nevent

    out=TFile(prefix + '_chi.root','RECREATE')
    for j in range(len(massbins)):
      for i in range(len(samples)):
        print "number of "+samples[i][0]+" events expected in",str(massbins[j][0])+"<m_{jj}<"+str(massbins[j][1])+" GeV:",plots[i][j].Integral()
        #print "mass: number of "+samples[i][0]+" events expected in",str(massbins[j][0])+"<m_{jj}<"+str(massbins[j][1])+" GeV:",plots[i][len(massbins)].Integral(plots[i][len(massbins)].FindBin(massbins[j][0]),plots[i][len(massbins)].FindBin(massbins[j][1]))
	if "chi" in plots[i][j].GetName():
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

    canvas.SaveAs(prefix + '_chi.pdf')
    canvas.SaveAs(prefix + '_chi.eps')
    if wait:
        os.system("ghostview "+prefix + '_chi.eps')

    canvas = TCanvas("","",0,0,200,200)
    canvas.SetLogy()

    legends=[]
    plots[0][len(massbins)].Draw("he")
    if "8" in prefix:
      plots[0][len(massbins)].GetXaxis().SetRangeUser(3500,5000)
    else:
      plots[0][len(massbins)].GetXaxis().SetRangeUser(4500,8000)
    legend1=TLegend(0.6,0.6,0.9,0.9)
    legends+=[legend1]
    legend1.AddEntry(plots[0][len(massbins)],samples[0][0],"l")
    for i in range(1,len(samples)):
      plots[i][len(massbins)].SetLineColor(color[i])
      plots[i][len(massbins)].Draw("hesame")
      legend1.AddEntry(plots[i][len(massbins)],samples[i][0],"l")
    legend1.SetTextSize(0.04)
    legend1.SetFillStyle(0)
    legend1.Draw("same")

    canvas.SaveAs(prefix + '_mass.pdf')
    canvas.SaveAs(prefix + '_mass.eps')
    if wait:
        os.system("ghostview "+prefix + '_mass.eps')

