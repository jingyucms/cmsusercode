import os, sys
from ROOT import *
import array
from math import *

#gROOT.Reset()
#gROOT.SetStyle("Plain")
#gStyle.SetOptStat(0)
#gStyle.SetOptFit(0)
#gStyle.SetTitleOffset(1.2,"Y")
#gStyle.SetPadLeftMargin(0.18)
#gStyle.SetPadBottomMargin(0.15)
#gStyle.SetPadTopMargin(0.03)
#gStyle.SetPadRightMargin(0.05)
#gStyle.SetMarkerSize(1.5)
#gStyle.SetHistLineWidth(1)
#gStyle.SetStatFontSize(0.020)
#gStyle.SetTitleSize(0.06, "XYZ")
#gStyle.SetLabelSize(0.05, "XYZ")
#gStyle.SetNdivisions(510, "XYZ")
#gStyle.SetLegendBorderSize(0)

print "Program Starts..."

def rebin(h1,nbins,binning):
    for b in range(h1.GetXaxis().GetNbins()):
        h1.SetBinContent(b+1,h1.GetBinContent(b+1)*h1.GetBinWidth(b+1))
        h1.SetBinError(b+1,h1.GetBinError(b+1)*h1.GetBinWidth(b+1))
    h1=h1.Rebin(nbins,h1.GetName()+"_rebin",binning)
    for b in range(h1.GetXaxis().GetNbins()):
        h1.SetBinContent(b+1,h1.GetBinContent(b+1)/h1.GetBinWidth(b+1))
        h1.SetBinError(b+1,h1.GetBinError(b+1)/h1.GetBinWidth(b+1))
    return h1

def rebin2(h1,nbins,binning):
    h1=h1.Rebin(nbins,h1.GetName()+"_rebin",binning)
    return h1

def cloneNormalize(h1):
    h1=h1.Clone(h1.GetName()+"clone")
    for b in range(h1.GetXaxis().GetNbins()):
        h1.SetBinContent(b+1,h1.GetBinContent(b+1)/h1.GetBinWidth(b+1))
        h1.SetBinError(b+1,h1.GetBinError(b+1)/h1.GetBinWidth(b+1))
    return h1

def responseMatrixSmearing(massbins,hists):
    print "Applying response matrix"
    matrix=TFile("datacards/responseMatrices.root",'READ')
    matrix1=matrix.Get("TMatrixT<double>;2") #low mass chi binning
    matrix2=matrix.Get("TMatrixT<double>;3") #highest mass chi binning
    matrixMassBins=[1000,1200,1500,1900,2400,3000,3600,4200,4800,5400,6000,13000]
    
    histsbackup=[]
    factor=1.
    for hist in hists:
        histbackup=hist.Clone(hist.GetName()+"_orig")
        histbackup.Scale(factor)
        histsbackup.append(histbackup)
        hist.Scale(0.)
    for j1 in range(len(massbins)):
        for b1 in range(hists[j1].GetNbinsX()):
            for j2 in range(len(massbins)):
                for b2 in range(hists[j1].GetNbinsX()):
                    if abs(j1-j2)>1 or j2<j1: continue
                    response=0
                    if j1==(len(massbins)-1) and j2==(len(massbins)-1):
                        # both in highest mass bin
                        response=matrix2[(j1+3)+b1*(len(matrixMassBins)-1)][(j2+3)+b2*(len(matrixMassBins)-1)]
                    elif j1!=(len(massbins)-1) and j2!=(len(massbins)-1):
                        # both in lower mass bins
                        response=matrix1[(j1+3)+b1*(len(matrixMassBins)-1)][(j2+3)+b2*(len(matrixMassBins)-1)]
                    elif j1==(len(massbins)-1):
                        # one in highest, one in lower mass bin
		        for bin1 in range(hists[0].GetNbinsX()):
                            if hists[0].GetBinCenter(bin1+1)>hists[j1].GetXaxis().GetBinLowEdge(b1+1) and\
                               hists[0].GetBinCenter(bin1+1)<hists[j1].GetXaxis().GetBinUpEdge(b1+1):
                                response+=matrix1[(j1+3)+bin1*(len(matrixMassBins)-1)][(j2+3)+b2*(len(matrixMassBins)-1)]
                    elif j2==(len(massbins)-1):
                        # one in highest, one in lower mass bin
		        for bin2 in range(hists[0].GetNbinsX()):
                            if hists[0].GetBinCenter(bin2+1)>hists[j2].GetXaxis().GetBinLowEdge(b2+1) and\
                               hists[0].GetBinCenter(bin2+1)<hists[j2].GetXaxis().GetBinUpEdge(b2+1):
                                response+=matrix1[(j1+3)+b1*(len(matrixMassBins)-1)][(j2+3)+bin2*(len(matrixMassBins)-1)]
                    
                    #print j1, b1, j2, b2, response
		    hists[j2].Fill(hists[j2].GetBinCenter(b2+1),histsbackup[j1].GetBinContent(b1+1)*response)

    for j in range(len(massbins)):
        print "smear factor:",hists[j].Integral()/histsbackup[j].Integral()
    return

