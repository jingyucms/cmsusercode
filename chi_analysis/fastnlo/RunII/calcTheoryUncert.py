from ROOT import *
import pdb, math, os

gROOT.ForceStyle()
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetOptTitle(0)
gStyle.SetMarkerSize(0.5)
gStyle.SetHistLineWidth(1)
gStyle.SetMarkerStyle(20)
gStyle.SetLegendBorderSize(0)

def calcHessianPDFUncert(myxsecs):
    myuncertup=0
    myuncertdown=0
    for myxsec in myxsecs:
        if myxsec>0:
            myuncertup+=myxsec**2
        if myxsec<0:
            myuncertdown+=myxsec**2
    myfinaluncertup=math.sqrt(myuncertup)
    myfinaluncertdown=(-1)*math.sqrt(myuncertdown)
    return myfinaluncertup,myfinaluncertdown

def multiplyBinWidth(myhist):
    mynewhist=TH1F(myhist.GetName()+"_norm",myhist.GetName()+"_norm",len(chibins)-1,chibins)
    for b in range(0,myhist.GetXaxis().GetNbins()):
        mynewhist.SetBinContent(b+1,myhist.GetBinContent(b+1)*myhist.GetBinWidth(b+1))
    return mynewhist

from getVariations import getVariations
myVariations=getVariations()

chibins=myVariations.bins
styles=myVariations.styles

massbins=[[1900,2400],[2400,3000],[3000,3600],[3600,4200],[4200,4800],[4800,5400],[5400,6000]]#,[6000,6600],[6600,13000]
ciDir="./csxsec_ct14nlo_0-56_LL/"

normalizeBack=False  

calcUncert=True        # calculate qcd+ci uncertainties
compareUncert=False      # compare qcd uncertainty with qcd+ci uncertainty

