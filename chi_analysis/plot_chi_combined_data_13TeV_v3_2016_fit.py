from ROOT import *
import ROOT
import array, math, sys
import os
from math import *
from scipy import stats

uncertaintynames=["jer","pdf","scale"]
for i in range(1,17):
    uncertaintynames.append("jes"+str(i))


def rebin(h1,nbins,binning):
    for b in range(h1.GetXaxis().GetNbins()):
        h1.SetBinContent(b+1,h1.GetBinContent(b+1)*h1.GetBinWidth(b+1))
        h1.SetBinError(b+1,h1.GetBinError(b+1)*h1.GetBinWidth(b+1))
    h1=h1.Rebin(nbins,h1.GetName()+"_rebin",binning)
    #h1.Scale(1./h1.Integral())
    for b in range(h1.GetXaxis().GetNbins()):
        h1.SetBinContent(b+1,h1.GetBinContent(b+1)/h1.GetBinWidth(b+1))
        h1.SetBinError(b+1,h1.GetBinError(b+1)/h1.GetBinWidth(b+1))
    return h1

def rebin2(h1,nbins,binning):
    h1=h1.Rebin(nbins,h1.GetName()+"_rebin",binning)
    #h1.Scale(1./h1.Integral())
    for b in range(h1.GetXaxis().GetNbins()):
        h1.SetBinContent(b+1,h1.GetBinContent(b+1)/h1.GetBinWidth(b+1))
        h1.SetBinError(b+1,h1.GetBinError(b+1)/h1.GetBinWidth(b+1))
    return h1

def divBinWidth(hist):
    #hist.SetLineColor(linecolor)
    #hist.SetLineStyle(linestyle)
    #hist.SetLineWidth(linewidth)
    #hist.Scale(1./hist.Integral())
    for b in range(hist.GetNbinsX()):
        hist.SetBinContent(b+1,hist.GetBinContent(b+1)/hist.GetBinWidth(b+1))
        hist.SetBinError(b+1,hist.GetBinError(b+1)/hist.GetBinWidth(b+1))
    return

def getFitResults(fitFile, treename):
    tree=fitFile.Get(treename)
    fitParameters=[]
    fitConstraints=[]
    for name in uncertaintynames:
        fitParameters.append(tree.floatParsFinal().find(name).getVal())
        fitConstraints.append(tree.floatParsFinal().find(name).getError())
    return fitParameters, fitConstraints

def applyFitResults(fitParameters,fitConstraints,uncertainties,hist):
    histbackup=hist.Clone(hist.GetName()+"_backup")
    for nn in range(len(fitParameters)):
        for b in range(hist.GetXaxis().GetNbins()):
            if fitParameters[nn]>0:
        	hist.SetBinContent(b+1,hist.GetBinContent(b+1)*(1+fitParameters[nn]*(uncertainties[nn][0].GetBinContent(b+1)-uncertainties[nn][2].GetBinContent(b+1))/uncertainties[nn][2].GetBinContent(b+1)))
        	histbackup.SetBinContent(b+1,histbackup.GetBinContent(b+1)*(1+fitParameters[nn]*(uncertainties[nn][0].GetBinContent(b+1)-uncertainties[nn][2].GetBinContent(b+1))/uncertainties[nn][2].GetBinContent(b+1)))
            else:
        	hist.SetBinContent(b+1,hist.GetBinContent(b+1)*(1-fitParameters[nn]*(uncertainties[nn][1].GetBinContent(b+1)-uncertainties[nn][2].GetBinContent(b+1))/uncertainties[nn][2].GetBinContent(b+1)))
        	histbackup.SetBinContent(b+1,histbackup.GetBinContent(b+1)*(1-fitParameters[nn]*(uncertainties[nn][1].GetBinContent(b+1)-uncertainties[nn][2].GetBinContent(b+1))/uncertainties[nn][2].GetBinContent(b+1)))
        	    
    h2new=histbackup.Clone("down"+str(massbins[massbin]))
    h3new=histbackup.Clone("up"+str(massbins[massbin]))
    for b in range(histbackup.GetXaxis().GetNbins()):
        sumdown=0
        sumup=0
        nn=0
        for up,down,central in uncertainties:
            addup=fitConstraints[nn]*pow(max(0,up.GetBinContent(b+1)-central.GetBinContent(b+1),down.GetBinContent(b+1)-central.GetBinContent(b+1)),2)/pow(central.GetBinContent(b+1),2)
            adddown=fitConstraints[nn]*pow(max(0,central.GetBinContent(b+1)-up.GetBinContent(b+1),central.GetBinContent(b+1)-down.GetBinContent(b+1)),2)/pow(central.GetBinContent(b+1),2)
            sumup+=addup
            sumdown+=adddown
            nn+=1
        sumdown=sqrt(sumdown)
        sumup=sqrt(sumup)
        
        h2new.SetBinContent(b+1,histbackup.GetBinContent(b+1)-sumdown*histbackup.GetBinContent(b+1))
        h3new.SetBinContent(b+1,histbackup.GetBinContent(b+1)+sumup*histbackup.GetBinContent(b+1))
    return h2new,h3new