if __name__ == '__main__':

    useUnfoldedData=False

    dmPrefix="./crystalBallSmearedAug30/"

    prefix="datacard_shapelimit13TeV"

    jessources = ["AbsoluteStat", 
                  #"AbsoluteScale", 
                  #"AbsoluteFlavMap", 
                  "AbsoluteMPFBias", 
                  "Fragmentation",
                  #"SinglePionECAL", 
                  "SinglePionHCAL",
                  #"FlavorQCD", 
                  "TimePtEta",
                  "RelativeJEREC1",
                  #"RelativeJEREC2",
                  "RelativeJERHF",
                  #"RelativePtBB",
                  "RelativePtEC1",
                  "RelativePtEC2",
                  #"RelativePtHF",
                  "RelativeBal",
                  "RelativeFSR",
                  "RelativeStatFSR", 
                  #"RelativeStatEC", 
                  #"RelativeStatHF",
                  "PileUpPtRef", 
                  #"PileUpPtBB", 
                  "PileUpPtEC1", 
                  "PileUpPtEC2", 
                  #"PileUpPtHF",
                  "PileUpMuZero", 
                  #"PileUpEnvelope",
                  "SumInQuadrature" ]
    
    print len(jessources)-1,"jes sources"
 
    chi_bins=[(1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,3,6,9,12,16),
              ]
    massbins=[(1900,2400),
              (2400,3000),
              (3000,3600),
              (3600,4200),
              (4200,4800),
              (4800,5400),
              (5400,6000),
              (6000,13000)]
    
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
    mass_bins_nlo_list=[(2,),
                        (3,),
                        (4,),
                        (5,),
                        (6,),
                        (7,),
                        (8,),
                        (9,),
    ]
    
    chi_binnings=[]
    for mass_bin in chi_bins:
        chi_binnings+=[array.array('d')]
        for chi_bin in mass_bin:
            chi_binnings[-1].append(chi_bin)

    samples=[]

    for mass in [6000]:
    #for mass in [2000,2250,2500,3000]:
    #for mass in [3500,4000,4500,5000]:
        mDMs=[1]
        for mDM in mDMs:
            for weight in ['gdmv_0_gdma_1p0_gv_0_ga_0p01', 'gdmv_0_gdma_1p0_gv_0_ga_0p05', 'gdmv_0_gdma_1p0_gv_0_ga_0p1', 'gdmv_0_gdma_1p0_gv_0_ga_0p2', 'gdmv_0_gdma_1p0_gv_0_ga_0p25', 'gdmv_0_gdma_1p0_gv_0_ga_0p3', 'gdmv_0_gdma_1p0_gv_0_ga_0p5', 'gdmv_0_gdma_1p0_gv_0_ga_0p75', 'gdmv_0_gdma_1p0_gv_0_ga_1', 'gdmv_0_gdma_1p0_gv_0_ga_1p5', 'gdmv_0_gdma_1p0_gv_0_ga_2p0', 'gdmv_0_gdma_1p0_gv_0_ga_2p5', 'gdmv_0_gdma_1p0_gv_0_ga_3p0']:
                samples+=[("DMAxial_Dijet_LO_Mphi_"+str(mass)+"_"+str(mDM)+"_1p0_1p0_Mar5_"+weight,[("DMAxial_Dijet_LO_Mphi_"+str(mass)+"_"+str(mDM)+"_1p0_1p0_Mar5_"+weight,0)]),]


    closefiles=[]

    # NLO QCD
    filename1nu2="fastnlo/RunII/fnl5662j_v23_fix_CT14nlo_allmu_ak4.root"
    print filename1nu2
    nlofile2 = TFile.Open(filename1nu2)
    closefiles+=[nlofile2]
    
    # NLO uncertainties
    filename1nu3="fastnlo/RunII/fnl5662j_cs_ct14nlo_30000_LL+.root"
    print filename1nu3
    nlofile3 = TFile.Open(filename1nu3)
    closefiles+=[nlofile3]
    
    # DM uncertainties
    filename1dmpdf="datacards/chi_dm_pdf_plots6000_13TeV_2016.root"
    print filename1dmpdf
    dmpdffile = TFile.Open(filename1dmpdf)
    closefiles+=[dmpdffile]

    # EWK correction
    filename1ewk="fastnlo/RunII/DijetAngularCMS13_ewk.root"
    print filename1ewk
    ewkfile = TFile.Open(filename1ewk)
    closefiles+=[ewkfile]
    
    dataevents={}
    nloqcdnormfactors=[]
    
    nloqcds=[]
    nloqcdnorms=[]
    nloPDFupqcds=[]
    nloPDFdownqcds=[]
    nloScaleupqcds={}
    nloScaledownqcds={}
    
    for j in range(len(massbins)):

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
        nloqcdnormfactor=nloqcdbackup.Integral()
        nloqcdnormfactors.append(nloqcdnormfactor)

        # NLO normalized
        nloqcdnorm=None
        for k in mass_bins_nlo_list[j]:
            histname='chi-'+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])
            print histname
            hnlo = TH1F(nlofile3.Get(histname))
            #hnlo.Scale(float(mass_bins_nlo3[k+1]-mass_bins_nlo3[k]))
            hnlo.Scale(nloqcdnormfactor)
            hnlo=rebin2(hnlo,len(chi_binnings[j])-1,chi_binnings[j])
            if nloqcdnorm:
                nloqcdnorm.Add(hnlo)
            else:
                nloqcdnorm=hnlo
        #print "massbin width:", float(mass_bins_nlo3[k+1]-mass_bins_nlo3[k])
        nloqcdnorms.append(nloqcdnorm)

        # EWK corrections
        histname='chi-'+str(massbins[j]).strip("()").replace(',',"-").replace(' ',"").replace("6000-13000","6000-6600")
        print histname
        ewk=ewkfile.Get(histname)
        for b in range(nloqcd.GetXaxis().GetNbins()):
            low_bin=ewk.FindBin(nloqcd.GetXaxis().GetBinLowEdge(b+1))
            up_bin=ewk.FindBin(nloqcd.GetXaxis().GetBinUpEdge(b+1))
            correction=ewk.Integral(low_bin,up_bin-1)/(up_bin-low_bin)
            nloqcd.SetBinContent(b+1,nloqcd.GetBinContent(b+1)*correction)
        #nloqcd.Scale(1./nloqcd.Integral())
        ewk.SetName("ewk-"+histname)
        nloqcds.append(nloqcd)

        # PDF uncertainty
        nloPDFupqcd=None
        for k in mass_bins_nlo_list[j]:
            histname='chi-'+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"PDFUp"
            print histname
            hnloPDFup = TH1F(nlofile3.Get(histname))
            #hnloPDFup.Scale(float(mass_bins_nlo3[k+1]-mass_bins_nlo3[k]))
            hnloPDFup.Scale(nloqcdnormfactor)
            hnloPDFup=rebin2(hnloPDFup,len(chi_binnings[j])-1,chi_binnings[j])
            if nloPDFupqcd:
                nloPDFupqcd.Add(hnloPDFup)
            else:
                nloPDFupqcd=hnloPDFup
            nloPDFupqcds.append(nloPDFupqcd)
        
        nloPDFdownqcd=None
        for k in mass_bins_nlo_list[j]:
            histname='chi-'+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"PDFDown"
            print histname
            hnloPDFdown = TH1F(nlofile3.Get(histname))
            #hnloPDFdown.Scale(float(mass_bins_nlo3[k+1]-mass_bins_nlo3[k]))
            hnloPDFdown.Scale(nloqcdnormfactor)
            hnloPDFdown=rebin2(hnloPDFdown,len(chi_binnings[j])-1,chi_binnings[j])
            if nloPDFdownqcd:
                nloPDFdownqcd.Add(hnloPDFdown)
            else:
                nloPDFdownqcd=hnloPDFdown
            nloPDFdownqcds.append(nloPDFdownqcd)


    for scaleVariation in ['MuR','MuF','']:
        nloScaleupqcds[scaleVariation]=[]
        nloScaledownqcds[scaleVariation]=[]
            
    for scaleVariation in ['MuR','MuF','']:
        for j in range(len(massbins)):                
            nloScaleupqcd=None
            for k in mass_bins_nlo_list[j]:
                histname='chi-'+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"scale"+scaleVariation+"Up"
                print histname
	        if scaleVariation=="":
                    hnloScaleup = TH1F(nlofile3.Get(histname))
                elif scaleVariation=="MuR":
                    hnloScaleup = TH1F(nlofile3.Get("CIJET_fnl5662j_cs_001_ct14nlo_0_56_30000_LL+_mu_qcd_chi-"+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"scale-2.0-1.0_addmu")).Clone(histname)
	        elif scaleVariation=="MuF":
                    hnloScaleup = TH1F(nlofile3.Get("CIJET_fnl5662j_cs_001_ct14nlo_0_56_30000_LL+_mu_qcd_chi-"+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"scale-1.0-2.0_addmu")).Clone(histname)
	        #hnloScaleup.Scale(float(mass_bins_nlo3[k+1]-mass_bins_nlo3[k]))
                hnloScaleup.Scale(nloqcdnormfactors[j])
                hnloScaleup=rebin2(hnloScaleup,len(chi_binnings[j])-1,chi_binnings[j])
                if nloScaleupqcd:
                    nloScaleupqcd.Add(hnloScaleup)
                else:
                    nloScaleupqcd=hnloScaleup
                nloScaleupqcds[scaleVariation]+=[nloScaleupqcd]

            nloScaledownqcd=None
            for k in mass_bins_nlo_list[j]:
                histname='chi-'+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"scale"+scaleVariation+"Down"
                print histname
                if scaleVariation=="":
                    hnloScaledown = TH1F(nlofile3.Get(histname))
                elif scaleVariation=="MuR":
                    hnloScaledown = TH1F(nlofile3.Get("CIJET_fnl5662j_cs_001_ct14nlo_0_56_30000_LL+_mu_qcd_chi-"+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"scale-0.5-1.0_addmu")).Clone(histname)
	        elif scaleVariation=="MuF":
                    hnloScaledown = TH1F(nlofile3.Get("CIJET_fnl5662j_cs_001_ct14nlo_0_56_30000_LL+_mu_qcd_chi-"+str(mass_bins_nlo3[k])+"-"+str(mass_bins_nlo3[k+1])+"scale-1.0-0.5_addmu")).Clone(histname)
	        #hnloScaledown.Scale(float(mass_bins_nlo3[k+1]-mass_bins_nlo3[k]))
                hnloScaledown.Scale(nloqcdnormfactors[j])
                #print nloqcdbackup.Integral(),hnloScaledown.Integral()
                hnloScaledown=rebin2(hnloScaledown,len(chi_binnings[j])-1,chi_binnings[j])
                if nloScaledownqcd:
                    nloScaledownqcd.Add(hnloScaledown)
                else:
                    nloScaledownqcd=hnloScaledown
                nloScaledownqcds[scaleVariation].append(nloScaledownqcd)
            
    responseMatrixSmearing(massbins,nloqcds)
    responseMatrixSmearing(massbins,nloqcdnorms)
    responseMatrixSmearing(massbins,nloPDFupqcds)
    responseMatrixSmearing(massbins,nloPDFdownqcds)

    for scaleVariation in ["MuR","MuF",""]:
        responseMatrixSmearing(massbins,nloScaleupqcds[scaleVariation])
        responseMatrixSmearing(massbins,nloScaledownqcds[scaleVariation])
    #sys.exit()

    for j in range(len(massbins)):
        nloPDFupqcds[j].Add(nloqcdnorms[j],-1)
        nloPDFupqcds[j].Scale(1./nloqcdnorms[j].Integral())
        nloPDFdownqcds[j].Add(nloqcdnorms[j],-1)
        nloPDFdownqcds[j].Scale(1./nloqcdnorms[j].Integral())
        for scaleVariation in ["MuR","MuF",""]:
            nloScaleupqcds[scaleVariation][j].Add(nloqcdnorms[j],-1)
            nloScaleupqcds[scaleVariation][j].Scale(1./nloqcdnorms[j].Integral())
            nloScaledownqcds[scaleVariation][j].Add(nloqcdnorms[j],-1)
            nloScaledownqcds[scaleVariation][j].Scale(1./nloqcdnorms[j].Integral())
        

    # JES uncertainty CI
    jescifiles=[]
    for n in range(5):
        filename1jesci="datacards/chi_systematic_plotschi_QCD"+str(n)+"RerecoV3_13TeV_2016.root"
        print filename1jesci
        jescifiles += [TFile.Open(filename1jesci)]
        closefiles+=[jescifiles[-1]]
    jescihists={}
    for j in range(len(massbins)):
        for source in jessources:
            jescihists[str(j)+source]=[]
	    for jescifile in jescifiles:
	        jespad=jescifile.Get("jes")
                jes=jespad.GetListOfPrimitives()[j+useUnfoldedData*1]
                jescihists[str(j)+source]+=[a for a in jes.GetListOfPrimitives() if source in str(a)]
            if len(jescihists[str(j)+source])!=2:
	        print "JES source not found", jesname
	        error

    for i in range(len(samples)):
    #for i in range(1):
        #sample="./crystalBallSmearedAug30/datacard_shapelimit13TeV_DMAxial_Dijet_LO_Mphi_6000_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_0p2_chi2016.root"
        sample=dmPrefix + prefix + "_" + samples[i][0] + '_chi2016.root'
        print sample
        out=TFile(sample,'UPDATE')
        closefiles+=[out]

        histprefix=sample.replace("_chi2016.root","").replace(dmPrefix,"").replace("datacard_shapelimit13TeV_","")
        print histprefix

        reference=TFile("./smearedDatacardsAug30/datacard_shapelimit13TeV_DMAxial_Dijet_LO_Mphi_6000_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_1_chi2016.root")
        refprefix='DMAxial_Dijet_LO_Mphi_6000_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_1'

