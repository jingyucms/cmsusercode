masspoint=2000

import os, sys
from ROOT import * 
from DataFormats.FWLite import Events,Handle
import array, math

#gROOT.Macro( os.path.expanduser( '~/rootlogon.C' ) )
gROOT.Reset()
gROOT.SetStyle("Plain")
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
#gStyle.SetTitleOffset(1.2,"Y")
gStyle.SetPadLeftMargin(0.18)
gStyle.SetPadBottomMargin(0.18)
gStyle.SetPadTopMargin(0.03)
gStyle.SetPadRightMargin(0.05)
gStyle.SetMarkerSize(1.5)
gStyle.SetHistLineWidth(1)
gStyle.SetStatFontSize(0.020)
gStyle.SetTitleSize(0.06, "XYZ")
gStyle.SetLabelSize(0.05, "XYZ")
gStyle.SetNdivisions(510, "XYZ")
gStyle.SetLegendBorderSize(0)

def createPlots(sample,prefix,weightname,massbins):
    files=[]
    print "list files"
    if sample.endswith(".txt"):
        filelist=open(sample)
	for line in filelist.readlines():
	    if ".root" in line:
	        files+=[line.strip()]
    else:
        #folders=os.listdir("/pnfs/psi.ch/cms/trivcat/store/user/hinzmann/dijet_angular/")
	folders=os.listdir("/mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_1_25_patch3/src/cmsusercode/chi_analysis")
	for folder in folders:
	  if sample in folder and ".root" in folder:
            #files+=["dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/user/hinzmann/dijet_angular/"+folder]#+"/GEN.root"
	    files+=["/mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_1_25_patch3/src/cmsusercode/chi_analysis/"+folder]
	    #break
        #files=["root://eoscms.cern.ch//eos/cms/store/cmst3/group/monojet/mc/model3_v2/gen/"+sample+".root"]

    print files
    #files=["GEN.root"]
    prunedgenjets_handle=Handle("std::vector<reco::GenJet>")
    prunedgenjets_label="ak4GenJets"

    plots=[]
    for massbin in massbins:
      plots += [TH1F(prefix+'#chi'+str(massbin).strip("()").replace(',',"_").replace(' ',""),';#chi;N',15,1,16)]
    plots += [TH1F(prefix+'dijetmass',';dijet mass;N',35,0,7000)]
    
    for plot in plots:
        plot.Sumw2()

    event_count=0
    acceptance=0
    sumweights=0
    firstxsec=0
    for f in files[:]:
     print f
     try:
      fil=TFile.Open(f)
      events=fil.Get('Events')
      nevents=events.GetEntries()
     except:
      print "error opening",f
      continue
     print sample,nevents,nxsec
     for event in events:
         xsec=event.LHEEventProduct_externalLHEProducer__GEN.product().originalXWGTUP()*1000. # convert to pb
	 if firstxsec>0 and xsec!=firstxsec:
	    print "inconsistent xsec",firstxsec,xsec
	    inconsistent
	 #weights=[(w.id,w.wgt) for w in event.LHEEventProduct_externalLHEProducer__GEN.product().weights()]
	 #print weights
	 try:
	  weight=[w.wgt for w in event.LHEEventProduct_externalLHEProducer__GEN.product().weights() if weightname==w.id][0]/event.LHEEventProduct_externalLHEProducer__GEN.product().weights()[0].wgt
	 except:
	  print "error reading weight"
	  break
	 #if weight<1./(nevents*len(files)): continue # ignore events with weight < 1/ngenerated
         event_count+=1
	 if event_count>10000000: break
         if event_count%10000==1: print "event",event_count
	 sumweights+=weight
	 #print xsec,weight
         jet1=TLorentzVector()
         jet2=TLorentzVector()
	 jets=event.recoGenJets_ak4GenJets__GEN.product()
	 if len(jets)<2: continue
	 j1=jets[0]
	 j2=jets[1]
         jet1.SetPtEtaPhiM(j1.pt(),j1.eta(),j1.phi(),j1.mass())
         jet2.SetPtEtaPhiM(j2.pt(),j2.eta(),j2.phi(),j2.mass())
         mjj=(jet1+jet2).M()
         chi=math.exp(abs(jet1.Rapidity()-jet2.Rapidity()))
         yboost=abs(jet1.Rapidity()+jet2.Rapidity())/2.
	 if abs(jet1.Eta())<2.5 and abs(jet2.Eta())<2.5 and abs(jet1.Eta()-jet2.Eta())<1.3:
	    plots[-1].Fill(mjj,weight)
	 irec=0
         if mjj<1500 or chi>16. or yboost>1.11: continue
         if mjj>2400: acceptance+=weight
	 for massbin in massbins:
            if yboost<1.11 and mjj>=massbin[0] and mjj<massbin[1]:
               plots[irec].Fill(chi,weight)
	    irec+=1
     fil.Close()
    print sample,weightname,"acceptance",acceptance/sumweights, "xsec",xsec*sumweights/event_count
    for plot in plots:
      if nevents>0:
        plot.Scale(xsec/event_count)
    print "Dijet mass integral", plots[-1].Integral()
    return plots

