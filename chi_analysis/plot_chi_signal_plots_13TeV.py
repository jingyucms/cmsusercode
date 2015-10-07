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

    prefix="datacard_shapelimit13TeV"

    colors=[2,3,4,6,7,8,9,11,12,13]
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
	      (4200,13000)]
    mass_bins_nlo3={}
    #mass_bins_nlo3[2]=1900
    #mass_bins_nlo3[3]=2400
    #mass_bins_nlo3[4]=3000
    mass_bins_nlo3[5]=3600
    mass_bins_nlo3[6]=4200
    mass_bins_nlo3[7]=4800
    mass_bins_nlo3[8]=5400
    mass_bins_nlo3[9]=6000
    mass_bins_nlo_list=[#(2,),
    	      #(3,),
    	      #(4,),
    	      (5,),
    	      (6,7,8,),
    	     ]
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

    samples=[[("QCDCIplusLL8000",[("pythia8_ci_m1500_1900_8000_1_0_0_13TeV_Oct1",3.307e-06),
		       ("pythia8_ci_m1900_2400_8000_1_0_0_13TeV_Oct1",8.836e-07),
		       ("pythia8_ci_m2400_2800_8000_1_0_0_13TeV_Oct1",1.649e-07),
		       ("pythia8_ci_m2800_3300_8000_1_0_0_13TeV_Oct1",6.446e-08),
		       ("pythia8_ci_m3300_3800_8000_1_0_0_13TeV_Oct1",1.863e-08),
		       ("pythia8_ci_m3800_4300_8000_1_0_0_13TeV_Oct1",5.867e-09),
		       ("pythia8_ci_m4300_13000_8000_1_0_0_13TeV_Oct1",3.507e-09),
		       ]),
             ("QCDCIplusLL9000",[("pythia8_ci_m1500_1900_9000_1_0_0_13TeV_Oct1",3.307e-06),
		       ("pythia8_ci_m1900_2400_9000_1_0_0_13TeV_Oct1",8.836e-07),
		       ("pythia8_ci_m2400_2800_9000_1_0_0_13TeV_Oct1",1.649e-07),
		       ("pythia8_ci_m2800_3300_9000_1_0_0_13TeV_Oct1",6.446e-08),
		       ("pythia8_ci_m3300_3800_9000_1_0_0_13TeV_Oct1",1.863e-08),
		       ("pythia8_ci_m3800_4300_9000_1_0_0_13TeV_Oct1",5.867e-09),
		       ("pythia8_ci_m4300_13000_9000_1_0_0_13TeV_Oct1",3.507e-09),
		       ]),
             ("QCDCIplusLL10000",[("pythia8_ci_m1500_1900_10000_1_0_0_13TeV_Oct1",3.307e-06),
		       ("pythia8_ci_m1900_2400_10000_1_0_0_13TeV_Oct1",8.836e-07),
		       ("pythia8_ci_m2400_2800_10000_1_0_0_13TeV_Oct1",1.649e-07),
		       ("pythia8_ci_m2800_3300_10000_1_0_0_13TeV_Oct1",6.446e-08),
		       ("pythia8_ci_m3300_3800_10000_1_0_0_13TeV_Oct1",1.863e-08),
		       ("pythia8_ci_m3800_4300_10000_1_0_0_13TeV_Oct1",5.867e-09),
		       ("pythia8_ci_m4300_13000_10000_1_0_0_13TeV_Oct1",3.507e-09),
		       ]),
             ("QCDCIplusLL11000",[("pythia8_ci_m1500_1900_11000_1_0_0_13TeV_Oct1",3.307e-06),
		       ("pythia8_ci_m1900_2400_11000_1_0_0_13TeV_Oct1",8.836e-07),
		       ("pythia8_ci_m2400_2800_11000_1_0_0_13TeV_Oct1",1.649e-07),
		       ("pythia8_ci_m2800_3300_11000_1_0_0_13TeV_Oct1",6.446e-08),
		       ("pythia8_ci_m3300_3800_11000_1_0_0_13TeV_Oct1",1.863e-08),
		       ("pythia8_ci_m3800_4300_11000_1_0_0_13TeV_Oct1",5.867e-09),
		       ("pythia8_ci_m4300_13000_11000_1_0_0_13TeV_Oct1",3.507e-09),
		       ]),
             ("QCDCIplusLL12000",[("pythia8_ci_m1500_1900_12000_1_0_0_13TeV_Oct1",3.307e-06),
		       ("pythia8_ci_m1900_2400_12000_1_0_0_13TeV_Oct1",8.836e-07),
		       ("pythia8_ci_m2400_2800_12000_1_0_0_13TeV_Oct1",1.649e-07),
		       ("pythia8_ci_m2800_3300_12000_1_0_0_13TeV_Oct1",6.446e-08),
		       ("pythia8_ci_m3300_3800_12000_1_0_0_13TeV_Oct1",1.863e-08),
		       ("pythia8_ci_m3800_4300_12000_1_0_0_13TeV_Oct1",5.867e-09),
		       ("pythia8_ci_m4300_13000_12000_1_0_0_13TeV_Oct1",3.507e-09),
		       ]),
             ("QCDCIplusLL13000",[("pythia8_ci_m1500_1900_13000_1_0_0_13TeV_Oct1",3.307e-06),
		       ("pythia8_ci_m1900_2400_13000_1_0_0_13TeV_Oct1",8.836e-07),
		       ("pythia8_ci_m2400_2800_13000_1_0_0_13TeV_Oct1",1.649e-07),
		       ("pythia8_ci_m2800_3300_13000_1_0_0_13TeV_Oct1",6.446e-08),
		       ("pythia8_ci_m3300_3800_13000_1_0_0_13TeV_Oct1",1.863e-08),
		       ("pythia8_ci_m3800_4300_13000_1_0_0_13TeV_Oct1",5.867e-09),
		       ("pythia8_ci_m4300_13000_13000_1_0_0_13TeV_Oct1",3.507e-09),
		       ]),
             ("QCDCIplusLL14000",[("pythia8_ci_m1500_1900_14000_1_0_0_13TeV_Oct1",3.307e-06),
		       ("pythia8_ci_m1900_2400_14000_1_0_0_13TeV_Oct1",8.836e-07),
		       ("pythia8_ci_m2400_2800_14000_1_0_0_13TeV_Oct1",1.649e-07),
		       ("pythia8_ci_m2800_3300_14000_1_0_0_13TeV_Oct1",6.446e-08),
		       ("pythia8_ci_m3300_3800_14000_1_0_0_13TeV_Oct1",1.863e-08),
		       ("pythia8_ci_m3800_4300_14000_1_0_0_13TeV_Oct1",5.867e-09),
		       ("pythia8_ci_m4300_13000_14000_1_0_0_13TeV_Oct1",3.507e-09),
		       ]),
             ("QCDCIplusLL16000",[("pythia8_ci_m1500_1900_16000_1_0_0_13TeV_Oct1",3.307e-06),
		       ("pythia8_ci_m1900_2400_16000_1_0_0_13TeV_Oct1",8.836e-07),
		       ("pythia8_ci_m2400_2800_16000_1_0_0_13TeV_Oct1",1.649e-07),
		       ("pythia8_ci_m2800_3300_16000_1_0_0_13TeV_Oct1",6.446e-08),
		       ("pythia8_ci_m3300_3800_16000_1_0_0_13TeV_Oct1",1.863e-08),
		       ("pythia8_ci_m3800_4300_16000_1_0_0_13TeV_Oct1",5.867e-09),
		       ("pythia8_ci_m4300_13000_16000_1_0_0_13TeV_Oct1",3.507e-09),
		       ]),
             ("QCDCIplusLL18000",[("pythia8_ci_m1500_1900_18000_1_0_0_13TeV_Oct1",3.307e-06),
		       ("pythia8_ci_m1900_2400_18000_1_0_0_13TeV_Oct1",8.836e-07),
		       ("pythia8_ci_m2400_2800_18000_1_0_0_13TeV_Oct1",1.649e-07),
		       ("pythia8_ci_m2800_3300_18000_1_0_0_13TeV_Oct1",6.446e-08),
		       ("pythia8_ci_m3300_3800_18000_1_0_0_13TeV_Oct1",1.863e-08),
		       ("pythia8_ci_m3800_4300_18000_1_0_0_13TeV_Oct1",5.867e-09),
		       ("pythia8_ci_m4300_13000_18000_1_0_0_13TeV_Oct1",3.507e-09),
		       ]),
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
        legend1=TLegend(0.4,0.6,0.9,0.95,(str(massbins[j][0])+"<m_{jj}<"+str(massbins[j][1])+" GeV").replace("4200<m_{jj}<7000","m_{jj}>4200").replace("4200<m_{jj}<13000","m_{jj}>4200"))
        legends[j]=legend1

     files=[]

     for l in range(len(samples[i])):
      sample=prefix + '_GEN_chi.root'
      print sample
      out=TFile(sample,'READ')
      files+=[out]
      closefiles=[]

      # data file
      insample='datacards/chi_EPS2.root'
      print insample
      infile=TFile(insample,'READ')

      # NLO correction
      filename1nu2="fastnlo/RunII/fnl5622i_v23.root"
      print filename1nu2
      nlofile2 = TFile.Open(filename1nu2)
      closefiles+=[nlofile2]
      filename1nu="fastnlo/fnl3622g_ct10-nlo_aspdf.root"
      print filename1nu
      nlofile = TFile.Open(filename1nu)
      closefiles+=[nlofile]

      # EWK correction
      filename1ewk="fastnlo/DijetAngularCMS-CT10nlo-8TeV_R0.5_MassBin_AllChiBins.root"
      print filename1ewk
      ewkfile = TFile.Open(filename1ewk)
      closefiles+=[ewkfile]

      # JES uncertainty QCD
      filename1jes="datacards/chi_systematic_plotschi_QCD4.root"
      print filename1jes
      jesfile = TFile.Open(filename1jes)
      closefiles+=[jesfile]

      # JES uncertainty CI
      filename1jesci="datacards/chi_systematic_plotschi_CI4.root"
      print filename1jesci
      jescifile = TFile.Open(filename1jesci)
      closefiles+=[jescifile]

      for j in range(len(massbins)):
        # data
        histname="dijet_"+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"").replace("13000","7000")+"_chi"
        print histname
        data = TH1F(infile.Get(histname))
        data=data.Rebin(len(chi_binnings[j])-1,data.GetName()+"_rebin1",chi_binnings[j])
	dataevents[j]=data.Integral()

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
        nloqcdbackup=nloqcd.Clone(nloqcd.GetName()+"_backup")

        # EWK corrections
        histname='chi-'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"").replace('_',"-").replace("13000","8000")
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
        qcd=out.Get(histname)
        qcd=qcd.Rebin(len(chi_binnings[j])-1,qcd.GetName(),chi_binnings[j])
	qcd.Scale(1e10)
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

     for closefile in closefiles:
          closefile.Close()