#        canvas = TCanvas("","",0,0,600,600)
#        canvas.Divide(3,3)
#        plots=[]
#        legends=[]
                    
        for j in range(len(massbins)):

            massstring=str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")

            # data
            histname='data_obs#chi'+massstring+"_rebin1"
            data=reference.Get(histname)
            dataevents[j]=data.Integral()
            print massstring, dataevents[j]
            out.cd()
            for k in range(0,200):
                out.Delete(histname+";"+str(k))
            data.Write(histname)

            # QCD
            histname='QCD#chi'+massstring+"_rebin1"
            qcd=reference.Get(histname)
            out.cd()
            for k in range(0,200):
                out.Delete(histname+";"+str(k))
            qcd.Write(histname)

            # ALT
            histname=refprefix+'_ALT#chi'+massstring+"_rebin1"
            alt=reference.Get(histname)
            alt_clone=alt.Clone(histprefix+'_ALT#chi'+massstring+'_rebin1')
            out.cd()
            for k in range(0,200):
                out.Delete(histprefix+'_ALT#chi'+massstring+'_rebin1'+";"+str(k))
                out.Delete(histprefix+'_ALT#chi'+massstring+'rebin1'+";"+str(k))
            alt_clone.Write(histprefix+'_ALT#chi'+massstring+'_rebin1')

            # ALT jes
            for source in jessources:
                if source=="SumInQuadrature":
                    jesname=''
                else:
                    jesname=str(jessources.index(source)+1)
                histnameup=refprefix+'_ALT#chi'+massstring+"_rebin1"+'_jes'+jesname+'Up'
                histnamedown=refprefix+'_ALT#chi'+massstring+"_rebin1"+'_jes'+jesname+'Down'
                altup=reference.Get(histnameup)
                altdown=reference.Get(histnamedown)
                altup_clone=altup.Clone(histprefix+'_ALT#chi'+massstring+"_rebin1"+'_jes'+jesname+'Up')
                altdown_clone=altdown.Clone(histprefix+'_ALT#chi'+massstring+"_rebin1"+'_jes'+jesname+'Down')
                out.cd()
                for k in range(0,200):
                    out.Delete(histprefix+'_ALT#chi'+massstring+"_rebin1"+'_jes'+jesname+'Up'+";"+str(k))
                    out.Delete(histprefix+'_ALT#chi'+massstring+"_rebin1"+'_jes'+jesname+'Down'+";"+str(k))
                altup_clone.Write(histprefix+'_ALT#chi'+massstring+"_rebin1"+'_jes'+jesname+'Up')
                altdown_clone.Write(histprefix+'_ALT#chi'+massstring+"_rebin1"+'_jes'+jesname+'Down')

            # ALT pdf, jer, scale
            for source in ['pdf','scale','scaleMuR','scaleMuF','jer']:
                histnameup=refprefix+'_ALT#chi'+massstring+"_rebin1"+'_'+source+'Up'
                histnamedown=refprefix+'_ALT#chi'+massstring+"_rebin1"+'_'+source+'Down'
                altup=reference.Get(histnameup)
                altdown=reference.Get(histnamedown)
                altup_clone=altup.Clone(histprefix+'_ALT#chi'+massstring+"_rebin1"+'_'+source+'Up')
                altdown_clone=altdown.Clone(histprefix+'_ALT#chi'+massstring+"_rebin1"+'_'+source+'Down')
                out.cd()
                for k in range(0,200):
                    out.Delete(histprefix+'_ALT#chi'+massstring+"_rebin1"+'_'+source+'Up'+";"+str(k))
                    out.Delete(histprefix+'_ALT#chi'+massstring+"_rebin1"+'_'+source+'Down'+";"+str(k))
                altup_clone.Write(histprefix+'_ALT#chi'+massstring+"_rebin1"+'_'+source+'Up')
                altdown_clone.Write(histprefix+'_ALT#chi'+massstring+"_rebin1"+'_'+source+'Down')

            # DM
            dm_clone=out.Get(histprefix.replace("Mar5","Smeared")+'#chi'+massstring+'_rebin1_backup')
            print dm_clone.GetName()
            dm=dm_clone.Clone(dm_clone.GetName())
            dm=dm.Rebin(len(chi_binnings[j])-1,histprefix+'#chi'+massstring+'_rebin1',chi_binnings[j])
            print "dm.Integral():",dm.Integral()
            print "nloqcd.Integral()", nloqcds[j].Integral()
            print "signal fraction in first bin", dm.GetBinContent(1)/nloqcds[j].GetBinContent(1)
            dm.Add(nloqcds[j])
            dm.Scale(dataevents[j]/dm.Integral())
            for b in range(dm.GetNbinsX()):
                dm.SetBinError(b+1,0)
            out.cd()
            for k in range(0,200):
                out.Delete(histprefix+'#chi'+massstring+'_rebin1'+";"+str(k))
            dm.Write(histprefix+'#chi'+massstring+'_rebin1')
            
            newnloqcd_clone=nloqcds[j].Clone(nloqcds[j].GetName()+"_ALT_crosscheck")
            newnloqcd_clone.Scale(dataevents[j]/newnloqcd_clone.Integral())
            for k in range(0,200):
                out.Delete(newnloqcd_clone.GetName()+";"+str(k))
            newnloqcd_clone.Write(newnloqcd_clone.GetName())
            print "signal fraction in first bin", (dm.GetBinContent(1)-newnloqcd_clone.GetBinContent(1))/newnloqcd_clone.GetBinContent(1)
            
            # DM jes
            for source in jessources:
	        if source=="SumInQuadrature":
	            jesname=""
	        else:
	            jesname=str(jessources.index(source)+1)
                histname=histprefix+'#chi'+massstring+"_rebin1"
                clone=dm.Clone(histname)
                clone=clone.Rebin(len(chi_binnings[j])-1,clone.GetName(),chi_binnings[j])
                dmjesup=clone.Clone(histname+"_jes"+jesname+"Up")
                dmjesdown=clone.Clone(histname+"_jes"+jesname+"Down")
                for b in range(clone.GetNbinsX()):
                    dmjesup.SetBinContent(b+1,clone.GetBinContent(b+1)*jescihists[str(j)+source][0].GetBinContent(b+1))
                    dmjesdown.SetBinContent(b+1,clone.GetBinContent(b+1)*jescihists[str(j)+source][1].GetBinContent(b+1))
                dmjesup.SetLineColor(4)
                dmjesup.SetLineStyle(2)
                dmjesdown.SetLineColor(4)
                dmjesdown.SetLineStyle(3)
                out.cd()
                for k in range(0,200):
                    out.Delete(histname+"_jes"+jesname+"Up"+";"+str(k))
                    out.Delete(histname+"_jes"+jesname+"Down"+";"+str(k))
                dmjesup.Write(histname+"_jes"+jesname+"Up")
                dmjesdown.Write(histname+"_jes"+jesname+"Down")

            # DM jer
            
            histname=histprefix+'#chi'+massstring+"_rebin1"
            clone=dm.Clone(histname)
            clone=clone.Rebin(len(chi_binnings[j])-1,clone.GetName(),chi_binnings[j])
            dmjerup=clone.Clone(histname+"_jerUp")
            dmjerdown=clone.Clone(histname+"_jerDown")
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
                dmjerup.SetBinContent(b+1,clone.GetBinContent(b+1)*(1.+(clone.GetBinCenter(b+1)-8.5)/7.5*slopes[massbins[j][0]]))
                dmjerdown.SetBinContent(b+1,clone.GetBinContent(b+1)*(1.-(clone.GetBinCenter(b+1)-8.5)/7.5*slopes[massbins[j][0]]))
            dmjerup.SetLineColor(3)
            dmjerup.SetLineStyle(2)
            dmjerdown.SetLineColor(3)
            dmjerdown.SetLineStyle(3)
            out.cd()
            for k in range(0,200):
                out.Delete(histname+"_jerUp"+";"+str(k))
                out.Delete(histname+"_jerDown"+";"+str(k))
            dmjerup.Write(histname+"_jerUp")
            dmjerdown.Write(histname+"_jerDown")

            # DM PDF
            if "Mphi_6000" in sample:
                nloPDFdowndm=nloPDFdownqcds[j].Clone("DM_pdf_down")
                nloPDFupdm=nloPDFupqcds[j].Clone("DM_pdf_up")
	        dmpdfcanvas=dmpdffile.Get("pdf")
	        dmpdfplot=dmpdfcanvas.GetListOfPrimitives()[j+useUnfoldedData*1]
	        dmpdfhist=[a for a in dmpdfplot.GetListOfPrimitives() if "mean" in str(a)][0]
	        for b in range(nloPDFdowndm.GetNbinsX()):
	            print nloPDFdowndm.GetBinContent(b+1),dmpdfhist.GetBinError(b+1)/dmpdfhist.GetBinContent(b+1)*dm.GetBinContent(b+1)/dataevents[j]
                    nloPDFupdm.SetBinContent(b+1,sqrt(pow(nloPDFupdm.GetBinContent(b+1),2)+pow(dmpdfhist.GetBinError(b+1)/dmpdfhist.GetBinContent(b+1)*dm.GetBinContent(b+1)/dataevents[j],2)))
                    nloPDFdowndm.SetBinContent(b+1,-sqrt(pow(nloPDFdowndm.GetBinContent(b+1),2)+pow(dmpdfhist.GetBinError(b+1)/dmpdfhist.GetBinContent(b+1)*dm.GetBinContent(b+1)/dataevents[j],2)))
	    else:
                nloPDFdowndm=nloPDFdownqcds[j]
                nloPDFupdm=nloPDFupqcds[j]

                
            dmpdfup=dm.Clone(dm.GetName().replace("_backup","")+"_pdfUp")
            dmpdfdown=dm.Clone(dm.GetName().replace("_backup","")+"_pdfDown")
            dmpdfup.Add(nloPDFupdm,dataevents[j])
            dmpdfdown.Add(nloPDFdowndm,dataevents[j])
            for b in range(dmpdfup.GetXaxis().GetNbins()):
                dmpdfup.SetBinError(b+1,0)
                dmpdfdown.SetBinError(b+1,0)
                if dmpdfup.GetBinCenter(b+1)-8.5>0:
                    tmp=dmpdfup.GetBinContent(b+1)
                    dmpdfup.SetBinContent(b+1,dmpdfdown.GetBinContent(b+1))
                    dmpdfdown.SetBinContent(b+1,tmp)
            dmpdfup.SetLineColor(6)
            dmpdfup.SetLineStyle(2)
            dmpdfdown.SetLineColor(6)
            dmpdfdown.SetLineStyle(3)
            out.cd()
            for k in range(0,200):
                out.Delete(dm.GetName().replace("_backup","")+"_pdfUp"+";"+str(k))
                out.Delete(dm.GetName().replace("_backup","")+"_pdfDown"+";"+str(k))
            dmpdfup.Write(dm.GetName().replace("_backup","")+"_pdfUp")
            dmpdfdown.Write(dm.GetName().replace("_backup","")+"_pdfDown")

            # DM scale
            for scaleVariation in ["MuR","MuF",""]:
                nloScaledowndm=nloScaledownqcds[scaleVariation][j]
                nloScaleupdm=nloScaleupqcds[scaleVariation][j]

                dmscaleup=dm.Clone(dm.GetName().replace("_backup","")+"_scale"+scaleVariation+"Up")
                dmscaledown=dm.Clone(dm.GetName().replace("_backup","")+"_scale"+scaleVariation+"Down")
                dmscaleup.Add(nloScaleupdm,dataevents[j])
                dmscaledown.Add(nloScaledowndm,dataevents[j])

                for b in range(dmscaleup.GetXaxis().GetNbins()):
                    dmscaleup.SetBinError(b+1,0)
                    dmscaledown.SetBinError(b+1,0)
                    if scaleVariation=="" and dmscaleup.GetBinCenter(b+1)-8.5>0:
                        tmp=dmscaleup.GetBinContent(b+1)
                        dmscaleup.SetBinContent(b+1,dmscaledown.GetBinContent(b+1))
                        dmscaledown.SetBinContent(b+1,tmp)
                dmscaleup.SetLineColor(7)
                dmscaleup.SetLineStyle(2)
                dmscaledown.SetLineColor(7)
                dmscaledown.SetLineStyle(3)
                out.cd()
                for k in range(0,200):
                    out.Delete(dm.GetName().replace("_backup","")+"_scale"+scaleVariation+"Up"+";"+str(k))
                    out.Delete(dm.GetName().replace("_backup","")+"_scale"+scaleVariation+"Down"+";"+str(k))
                dmscaleup.Write(dm.GetName().replace("_backup","")+"_scale"+scaleVariation+"Up")
                dmscaledown.Write(dm.GetName().replace("_backup","")+"_scale"+scaleVariation+"Down")