def getUncertainties(fsys,basename,pname):
    uncertainties=[]
    for u in uncertaintynames:
        hup_orig=fsys.Get(basename+"_"+u+"Up")
        up=hup_orig.Clone(pname+'#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1_"+u+"Up")
        divBinWidth(up)

        hdown_orig=fsys.Get(basename+"_"+u+"Down")
        down=hdown_orig.Clone(pname+'#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1_"+u+"Down")
        divBinWidth(down)

        hcentral_orig=fsys.Get(basename)
        central=hcentral_orig.Clone(pname+'#chi'+str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")+"_rebin1")
        divBinWidth(central)
        
        uncertainties+=[[up,down,central]]

    return uncertainties
    
                

if __name__=="__main__":

    unfoldedData=False
    isCB=False

    print "start ROOT"
    gROOT.Reset()
    gROOT.SetStyle("Plain")
    gStyle.SetOptStat(0)
    gStyle.SetOptFit(0)
    gStyle.SetTitleOffset(1.2,"Y")
    gStyle.SetPadLeftMargin(0.15)
    gStyle.SetPadBottomMargin(0.11)
    gStyle.SetPadTopMargin(0.05)
    gStyle.SetPadRightMargin(0.05)
    gStyle.SetMarkerSize(2.5)
    gStyle.SetHistLineWidth(1)
    gStyle.SetStatFontSize(0.020)
    gStyle.SetTitleSize(0.06, "XYZ")
    gStyle.SetLabelSize(0.05, "XYZ")
    gStyle.SetLegendBorderSize(0)
    gStyle.SetPadTickX(1)
    gStyle.SetPadTickY(1)
    gStyle.SetEndErrorSize(5)

    if unfoldedData:
        SaveDir="./fitcheckGENv5/"
    elif isCB:
        SaveDir="./fitcheckDETCBv5/"
    else:
        SaveDir="./fitcheckDETv5/"
    

    if os.path.exists(SaveDir)==False:
        os.mkdir(SaveDir)

    signalMasses=[2000,2250,2500,3000,3500,4000,4500,5000,6000]

    gas=["0p01","0p05","0p1","0p2","0p25","0p3","0p5","0p75","1","1p5","2p0","2p5","3p0"]

    counter=1100
    signalExtraName={}
    GA={}
    for mdm in ["1"]:
        for ga in gas:
            signalExtraName[counter]="_"+mdm+"_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_"+ga
            GA[counter]=ga
            counter+=1

    #print signalName,signalExtraName

    prefix="datacard_shapelimit"
    if unfoldedData:
            prefix+="_unfolded"

    new_hists=[]
    for j in [1102,1103,1104,1105,1106,1107,1108]:
        for signalMass in signalMasses:
            if signalMass<=2500:
                massbins=[(2400,3000)]
            elif signalMass<=3000:
                massbins=[(2400,3000),(3000,3600)]
            elif signalMass<=3500:
                massbins=[(2400,3000),(3000,3600),(3600,4200)]
            elif signalMass<=4000:
                massbins=[(2400,3000),(3000,3600),(3600,4200)]
            elif signalMass<=4500:
                massbins=[(2400,3000),(3000,3600),(3600,4200),(4200,4800)]  
            elif signalMass<=5000:
                massbins=[(2400,3000),(3000,3600),(3600,4200),(4200,4800),(4800,5400),(5400,6000)]
            elif signalMass<=6000:
                massbins=[(3000,3600),(3600,4200),(4200,4800),(4800,5400),(5400,6000),(6000,13000)]

            histnameprefix="DMAxial_Dijet_LO_Mphi_"+str(signalMass)+signalExtraName[j]
            filenameprefix="datacard_shapelimit13TeV_"+histnameprefix
        
            for massbin in range(len(massbins)):
            
                masstext=str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")

                # Unfolded data

                filename="datacards/Unfolded_chiNtuple_dataReReco_v3_Coarse_PFHT900_fromCB_AK4SF_pythia8_Pt_170toInf_MatrixInvert.root"
                masstext=str(massbins[massbin]).strip("()").replace(',',"_").replace(' ',"")
                if unfoldedData:
                    histname="dijet_mass_"+masstext+"_chi_unfolded"
    	        else:
                    histname="dijet_mass_"+masstext+"_chi"
              
                print filename
                fData = TFile.Open(filename)
                new_hists+=[fData]
                print histname
                h14=fData.Get(histname)
    	        divBinWidth(h14)
                h14.SetLineColor(4)
                new_hists+=[h14]

                # open datacards
                if unfoldedData:
                    filename="./invertMatrixAug30/"+filenameprefix+"_chi2016.root"
                elif isCB:
                    filename="./crystalBallSmearedAug30/"+filenameprefix+"_chi2016.root"
                else:
                    filename="./smearedDatacardsAug30/"+filenameprefix+"_chi2016.root"

                if unfoldedData:
                    fitFile=TFile("limitsGenLHCa"+str(j)+"_DMAxial_Dijet_LO_Mphi_v5/mlfit"+histnameprefix+".root")
                elif isCB:
                    fitFile=TFile("limitsDetCBLHCa"+str(j)+"_DMAxial_Dijet_LO_Mphi_v5/mlfit"+histnameprefix+".root")
                else:
                    fitFile=TFile("limitsDetLHCa"+str(j)+"_DMAxial_Dijet_LO_Mphi_v5/mlfit"+histnameprefix+".root")

                print "Fit Parameters from:", fitFile.GetName()

                basename=histnameprefix+"_ALT#chi"+masstext+"_rebin1"
                print "Background Hist Name:",basename
                
                f=TFile.Open(filename)
                new_hists+=[f]

                # NLO OCD plot (with EWK correction)
                
                hNloQcd_orig=f.Get(basename)
                new_hists+=[hNloQcd_orig]
                hNloQcd=hNloQcd_orig.Clone()
                new_hists+=[hNloQcd]
    
                for b in range(hNloQcd.GetXaxis().GetNbins()):
    	            hNloQcd.SetBinContent(b+1,hNloQcd.GetBinContent(b+1)/hNloQcd.GetBinWidth(b+1))
    
                hNloQcd.SetLineColor(1)
                hNloQcd.SetLineStyle(2)
                hNloQcd.SetLineWidth(1)
            
                hNloQcd.SetTitle("")
                hNloQcd.GetXaxis().SetTitle("#chi")
                hNloQcd.GetXaxis().SetTitleOffset(0.7)
                hNloQcd.GetYaxis().SetTitle("N")

                # QCD systematics

                pname='QCD'
                uncertainties=getUncertainties(f,basename,pname)
                
                new_hists+=[uncertainties]

                hbPrefit=hNloQcd_orig.Clone("QCDprefit"+str(massbins[massbin]))
                divBinWidth(hbPrefit)
                hbPrefit.SetLineWidth(1)
                hbPrefit.SetLineColor(1)
                hbPrefit.SetLineStyle(1)
                new_hists+=[hbPrefit]
    
                # Shift theory prediction according to fitted nuisance parameters
                
                bfitParameters,bfitConstraints=getFitResults(fitFile, 'fit_b')

                h2bnew,h3bnew=applyFitResults(bfitParameters,bfitConstraints,uncertainties,hNloQcd)

                # DM plot
                basename=histnameprefix+"#chi"+masstext+"_rebin1"
                print "Signal Hist Name:",basename
                
                hDm_orig=f.Get(basename)
                new_hists+=[hDm_orig]
                hDm=hDm_orig.Clone()
                new_hists+=[hDm]
    
                for b in range(hDm.GetXaxis().GetNbins()):
    	            hDm.SetBinContent(b+1,hDm.GetBinContent(b+1)/hDm.GetBinWidth(b+1))
    
                hDm.SetLineColor(2)
                hDm.SetLineStyle(3)
                hDm.SetLineWidth(2)
            
                # DM systematics

                pname='DM'
                uncertainties=getUncertainties(f,basename,pname)
                
                new_hists+=[uncertainties]

                hsPrefit=hDm_orig.Clone("DMprefit"+str(massbins[massbin]))
                divBinWidth(hsPrefit)
                hsPrefit.SetLineWidth(2)
                hsPrefit.SetLineColor(2)
                hsPrefit.SetLineStyle(1)
                new_hists+=[hsPrefit]
    
                # Shift theory prediction according to fitted nuisance parameters
                
                sfitParameters,sfitConstraints=getFitResults(fitFile, 'fit_s')

                h2snew,h3snew=applyFitResults(sfitParameters,sfitConstraints,uncertainties,hDm)
        
                # Plotting
                h2bnew.SetLineStyle(1)
                h2bnew.SetLineColor(15)
                h2bnew.SetFillColor(10)
                
                h3bnew.SetLineStyle(1)
                h3bnew.SetLineColor(15)
                h3bnew.SetFillColor(15)
    
                h3newnew=h3bnew.Clone()
                h3newnew.SetLineStyle(2)
                h3newnew.SetLineColor(1)
        
                new_hists+=[h2bnew]
                new_hists+=[h3bnew]
        
                canvas=TCanvas("post-fit", "post-fit", 0, 0, 1500, 1200)
                canvas.cd()

                if signalMass==6000:
                    massbin=massbin+1
                if massbin<1:
                    hNloQcd.SetMaximum(33000*1.2)
                    hNloQcd.SetMinimum(20000)
                elif massbin<2:
                    hNloQcd.SetMaximum(6000*1.2)
                    hNloQcd.SetMinimum(4000)
                elif massbin<3:
                    hNloQcd.SetMaximum(1400*1.2)
                    hNloQcd.SetMinimum(900)
                elif massbin<4:
                    hNloQcd.SetMaximum(400*1.2)
                    hNloQcd.SetMinimum(200)
                elif massbin<5:
                    hNloQcd.SetMaximum(110*1.2)
                    hNloQcd.SetMinimum(50)
                elif massbin<6:
                    hNloQcd.SetMaximum(50*1.2)
                    hNloQcd.SetMinimum(0) 
                else:
                    hNloQcd.SetMaximum(15*1.2)
                    hNloQcd.SetMinimum(0)
        
                hNloQcd.Draw("axissame")
                h3bnew.Draw("histsame")
                h2bnew.Draw("histsame")
                h14.Draw("same")
                hNloQcd.Draw("histsame")
                hbPrefit.Draw("histsame")
                hDm.Draw("histsame")
                hsPrefit.Draw("histsame")
                hNloQcd.Draw("axissame")

                l1=TLegend(0.19,0.6,0.45,0.95,masstext.replace("_","<m_{jj}<"))
                l1.SetFillStyle(0)
                l1.SetTextSize(0.035)
                l1.Draw("same")

                l3=TLegend(0.19,0.8,0.45,0.95,"M_{Med}="+str(signalMass)+", g_{q}="+GA[j].replace("p","."))
                l3.SetFillStyle(0)
                l3.SetTextSize(0.035)
                l3.Draw("same")
                
                if unfoldedData:
                    l2=TLegend(0.45,0.6,0.95,0.93,"Particle-Level")
                elif isCB:
                    l2=TLegend(0.45,0.6,0.95,0.93,"Detector-Level CB Smeared")
                else:
                    l2=TLegend(0.45,0.6,0.95,0.93,"Detector-Level RM Smeared")
                
                l2.SetTextSize(0.035)
                l2.AddEntry(h14,"Data","ple")
                l2.AddEntry(h3newnew,"Background post-fit","fl")
                l2.AddEntry(hbPrefit,"Background pre-fit","l")
                l2.AddEntry(hDm,"Background+Signal post-fit","fl")
                l2.AddEntry(hsPrefit,"Background+Signal pre-fit","l")
                l2.SetFillStyle(0)
                l2.Draw("same")
        
                h2bnew.SetLineStyle(1)
                h2bnew.SetLineColor(15)
                h2bnew.SetFillColor(10)
                
                h3bnew.SetLineStyle(1)
                h3bnew.SetLineColor(15)
                h3bnew.SetFillColor(15)
        
                canvas.SaveAs(SaveDir + prefix + "_combined_RunII_25ns_v3_2016_fit_"+histnameprefix+"_"+masstext+".pdf")

                #sys.exit()
