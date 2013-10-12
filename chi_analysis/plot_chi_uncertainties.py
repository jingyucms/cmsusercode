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

    prefixs=["datacard_shapelimit"]
 
    chi_bins=[(1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,3,5,7,10,12,14,16),
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
	      (4200,8000)]
    mass_bins_nlo={}
    mass_bins_nlo[2]=1900
    mass_bins_nlo[3]=2400
    mass_bins_nlo[4]=3000
    mass_bins_nlo[5]=3600
    mass_bins_nlo[6]=4000
    mass_bins_nlo[7]=4200
    mass_bins_nlo[8]=8000
    mass_bins_nlo2=[(2,),
    	      (3,),
    	      (4,),
    	      (5,6,),
    	      (7,),
    	     ]
    mass_bins_nlo_max=7


    samples=[("QCD",[]),
             ]
 
    dataevents={}
    data={}
    for prefix in prefixs: 
     ## data cards
     #sample=prefix + '_data_obs_chi.root'
     #print sample
     #out=TFile(sample,'RECREATE')

     # signal cards
     for i in range(len(samples)):
      sample=prefix + "_"+samples[i][0] + '_chi.root'
      print sample
      out=TFile(sample,'UPDATE')

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

      canvas = TCanvas("","",0,0,600,400)
      canvas.Divide(3,2)
      plots=[]
      legends=[]

      for j in range(len(massbins)):
        # data
        histname="dijet_"+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"").replace("8000","7000")+"_chi"
        print histname
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
        f=file("xsecs.txt")
        crosssections=eval(f.readline())
        xsec_qcd=1
        for xsec in crosssections:
          if xsec[0]=="QCD" and massbins[j] in xsec[1]:
              xsec_qcd=float(xsec[2])
	qcd.Scale(1e10*xsec_qcd)
	print "k-factor", nloqcdbackup.Integral()/qcd.Integral()

        # CI (=LO CI+NLO QCD)
	histname=samples[i][0]+'#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1_backup"
        print histname
	if "LOCI" in samples[i][0]:
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
          histname2="chi-"+str(massbins[j][0])+"-"+str(massbins[j][1])
          print histname2
  	  histname=histname.replace("_backup","")
          ci = TH1F(cinlofile.Get(histname2))
          ci=ci.Rebin(len(chi_binnings[j])-1,ci.GetName()+"_rebin1",chi_binnings[j]).Clone(histname)
	  ci.Scale(1./nloqcdbackup.Integral())
	  if "QCDADLO" in samples[i][0]:
	    ci.Scale(-1)
          ci.Add(nloqcd)
	else:
          cibackup=out.Get(histname)
  	  histname=cibackup.GetName().replace("_backup","")
          ci=cibackup.Clone(histname)
	  # properly normalize LO QCD+CI and LO QCD before substracting LO QCD
	  xsec_ci=0
	  for xsec in crosssections:
	    if xsec[0]==samples[i][0] and massbins[j] in xsec[1]:
	        xsec_ci=float(xsec[2])
	  ci.Scale(xsec_ci)
          ci.Add(qcd,-1)
	  ci.Scale(1./qcd.Integral())
          ci.Add(nloqcd)
	if ci.Integral()>0:
          ci.Scale(dataevents[j]/ci.Integral())
        for b in range(ci.GetXaxis().GetNbins()):
            ci.SetBinError(b+1,0)
        out.cd()
	for k in range(0,200):
            out.Delete(histname+";"+str(k))
        ci.Write()

        # ALT (=NLO QCD)
        histname=samples[i][0]+'#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print histname
	if "LOCI" in samples[i][0]:
    	    alt=nloqcd.Clone(histname)
	else:
            alt=out.Get(histname)
        alt.Add(alt,-1)
        alt.Add(nloqcd)
        alt.Scale(dataevents[j]/alt.Integral())
        for b in range(alt.GetXaxis().GetNbins()):
            alt.SetBinError(b+1,0)
        out.cd()
	for k in range(0,200):
            out.Delete(histname+";"+str(k))
        alt.Write(histname)
	
        # JER uncertainty
        histname=samples[i][0]+'#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
	if "LOCI" in samples[i][0]:
    	    clone=ci.Clone(histname)
	else:
            clone=out.Get(histname)
	jerup=clone.Clone(histname+"_jerUp")
        jerdown=clone.Clone(histname+"_jerDown")
	slopes={}
	slopes[1900]=0.05
	slopes[2400]=0.05
	slopes[3000]=0.05
	slopes[3600]=0.05
	slopes[4200]=0.05
	for b in range(clone.GetNbinsX()):
	    jerup.SetBinContent(b+1,clone.GetBinContent(b+1)*(1.+(clone.GetBinCenter(b+1)-8.5)/7.5*slopes[massbins[j][0]]))
            jerdown.SetBinContent(b+1,clone.GetBinContent(b+1)*(1.-(clone.GetBinCenter(b+1)-8.5)/7.5*slopes[massbins[j][0]]))
	out.cd()
	for k in range(0,200):
            out.Delete(histname+"_jerUp"+";"+str(k))
            out.Delete(histname+"_jerDown"+";"+str(k))
        jerup.Write()
        jerdown.Write()
        #histname=samples[i][0]+'_ALT#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
	#if "LOCI" in samples[i][0]:
    	#    clone=alt.Clone(histname)
	#else:
        #    clone=out.Get(histname)
        #jerup=clone.Clone(histname+"_jerUp")
        #jerdown=clone.Clone(histname+"_jerDown")
	#for b in range(clone.GetNbinsX()):
	#    jerup.SetBinContent(b+1,clone.GetBinContent(b+1)*(1.+(clone.GetBinCenter(b+1)-8.5)/7.5*slopes[massbins[j][0]]))
        #    jerdown.SetBinContent(b+1,clone.GetBinContent(b+1)*(1.-(clone.GetBinCenter(b+1)-8.5)/7.5*slopes[massbins[j][0]]))
	#out.cd()
	#for k in range(0,200):
        #    out.Delete(histname+"_jerUp"+";"+str(k))
        #    out.Delete(histname+"_jerDown"+";"+str(k))
        #jerup.Write()
        #jerdown.Write()

        # jes uncertainty
        histname=samples[i][0]+'#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
	if "LOCI" in samples[i][0]:
    	    clone=ci.Clone(histname)
	else:
            clone=out.Get(histname)
        jesup=clone.Clone(histname+"_jesUp")
        jesdown=clone.Clone(histname+"_jesDown")
        jespad=jescifile.Get("jes")
	jes=jespad.GetListOfPrimitives()[-len(massbins)-1+j]
	for b in range(clone.GetNbinsX()):
	    jesup.SetBinContent(b+1,clone.GetBinContent(b+1)*jes.GetListOfPrimitives()[2].GetBinContent(b+1))
            jesdown.SetBinContent(b+1,clone.GetBinContent(b+1)*jes.GetListOfPrimitives()[4].GetBinContent(b+1))
	out.cd()
	for k in range(0,200):
            out.Delete(histname+"_jesUp"+";"+str(k))
            out.Delete(histname+"_jesDown"+";"+str(k))
        jesup.Write()
        jesdown.Write()
        #histname=samples[i][0]+'_ALT#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
	#if "LOCI" in samples[i][0]:
    	#    clone=alt.Clone(histname)
	#else:
        #    clone=out.Get(histname)
        #jesup=clone.Clone(histname+"_jesUp")
        #jesdown=clone.Clone(histname+"_jesDown")
        #jespad=jesfile.Get("jes")
	#jes=jespad.GetListOfPrimitives()[-len(massbins)-1+j]
	#for b in range(clone.GetNbinsX()):
	#    jesup.SetBinContent(b+1,clone.GetBinContent(b+1)*jes.GetListOfPrimitives()[2].GetBinContent(b+1))
        #    jesdown.SetBinContent(b+1,clone.GetBinContent(b+1)*jes.GetListOfPrimitives()[4].GetBinContent(b+1))
	#out.cd()
	#for k in range(0,200):
        #    out.Delete(histname+"_jesUp"+";"+str(k))
        #    out.Delete(histname+"_jesDown"+";"+str(k))
        #jesup.Write()
        #jesdown.Write()

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
	out.cd()
	for k in range(0,200):
            out.Delete(alt.GetName()+"_pdfUp"+";"+str(k))
            out.Delete(alt.GetName()+"_pdfDown"+";"+str(k))
        pdfup.Write()
        pdfdown.Write()

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
	out.cd()
	for k in range(0,200):
            out.Delete(alt.GetName()+"_scaleUp"+";"+str(k))
            out.Delete(alt.GetName()+"_scaleDown"+";"+str(k))
        scaleup.Write()
        scaledown.Write()

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
      
        jerup.Divide(jerup,alt)
        jerdown.Divide(jerdown,alt)
        jesup.Divide(jesup,alt)
        jesdown.Divide(jesdown,alt)
        pdfup.Divide(pdfup,alt)
        pdfdown.Divide(pdfdown,alt)
        scaleup.Divide(scaleup,alt)
        scaledown.Divide(scaledown,alt)
        alt.Divide(alt,alt)
      
        # PLOTS
        canvas.cd(j+1)
        legend1=TLegend(0.5,0.6,0.9,0.95,(str(massbins[j][0])+"<m_{jj}<"+str(massbins[j][1])+" GeV").replace("4200<m_{jj}<7000","m_{jj}>4200").replace("4200<m_{jj}<8000","m_{jj}>4200"))
        legends+=[legend1]
        #legend1.AddEntry(data,"data","lpe")
	plots+=[alt]
	alt.SetLineColor(2)
	alt.SetTitle("")
        alt.Draw("he")
	alt.GetYaxis().SetRangeUser(0.8,1.3)
        legend1.AddEntry(alt,"QCD","l")
	plots+=[jerup]
	jerup.SetLineColor(3)
	jerup.SetLineStyle(2)
        jerup.Draw("hesame")
        legend1.AddEntry(jerup,"JER up","l")
	plots+=[jerdown]
	jerdown.SetLineColor(3)
	jerdown.SetLineStyle(3)
        jerdown.Draw("hesame")
        legend1.AddEntry(jerdown,"JER down","l")
	plots+=[jesup]
	jesup.SetLineColor(4)
	jesup.SetLineStyle(2)
        jesup.Draw("hesame")
        legend1.AddEntry(jesup,"JES up","l")
	plots+=[jesdown]
	jesdown.SetLineColor(4)
	jesdown.SetLineStyle(3)
        jesdown.Draw("hesame")
        legend1.AddEntry(jesdown,"JES down","l")
	plots+=[pdfup]
	pdfup.SetLineColor(6)
	pdfup.SetLineStyle(2)
        pdfup.Draw("hesame")
        legend1.AddEntry(pdfup,"PDF up","l")
	plots+=[pdfdown]
	pdfdown.SetLineColor(6)
	pdfdown.SetLineStyle(3)
        pdfdown.Draw("hesame")
        legend1.AddEntry(pdfdown,"PDF down","l")
	plots+=[scaleup]
	scaleup.SetLineColor(7)
	scaleup.SetLineStyle(2)
        scaleup.Draw("hesame")
        legend1.AddEntry(scaleup,"scale up","l")
	plots+=[scaledown]
	scaledown.SetLineColor(7)
	scaledown.SetLineStyle(3)
        scaledown.Draw("hesame")
        legend1.AddEntry(scaledown,"scale down","l")
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
	
        legend1.SetTextSize(0.04)
        legend1.SetFillStyle(0)
        legend1.Draw("same")

      canvas.SaveAs(prefix + "_"+samples[i][0] + '_sys.pdf')
      canvas.SaveAs(prefix + "_"+samples[i][0] + '_sys.eps')
