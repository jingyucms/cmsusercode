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
 
    chi_bins=[#(1,2,3,4,5,6,7,8,9,10,12,14,16),
               #(1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,2,3,4,5,6,7,8,9,10,12,14,16),
               (1,3,5,7,10,12,14,16),
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
	      (3000,3600),
	      (3600,4200),
	      (4200,8000)]

    samples=[("QCDCI4000",[("fileList_pythia8_ci_m2500_4000_1_0_0_May27_grid.txt",[(3000,3600),(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_4000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI6000",[("fileList_pythia8_ci_m2500_6000_1_0_0_May27_grid.txt",[(3000,3600),(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_6000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI8000",[("fileList_pythia8_ci_m2500_8000_1_0_0_May27_grid.txt",[(3000,3600),(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_8000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI10000",[("fileList_pythia8_ci_m2500_10000_1_0_0_May27_grid.txt",[(3000,3600),(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_10000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI12000",[("fileList_pythia8_ci_m2500_12000_1_0_0_May27_grid.txt",[(3000,3600),(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_12000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI14000",[("fileList_pythia8_ci_m2500_14000_1_0_0_May27_grid.txt",[(3000,3600),(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_14000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI15000",[("fileList_pythia8_ci_m2500_15000_1_0_0_May27_grid.txt",[(3000,3600),(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_15000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI16000",[("fileList_pythia8_ci_m2500_16000_1_0_0_May27_grid.txt",[(3000,3600),(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_16000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI18000",[("fileList_pythia8_ci_m2500_18000_1_0_0_May27_grid.txt",[(3000,3600),(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_18000_1_0_0_May27_grid.txt",[(4200,8000)])]),
             ("QCDCI20000",[("fileList_pythia8_ci_m2500_20000_1_0_0_May27_grid.txt",[(3000,3600),(3600,4200)]),
		        ("fileList_pythia8_ci_m3700_20000_1_0_0_May27_grid.txt",[(4200,8000)])]),
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
      sample=prefix + "_"+samples[i][0].replace("QCDCI","CI") + '_chi.root'
      print sample
      out=TFile(sample,'UPDATE')

      insample='chi_Moriond.root'
      print insample
      infile=TFile(insample,'READ')

      # NLO correction
      mass_bins_nlo={}
      mass_bins_nlo[4]=3000
      mass_bins_nlo[5]=3600
      mass_bins_nlo[6]=4000
      mass_bins_nlo[7]=4200
      mass_bins_nlo[8]=8000
      mass_bins_nlo2=[(4,),
                (5,6,),
                (7,),
               ]
      mass_bins_nlo_max=7
      filename1nu="fastnlo/fnl3622g_ct10-nlo_aspdf.root"
      print filename1nu
      nlofile = TFile.Open(filename1nu)

      canvas = TCanvas("","",0,0,600,200)
      canvas.Divide(3,1)
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
	data.Write('data_obs#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1")

        # NLO
        nloqcd=None
        for k in mass_bins_nlo2[j]:
         histname="h10"
         if k+mass_bins_nlo_max<10: histname+="0"
         histname+=str(k+mass_bins_nlo_max)+"00"
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
	nloqcd.Scale(1./nloqcd.Integral())

        # QCD (empty background, not used in limit)
        histname='QCD#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print histname
        qcd=out.Get(histname)
	qcd.Scale(1e10)

        # CI (=LO CI+NLO QCD)
	histname=samples[i][0]+'#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1_backup"
        print histname
        cibackup=out.Get(histname)
	histname=cibackup.GetName().replace("_backup","")
        ci=cibackup.Clone(histname)
	# properly normalize LO QCD+CI and LO QCD before substracting LO QCD
	f=file("xsecs.txt")
	crosssections=eval(f.readline())
	xsec_qcd=1
	xsec_ci=1
	for xsec in crosssections:
	    if xsec[0]=="QCD" and massbins[j] in xsec[1]:
	        xsec_qcd=float(xsec[2])
	    if xsec[0]==samples[i][0] and massbins[j] in xsec[1]:
	        xsec_ci=float(xsec[2])
	ci.Scale(xsec_ci/xsec_qcd)
        ci.Add(qcd,-1)
	ci.Scale(1./qcd.Integral())
        ci.Add(nloqcd)
	ci.Scale(dataevents[j]/ci.Integral())
        for b in range(ci.GetXaxis().GetNbins()):
            ci.SetBinError(b+1,0)
        out.cd()
	for k in range(0,100):
            out.Delete(histname+";"+str(k))
        ci.Write()

        # ALT (=NLO QCD)
        histname=samples[i][0]+'_ALT#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
        print histname
        alt=out.Get(histname)
        alt.Add(alt,-1)
        alt.Add(nloqcd)
	alt.Scale(dataevents[j]/alt.Integral())
        for b in range(alt.GetXaxis().GetNbins()):
            alt.SetBinError(b+1,0)
        out.cd()
	for k in range(0,100):
            out.Delete(histname+";"+str(k))
        alt.Write(histname)
	
        # jes uncertainty
        histname=samples[i][0]+'#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
	clone=out.Get(histname)
        jesup=clone.Clone(histname+"_jesUp")
        jesdown=clone.Clone(histname+"_jesDown")
	for b in range(clone.GetNbinsX()):
	    jesup.SetBinContent(b+1,clone.GetBinContent(b+1)*(1+(8.5-clone.GetBinCenter(b+1))/7.5*0.1))
            jesdown.SetBinContent(b+1,clone.GetBinContent(b+1)*(1-(8.5-clone.GetBinCenter(b+1))/7.5*0.1))
	out.cd()
	for k in range(0,100):
            out.Delete(histname+"_jesUp"+";"+str(k))
            out.Delete(histname+"_jesDown"+";"+str(k))
        jesup.Write()
        jesdown.Write()
        histname=samples[i][0]+'_ALT#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"
	clone=out.Get(histname)
        jesup=clone.Clone(histname+"_jesUp")
        jesdown=clone.Clone(histname+"_jesDown")
	for b in range(clone.GetNbinsX()):
	    jesup.SetBinContent(b+1,clone.GetBinContent(b+1)*(1+(8.5-clone.GetBinCenter(b+1))/7.5*0.1))
            jesdown.SetBinContent(b+1,clone.GetBinContent(b+1)*(1-(8.5-clone.GetBinCenter(b+1))/7.5*0.1))
	out.cd()
	for k in range(0,100):
            out.Delete(histname+"_jesUp"+";"+str(k))
            out.Delete(histname+"_jesDown"+";"+str(k))
        jesup.Write()
        jesdown.Write()

        # NLO PDFup
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

        pdfup=alt.Clone(alt.GetName()+"_pdfUp")
	pdfup.Add(nloPDFupqcd,dataevents[j])
        for b in range(pdfup.GetXaxis().GetNbins()):
            pdfup.SetBinError(b+1,0)
	out.cd()
	for k in range(0,100):
            out.Delete(alt.GetName()+"_pdfUp"+";"+str(k))
        pdfup.Write()

        # NLO PDFdown
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

        pdfdown=alt.Clone(alt.GetName()+"_pdfDown")
	pdfdown.Add(nloPDFdownqcd,dataevents[j])
        for b in range(pdfdown.GetXaxis().GetNbins()):
            pdfdown.SetBinError(b+1,0)
	out.cd()
	for k in range(0,100):
            out.Delete(alt.GetName()+"_pdfDown"+";"+str(k))
        pdfdown.Write()

        # NLO Scaleup
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

        scaleup=alt.Clone(alt.GetName()+"_scaleUp")
	scaleup.Add(nloScaleupqcd,dataevents[j])
        for b in range(scaleup.GetXaxis().GetNbins()):
            scaleup.SetBinError(b+1,0)
	out.cd()
	for k in range(0,100):
            out.Delete(alt.GetName()+"_scaleUp"+";"+str(k))
        scaleup.Write()

        # NLO Scaledown
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

        scaledown=alt.Clone(alt.GetName()+"_scaleDown")
	scaledown.Add(nloScaledownqcd,dataevents[j])
        for b in range(scaledown.GetXaxis().GetNbins()):
            scaledown.SetBinError(b+1,0)
	out.cd()
	for k in range(0,100):
            out.Delete(alt.GetName()+"_scaleDown"+";"+str(k))
        scaledown.Write()

	# DATA BLINDED
	#data=alt.Clone("data_blinded")
        #for b in range(data.GetXaxis().GetNbins()):
        #    data.SetBinError(b+1,sqrt(data.GetBinContent(b+1)))
        #out.cd()
	#for k in range(0,100):
        #    out.Delete('data_obs#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"+";"+str(k))
	#data.Write('data_obs#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1")
      
	# FAKE SIGNAL
	#ci=alt.Clone("fake_signal")
        #out.cd()
	#for k in range(0,100):
        #    out.Delete(samples[i][0]+'chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1"+";"+str(k))
	#ci.Write(samples[i][0]+'#chi'+str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1")
      
        # PLOTS
        canvas.cd(j+1)
        legend1=TLegend(0.2,0.6,0.9,0.95,"")
        legends+=[legend1]
        legend1.AddEntry(data,"data","lpe")
	plots+=[alt]
	alt.SetLineColor(2)
        alt.Draw("he")
	alt.GetYaxis().SetRangeUser(0,alt.GetMaximum()*2)
        legend1.AddEntry(alt,"QCD","l")
	plots+=[jesup]
	jesup.SetLineColor(3)
	jesup.SetLineStyle(2)
        jesup.Draw("hesame")
        legend1.AddEntry(jesup,"JES up","l")
	plots+=[jesdown]
	jesdown.SetLineColor(4)
	jesdown.SetLineStyle(2)
        jesdown.Draw("hesame")
        legend1.AddEntry(jesdown,"JES down","l")
	plots+=[pdfup]
	pdfup.SetLineColor(5)
	pdfup.SetLineStyle(2)
        pdfup.Draw("hesame")
        legend1.AddEntry(pdfup,"PDF up","l")
	plots+=[pdfdown]
	pdfdown.SetLineColor(6)
	pdfdown.SetLineStyle(2)
        pdfdown.Draw("hesame")
        legend1.AddEntry(pdfdown,"PDF down","l")
	plots+=[scaleup]
	scaleup.SetLineColor(7)
	scaleup.SetLineStyle(2)
        scaleup.Draw("hesame")
        legend1.AddEntry(scaleup,"scale up","l")
	plots+=[scaledown]
	scaledown.SetLineColor(8)
	scaledown.SetLineStyle(2)
        scaledown.Draw("hesame")
        legend1.AddEntry(scaledown,"scale down","l")
	plots+=[ci]
        ci.Draw("hesame")
        legend1.AddEntry(ci,"CI","l")
	plots+=[data]
	data.SetLineColor(1)
	data.SetMarkerStyle(24)
        data.SetMarkerSize(0.5)
        data.Draw("pesame")
	
        legend1.SetTextSize(0.04)
        legend1.SetFillStyle(0)
        legend1.Draw("same")

      canvas.SaveAs(prefix + "_"+samples[i][0].replace("QCDCI","CI") + '_sys.pdf')
      canvas.SaveAs(prefix + "_"+samples[i][0].replace("QCDCI","CI") + '_sys.eps')
