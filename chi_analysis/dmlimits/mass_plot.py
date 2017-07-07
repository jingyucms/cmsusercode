from ROOT import *
import ROOT,sys,os,math
from math import *
import numpy as np

gROOT.ForceStyle()
gStyle.SetLegendBorderSize(0)
gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)
gStyle.SetPadRightMargin(0.03)
gStyle.SetPadTopMargin(0.07)

def Gammaqq(gq,Mmed,mq,style):
    if style=="Axial":
        return gq**2*Mmed*math.pow((1-float(4*mq**2)/Mmed**2),1.5)*(1+2*float(mq**2)/Mmed**2)/(4*pi)
    elif style=="Vector":
        return gq**2*Mmed*math.pow((1-float(4*mq**2)/Mmed**2),0.5)/(4*pi)

def Gammaqq_tot(gq,Mmed,style):
    if Mmed>173:
        return 5*Gammaqq(gq,Mmed,0,style)+Gammaqq(gq,Mmed,173,style)
    else:
        return 5*Gammaqq(gq,Mmed,0,style)

def GammaDM(gDM,Mmed,mDM,style):
    if 2*mDM<=Mmed:
        if style=="Axial":
            return gDM**2*Mmed*math.pow((1-float(4*mDM**2)/Mmed**2),1.5)/(12*pi)
        elif style=="Vector":
            return gDM**2*Mmed*math.pow((1-float(4*mDM**2)/Mmed**2),0.5)*(1+2*float(mDM**2)/Mmed**2)/(12*pi)
    else:
        return 0

def A(gq,Mmed,mDM,style):
    return gq**2*Gammaqq_tot(gq,Mmed,style)/(Gammaqq_tot(gq,Mmed,style)+GammaDM(1,Mmed,mDM,style))

def B(gq,Mmed,mDM,style):
    return gq**4*GammaDM(1,Mmed,1,style)/(Gammaqq_tot(gq,Mmed,style)+GammaDM(1,Mmed,mDM,style))

def g_q(gq,Mmed,mDM,style):
    return math.pow((A(gq,Mmed,mDM,style)+math.pow(A(gq,Mmed,mDM,style)**2+4*B(gq,Mmed,mDM,style),0.5))*0.5,0.5)

def SetCurveStyle(gr,color,lineStyle,lineWidth,markerSize):
    gr.SetMarkerColor(color)
    gr.SetMarkerSize(markerSize)
    gr.SetLineColor(color)
    gr.SetLineWidth(lineWidth)
    gr.SetFillStyle(lineStyle)
    gr.SetFillColor(color)
    return 

if __name__=="__main__":

    doMonoJet=True
    doRelic=True

    filename="limitsLHCa_DMAxial_mdm1_v4.root"
    style="Axial"
    #filename="limitsLHCa_DMVector_mdm1_v4.root"
    #style="Vector"
    
    filein=TFile(filename)

    g_q_obs=filein.Get("gq_obs")
    g_q_exp=filein.Get("gq_exp")

    filein.Close()
    
    canvas=TCanvas("myCanvas","myCanvas",0,0,1800,1200)
    #canvas.SetLogx()
    
    m_m_exp=TGraph()
    
    m_m_obs=TGraph()

    mg=TMultiGraph()

    med_min=2500
    med_max=6000
    dm_min=-100
    dm_max=3000
    med_step=10
    dm_step=10
    
    meds_exp2={}
    meds_obs={}
    for mmed in np.linspace(med_min,med_max,num=int((med_max-med_min)/med_step+1)):
        meds_exp2[int(mmed)]=[]
        meds_obs[int(mmed)]=[]
        for mdm in np.linspace(dm_min,dm_max,num=int((dm_max-dm_min)/dm_step+1)):
            if g_q(1,mmed,mdm,style)>g_q_exp.Eval(mmed,0):
                meds_exp2[int(mmed)].append(mdm)
            if g_q(1,mmed,mdm,style)>g_q_obs.Eval(mmed,0):
                meds_obs[int(mmed)].append(mdm)

