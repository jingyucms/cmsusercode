import os, sys
from ROOT import *
import array
from math import *

if __name__ == '__main__':

    #refdmPrefix="./crystalBallSmearedAug30/"
    #dmPrefix="./crystalBallSmearedAug30Injection1p0/"
    #dmPrefix="./crystalBallSmearedAug30Injection0p75/"

    refdmPrefix="./invertMatrixAug30/"
    #dmPrefix="./invertMatrixAug30Injection1p0/"
    dmPrefix="./invertMatrixAug30Injection0p75/"

    #refdmPrefix="./smearedDatacardsAug30/"
    #dmPrefix="./smearedDatacardsAug30Injection1p0/"
    #dmPrefix="./smearedDatacardsAug30Injection0p75/"

    os.system("rm -rf "+dmPrefix)
    os.system("cp -r "+refdmPrefix+" "+dmPrefix)

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
    refsamples=[]

    for mass in [2000,2250,2500,3000,3500,4000,4500]:
        mDMs=[1]
        for mDM in mDMs:
            for weight in ['gdmv_0_gdma_1p0_gv_0_ga_0p01', 'gdmv_0_gdma_1p0_gv_0_ga_0p05', 'gdmv_0_gdma_1p0_gv_0_ga_0p1', 'gdmv_0_gdma_1p0_gv_0_ga_0p2', 'gdmv_0_gdma_1p0_gv_0_ga_0p25', 'gdmv_0_gdma_1p0_gv_0_ga_0p3', 'gdmv_0_gdma_1p0_gv_0_ga_0p5', 'gdmv_0_gdma_1p0_gv_0_ga_0p75', 'gdmv_0_gdma_1p0_gv_0_ga_1', 'gdmv_0_gdma_1p0_gv_0_ga_1p5', 'gdmv_0_gdma_1p0_gv_0_ga_2p0', 'gdmv_0_gdma_1p0_gv_0_ga_2p5', 'gdmv_0_gdma_1p0_gv_0_ga_3p0']:
                samples+=[("DMAxial_Dijet_LO_Mphi_"+str(mass)+"_"+str(mDM)+"_1p0_1p0_Mar5_"+weight,[("DMAxial_Dijet_LO_Mphi_"+str(mass)+"_"+str(mDM)+"_1p0_1p0_Mar5_"+weight,0)]),]

    for mass in [2000,2250,2500,3000,3500,4000,4500]:
        mDMs=[1]
        for mDM in mDMs:
            #for weight in ['gdmv_0_gdma_1p0_gv_0_ga_1']:
            for weight in ['gdmv_0_gdma_1p0_gv_0_ga_0p75']:
                refsamples+=[("DMAxial_Dijet_LO_Mphi_"+str(mass)+"_"+str(mDM)+"_1p0_1p0_Mar5_"+weight,[("DMAxial_Dijet_LO_Mphi_"+str(mass)+"_"+str(mDM)+"_1p0_1p0_Mar5_"+weight,0)]),]

    #print samples
    #print refsamples

    refhists={}
    closefiles=[]
    for i in range(len(refsamples)):
        refsample=refdmPrefix + prefix + "_" + refsamples[i][0] + '_chi2016.root'
        refhists[refsample]=[]
    for refhist in refhists:
        fil=TFile(refhist)
        closefiles+=[fil]
        histprefix=refhist.replace("_chi2016.root","").replace(refdmPrefix,"").replace("datacard_shapelimit13TeV_","")
        for j in range(len(massbins)):
            massstring=str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")
            histname=histprefix+'#chi'+massstring+'_rebin1'
            hist=fil.Get(histname)
            qcdhistname=histname.replace("#chi","_ALT#chi")
            qcdhist=fil.Get(qcdhistname)
            refhists[refhist]+=[[hist,qcdhist]]

    print refhists
    #sys.exit()

    for i in range(len(samples)):
        sample=dmPrefix + prefix + "_" + samples[i][0] + '_chi2016.root'
        print sample
        out=TFile(sample,'UPDATE')
        closefiles+=[out]
        for mass in [2000,2250,2500,3000,3500,4000,4500]:
            signalMass="Mphi_" + str(mass)
            for refhist in refhists:
                if signalMass in refhist and signalMass in sample:
                    ref=refhists[refhist]
        print ref
        for j in range(len(massbins)):
            histprefix=sample.replace("_chi2016.root","").replace(dmPrefix,"").replace("datacard_shapelimit13TeV_","")
            massstring=str(massbins[j]).strip("()").replace(',',"_").replace(' ',"")
            histname='data_obs#chi'+massstring+"_rebin1"
            histnameref=histprefix+'#chi'+massstring+'_rebin1'
            data=out.Get(histname)
            databackup=data.Clone(histname+"_backup")
            nevents=data.Integral()
            add=ref[j][0]
            sub=ref[j][1]
            data.Add(sub,-1)
            data.Add(add)
            #data.Scale(float(nevents)/data.Integral())
            print "Check data normalization:",float(nevents)/data.Integral()
            out.cd()
            for k in range(0,200):
                out.Delete(histname+";"+str(k))
                out.Delete(histname+"_backup"+";"+str(k))
            data.Write(histname)
            databackup.Write()

    for closefile in closefiles:
          closefile.Close()
            
        
        
