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

    useLensData=False
    useUnfoldedData=True

    prefixs=["datacard_shapelimit13TeV"]
 
    chi_bins=[#(1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,3,6,9,12,16),
              ]
    chi_binnings=[]
    for mass_bin in chi_bins:
        chi_binnings+=[array.array('d')]
        for chi_bin in mass_bin:
            chi_binnings[-1].append(chi_bin)
    massbins=[#(1900,2400),
              (2400,3000),
	      (3000,3600),
	      (3600,4200),
	      (4200,4800),
	      (4800,5400),
	      (5400,6000),
	      (6000,13000)
	      ]
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
    mass_bins_nlo_list=[#(2,),
    	      (3,),
    	      (4,),
    	      (5,),
    	      (6,),
	      (7,),
	      (8,),
	      (9,10,),
    	     ]


    samples=[("QCD",[]),
             ]
 
    dataevents={}
    data={}
    for prefix in prefixs: 
     # signal cards
     for i in range(len(samples)):
      sample=prefix + "_"+samples[i][0] + '_chi2016.root'
      print sample
      out=TFile(sample,'UPDATE')

      closefiles=[]

      # LO QCD file
      sample2="datacards/"+prefix + '_GENv4_chi.root'
      print sample2
      in2=TFile(sample2,'READ')

      # data file
      insample='datacards/datacard_shapelimit13TeV_25nsData11combi_chi.root'
      print insample
      infile=TFile(insample,'READ')

      # unfolded data file
      unfoldsample='datacards/Unfolded_chiNtuple_dataReReco_v3_Coarse_PFHT900_fromCB_AK4SF_pythia8_Pt_170toInf.root'
      print unfoldsample
      unfoldfile=TFile(unfoldsample,'READ')

      # NLO correction
      filename1nu2="fastnlo/RunII/fnl5662j_v23_fix_CT14nlo_allmu_ak4.root"
      print filename1nu2
      nlofile2 = TFile.Open(filename1nu2)
      closefiles+=[nlofile2]

      # NLO uncertainties
      filename1nu3="fastnlo/RunII/fnl5662j_cs_ct14nlo_30000_LL+.root"
      print filename1nu3
      nlofile3 = TFile.Open(filename1nu3)
      closefiles+=[nlofile3]

      # EWK correction
      filename1ewk="fastnlo/RunII/DijetAngularCMS13_ewk.root"
      print filename1ewk
      ewkfile = TFile.Open(filename1ewk)
      closefiles+=[ewkfile]

      # JES uncertainty QCD
      filename1jes="datacards/chi_systematic_plotschi_QCD4RerecoV3_13TeV_2016.root"
      print filename1jes
      jesfile = TFile.Open(filename1jes)
      closefiles+=[jesfile]

      # JES uncertainty CI
      filename1jesci="datacards/chi_systematic_plotschi_QCD4RerecoV3_13TeV_2016.root"
      print filename1jesci
      jescifile = TFile.Open(filename1jesci)
      closefiles+=[jescifile]

      canvas = TCanvas("","",0,0,600,600)
      canvas.Divide(3,3)
      plots=[]
      legends=[]

      for j in range(len(massbins)):
        # data
        histname="dijet_"+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_chi"
        print histname
	if useLensData:
  	  if "13000" in str(massbins[j]):
            histname2="dijet_m_chi_2__projY_"+str(massbins[j]).strip("()").replace(',',"-").replace(' ',"")
          else:
	    histname2="dijet_m_chi_2__projY_"+str(massbins[j]).strip("()").replace(',',"-").replace(' ',"")
          print histname2
  	  #if "1900" in str(massbins[j]):
          #   data = TH1F(unfoldfile2.Get(histname2))
	  #else:   
          data = TH1D(unfoldfile.Get(histname2))
	  data.SetName(histname)
	elif useUnfoldedData:
          histname2="dijet_mass_"+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_chi_unfolded"
          print histname2
  	  #if "1900" in str(massbins[j]):
          #   data = TH1F(unfoldfile2.Get(histname2))
	  #else:   
          data = TH1F(unfoldfile.Get(histname2))
	  data.SetName(histname)
	else:
          data = TH1F(infile.Get("data_obs#chi"+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"))
        data=data.Rebin(len(chi_binnings[j])-1,data.GetName()+"_rebin1",chi_binnings[j])
	dataevents[j]=data.Integral()
	out.cd()
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

        # NLO normalized
        nloqcdnorm=None
        for k in mass_bins_nlo_list[j]:
         histname='chi-'+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])
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
	    nloqcd.SetBinContent(b+1,nloqcd.GetBinContent(b+1)*correction)
	nloqcd.Scale(1./nloqcd.Integral())
        ewk.SetName("ewk-"+histname)

        # QCD (empty background, not used in limit)
        histname='QCD#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print histname
        qcd=in2.Get(histname)
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
	histname=samples[i][0]+'#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print histname
        ci=nloqcd.Clone(histname)
        ci.Scale(dataevents[j]/ci.Integral())
        for b in range(ci.GetXaxis().GetNbins()):
            ci.SetBinError(b+1,0)
        out.cd()
	for k in range(0,200):
            out.Delete(histname+";"+str(k))
        ci.Write(histname)

        # ALT (=NLO QCD)
        histname=samples[i][0]+'#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print histname
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
	for k in range(0,200):
            out.Delete(histname+";"+str(k))
        alt.Write(histname)
	
        # JER uncertainty
        histname=samples[i][0]+'#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        clone=alt.Clone(histname)
        clone=clone.Rebin(len(chi_binnings[j])-1,clone.GetName(),chi_binnings[j])
	jerup=clone.Clone(histname+"_jerUp")
        jerdown=clone.Clone(histname+"_jerDown")
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
	    jerup.SetBinContent(b+1,clone.GetBinContent(b+1)*(1.+(clone.GetBinCenter(b+1)-8.5)/7.5*slopes[massbins[j][0]]))
            jerdown.SetBinContent(b+1,clone.GetBinContent(b+1)*(1.-(clone.GetBinCenter(b+1)-8.5)/7.5*slopes[massbins[j][0]]))
	out.cd()
	for k in range(0,200):
            out.Delete(histname+"_jerUp"+";"+str(k))
            out.Delete(histname+"_jerDown"+";"+str(k))
        jerup.Write()
        jerdown.Write()
        histname=samples[i][0]+'_ALT#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        clone=alt.Clone(histname)
        clone=clone.Rebin(len(chi_binnings[j])-1,clone.GetName(),chi_binnings[j])
        jerup=clone.Clone(histname+"_jerUp")
        jerdown=clone.Clone(histname+"_jerDown")
	for b in range(clone.GetNbinsX()):
	    jerup.SetBinContent(b+1,clone.GetBinContent(b+1)*(1.+(clone.GetBinCenter(b+1)-8.5)/7.5*slopes[massbins[j][0]]))
            jerdown.SetBinContent(b+1,clone.GetBinContent(b+1)*(1.-(clone.GetBinCenter(b+1)-8.5)/7.5*slopes[massbins[j][0]]))
	out.cd()
	for k in range(0,200):
            out.Delete(histname+"_jerUp"+";"+str(k))
            out.Delete(histname+"_jerDown"+";"+str(k))
        jerup.Write()
        jerdown.Write()

        # Unfold uncertainty
        #histname=samples[i][0]+'#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        #clone=alt.Clone(histname)
        #clone=clone.Rebin(len(chi_binnings[j])-1,clone.GetName(),chi_binnings[j])
	#unfoldup=clone.Clone(histname+"_unfoldUp")
        #unfolddown=clone.Clone(histname+"_unfoldDown")
	#slopes={}
	#slopes[1900]=0.08
	#slopes[2400]=0.08
	#slopes[3000]=0.08
	#slopes[3600]=0.08
	#slopes[4200]=0.08
	#slopes[4800]=0.08
	#slopes[5400]=0.08
	#for b in range(clone.GetNbinsX()):
	#    unfoldup.SetBinContent(b+1,clone.GetBinContent(b+1)*(1.-slopes[massbins[j][0]]/2.+abs(clone.GetBinCenter(b+1)-8.5)/7.5*slopes[massbins[j][0]]))
        #    unfolddown.SetBinContent(b+1,clone.GetBinContent(b+1)*(1.+slopes[massbins[j][0]]/2.-abs(clone.GetBinCenter(b+1)-8.5)/7.5*slopes[massbins[j][0]]))
	#out.cd()
	#for k in range(0,200):
        #    out.Delete(histname+"_unfoldUp"+";"+str(k))
        #    out.Delete(histname+"_unfoldDown"+";"+str(k))
        #unfoldup.Write()
        #unfolddown.Write()
        #histname=samples[i][0]+'_ALT#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        #clone=alt.Clone(histname)
        #clone=clone.Rebin(len(chi_binnings[j])-1,clone.GetName(),chi_binnings[j])
        #unfoldup=clone.Clone(histname+"_unfoldUp")
        #unfolddown=clone.Clone(histname+"_unfoldDown")
	#for b in range(clone.GetNbinsX()):
	#    unfoldup.SetBinContent(b+1,clone.GetBinContent(b+1)*(1.-slopes[massbins[j][0]]/2.+abs(clone.GetBinCenter(b+1)-8.5)/7.5*slopes[massbins[j][0]]))
        #    unfolddown.SetBinContent(b+1,clone.GetBinContent(b+1)*(1.+slopes[massbins[j][0]]/2.-abs(clone.GetBinCenter(b+1)-8.5)/7.5*slopes[massbins[j][0]]))
	#out.cd()
	#for k in range(0,200):
        #    out.Delete(histname+"_unfoldUp"+";"+str(k))
        #    out.Delete(histname+"_unfoldDown"+";"+str(k))
        #unfoldup.Write()
        #unfolddown.Write()

        # jes uncertainty
        histname=samples[i][0]+'#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        clone=alt.Clone(histname)
        clone=clone.Rebin(len(chi_binnings[j])-1,clone.GetName(),chi_binnings[j])
        jesup=clone.Clone(histname+"_jesUp")
        jesdown=clone.Clone(histname+"_jesDown")
        jespad=jescifile.Get("jes")
	jes=jespad.GetListOfPrimitives()[j+1]
	for b in range(clone.GetNbinsX()):
	    jesup.SetBinContent(b+1,clone.GetBinContent(b+1)*jes.GetListOfPrimitives()[2].GetBinContent(b+1))
            jesdown.SetBinContent(b+1,clone.GetBinContent(b+1)*jes.GetListOfPrimitives()[4].GetBinContent(b+1))
	out.cd()
	for k in range(0,200):
            out.Delete(histname+"_jesUp"+";"+str(k))
            out.Delete(histname+"_jesDown"+";"+str(k))
        jesup.Write()
        jesdown.Write()
        histname=samples[i][0]+'_ALT#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        clone=alt.Clone(histname)
        clone=clone.Rebin(len(chi_binnings[j])-1,clone.GetName(),chi_binnings[j])
        jesup=clone.Clone(histname+"_jesUp")
        jesdown=clone.Clone(histname+"_jesDown")
        jespad=jesfile.Get("jes")
	jes=jespad.GetListOfPrimitives()[j+1]
	for b in range(clone.GetNbinsX()):
	    jesup.SetBinContent(b+1,clone.GetBinContent(b+1)*jes.GetListOfPrimitives()[2].GetBinContent(b+1))
            jesdown.SetBinContent(b+1,clone.GetBinContent(b+1)*jes.GetListOfPrimitives()[4].GetBinContent(b+1))
	out.cd()
	for k in range(0,200):
            out.Delete(histname+"_jesUp"+";"+str(k))
            out.Delete(histname+"_jesDown"+";"+str(k))
        jesup.Write()
        jesdown.Write()

        # NLO PDFup/down
        nloPDFupqcd=None
        for k in mass_bins_nlo_list[j]:
         histname='chi-'+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"PDFUp"
         print histname
         hnloPDFup = TH1F(nlofile3.Get(histname))
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
         hnloPDFdown = TH1F(nlofile3.Get(histname))
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
	out.cd()
	for k in range(0,200):
            out.Delete(qcd.GetName().replace("_backup","")+"_pdfUp"+";"+str(k))
            out.Delete(qcd.GetName().replace("_backup","")+"_pdfDown"+";"+str(k))
        pdfup.Write(qcd.GetName().replace("_backup","")+"_pdfUp")
        pdfdown.Write(qcd.GetName().replace("_backup","")+"_pdfDown")

        # NLO Scaleup/down
        nloScaleupqcd=None
        for k in mass_bins_nlo_list[j]:
         histname='chi-'+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"scaleUp"
         print histname
         hnloScaleup = TH1F(nlofile3.Get(histname))
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
         histname='chi-'+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"scaleDown"
         print histname
         hnloScaledown = TH1F(nlofile3.Get(histname))
         hnloScaledown.Scale(float(mass_bins_nlo3[k+1]-mass_bins_nlo3[k]))
         hnloScaledown=rebin(hnloScaledown,len(chi_binnings[j])-1,chi_binnings[j])
	 if nloScaledownqcd:
	    nloScaledownqcd.Add(hnloScaledown)
	 else:
	    nloScaledownqcd=hnloScaledown
        nloScaledownqcd.Add(nloqcdnorm,-1)
        nloScaledownqcd.Scale(1./nloqcdnorm.Integral())

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
	out.cd()
	for k in range(0,200):
            out.Delete(qcd.GetName().replace("_backup","")+"_scaleUp"+";"+str(k))
            out.Delete(qcd.GetName().replace("_backup","")+"_scaleDown"+";"+str(k))
        scaleup.Write(qcd.GetName().replace("_backup","")+"_scaleUp")
        scaledown.Write(qcd.GetName().replace("_backup","")+"_scaleDown")
	
	# DATA BLINDED
	#data=alt.Clone("data_blinded")
        #for b in range(data.GetXaxis().GetNbins()):
        #    data.SetBinError(b+1,sqrt(data.GetBinContent(b+1)))
        #out.cd()
      
	# FAKE SIGNAL
	#ci=alt.Clone("fake_signal")
        #out.cd()
      
        jerup.Divide(jerup,alt)
        jerdown.Divide(jerdown,alt)
        #unfoldup.Divide(unfoldup,alt)
        #unfolddown.Divide(unfolddown,alt)
        jesup.Divide(jesup,alt)
        jesdown.Divide(jesdown,alt)
        pdfup.Divide(pdfup,alt)
        pdfdown.Divide(pdfdown,alt)
        scaleup.Divide(scaleup,alt)
        scaledown.Divide(scaledown,alt)
        alt.Divide(alt,alt)
      
        # PLOTS
        canvas.cd(j+1)
        legend1=TLegend(0.5,0.6,0.9,0.90,(str(massbins[j][0])+"<m_{jj}<"+str(massbins[j][1])+" GeV").replace("6000<m_{jj}<13000","m_{jj}>6000"))
        legends+=[legend1]
        #legend1.AddEntry(data,"data","lpe")
	plots+=[alt]
        alt.GetXaxis().SetTitle("#chi_{dijet}")
        alt.GetYaxis().SetTitle("variation")
        alt.GetYaxis().SetTitleOffset(1.4)
        alt.GetXaxis().SetTitleOffset(0.8)
        alt.GetYaxis().SetTitleSize(0.05)
        alt.GetYaxis().SetLabelSize(0.04)
        alt.GetXaxis().SetTitleSize(0.05)
        alt.GetXaxis().SetLabelSize(0.04)
        alt.GetXaxis().SetTickLength(0.02)
	alt.SetLineColor(1)
	alt.SetTitle("")
        alt.Draw("he")
	alt.GetYaxis().SetRangeUser(0.8,1.3)
        legend1.AddEntry(alt,"QCD","l")
	plots+=[jerup]
	jerup.SetLineColor(3)
	jerup.SetLineStyle(2)
        jerup.Draw("hesame")
        legend1.AddEntry(jerup,"JER","l")
	plots+=[jerdown]
	jerdown.SetLineColor(3)
	jerdown.SetLineStyle(2)
        jerdown.Draw("hesame")
	#plots+=[unfoldup]
	#unfoldup.SetLineColor(8)
	#unfoldup.SetLineStyle(2)
        #unfoldup.Draw("hesame")
        #legend1.AddEntry(unfoldup,"Unfold","l")
	#plots+=[unfolddown]
	#unfolddown.SetLineColor(8)
	#unfolddown.SetLineStyle(3)
        #unfolddown.Draw("hesame")
	plots+=[jesup]
	jesup.SetLineColor(4)
	jesup.SetLineStyle(3)
        jesup.Draw("hesame")
        legend1.AddEntry(jesup,"JES","l")
	plots+=[jesdown]
	jesdown.SetLineColor(4)
	jesdown.SetLineStyle(3)
        jesdown.Draw("hesame")
	plots+=[pdfup]
	pdfup.SetLineColor(6)
	pdfup.SetLineStyle(4)
        pdfup.Draw("hesame")
        legend1.AddEntry(pdfup,"PDF","l")
	plots+=[pdfdown]
	pdfdown.SetLineColor(6)
	pdfdown.SetLineStyle(4)
        pdfdown.Draw("hesame")
	plots+=[scaleup]
	scaleup.SetLineColor(2)
	scaleup.SetLineStyle(5)
        scaleup.Draw("hesame")
        legend1.AddEntry(scaleup,"#mu scale","l")
	plots+=[scaledown]
	scaledown.SetLineColor(2)
	scaledown.SetLineStyle(5)
        scaledown.Draw("hesame")
	#plots+=[ci]
        #ci.Draw("hesame")
        #legend1.AddEntry(ci,"CI","l")
	data=TGraphAsymmErrors(data)
	plots+=[data]
	alpha=1.-0.6827
	for b in range(data.GetN()):
	    N=data.GetY()[b]
	    L=0
	    if N>0:
	      L=ROOT.Math.gamma_quantile(alpha/2.,N,1.)
            U=ROOT.Math.gamma_quantile_c(alpha/2.,N+1,1.)
            data.SetPointEYlow(b,N-L)
            data.SetPointEYhigh(b,U-N)
	data.SetLineColor(1)
	data.SetMarkerStyle(24)
        data.SetMarkerSize(0.5)
        #data.Draw("pe0zsame")
	
    	l5=TLegend(0.5,0.9,0.9,0.95,"CMS Simulation")
    	l5.SetTextSize(0.04)
    	l5.SetFillStyle(0)
    	l5.Draw("same")
	plots+=[l5]
    	 
        legend1.SetTextSize(0.04)
        legend1.SetFillStyle(0)
        legend1.Draw("same")

      canvas.SaveAs(prefix + "_"+samples[i][0] + '_sys_2016.pdf')
      canvas.SaveAs(prefix + "_"+samples[i][0] + '_sys_2016.eps')

      for closefile in closefiles:
          closefile.Close()
