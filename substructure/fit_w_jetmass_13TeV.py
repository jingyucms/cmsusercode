from ROOT import gROOT,gStyle,TH1F,TGaxis,TFile,TCanvas,TLegend,TLatex,RooFit,RooRealVar,RooDataHist,RooArgList,RooHistPdf,RooAbsReal,RooArgSet,RooChebychev,RooAddPdf,kDashed,kDotted,RooExponential,RooVoigtian,RooAbsData,RooGaussian,RooPolynomial,RooCategory,RooSimultaneous,RooDataSet,RooCmdArg,RooCBShape,RooBifurGauss,RooChi2Var

gROOT.ProcessLine(".L RooLogistics.cxx+")
gROOT.ProcessLine(".L RooExpAndGauss.C+")
gROOT.SetBatch(True)

from ROOT import RooLogistics,RooExpAndGauss

if __name__ == '__main__':
 plots = [("jetAK8_pruned_massCorr","pruned jet mass (GeV)"),
           ("jetAK8_softdrop_mass","softdrop jet mass (GeV)"),
           #("jetAK10_trimmed_massCorr","trimmed jet mass (GeV)", ),
	   #("jetAK8_pt","jet p_{T} (GeV)"),
	   #("jetAK8_eta","jet #eta"),
           ]
 cuts= [0,0.45,0.6,1.6,1.0,2.0]
 massmin=65
 massmax=165
 prefix="w_jet_mass13TeV_76_400_0"
 #prefix="w_jet_mass13TeV_400_0_massdrop0.4"
 
 signalSF=1.21
 signalweight=1.21 # adapt injected signal to data by hand

 mass=RooRealVar("mass","mass",(massmax-massmin)/5,massmin,massmax)
 s0=RooRealVar("s0","s0",85,80.,90.)
 s1=RooRealVar("s1","s1",8,6.,10.)
 sig=RooGaussian("sig","sig",mass,s0,s1) 

 files=[]
 
 for plot in plots:
  for fit in ["data","b","sb"]:
   datalist={}
   modellist={}
   pdflist=[]
   files=[]
   for cut in cuts[1:]:
    if cut<=1:
      #print prefix+"_"+plot[0]+str(cut)+".root"
      #f=TFile.Open(prefix+"_"+plot[0]+str(cut)+".root")
      #files+=[f]
      #canvas=f.Get("c1").GetListOfPrimitives()[0]
      #print [a for a in canvas.GetListOfPrimitives()]
      #hdata=canvas.GetListOfPrimitives()[1]
      #hqcd=canvas.GetListOfPrimitives()[3]
      #hvv=canvas.GetListOfPrimitives()[2]
      f=TFile.Open(prefix+".root")
      files+=[f]
      hdata=f.Get("plot"+plot[0]+str(cut)+"data")
      hqcd=f.Get("plot"+plot[0]+str(cut)+"QCD")
      hvv=f.Get("plot"+plot[0]+str(cut)+"V+jets")
      #hqcd.Scale(2600.)
      hqcd.Scale(hdata.Integral()/hqcd.Integral())
      hvv.Scale(2600.*signalSF)
      print hdata,hqcd,hvv
      integrals=eval(open(prefix+"_"+plot[0]+str(cut)+".txt").readline())
      print integrals
      datahist=hdata.Clone("datahist")
      if cuts.index(cut)==1:
        sumdatahist=hdata.Clone("datahist")
      else:
        sumdatahist.Add(hdata)
      qcdhist=hqcd.Clone("qcdhist")
      if cuts.index(cut)==1:
        sumqcdhist=hqcd.Clone("qcdhist")
      else:
        sumqcdhist.Add(hqcd)
      sbhist=hqcd.Clone("sbhist")
      #if integrals[2][1]>0:
      #  weight=integrals[1][1]/integrals[2][1]
      sbhist.Add(hvv,signalweight)
      sbhist.Scale(hqcd.Integral()/sbhist.Integral())
      mchist=sbhist.Clone("mchist")
      if cuts.index(cut)==1:
        summchist=sbhist.Clone("mchist")
      else:
        summchist.Add(sbhist)
      sighist=hvv.Clone("sighist")
      if cuts.index(cut)==1:
     	sumsighist=hvv.Clone("sighist")
      else:
     	sumsighist.Add(hvv)
   
    if fit=="data":
      if cut>1:
        data=RooDataHist("data"+str(cut),"data",RooArgList(mass),sumdatahist)
      else:
        data=RooDataHist("data"+str(cut),"data",RooArgList(mass),datahist)
    elif fit=="b":
      if cut>1:
        data=RooDataHist("data"+str(cut),"QCD",RooArgList(mass),sumqcdhist)
      else:
        data=RooDataHist("data"+str(cut),"QCD",RooArgList(mass),qcdhist)
    elif fit=="sb":
      if cut>1:
        data=RooDataHist("data"+str(cut),"QCD + V+jets",RooArgList(mass),summchist)
      else:
        data=RooDataHist("data"+str(cut),"QCD + V+jets",RooArgList(mass),mchist)
    if cut>1:
      signal=RooDataHist("signal"+str(cut),"signal",RooArgList(mass),sumsighist)
    else:
      signal=RooDataHist("signal"+str(cut),"signal",RooArgList(mass),sighist)
    #sig=RooHistPdf("sig","sig",RooArgSet(mass),signal)

    nsig=RooRealVar("nsig"+str(cut),"number of signal events",100,0,1e10)
    nbkg=RooRealVar("nbkg"+str(cut),"number of background events",100,0,1e10)
    nbkg1=RooRealVar("nbkg1"+str(cut),"number of background events",100,0,1e10)
    nbkg2=RooRealVar("nbkg2"+str(cut),"number of background events",100,0,1e10)

    l0=RooRealVar("l0","l0",100.,0.,1000.)
    l1=RooRealVar("l1","l1",1.,0.,1000.)
    l2=RooRealVar("l2","l2",1.,0.,1000.)
    #sigbkg=RooPolynomial("sigbkg"+str(cut),"bkg",mass,RooArgList(l0,l1,l2))
    #sigbkg=RooChebychev("sigbkg"+str(cut),"bkg",mass,RooArgList(l0,l1))
    sigbkg=RooLogistics("sigbkg"+str(cut),"bkg",mass,l0,l1)
    #sigbkg=RooExponential("sigbkg"+str(cut),"sigbkg",mass,l0)
    nsigref=RooRealVar("nsigref","number of signal events",100,0,1e10)
    sigmodel=RooAddPdf("sigmodel"+str(cut),"sig+bkg",RooArgList(sigbkg,sig),RooArgList(nbkg,nsigref))
    s0.setConstant(False)
    s1.setConstant(False) 
    sigmodel.fitTo(signal,RooFit.SumW2Error(True)) #,RooFit.Range("signal")
    sigmodel.fitTo(signal,RooFit.SumW2Error(True)) #,RooFit.Range("signal")
    sigmodel.fitTo(signal,RooFit.SumW2Error(True)) #,RooFit.Range("signal")
    chi2=RooChi2Var("chi2","chi2",sigmodel,signal,RooFit.DataError(RooAbsData.SumW2))
    nbins=data.numEntries()
    nfree=sigmodel.getParameters(data).selectByAttrib("Constant",False).getSize()
    s0.setConstant(True) 
    s1.setConstant(True) 

    if cut>=1:
      fullintegral=sumsighist.Integral()
    else:
      fullintegral=sighist.Integral()
    print "SIGNAL FRACTION",nsigref.getValV()/(nsigref.getValV()+nbkg.getValV())
    if nsigref.getValV()==0: continue

    if fit=="data":
      xframe=mass.frame(RooFit.Title("signal fraction in peak ="+str(int(nsigref.getValV()/(nsigref.getValV()+nbkg.getValV())*1000.)/1000.)+"+-"+str(int(nsigref.getError()/(nsigref.getValV()+nbkg.getValV())*1000.)/1000.)+", #chi^{2}/DOF = "+str(int((chi2.getVal()/(nbins-nfree))*10.)/10.)))
      signal.plotOn(xframe,RooFit.DataError(RooAbsData.SumW2))
      sigmodel.plotOn(xframe,RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
      sigmodel.plotOn(xframe,RooFit.Components("sigbkg"+str(cut)),RooFit.LineStyle(kDashed),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
      sigmodel.plotOn(xframe,RooFit.Components("sig"),RooFit.LineStyle(kDotted),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
      canvas=TCanvas("c3","c3",0,0,600,600)
      xframe.Draw()
      canvas.SaveAs(prefix+"_"+plot[0]+str(cut)+"_sigfit.pdf")

    a0=RooRealVar("a0"+str(cut),"a0",100.,0.,1000.)
    a1=RooRealVar("a1"+str(cut),"a1",100.,0.,1000.)
    a2=RooRealVar("a2"+str(cut),"a2",50.,0.,1000.)
    a3=RooRealVar("a3"+str(cut),"a3",0.1,0.,1000.)
    b0=RooRealVar("b0"+str(cut),"b0",120.,0.,100.)
    b1=RooRealVar("b1"+str(cut),"b1",50.,0.,100.)
    b2=RooRealVar("b2"+str(cut),"b2",50.,0.,100.)
    c0=RooRealVar("c0"+str(cut),"c0",100.,-1000.,1000.)
    c1=RooRealVar("c1"+str(cut),"c1",100.,-1000.,1000.)
    c2=RooRealVar("c2"+str(cut),"c2",50.,-1000.,1000.)
    c3=RooRealVar("c3"+str(cut),"c3",0.1,-1000.,1000.)
    #bkg=RooVoigtian("bkg"+str(cut),"bkg",mass,a0,a1,a2)
    bkg=RooLogistics("bkg"+str(cut),"bkg",mass,a0,a1)
    #bkg=RooExpAndGauss("bkg"+str(cut),"bkg",mass,b0,b1,b2)
    #bkg=RooCBShape("bkg"+str(cut),"bkg",mass,a0,a1,a2,a3)
    #bkg=RooBifurGauss("bkg"+str(cut),"bkg",mass,b0,b1,b2)
    #bkg=RooPolynomial("bkg"+str(cut),"bkg",mass,RooArgList(c0,c1,c2))
    
    #bkg1=RooVoigtian("bkg1"+str(cut),"bkg1",mass,a0,a1,a2)
    #bkg1=RooPolynomial("bkg1"+str(cut),"bkg1",mass,RooArgList(a0,a1))
    #bkg2=RooLogistics("bkg2"+str(cut),"bkg2",mass,b0,b1)
    #bkg=RooAddPdf("bkg"+str(cut),"bkg1+bkg2",RooArgList(bkg1,bkg2),RooArgList(nbkg1,nbkg2))
    
    model=RooAddPdf("model"+str(cut),"sig+bkg",RooArgList(bkg,sig),RooArgList(nbkg,nsig))
    pdflist+=[nsig,nbkg,sig,bkg,a0,a1,a2,a3,b0,b1,b2]

    if fit=="b":
      bkgmodel=RooAddPdf("bkgmodel"+str(cut),"bkg",RooArgList(bkg),RooArgList(nbkg))
      bkgmodel.fitTo(data,RooFit.SumW2Error(True)) 
      bkgmodel.fitTo(data,RooFit.SumW2Error(True)) 
      bkgmodel.fitTo(data,RooFit.SumW2Error(True)) 
      chi2=RooChi2Var("chi2","chi2",bkgmodel,data,RooFit.DataError(RooAbsData.SumW2))
      nbins=data.numEntries()
      nfree=bkgmodel.getParameters(data).selectByAttrib("Constant",False).getSize()
      xframe=mass.frame()
      data.plotOn(xframe,RooFit.DataError(RooAbsData.SumW2))
      bkgmodel.plotOn(xframe,RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
      canvas=TCanvas("c4","c4",0,0,600,600)
      xframe.Draw()
      xframe.SetTitle("#chi^{2}/DOF = "+str(int((chi2.getVal()/(nbins-nfree))*10.)/10.))
      xframe.Draw()
      canvas.SaveAs(prefix+"_"+plot[0]+str(cut)+"_bkgfit.pdf")

    datalist[cut]=data
    modellist[cut]=model
    if fit=="data":
      model.fitTo(data) 
      model.fitTo(data) 
      model.fitTo(data) 
      chi2=RooChi2Var("chi2","chi2",model,data)
    else:
      model.fitTo(data,RooFit.SumW2Error(True))
      model.fitTo(data,RooFit.SumW2Error(True))
      model.fitTo(data,RooFit.SumW2Error(True))
      chi2=RooChi2Var("chi2","chi2",model,data,RooFit.DataError(RooAbsData.SumW2))
    nbins=data.numEntries()
    nfree=model.getParameters(data).selectByAttrib("Constant",False).getSize()
    nsigv=nsig.getValV()
    nsige=nsig.getError()
    if integrals[1][1]>0:
      musigv=nsigv/nsigref.getValV()*fullintegral/(integrals[1][1]*2600.*signalSF)
      musige=nsige/nsigref.getValV()*fullintegral/(integrals[1][1]*2600.*signalSF)
    else:
      musigv=9999.
      musige=9999.
    #if fit=="sb":
    #  musigv/=signalweight
    #  musige/=signalweight

    #N(sig)="+str(int(nsigv))+"+-"+str(int(nsige))+", 
    xframe=mass.frame(RooFit.Title("#mu(sig)="+str(int(musigv*1000.)/1000.)+"+-"+str(int(musige*1000.)/1000.)+", #chi^{2}/DOF = "+str(int((chi2.getVal()/(nbins-nfree))*10.)/10.)))
    if fit=="data":
      data.plotOn(xframe)
    else:
      data.plotOn(xframe,RooFit.DataError(RooAbsData.SumW2))
    model.plotOn(xframe,RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
    model.plotOn(xframe,RooFit.Components("bkg"+str(cut)),RooFit.LineStyle(kDashed),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
    model.plotOn(xframe,RooFit.Components("sig"),RooFit.LineStyle(kDotted),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
    canvas=TCanvas("c2","c2",0,0,600,600)
    xframe.Draw()
    canvas.SaveAs(prefix+"_"+plot[0]+str(cut)+"_fit"+fit+".pdf")

   sample=RooCategory("sample","sample")
   datasets=[]
   for cut in cuts[1:-1]:
     sample.defineType(str(cut))
     datasets+=[RooFit.Import(str(cut),datalist[cut])]
   combData=RooDataHist("combData","combined data",RooArgList(mass),RooFit.Index(sample),*datasets)
   simPdf=RooSimultaneous("simPdf","simultaneous pdf",sample)
   for cut in cuts[1:-1]:
     simPdf.addPdf(modellist[cut],str(cut)) 
   #simPdf.fitTo(combData)
   #simPdf.fitTo(combData)
   #simPdf.fitTo(combData)