if calcUncert:
    
    scales=[[1.0,1.0],[0.5,0.5],[2.0,2.0],[0.5,1.0],[1.0,0.5],[1.0,2.0],[2.0,1.0]]
    
    qcdmufile=TFile.Open("InclusiveNJetEvents_fnl5662j_v23_fix_CT14nlo_allmu.root")
    qcdmemfile=TFile.Open("InclusiveNJetEvents_fnl5662j_v23_fix_CT14nlo_allmem.root")

    cimufiles=[]
    cimemfiles=[]
    for j in styles:
        for i in range(5,31):
            cimufile="CIJET_fnl5662i_cs_ct14nlo_0_"+str(int(i*1000))+"_"+j+"_mu.root"
            cimemfile="CIJET_fnl5662i_cs_ct14nlo_"+str(int(i*1000))+"_"+j+"_mem.root"
            cimufiles.append(cimufile)
            cimemfiles.append(cimemfile)
    
    scaleFactorsmu={}
    for f in cimufiles:
        print "creating",f
        scaleFactorsmu[f.replace(".root","")]=[]
        file=TFile(ciDir+f)
        newfile=TFile(f.replace("CIJET_","").replace("_mu","").replace("_0_","_"),"RECREATE")
        for massbin in massbins:
            if massbins.index(massbin)<3:
                for scale in scales:
                    qcdhist=qcdmufile.Get("qcd_chi-"+str(massbin[0])+"-"+str(massbin[1])+"scale-"+str(scale[0])+"-"+str(scale[1]))
                    if scales.index(scale)==0:
                        scaleFactor=qcdhist.Integral()
                        scaleFactorsmu[f.replace(".root","")].append(scaleFactor)
                    qcdhistadd=qcdhist.Clone(f.replace(".root","")+"_"+qcdhist.GetName()+"_addmu")
                    qcdhistadd.Scale(1./qcdhistadd.Integral())
                    qcdhistadd.Write()
            else:
                for scale in scales:            
                    cihist=file.Get(f.replace("mu.root","")+"chi-"+str(massbin[0])+"-"+str(massbin[1])+"scale-"+str(scale[0])+"-"+str(scale[1]))
                    qcdhist=qcdmufile.Get("qcd_chi-"+str(massbin[0])+"-"+str(massbin[1])+"scale-"+str(scale[0])+"-"+str(scale[1]))
                    qcdhistadd=qcdhist.Clone(f.replace(".root","")+"_"+qcdhist.GetName()+"_addmu")
                    qcdhistadd.Add(cihist)
                    if scales.index(scale)==0:
                        scaleFactor=qcdhistadd.Integral()
                        scaleFactorsmu[f.replace(".root","")].append(scaleFactor)
                    #pdb.set_trace()
                    qcdhistadd.Scale(1./qcdhistadd.Integral())
                    qcdhistadd.Write()
        newfile.Close()
    
    scaleFactorsmem={}
    for f in cimemfiles:
        scaleFactorsmem[f.replace(".root","")]=[]
        file=TFile(ciDir+f)
        myfile=TFile(f.replace("CIJET_","").replace("_mem",""),"UPDATE")
	print "updating",f.replace("CIJET_","").replace("_mem","")
        for massbin in massbins:
            if massbins.index(massbin)<3:
                for i in range(0,57):
                    qcdhist=qcdmemfile.Get("qcd_chi-"+str(massbin[0])+"-"+str(massbin[1])+"PDF-"+str(i))
                    if i==0:
                        scaleFactor=qcdhist.Integral()
                        scaleFactorsmem[f.replace(".root","")].append(scaleFactor)
                    qcdhistadd=qcdhist.Clone(f.replace(".root","")+"_"+"qcd_chi-"+str(massbin[0])+"-"+str(massbin[1])+"PDF-"+str(i)+"_addmem")
                    qcdhistadd.Scale(1./qcdhistadd.Integral())
                    qcdhistadd.Write()
            else:
                for i in range(0,57):            
                    cihist=file.Get(f.replace("mem.root","")+"chi-"+str(massbin[0])+"-"+str(massbin[1])+"PDF-"+str(i))
                    qcdhist=qcdmemfile.Get("qcd_chi-"+str(massbin[0])+"-"+str(massbin[1])+"PDF-"+str(i))
                    #print qcdhist
                    qcdhistadd=qcdhist.Clone(f.replace(".root","")+"_"+"qcd_chi-"+str(massbin[0])+"-"+str(massbin[1])+"PDF-"+str(i)+"_addmem")
                    qcdhistadd.Add(cihist)
                    if i==0:
                        scaleFactor=qcdhistadd.Integral()
                        scaleFactorsmem[f.replace(".root","")].append(scaleFactor)
                    qcdhistadd.Scale(1./qcdhistadd.Integral())
                    qcdhistadd.Write()
                        
    for f in cimufiles:
        myfile=TFile(f.replace("CIJET_","").replace("_mu","").replace("_0_","_"),"UPDATE")
	print "updating",f.replace("CIJET_","").replace("_mu","").replace("_0_","_")
        for massbin in massbins:
            histcentral=TH1F("chi-"+str(massbin[0])+"-"+str(massbin[1]),"chi-"+str(massbin[0])+"-"+str(massbin[1]),len(chibins)-1,chibins)
            histcentral.Sumw2()
            histscaleup=TH1F("chi-"+str(massbin[0])+"-"+str(massbin[1])+"scaleUp","chi-"+str(massbin[0])+"-"+str(massbin[1])+"scaleUp",len(chibins)-1,chibins)
            histscaleup.Sumw2()
            histscaledown=TH1F("chi-"+str(massbin[0])+"-"+str(massbin[1])+"scaleDown","chi-"+str(massbin[0])+"-"+str(massbin[1])+"scaleDown",len(chibins)-1,chibins)
            histscaledown.Sumw2()
            for b in range(1,len(chibins)):
                xsec=[]
                i=0
                for scale in scales:
                    myhist=myfile.Get(f.replace(".root","")+"_"+"qcd_chi-"+str(massbin[0])+"-"+str(massbin[1])+"scale-"+str(scale[0])+"-"+str(scale[1])+"_addmu")
                    xsec.append(myhist.GetBinContent(b))
                    i+=1
                    if i==1:
                        central=myhist.GetBinContent(b)
                        histcentral.SetBinContent(b,central)
                    if i==7:
                        scale_up=max(xsec)
                        scale_down=min(xsec)
                        histscaleup.SetBinContent(b,scale_up)
                        histscaledown.SetBinContent(b,scale_down)
    
            if normalizeBack:
                histcentral.Scale(scaleFactorsmu[f.replace(".root","")][massbins.index(massbin)])
                histscaleup.Scale(scaleFactorsmu[f.replace(".root","")][massbins.index(massbin)])
                histscaledown.Scale(scaleFactorsmu[f.replace(".root","")][massbins.index(massbin)])
            histcentral.Write()
            histscaleup.Write()
            histscaledown.Write()
    
    for f in cimemfiles:
        myfile=TFile(f.replace("CIJET_","").replace("_mem",""),"UPDATE")
	print "updating",f.replace("CIJET_","").replace("_mem","")
        for massbin in massbins:
            histcentral=TH1F("chi-"+str(massbin[0])+"-"+str(massbin[1])+"backup","chi-"+str(massbin[0])+"-"+str(massbin[1]),len(chibins)-1,chibins)
            histcentral.Sumw2()
            histscaleup=TH1F("chi-"+str(massbin[0])+"-"+str(massbin[1])+"PDFUp","chi-"+str(massbin[0])+"-"+str(massbin[1])+"PDFUp",len(chibins)-1,chibins)
            histscaleup.Sumw2()
            histscaledown=TH1F("chi-"+str(massbin[0])+"-"+str(massbin[1])+"PDFDown","chi-"+str(massbin[0])+"-"+str(massbin[1])+"PDFDown",len(chibins)-1,chibins)
            histscaledown.Sumw2()
            for b in range(1,len(chibins)):
                xsec=[]
                i=0
                for i in range(0,57):
                    myhist=myfile.Get(f.replace(".root","")+"_"+"qcd_chi-"+str(massbin[0])+"-"+str(massbin[1])+"PDF-"+str(i)+"_addmem")
                    i+=1
                    if i==1:
                        central=myhist.GetBinContent(b)
                        histcentral.SetBinContent(b,central)
                    #print myhist
                    xsec.append(myhist.GetBinContent(b)-central)
                    if i==57:
                        pdf_up,pdf_down=calcHessianPDFUncert(xsec)
                        histscaleup.SetBinContent(b,central+pdf_up)
                        histscaledown.SetBinContent(b,central+pdf_down)
    
            if normalizeBack:
                histcentral.Scale(scaleFactorsmem[f.replace(".root","")][massbins.index(massbin)])
                histscaledown.Scale(scaleFactorsmem[f.replace(".root","")][massbins.index(massbin)])
                histscaleup.Scale(scaleFactorsmem[f.replace(".root","")][massbins.index(massbin)])
            histcentral.Write()
            histscaleup.Write()
            histscaledown.Write()
    
    