#            canvas.cd(j+1)#j-2
#            legend1=TLegend(0.2,0.6,0.9,0.95,(str(massbins[j][0])+"<m_{jj}<"+str(massbins[j][1])+" GeV").replace("4800<m_{jj}<7000","m_{jj}>4800").replace("4800<m_{jj}<13000","m_{jj}>4800"))
#            legends+=[legend1]
#            legend1.AddEntry(data,"data","lpe")
#            alt_clone=cloneNormalize(alt_clone)
#            plots+=[alt_clone]
#            alt_clone.Draw("he")
#            alt_clone.GetYaxis().SetRangeUser(alt.GetMinimum()*0.8,(alt.GetMaximum()-alt.GetMinimum())*2.+alt.GetMinimum())
#            legend1.AddEntry(alt_clone,"QCD","l")
#        
#            # background uncertainties
#            jerup=cloneNormalize(jerup)
#            plots+=[jerup]
#            jerup.Draw("hesame")
#            legend1.AddEntry(jerup,"JER","l")
#            jerdown=cloneNormalize(jerdown)
#            plots+=[jerdown]
#            jerdown.Draw("hesame")
#            jesup=cloneNormalize(jesup)
#            plots+=[jesup]
#            jesup.Draw("hesame")
#            legend1.AddEntry(jesup,"JES","l")
#            jesdown=cloneNormalize(jesdown)
#            plots+=[jesdown]
#            jesdown.Draw("hesame")
#            pdfup=cloneNormalize(pdfup)
#            plots+=[pdfup]
#            pdfup.Draw("hesame")
#            legend1.AddEntry(pdfup,"PDF","l")
#            pdfdown=cloneNormalize(pdfdown)
#            plots+=[pdfdown]
#            pdfdown.Draw("hesame")
#            scaleup=cloneNormalize(scaleup)
#            plots+=[scaleup]
#            scaleup.Draw("hesame")
#            legend1.AddEntry(scaleup,"scale","l")
#            scaledown=cloneNormalize(scaledown)
#            plots+=[scaledown]
#            scaledown.Draw("hesame")
#        
#            ci=cloneNormalize(ci)
#            plots+=[ci]
#            ci.Draw("hesame")
#            legend1.AddEntry(ci,"New Physics","l")
#        
#            # signal uncertainties
#            cijerup=cloneNormalize(cijerup)
#            plots+=[cijerup]
#            cijerup.Draw("hesame")
#            cijerdown=cloneNormalize(cijerdown)
#            plots+=[cijerdown]
#            cijerdown.Draw("hesame")
#            cijesup=cloneNormalize(cijesup)
#            plots+=[cijesup]
#            cijesup.Draw("hesame")
#            cijesdown=cloneNormalize(cijesdown)
#            plots+=[cijesdown]
#            cijesdown.Draw("hesame")
#            cipdfup=cloneNormalize(cipdfup)
#            plots+=[cipdfup]
#            cipdfup.Draw("hesame")
#            cipdfdown=cloneNormalize(cipdfdown)
#            plots+=[cipdfdown]
#            cipdfdown.Draw("hesame")
#            ciscaleup=cloneNormalize(ciscaleup)
#            plots+=[ciscaleup]
#            ciscaleup.Draw("hesame")
#            ciscaledown=cloneNormalize(ciscaledown)
#            plots+=[ciscaledown]
#            ciscaledown.Draw("hesame")
# 
#            origdata=data
#            dataplot[j]=TGraphAsymmErrors(cloneNormalize(data))
#            plots+=[dataplot[j]]
#            alpha=1.-0.6827
#            for b in range(dataplot[j].GetN()):
#                if useUnfoldedData:
#                    N=1./pow(origdata.GetBinError(b+1)/origdata.GetBinContent(b+1),2)
#                else:
#                    N=origdata.GetBinContent(b+1)
#                L=0
#                if N>0:
#                    L=ROOT.Math.gamma_quantile(alpha/2.,N,1.)
#                U=ROOT.Math.gamma_quantile_c(alpha/2.,N+1,1.)
#                dataplot[j].SetPointEYlow(b,(N-L)/origdata.GetBinWidth(b+1))
#                dataplot[j].SetPointEYhigh(b,(U-N)/origdata.GetBinWidth(b+1))
#            dataplot[j].SetLineColor(1)
#            dataplot[j].SetMarkerStyle(24)
#            dataplot[j].SetMarkerSize(0.5)
#            dataplot[j].Draw("pe0zsame")
#        
#            legend1.SetTextSize(0.04)
#            legend1.SetFillStyle(0)
#            legend1.Draw("same")
#
#        canvas.SaveAs(prefix + "_"+samples[i][0].replace("QCD","") + '_sys2016.pdf')
#        #canvas.SaveAs(prefix + "_"+samples[i][0].replace("QCD","") + '_sys2016.eps')
            
    for closefile in closefiles:
          closefile.Close()
                

            

            


            
            
            

            

            
      