##     meds_obs={}
##     for mmed in np.linspace(med_min,med_max,num=int((med_max-med_min)/med_step+1)):
##         meds_obs[int(mmed)]=[]
##         for mdm in np.linspace(dm_min,dm_max,num=int((dm_max-dm_min)/dm_step+1)):
##             if g_q(mmed,mdm,style)>g_q_obs.Eval(mmed,0):
##                 #m_m_exp.SetPoint(m_m_exp.GetN(),mmed,mdm)
##                 meds_obs[int(mmed)].append(mdm)

    for mmed in np.linspace(med_min,med_max,num=int((med_max-med_min)/med_step+1)):
        if meds_exp2[int(mmed)]!=[]:
            mmed_low_exp=mmed
            for mdm in np.linspace(dm_max,dm_min,num=int((dm_max-dm_min)/dm_step+1)):
                m_m_exp.SetPoint(m_m_exp.GetN(),mmed,mdm)
            break
    
    for mmed in np.linspace(med_min,med_max,num=int((med_max-med_min)/med_step+1)):
        if meds_exp2[int(mmed)]!=[] and mmed!=mmed_low_exp:
            m_m_exp.SetPoint(m_m_exp.GetN(),mmed,meds_exp2[mmed][0])
            mmed_high_exp=mmed

    m_m_exp.SetPoint(m_m_exp.GetN(),mmed_high_exp,dm_max)

    for mmed in np.linspace(med_min,med_max,num=int((med_max-med_min)/med_step+1)):
        if meds_obs[int(mmed)]!=[]:
            mmed_low_obs=mmed
            for mdm in np.linspace(dm_max,dm_min,num=int((dm_max-dm_min)/dm_step+1)):
                m_m_obs.SetPoint(m_m_obs.GetN(),mmed,mdm)
            break
    
    for mmed in np.linspace(med_min,med_max,num=int((med_max-med_min)/med_step+1)):
        if meds_obs[int(mmed)]!=[] and mmed!=mmed_low_obs:
            m_m_obs.SetPoint(m_m_obs.GetN(),mmed,meds_obs[mmed][0])
            mmed_high_obs=mmed

    m_m_obs.SetPoint(m_m_obs.GetN(),mmed_high_obs,dm_max)
    
                    
    #print meds_obs[1750]

    #sys.exit()

    if doMonoJet:
        m_m_obs_monojet=TGraph()
        m_m_exp_monojet=TGraph()
        
        if "Axial" in filename:
            filemonojet=TFile("./fromZeynep/monojet_AV_MM_ICHEP2016_obs_g1.root")
        elif "Vector" in filename:
            filemonojet=TFile("./fromZeynep/monojet_V_MM_ICHEP2016_obs_g1.root")
        m_m_obs_monojet=filemonojet.Get("monojet_obs")

        if "Axial" in filename:
            filemonojet=TFile("./fromZeynep/monojet_AV_MM_ICHEP2016_exp_g1.root")
        elif "Vector" in filename:
            filemonojet=TFile("./fromZeynep/monojet_V_MM_ICHEP2016_exp_g1.root")
        m_m_exp_monojet=filemonojet.Get("monojet_exp")
        SetCurveStyle(m_m_obs_monojet,kRed+2,3004,202,0.1)
        mg.Add(m_m_obs_monojet)
        SetCurveStyle(m_m_exp_monojet,kRed-10,3004,202,0.1)
        mg.Add(m_m_exp_monojet)
        
    if doRelic:
        if "Axial" in filename:
            #filerelic=TFile("./MetxCombo2016/Relic/madDMv2_0_6/relicContour_A_g1.root")
            filerelic=TFile("./relic_axial_gq1.root")
            listrelic=filerelic.Get("mytlist")
            relic1=listrelic.At(0)
            #relic2=listrelic.At(1)
            SetCurveStyle(relic1,kGray+1,3005,202,0.1)
            #SetCurveStyle(relic2,kGray+1,3005,202,0.1)
            mg.Add(relic1)
            #mg.Add(relic2)
        elif "Vector" in filename:
            #filerelic=TFile("./MetxCombo2016/Relic/madDMv2_0_6/relicContour_V_g1.root")
            filerelic=TFile("./relic_vector_gq1.root")
            listrelic=filerelic.Get("mytlist")
            relic=listrelic.At(0)
            SetCurveStyle(relic,kGray+1,3005,202,0.1)
            mg.Add(relic)
    
    SetCurveStyle(m_m_exp,kAzure+6,3004,202,0.1)
    SetCurveStyle(m_m_obs,kAzure,3004,202,0.1)

    mg.Add(m_m_exp)
    mg.Add(m_m_obs)
    
    mg.Draw("apl")
    
    #mg.GetXaxis().SetRangeUser(0.,7000.)
    mg.GetXaxis().SetLimits(0.,9000.)
    mg.GetYaxis().SetRangeUser(0.,3000.)
    mg.SetName("exp_obs_MvsM")
    mg.GetXaxis().SetTitle("M_{Med} [GeV]")
    mg.GetYaxis().SetTitle("M_{DM} [GeV]")
    mg.GetYaxis().SetTitleOffset(1.)
    mg.GetXaxis().SetTitleOffset(0.9)
    mg.GetYaxis().SetLabelSize(0.035)
    mg.GetXaxis().SetLabelSize(0.035)
    mg.GetYaxis().SetTitleSize(0.045)
    mg.GetXaxis().SetTitleSize(0.045)

    f1 = TF1("f1","x/2.",0,6000)
    g1 = TGraph(f1)
    g1.SetLineColor(kGray+1)
    g1.SetLineStyle(kDashed)
    g1.Draw("same")
    
    legd=TLatex(3000,1600,"M_{Med} = 2 x m_{DM}")
    legd.SetTextAngle(42)
    legd.SetTextFont(42)
    legd.SetTextSize(0.040)
    legd.SetTextColor(kGray+1)
    legd.Draw("same")

    if doRelic:
        if "Axial" in filename:
            legrelic=TLatex(3000,1150,"#Omega_{c} h^{2} #geq 0.12")
            legrelic.SetTextAngle(44)
            legrelic.SetTextFont(42)
        elif "Vector" in filename:
            legrelic=TLatex(3000,310,"#Omega_{c} h^{2} #geq 0.12")
            legrelic.SetTextAngle(18.5)
            legrelic.SetTextFont(42)
        legrelic.SetTextColor(kGray+1)
        legrelic.SetTextSize(0.04)
        legrelic.Draw("same")

    if "Axial" in filename:
        Mediator="Axial"
        leg1=TLatex(6000, 2500,"#splitline{#bf{"+Mediator+"-vector mediator}}{#bf{& Dirac DM}}")
    elif "Vector" in filename:
        leg1=TLatex(5600, 2500,"#splitline{#bf{Vector mediator}}{#bf{& Dirac DM}}")
    #leg5=TLatex(6000, 2210,"#bf{Dirac DM}")
    leg4=TLatex(6400, 2010,"#splitline{#it{g_{q} = 1.0}}{#it{g_{DM} = 1.0}}")
    leg1.SetTextFont(42)
    leg4.SetTextFont(42)
    #leg5.SetTextFont(42)
    leg1.SetTextSize(0.040)
    leg4.SetTextSize(0.040)
    #leg5.SetTextSize(0.040)
    leg4.Draw("same")
    #leg5.Draw("same")
    leg1.Draw("same")

    leg=TLegend(0.62,0.13,0.91,0.55,"             CMS 95% CL")
    leg.SetFillStyle(0)
    leg.SetTextSize(0.034)
    leg.AddEntry(m_m_obs,"Dijet Chi Observed (35.9 fb^{-1} )","fl")
    leg.AddEntry(m_m_exp,"Dijet Chi Expected (35.9 fb^{-1} )","fl")
    if doMonoJet:
        leg.AddEntry(m_m_obs_monojet,"DM + j/V_{qq} Observed (12.9 fb^{-1} )","fl")
        leg.AddEntry(m_m_exp_monojet,"DM + j/V_{qq} Expected (12.9 fb^{-1} )","fl")
    leg.Draw()

    # CMS
    #leg2=TLatex(0,3050,"#bf{CMS} #it{Preliminary}")
    leg2=TLatex(0,3050,"#bf{CMS} #it{Supplementary}")
    leg2.SetTextFont(42)
    leg2.SetTextSize(0.04)
    # lumi
    leg3=TLatex(6500,3050,"12.9 & 35.9 fb^{-1} (13 TeV)")
    leg3.SetTextFont(42)
    leg3.SetTextSize(0.04)
    leg2.Draw("same")
    leg3.Draw("same")

    canvas.SaveAs(filename.replace("mdm1","mdmAll").replace(".root",".pdf"))

    fileout=TFile(filename.replace("mdm1","mdmAll"),"RECREATE")
    mg.Write()
    #mg_exp.Write()
    #mg_obs.Write()

    fileout.Close()

            