if compareUncert: 
    os.system("cp ~/../../../work/z/zhangj/private/dirPrelimExam13TeV/CMSSW_7_4_7_patch2/src/cmsusercode/chi_analysis/fastnlo/RunII/fnl5662i_v23_fix_CT14_ak4.root .")   # copy qcd file to current directory, this file will be used in the comparison
    
    ciqcdfilename="fnl5662i_cs_ct14nlo_30000_LL+.root" 

    hist1s=[]
    hist1scaleups=[]
    hist1scaledowns=[]
    hist1pdfups=[]
    hist1pdfdowns=[]
    hist2s=[]
    hist2scaleups=[]
    hist2scaledowns=[]
    hist2pdfups=[]
    hist2pdfdowns=[]

    file1=TFile("fnl5662i_v23_fix_CT14_ak4.root","UPDATE")
    for massbin in massbins[:6]:
        histname="chi-"+str(massbin[0])+"-"+str(massbin[1])
        h1=file1.Get(histname)
        h1scaleup=file1.Get(histname+"scaleUp")
        h1scaledown=file1.Get(histname+"scaleDown")
        h1pdfup=file1.Get(histname+"PDFUp")
        h1pdfdown=file1.Get(histname+"PDFDown")
        hist1=multiplyBinWidth(h1)
        hist1scaleup=multiplyBinWidth(h1scaleup)
        hist1scaledown=multiplyBinWidth(h1scaledown)
        hist1pdfup=multiplyBinWidth(h1pdfup)
        hist1pdfdown=multiplyBinWidth(h1pdfdown)
        scaleFactor=hist1.Integral()
        hist1.Scale(1./scaleFactor)
        hist1scaleup.Scale(1./scaleFactor)
        hist1scaledown.Scale(1./scaleFactor)
        hist1pdfup.Scale(1./scaleFactor)
        hist1pdfdown.Scale(1./scaleFactor)
        hist1.Write()
        hist1scaleup.Write()
        hist1scaledown.Write()
        hist1pdfup.Write()
        hist1pdfdown.Write()
    file1.Close()

    file1new=TFile("fnl5662i_v23_fix_CT14_ak4.root")
    for massbin in massbins[:6]:
        histname="chi-"+str(massbin[0])+"-"+str(massbin[1])
        hist1=file1new.Get(histname+"_norm")
        hist1scaleup=file1new.Get(histname+"scaleUp"+"_norm")
        hist1scaleup.Divide(hist1)
        hist1scaledown=file1new.Get(histname+"scaleDown"+"_norm")
        hist1scaledown.Divide(hist1)
        hist1pdfup=file1new.Get(histname+"PDFUp"+"_norm")
        hist1pdfup.Divide(hist1)
        hist1pdfdown=file1new.Get(histname+"PDFDown"+"_norm")
        hist1pdfdown.Divide(hist1)
        hist1s.append(hist1)
        hist1scaleups.append(hist1scaleup)
        hist1scaledowns.append(hist1scaledown)
        hist1pdfups.append(hist1pdfup)
        hist1pdfdowns.append(hist1pdfdown)

    file2=TFile.Open(ciqcdfilename)
    for massbin in massbins[:6]:
        histname="chi-"+str(massbin[0])+"-"+str(massbin[1])
        hist2=file2.Get(histname)
        hist2scaleup=file2.Get(histname+"scaleUp")
        hist2scaleup.Divide(hist2)
        hist2scaledown=file2.Get(histname+"scaleDown")
        hist2scaledown.Divide(hist2)
        hist2pdfup=file2.Get(histname+"PDFUp")
        hist2pdfup.Divide(hist2)
        hist2pdfdown=file2.Get(histname+"PDFDown")
        hist2pdfdown.Divide(hist2)
        hist2s.append(hist2)
        hist2scaleups.append(hist2scaleup)
        hist2scaledowns.append(hist2scaledown)
        hist2pdfups.append(hist2pdfup)
        hist2pdfdowns.append(hist2pdfdown)

    canvas=TCanvas("MyCanvas","MyCanvas",0,0,1200,900)
    saveName=ciqcdfilename.replace(".root","_xsec.pdf")
    saveName2=ciqcdfilename.replace(".root","_uncert.pdf")
    canvas.cd()
    canvas.Divide(3,2)
    
    legends=[]
    for j in range(len(massbins[:6])):
        
        legend=TLegend(0.4,0.73,0.79,0.9,(str(massbins[j][0])+"<m_{jj}<"+str(massbins[j][1])+" GeV"))
        legend.SetFillStyle(0)
        legend.AddEntry(hist1s[j],"2015 NLOJET","l")
        legend.AddEntry(hist2s[j],"2016 NLOJET+CIJET","l")
        legends.append(legend)

    for j in range(len(massbins[:6])):
        canvas.cd(j+1)
        pad1=TPad("","",0, 0, 1, 1)
        pad1.Draw()
        pad1.cd()
        hist2s[j].SetLineColor(2)
        hist2s[j].SetMaximum(hist2s[j].GetMaximum()*2)
        hist2s[j].GetXaxis().SetTitle("#chi_{dijet}")
        hist2s[j].Draw()
        hist1s[j].SetLineColor(1)
        hist1s[j].Draw("samehist")
        legends[j].Draw()

    canvas.SaveAs(saveName)

    canvas2=TCanvas("MyCanvas","MyCanvas",0,0,1200,900)
    canvas2.cd()
    canvas2.Divide(3,2)
    
    legends2=[]
    for j in range(len(massbins[:6])):
        
        legend=TLegend(0.2,0.5,0.8,0.9,(str(massbins[j][0])+"<m_{jj}<"+str(massbins[j][1])+" GeV"))
        legend.SetFillStyle(0)
        legend.AddEntry(hist1pdfups[j],"2015 NLOJET PDF Uncertainty","l")
        legend.AddEntry(hist1scaleups[j],"2015 NLOJET scale Uncertainty","l")
        legend.AddEntry(hist2pdfups[j],"2016 NLOJET+CIJET PDF Uncertainty","l")
        legend.AddEntry(hist2scaleups[j],"2016 NLOJET+CIJET scale Uncertainty","l")
        legends2.append(legend)

    for j in range(len(massbins[:6])):
        canvas2.cd(j+1)
        pad2=TPad("","",0, 0, 1, 1)
        pad2.Draw()
        pad2.cd()
        pad2.SetLeftMargin(0.05)
        pad2.SetBottomMargin(0.08)
        pad2.SetTopMargin(0.03)
        pad2.SetRightMargin(0.05)
        hist1pdfups[j].SetLineColor(4)
        hist1pdfups[j].SetLineStyle(2)
        hist1pdfups[j].SetMinimum(0.85)
        hist1pdfups[j].SetMaximum(1.5)
        hist1pdfups[j].GetXaxis().SetTitle("#chi_{dijet}")
        hist1pdfups[j].Draw("hist")
        hist1pdfdowns[j].SetLineColor(4)
        hist1pdfdowns[j].SetLineStyle(2)
        hist1pdfdowns[j].Draw("samehist")
        
        hist1scaleups[j].SetLineColor(6)
        hist1scaleups[j].SetLineStyle(2)
        hist1scaleups[j].GetXaxis().SetTitle("#chi_{dijet}")
        hist1scaleups[j].Draw("samehist")
        hist1scaledowns[j].SetLineColor(6)
        hist1scaledowns[j].SetLineStyle(2)
        hist1scaledowns[j].Draw("samehist")
        
        hist2pdfups[j].SetLineColor(1)
        hist2pdfups[j].SetLineStyle(1)
        hist2pdfups[j].GetXaxis().SetTitle("#chi_{dijet}")
        hist2pdfups[j].Draw("samehist")
        hist2pdfdowns[j].SetLineColor(1)
        hist2pdfdowns[j].SetLineStyle(1)
        hist2pdfdowns[j].Draw("samehist")
        
        hist2scaleups[j].SetLineColor(2)
        hist2scaleups[j].SetLineStyle(1)
        hist2scaleups[j].GetXaxis().SetTitle("#chi_{dijet}")
        hist2scaleups[j].Draw("samehist")
        hist2scaledowns[j].SetLineColor(2)
        hist2scaledowns[j].SetLineStyle(1)
        hist2scaledowns[j].Draw("samehist")
        
        
        hist1s[j].SetLineColor(1)
        hist1s[j].Draw("samehist")
        legends2[j].Draw()

    canvas2.SaveAs(saveName2)

    
    
    


    
    

    
    

    