if __name__ == '__main__':

    if len(sys.argv)<2:
       print "ERROR: need to provide sample name as argument"
    point=sys.argv[1]
    #point="Vector_Dijet_LO_Mphi_1500_1_1p5_1p0_Feb25"
    nxsec=int(sys.argv[2])
    #nxsec=0
    print point
    if "Vector" in point:
      weights=['gdmv_1p0_gdma_0_gv_0p01_ga_0', 'gdmv_1p0_gdma_0_gv_0p05_ga_0', 'gdmv_1p0_gdma_0_gv_0p1_ga_0', 'gdmv_1p0_gdma_0_gv_0p2_ga_0', 'gdmv_1p0_gdma_0_gv_0p25_ga_0', 'gdmv_1p0_gdma_0_gv_0p3_ga_0', 'gdmv_1p0_gdma_0_gv_0p5_ga_0', 'gdmv_1p0_gdma_0_gv_0p75_ga_0', 'gdmv_1p0_gdma_0_gv_1_ga_0', 'gdmv_1p0_gdma_0_gv_1p5_ga_0', 'gdmv_1p0_gdma_0_gv_2p0_ga_0', 'gdmv_1p0_gdma_0_gv_2p5_ga_0', 'gdmv_1p0_gdma_0_gv_3p0_ga_0']
    else:
      weights=['gdmv_0_gdma_1p0_gv_0_ga_0p01', 'gdmv_0_gdma_1p0_gv_0_ga_0p05', 'gdmv_0_gdma_1p0_gv_0_ga_0p1', 'gdmv_0_gdma_1p0_gv_0_ga_0p2', 'gdmv_0_gdma_1p0_gv_0_ga_0p25', 'gdmv_0_gdma_1p0_gv_0_ga_0p3', 'gdmv_0_gdma_1p0_gv_0_ga_0p5', 'gdmv_0_gdma_1p0_gv_0_ga_0p75', 'gdmv_0_gdma_1p0_gv_0_ga_1', 'gdmv_0_gdma_1p0_gv_0_ga_1p5', 'gdmv_0_gdma_1p0_gv_0_ga_2p0', 'gdmv_0_gdma_1p0_gv_0_ga_2p5', 'gdmv_0_gdma_1p0_gv_0_ga_3p0']
 
    wait=False
    
    prefix="datacard_shapelimit13TeV_DM"+point+"_"+weights[nxsec]
 
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
 
    samples=[("DM"+point+"_"+weights[nxsec],[(point,weights[nxsec])]),
             ]
    
    #xsecs={}
    #for l in open("xsecs_13TeV_dm_2016.txt").readlines():
    #  xsecs=eval(l)
    #print xsecs

    chi_binnings=[]
    for mass_bin in chi_bins:
        chi_binnings+=[array.array('d')]
        for chi_bin in mass_bin:
            chi_binnings[-1].append(chi_bin)
        
    print prefix, samples

    canvas = TCanvas("","",0,0,400,400)
    canvas.SetLogy()

    plots=[]
    for name,files in samples:
      plots+=[[]]
      i=0
      for filename,weightname in files:
        i+=1
        ps=createPlots(filename,name,weightname,massbins)
        if i==1:
          plots[-1]+=ps
	else:
	  for i in range(len(plots[-1])):
            plots[-1][i].Add(ps[i])
    try:
     out=TFile(prefix + '_chi2016.root','RECREATE')
     for j in range(len(massbins)+1):#+1
      for i in range(len(samples)):
        #if plots[i][j].Integral()>0:
        #  plots[i][j].Scale(expectedevents[j]/plots[i][j].Integral())
	if j<len(massbins):
          plots[i][j]=plots[i][j].Rebin(len(chi_binnings[j])-1,plots[i][j].GetName()+"_rebin1",chi_binnings[j])
        else:
	  plots[i][j].Draw()
	  canvas.SaveAs(prefix + '_mass.pdf')
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
        #if plots[i][j].Integral()>0:
        #  plots[i][j].Scale(1./plots[i][j].Integral())
        for b in range(plots[i][j].GetXaxis().GetNbins()):
          plots[i][j].SetBinContent(b+1,plots[i][j].GetBinContent(b+1)/plots[i][j].GetBinWidth(b+1))
          plots[i][j].SetBinError(b+1,plots[i][j].GetBinError(b+1)/plots[i][j].GetBinWidth(b+1))
        #plots[i][j].GetYaxis().SetRangeUser(0,0.2)

     canvas = TCanvas("","",0,0,400,200)
     canvas.SetLogy(False)
     canvas.Divide(2,1)
     if len(massbins)>2:
      canvas = TCanvas("","",0,0,600,400)
      canvas.Divide(3,2)
     if len(massbins)>6:
      canvas = TCanvas("","",0,0,600,600)
      canvas.Divide(3,3)

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
    except:
      print sys.exc_info()[0]
