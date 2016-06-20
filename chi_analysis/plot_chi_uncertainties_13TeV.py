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
 
    chi_bins=[(1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               #(1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,3,6,9,12,16),
              ]
    chi_binnings=[]
    for mass_bin in chi_bins:
        chi_binnings+=[array.array('d')]
        for chi_bin in mass_bin:
            chi_binnings[-1].append(chi_bin)
    massbins=[(1900,2400),
              (2400,3000),
	      (3000,3600),
	      (3600,4200),
	      (4200,4800),
	      (4800,13000),
	      #(5400,13000)
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
    mass_bins_nlo_list=[(2,),
    	      (3,),
    	      (4,),
    	      (5,),
    	      (6,),
	      (7,),
	      (8,),
    	     ]


    samples=[("QCD",[]),
             ]
 
    dataevents={}
    data={}
    for prefix in prefixs: 
     # signal cards
     for i in range(len(samples)):
      sample=prefix + "_"+samples[i][0] + '_chi.root'
      print sample
      out=TFile(sample,'UPDATE')

      closefiles=[]

      # LO QCD file
      sample2=prefix + '_GENv3_chi.root'
      print sample2
      in2=TFile(sample2,'READ')

      # data file
      insample='datacards/chi_EPS2.root'
      print insample
      infile=TFile(insample,'READ')

      # unfolded data file
      unfoldsample='datacards/Unfolded_chiNtuple_PFHT800_20160530_fromCB_AK4SF_DataToMCSF_Pythia_M_1000toInf.root '
      print unfoldsample
      unfoldfile=TFile(unfoldsample,'READ')
      unfoldsample2='datacards/Unfolded_chiNtuple_PFHT800_20160530_fromCB_AK4SF_DataToMCSF_Pythia_M_1000toInf.root '
      print unfoldsample2
      unfoldfile2=TFile(unfoldsample2,'READ')

      # NLO correction
      filename1nu2="fastnlo/RunII/fnl5662i_v23_fix_CT14_ak4.root"
      print filename1nu2
      nlofile2 = TFile.Open(filename1nu2)
      closefiles+=[nlofile2]

      # EWK correction
      filename1ewk="fastnlo/RunII/DijetAngularCMS13_ewk.root"
      print filename1ewk
      ewkfile = TFile.Open(filename1ewk)
      closefiles+=[ewkfile]

      # JES uncertainty QCD
      filename1jes="chi_systematic_plotschi_QCD4_13TeV.root"
      print filename1jes
      jesfile = TFile.Open(filename1jes)
      closefiles+=[jesfile]

      # JES uncertainty CI
      filename1jesci="chi_systematic_plotschi_QCD4_13TeV.root"
      print filename1jesci
      jescifile = TFile.Open(filename1jesci)
      closefiles+=[jescifile]

      canvas = TCanvas("","",0,0,600,400)
      canvas.Divide(3,2)
      plots=[]
      legends=[]

      for j in range(len(massbins)):
        # data
        histname="dijet_"+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"").replace("4200_4800","4200_13000").replace("4800_5400","4200_13000").replace("4800_13000","4200_13000").replace("13000","7000")+"_chi"
        print histname
	if useLensData:
  	  if "13000" in str(massbins[j]):
            histname2="dijet_m_chi_2__projY_"+str(massbins[j]).strip("()").replace(',',"-").replace(' ',"")
          else:
	    histname2="dijet_m_chi_2__projY_"+str(massbins[j]).strip("()").replace(',',"-").replace(' ',"")
          print histname2
  	  if "1900" in str(massbins[j]):
             data = TH1D(unfoldfile2.Get(histname2))
	  else:   
             data = TH1D(unfoldfile.Get(histname2))
	  data.SetName(histname)
	elif useUnfoldedData:
  	  if "13000" in str(massbins[j]):
            histname2="dijet_mass1_chi2__projY_"+str(massbins[j]).strip("()").replace(',',".0-").replace(' ',"")+".0_unfolded"
          else:
	    histname2="dijet_mass1_chi2__projY_"+str(massbins[j]).strip("()").replace(',',".0-").replace(' ',"")+".0_unfolded"
          print histname2
  	  if "1900" in str(massbins[j]):
             data = TH1F(unfoldfile2.Get(histname2))
	  else:   
             data = TH1F(unfoldfile.Get(histname2))
	  data.SetName(histname)
	else:
          data = TH1F(infile.Get(histname))
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
         hnlo=rebin(hnlo,len(chi_binnings[j])-1,chi_binnings[j])
	 if nloqcd:
	    nloqcd.Add(hnlo)
	 else:
	    nloqcd=hnlo
        for b in range(nloqcd.GetXaxis().GetNbins()):
           nloqcd.SetBinContent(b+1,nloqcd.GetBinContent(b+1)*nloqcd.GetBinWidth(b+1))
        nloqcdbackup=nloqcd.Clone(nloqcd.GetName()+"_backup")

        # EWK corrections
        histname='chi-'+str(massbins[j]).strip("()").replace(',',"-").replace(' ',"").replace("4800-13000","4800-5400").replace("4800-13000","4800-5400")
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
	if "LOCI" in samples[i][0]:
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
	slopes[1900]=0.01 
	slopes[2400]=0.01 
	slopes[3000]=0.02 
	slopes[3600]=0.03
	slopes[4200]=0.04
	slopes[4800]=0.05
	#slopes[5400]=0.15
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
        histname=samples[i][0]+'#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        clone=alt.Clone(histname)
        clone=clone.Rebin(len(chi_binnings[j])-1,clone.GetName(),chi_binnings[j])
	unfoldup=clone.Clone(histname+"_unfoldUp")
        unfolddown=clone.Clone(histname+"_unfoldDown")
	slopes={}
	slopes[1900]=0.08
	slopes[2400]=0.08
	slopes[3000]=0.08
	slopes[3600]=0.08
	slopes[4200]=0.08
	slopes[4800]=0.08
	slopes[5400]=0.08
	for b in range(clone.GetNbinsX()):
	    unfoldup.SetBinContent(b+1,clone.GetBinContent(b+1)*(1.-slopes[massbins[j][0]]/2.+abs(clone.GetBinCenter(b+1)-8.5)/7.5*slopes[massbins[j][0]]))
            unfolddown.SetBinContent(b+1,clone.GetBinContent(b+1)*(1.+slopes[massbins[j][0]]/2.-abs(clone.GetBinCenter(b+1)-8.5)/7.5*slopes[massbins[j][0]]))
	out.cd()
	for k in range(0,200):
            out.Delete(histname+"_unfoldUp"+";"+str(k))
            out.Delete(histname+"_unfoldDown"+";"+str(k))
        unfoldup.Write()
        unfolddown.Write()
        histname=samples[i][0]+'_ALT#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        clone=alt.Clone(histname)
        clone=clone.Rebin(len(chi_binnings[j])-1,clone.GetName(),chi_binnings[j])
        unfoldup=clone.Clone(histname+"_unfoldUp")
        unfolddown=clone.Clone(histname+"_unfoldDown")
	for b in range(clone.GetNbinsX()):
	    unfoldup.SetBinContent(b+1,clone.GetBinContent(b+1)*(1.-slopes[massbins[j][0]]/2.+abs(clone.GetBinCenter(b+1)-8.5)/7.5*slopes[massbins[j][0]]))
            unfolddown.SetBinContent(b+1,clone.GetBinContent(b+1)*(1.+slopes[massbins[j][0]]/2.-abs(clone.GetBinCenter(b+1)-8.5)/7.5*slopes[massbins[j][0]]))
	out.cd()
	for k in range(0,200):
            out.Delete(histname+"_unfoldUp"+";"+str(k))
            out.Delete(histname+"_unfoldDown"+";"+str(k))
        unfoldup.Write()
        unfolddown.Write()

        # jes uncertainty
        histname=samples[i][0]+'#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        clone=alt.Clone(histname)
        clone=clone.Rebin(len(chi_binnings[j])-1,clone.GetName(),chi_binnings[j])
        jesup=clone.Clone(histname+"_jesUp")
        jesdown=clone.Clone(histname+"_jesDown")
        jespad=jescifile.Get("jes")
	jes=jespad.GetListOfPrimitives()[j]
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
	jes=jespad.GetListOfPrimitives()[j]
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
         hnloPDFup = TH1F(nlofile2.Get(histname))
         hnloPDFup=rebin(hnloPDFup,len(chi_binnings[j])-1,chi_binnings[j])
	 if nloPDFupqcd:
	    nloPDFupqcd.Add(hnloPDFup)
	 else:
	    nloPDFupqcd=hnloPDFup
        for b in range(nloPDFupqcd.GetXaxis().GetNbins()):
           nloPDFupqcd.SetBinContent(b+1,nloPDFupqcd.GetBinContent(b+1)*nloPDFupqcd.GetBinWidth(b+1))
	nloPDFupqcd.Add(nloqcdbackup,-1)
	nloPDFupqcd.Scale(1./nloqcdbackup.Integral())

        nloPDFdownqcd=None
        for k in mass_bins_nlo_list[j]:
         histname='chi-'+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"PDFDown"
         print histname
         hnloPDFdown = TH1F(nlofile2.Get(histname))
         hnloPDFdown=rebin(hnloPDFdown,len(chi_binnings[j])-1,chi_binnings[j])
	 if nloPDFdownqcd:
	    nloPDFdownqcd.Add(hnloPDFdown)
	 else:
	    nloPDFdownqcd=hnloPDFdown
        for b in range(nloPDFdownqcd.GetXaxis().GetNbins()):
           nloPDFdownqcd.SetBinContent(b+1,nloPDFdownqcd.GetBinContent(b+1)*nloPDFdownqcd.GetBinWidth(b+1))
	nloPDFdownqcd.Add(nloqcdbackup,-1)
	nloPDFdownqcd.Scale(1./nloqcdbackup.Integral())

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
            out.Delete(alt.GetName()+"_pdfUp"+";"+str(k))
            out.Delete(alt.GetName()+"_pdfDown"+";"+str(k))
        pdfup.Write()
        pdfdown.Write()
        if samples[i][0]=="QCD":
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
         hnloScaleup = TH1F(nlofile2.Get(histname))
         hnloScaleup=rebin(hnloScaleup,len(chi_binnings[j])-1,chi_binnings[j])
	 if nloScaleupqcd:
	    nloScaleupqcd.Add(hnloScaleup)
	 else:
	    nloScaleupqcd=hnloScaleup
        for b in range(nloScaleupqcd.GetXaxis().GetNbins()):
           nloScaleupqcd.SetBinContent(b+1,nloScaleupqcd.GetBinContent(b+1)*nloScaleupqcd.GetBinWidth(b+1))
	nloScaleupqcd.Add(nloqcdbackup,-1)
	nloScaleupqcd.Scale(1./nloqcdbackup.Integral())

        nloScaledownqcd=None
        for k in mass_bins_nlo_list[j]:
         histname='chi-'+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"scaleDown"
         print histname
         hnloScaledown = TH1F(nlofile2.Get(histname))
         hnloScaledown=rebin(hnloScaledown,len(chi_binnings[j])-1,chi_binnings[j])
	 if nloScaledownqcd:
	    nloScaledownqcd.Add(hnloScaledown)
	 else:
	    nloScaledownqcd=hnloScaledown
        for b in range(nloScaledownqcd.GetXaxis().GetNbins()):
           nloScaledownqcd.SetBinContent(b+1,nloScaledownqcd.GetBinContent(b+1)*nloScaledownqcd.GetBinWidth(b+1))
	nloScaledownqcd.Add(nloqcdbackup,-1)
	nloScaledownqcd.Scale(1./nloqcdbackup.Integral())

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
            out.Delete(alt.GetName()+"_scaleUp"+";"+str(k))
            out.Delete(alt.GetName()+"_scaleDown"+";"+str(k))
        scaleup.Write()
        scaledown.Write()
        if samples[i][0]=="QCD":
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
        unfoldup.Divide(unfoldup,alt)
        unfolddown.Divide(unfolddown,alt)
        jesup.Divide(jesup,alt)
        jesdown.Divide(jesdown,alt)
        pdfup.Divide(pdfup,alt)
        pdfdown.Divide(pdfdown,alt)
        scaleup.Divide(scaleup,alt)
        scaledown.Divide(scaledown,alt)
        alt.Divide(alt,alt)
      
        # PLOTS
        canvas.cd(j+1)
        legend1=TLegend(0.5,0.6,0.9,0.90,(str(massbins[j][0])+"<m_{jj}<"+str(massbins[j][1])+" GeV").replace("4200<m_{jj}<7000","m_{jj}>4200").replace("4200<m_{jj}<8000","m_{jj}>4200"))
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

      canvas.SaveAs(prefix + "_"+samples[i][0] + '_sys.pdf')
      canvas.SaveAs(prefix + "_"+samples[i][0] + '_sys.eps')

      for closefile in closefiles:
          closefile.Close()
