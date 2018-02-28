from ROOT import gROOT,gStyle,TH1F,TGaxis,TFile,TCanvas,TLegend,TLatex,RooFit,RooRealVar,RooDataHist,RooArgList,RooHistPdf,RooAbsReal,RooArgSet,RooChebychev,RooAddPdf,kDashed,kDotted,RooExponential,RooVoigtian,RooAbsData,RooGaussian,RooPolynomial,RooCategory,RooSimultaneous,RooDataSet,RooCmdArg,RooCBShape,RooBifurGauss,RooChi2Var,RooFormulaVar,kBlue,kRed,kDashDotted

gROOT.ProcessLine(".L RooLogistics.cxx+")
gROOT.ProcessLine(".L RooExpAndGauss.C+")
gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetTitleOffset(1.4,"Y")
gStyle.SetPadLeftMargin(0.18)
gStyle.SetPadBottomMargin(0.15)
gStyle.SetPadTopMargin(0.08)
gStyle.SetPadRightMargin(0.08)
gStyle.SetMarkerSize(0.5)
gStyle.SetHistLineWidth(1)
#gStyle.SetStatFontSize(0.020)
gStyle.SetTitleSize(0.06, "XYZ")
gStyle.SetLabelSize(0.05, "XYZ")
gStyle.SetNdivisions(506, "XYZ")
gStyle.SetLegendBorderSize(0)

from ROOT import RooLogistics,RooExpAndGauss

if __name__ == '__main__':
 plots = [("mass_mmdt","MMDT jet mass (GeV)"),
           ]
 scenarios=[#(21,21),(22,22),(23,23),(24,24) #tau21
            #(25,25),(26,26),(26,25),(27,27),(27,26),(27,25),(28,28), #n2b1
            #(61,61),(62,62),(63,63),(64,64),(65,65),(66,66),(67,67),(68,68),(69,69), #ddt n2b1
	    #(61,62),(62,63),(63,64),(64,65),(65,66),(66,67),(67,68),(68,69), #ddt n2b1
	    #(61,63),(62,64),(63,65),(64,66),(65,67),(66,68),(67,69), #ddt n2b1
	    #(31,31),(32,32),(33,33),(34,34), #pt300 n2b1
	    #(35,35),(36,36),(37,37),(38,38), #pt400 n2b1
            #(62,62),(63,63),(64,64),(65,65),(66,66),(67,67), #pt500 ddt n2b1
	    #(71,71),(72,72),(73,73),(74,74),(75,75),(76,76), #pt300 ddt n2b1
	    #(81,81),(82,82),(83,83),(84,84),(85,85),(86,86), #pt400 ddt n2b1
	    #(91,91),(92,92),(93,93),(94,94),(95,95),(96,96), #pt500 ddt n2b2
	    #(101,101),(102,102),(103,103),(104,104),(105,105),(106,106), #pt300 ddt n2b2
	    #(111,111),(112,112),(113,113),(114,114),(115,115),(116,116), #pt400 ddt n2b2
	    #(27,27),
	    #(64,64),
	    #(74,74),
	    #(83,83),
	    #(94,94),
	    (66,66),
	    #(75,75),
	    #(85,85),
	    #(95,95),
	    ]
 #scenarios=[(73,73),(74,74)]
 #scenarios=[(99,99)]
 massmin=50#50#65
 massmax=150# 130(pT=300 ddtn2b1 and all n2b1) or 150 (pT=400/500 ddtn2b1)
 #lumi=40000#/pb
 lumi=3000000#/pb
 prefix="w_jet_wmass"
 
 signalSF=1.
 signalweight=1. # adapt injected signal to data by hand
 #doubleBeff=0.85 #loose
 #doubleBfake=0.1
 #doubleBeff=0.75 #medium
 #doubleBfake=0.05
 doubleBeff=0.45 #tight
 doubleBfake=0.01
 #doubleBeff=0.30 #super tight
 #doubleBfake=0.005
 #doubleBeff=0.10 #mega tight
 #doubleBfake=0.001
 correlateBackgroundFitParameters=False

 mass=RooRealVar("mass","m_{mMDT} (GeV)",(massmax-massmin),massmin,massmax)
 mass.setBins((massmax-massmin))
 meanW=RooRealVar("meanW","meanW",81,71.,91.)
 meanWZ=RooRealVar("meanWZ","meanWZ",10,4.,14.)
 meanZ=RooFormulaVar("meanZ","@0+@1",RooArgList(meanW,meanWZ));
 widthWZ=RooRealVar("widthWZ","widthWZ",8,5.,10.)
 sigW=RooGaussian("sigW","sigW",mass,meanW,widthWZ) 
 sigZ=RooGaussian("sigZ","sigZ",mass,meanZ,widthWZ)

 files=[]
 
 for Wonly in [True,False]:
  for plot in plots:
   for scenario,btagscenario in scenarios:
    pseudodata={}
    for fit in ["b","sb","data"]:
     datalist={}
     modellist={}
     pdflist=[]
     files=[]
     if correlateBackgroundFitParameters and Wonly==False:
       a0corr=RooRealVar("a0","a0",100.,0.,1000.)
       a1corr=RooRealVar("a1","a1",100.,0.,1000.)
     for category in ["","anti-btag","btag"]:
      if category=="btag":
  	 altscenario=btagscenario
      else:
  	 altscenario=scenario
      if Wonly and category!="": continue
      name=str(altscenario)+category
      if Wonly:
  	name+="Wonly"
      else:
  	name+="WvsZ"
      f=TFile.Open(prefix+"_"+str(altscenario)+"_out.root")
      files+=[f]
      if scenario < 60:
     	 hqcd=f.Get("plot"+plot[0]+"3")
     	 hqcd.Scale(lumi*32100./2185120) #HT500
     	 hqcdadd=f.Get("plot"+plot[0]+"4")
     	 hqcd.Add(hqcdadd,lumi*6831./1713079) #HT700
     	 hqcdadd=f.Get("plot"+plot[0]+"5")
     	 hqcd.Add(hqcdadd,lumi*1207./1362432) #HT1000
     	 hqcdadd=f.Get("plot"+plot[0]+"6")
     	 hqcd.Add(hqcdadd,lumi*119.9/668887) #HT1500
     	 hqcdadd=f.Get("plot"+plot[0]+"7")
     	 hqcd.Add(hqcdadd,lumi*25.24/689668) #HT2000
      else:
     	 hqcd=f.Get("plot"+plot[0]+"3")
     	 hqcd.Scale(lumi*3.50e+05/1634880) #HT300
     	 hqcdadd=f.Get("plot"+plot[0]+"4")
     	 hqcd.Add(hqcdadd,lumi*32100./2185120) #HT500
     	 hqcdadd=f.Get("plot"+plot[0]+"5")
     	 hqcd.Add(hqcdadd,lumi*6831./1713079) #HT700
     	 hqcdadd=f.Get("plot"+plot[0]+"6")
     	 hqcd.Add(hqcdadd,lumi*1207./1362432) #HT1000
     	 hqcdadd=f.Get("plot"+plot[0]+"7")
     	 hqcd.Add(hqcdadd,lumi*119.9/668887) #HT1500
     	 hqcdadd=f.Get("plot"+plot[0]+"8")
     	 hqcd.Add(hqcdadd,lumi*25.24/689668) #HT2000
      hvvW=f.Get("plot"+plot[0]+"1")
      #hvvW.Scale(lumi*95.14/636594) #HT600 WJetsToQQ_HT-600toInf_tarball
      hvvW.Scale(lumi*95.14/217099) #HT600 processed-output.dat-rth:W
      hvvZ=f.Get("plot"+plot[0]+"2")
      #hvvZ.Scale(lumi*4.134e+01/671159) #HT600 ZJetsToQQ_HT600toInf_gridpack (old wrong? number 1005952)
      hvvZ.Scale(lumi*4.134e+01/1341291) #HT600 processed-output.dat-rth:Z01
      #hvvZ.Scale(lumi*1036./1389394) #HT180 ZJetsFullyHadronic_HT180_LO_MLM_tarball
      qcdhist=hqcd.Clone("qcdhist")
      sigWhist=hvvW.Clone("sigWhist")
      sigWhist.Scale(signalSF)
      sigZhist=hvvZ.Clone("sigZhist")
      sigZhist.Scale(signalSF)
      if category=="btag":
  	qcdhist.Scale(doubleBfake)
  	sigWhist.Scale(doubleBfake)
  	sigZhist.Scale(0.1512*doubleBeff+(1.-0.1512)*doubleBfake)
      if category=="anti-btag":
  	qcdhist.Scale(1.-doubleBfake)
  	sigWhist.Scale(1.-doubleBfake)
  	sigZhist.Scale(0.1512*(1.-doubleBeff)+(1.-0.1512)*(1.-doubleBfake))
      sighist=sigWhist.Clone("sighist")
      sighist.Add(sigZhist)
      sbhist=hqcd.Clone("sbhist")
      sbhist.Add(sighist,signalweight)
    
      if fit=="data":
  	data=pseudodata[name]
      elif fit=="b":
  	data=RooDataHist("data"+name,"QCD",RooArgList(mass),qcdhist)
      elif fit=="sb":
  	data=RooDataHist("data"+name,"QCD + V+jets",RooArgList(mass),sbhist)
      signal=RooDataHist("signal"+name,"signal",RooArgList(mass),sighist)
      signalW=RooDataHist("signalW"+name,"signalW",RooArgList(mass),sigWhist)
      signalZ=RooDataHist("signalZ"+name,"signalZ",RooArgList(mass),sigZhist)

      nsigbkg=RooRealVar("nsigbkg"+name,"number of signal background events",sighist.Integral(),0,10*sighist.Integral())
      nbkg=RooRealVar("nbkg"+name,"number of background events",qcdhist.Integral(),0,10*qcdhist.Integral())
      nbkg1=RooRealVar("nbkg1"+name,"number of background events",qcdhist.Integral(),0,10*qcdhist.Integral())
      nbkg2=RooRealVar("nbkg2"+name,"number of background events",qcdhist.Integral(),0,10*qcdhist.Integral())

      l0=RooRealVar("l0","l0",100.,0.,1000.)
      l1=RooRealVar("l1","l1",1.,0.,1000.)
      l2=RooRealVar("l2","l2",1.,0.,1000.)
      #sigbkg=RooPolynomial("sigbkg"+name,"bkg",mass,RooArgList(l0,l1,l2))
      #sigbkg=RooChebychev("sigbkg"+name,"bkg",mass,RooArgList(l0,l1))
      sigbkg=RooLogistics("sigbkg"+name,"bkg",mass,l0,l1)
      #sigbkg=RooExponential("sigbkg"+name,"sigbkg",mass,l0)
      nsigref=RooRealVar("nsigref"+name,"number of signal events",sighist.Integral(),0,10*sighist.Integral())
      nsigrefW=RooRealVar("nsigrefW"+name,"number of signal W events",sigWhist.Integral(),0,10*sigWhist.Integral())
      nsigrefZ=RooRealVar("nsigrefZ"+name,"number of signal Z events",sigZhist.Integral(),0,10*sigZhist.Integral())
      sigWfrac=RooRealVar("sigWfrac"+name,"fraction of W in signal",0.5,0,1.0)
      sig=RooAddPdf("sig"+name,"sig"+name,sigW,sigZ,sigWfrac) ;
      sigmodel=RooAddPdf("sigmodel"+name,"sig+sigbkg",RooArgList(sigbkg,sig),RooArgList(nsigbkg,nsigref))
      meanW.setConstant(False)
      meanWZ.setConstant(False) 
      widthWZ.setConstant(False) 
      sigWfrac.setConstant(False)

      sigmodelW=RooAddPdf("sigmodelW"+name,"sigW",RooArgList(sigbkg,sigW),RooArgList(nsigbkg,nsigrefW))
      sigmodelW.fitTo(signalW,RooFit.SumW2Error(True))
      sigmodelW.fitTo(signalW,RooFit.SumW2Error(True))
      sigmodelW.fitTo(signalW,RooFit.SumW2Error(True))
      xframe=mass.frame(RooFit.Title("             m="+str(int((meanW.getValV())*1000.)/1000.)+"#pm"+str(int(meanW.getError()*1000.)/1000.)+" GeV"))
      signalW.plotOn(xframe,RooFit.DataError(RooAbsData.SumW2))
      sigmodelW.plotOn(xframe,RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
      canvas=TCanvas("c3","c3",0,0,600,600)
      xframe.GetYaxis().SetTitle("Events")
      xframe.Draw()
      canvas.SaveAs(prefix+"_"+plot[0]+name+"_sigWfit.pdf")
      meanW.setConstant(True)
      widthWZ.setConstant(True) 
      sigmodelZ=RooAddPdf("sigmodelZ"+name,"sigZ",RooArgList(sigbkg,sigZ),RooArgList(nsigbkg,nsigrefZ))
      sigmodelZ.fitTo(signalZ,RooFit.SumW2Error(True))
      sigmodelZ.fitTo(signalZ,RooFit.SumW2Error(True))
      sigmodelZ.fitTo(signalZ,RooFit.SumW2Error(True))
      xframe=mass.frame(RooFit.Title("             #Delta m="+str(int((meanWZ.getValV())*1000.)/1000.)+"#pm"+str(int(meanWZ.getError()*1000.)/1000.)+" GeV"))
      signalZ.plotOn(xframe,RooFit.DataError(RooAbsData.SumW2))
      sigmodelZ.plotOn(xframe,RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
      canvas=TCanvas("c3","c3",0,0,600,600)
      xframe.GetYaxis().SetTitle("Events")
      xframe.Draw()
      canvas.SaveAs(prefix+"_"+plot[0]+name+"_sigZfit.pdf")
      sigWfrac.setVal(nsigrefW.getValV()/(nsigrefW.getValV()+nsigrefZ.getValV()))
      meanWZ.setConstant(True) 
      sigWfrac.setConstant(True)

      sigmodel.fitTo(signal,RooFit.SumW2Error(True))
      sigmodel.fitTo(signal,RooFit.SumW2Error(True))
      sigmodel.fitTo(signal,RooFit.SumW2Error(True))
      chi2=RooChi2Var("chi2","chi2",sigmodel,signal,RooFit.DataError(RooAbsData.SumW2))
      nbins=data.numEntries()
      nfree=sigmodel.getParameters(data).selectByAttrib("Constant",False).getSize()
      refmass=meanW.getValV()
      meanW.setConstant(False) # let W mass float
      if not Wonly:
  	meanWZ.setConstant(False) # let Z mass float

      print "SIGNAL FRACTION",nsigref.getValV()/(nsigref.getValV()+nsigbkg.getValV())
      if nsigref.getValV()==0: continue

      if fit=="sb":
  	xframe=mass.frame(RooFit.Title("             signal fraction in peak ="+str(int(nsigref.getValV()/(nsigref.getValV()+nsigbkg.getValV())*1000.)/1000.)+"#pm"+str(int(nsigref.getError()/(nsigref.getValV()+nsigbkg.getValV())*1000.)/1000.)+", #chi^{2}/N="+str(int((chi2.getVal()/(nbins-nfree))*10.)/10.)))
  	signal.plotOn(xframe,RooFit.DataError(RooAbsData.SumW2))
  	sigmodel.plotOn(xframe,RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
  	sigmodel.plotOn(xframe,RooFit.Components("sigbkg"+name),RooFit.LineStyle(kDashed),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
  	sigmodel.plotOn(xframe,RooFit.Components("sigW"),RooFit.LineStyle(kDotted),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
  	sigmodel.plotOn(xframe,RooFit.Components("sigZ"),RooFit.LineStyle(kDashDotted),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
  	canvas=TCanvas("c3","c3",0,0,600,600)
        xframe.GetYaxis().SetTitle("Events")
  	xframe.Draw()
  	canvas.SaveAs(prefix+"_"+plot[0]+name+"_sigfit.pdf")

      a0=RooRealVar("a0"+name,"a0",100.,0.,1000.)
      a1=RooRealVar("a1"+name,"a1",100.,0.,1000.)
      a2=RooRealVar("a2"+name,"a2",50.,0.,1000.)
      a3=RooRealVar("a3"+name,"a3",0.1,0.,1000.)
      b0=RooRealVar("b0"+name,"b0",120.,0.,100.)
      b1=RooRealVar("b1"+name,"b1",50.,0.,100.)
      b2=RooRealVar("b2"+name,"b2",50.,0.,100.)
      c0=RooRealVar("c0"+name,"c0",0.,-1000.,1000.)
      c1=RooRealVar("c1"+name,"c1",0.,-1000.,1000.)
      c2=RooRealVar("c2"+name,"c2",50.,-1000.,1000.)
      c3=RooRealVar("c3"+name,"c3",0.1,-1000.,1000.)
      #bkg=RooVoigtian("bkg"+name,"bkg",mass,a0,a1,a2)
      if correlateBackgroundFitParameters and Wonly==False:
        bkg=RooLogistics("bkg"+name,"bkg",mass,a0corr,a1corr)
      else:
        bkg=RooLogistics("bkg"+name,"bkg",mass,a0,a1)
      #bkg=RooExpAndGauss("bkg"+name,"bkg",mass,b0,b1,b2)
      #bkg=RooCBShape("bkg"+name,"bkg",mass,a0,a1,a2,a3)
      #bkg=RooBifurGauss("bkg"+name,"bkg",mass,b0,b1,b2)
      #if scenario>=60:
      #bkg=RooPolynomial("bkg"+name,"bkg",mass,RooArgList(c0,c1))
      #bkg=RooChebychev("bkg"+name,"bkg",mass,RooArgList(c0,c1))
      
      #bkg1=RooVoigtian("bkg1"+name,"bkg1",mass,a0,a1,a2)
      #bkg1=RooPolynomial("bkg1"+name,"bkg1",mass,RooArgList(a0,a1))
      #bkg2=RooLogistics("bkg2"+name,"bkg2",mass,b0,b1)
      #bkg=RooAddPdf("bkg"+name,"bkg1+bkg2",RooArgList(bkg1,bkg2),RooArgList(nbkg1,nbkg2))
      
      nsig=RooRealVar("nsig"+name,"number of signal events",signalweight*nsigref.getValV(),0,10*signalweight*nsigref.getValV())
      model=RooAddPdf("model"+name,"sig+bkg",RooArgList(bkg,sig),RooArgList(nbkg,nsig))
      pdflist+=[nsig,nbkg,sig,sigWfrac,bkg,a0,a1,a2,a3,b0,b1,b2,c0,c1,c2,c3]

      if fit=="b":
  	bkgmodel=RooAddPdf("bkgmodel"+name,"bkg",RooArgList(bkg),RooArgList(nbkg))
  	bkgmodel.fitTo(data,RooFit.SumW2Error(True)) 
  	bkgmodel.fitTo(data,RooFit.SumW2Error(True)) 
  	bkgmodel.fitTo(data,RooFit.SumW2Error(True)) 
  	chi2=RooChi2Var("chi2","chi2",bkgmodel,data,RooFit.DataError(RooAbsData.SumW2))
  	nbins=data.numEntries()
  	nfree=bkgmodel.getParameters(data).selectByAttrib("Constant",False).getSize()
  	xframe=mass.frame(RooFit.Title("            #chi^{2}/N="+str(int((chi2.getVal()/(nbins-nfree))*10.)/10.)))
  	data.plotOn(xframe,RooFit.DataError(RooAbsData.SumW2),RooFit.MarkerSize(1))
  	bkgmodel.plotOn(xframe,RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
  	canvas=TCanvas("c4","c4",0,0,600,600)
        xframe.GetYaxis().SetTitle("Events")
  	xframe.Draw()
  	canvas.SaveAs(prefix+"_"+plot[0]+name+"_bkgfit.pdf")
  	print "generating pseudodata", nbkg.getValV()+nsigref.getValV()
  	pseudodata[name]=model.generateBinned(RooArgSet(mass),nbkg.getValV()+nsigref.getValV())

      datalist[name]=data
      modellist[name]=model
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
      if sighist.Integral()>0:
  	musigv=nsigv/nsigref.getValV()
  	musige=nsige/nsigref.getValV()
      else:
  	musigv=9999.
  	musige=9999.
      #if fit=="sb":
      #  musigv/=signalweight
      #  musige/=signalweight

      print "N(sig)="+str(int(nsigv))+"#pm"+str(int(nsige))
      if meanWZ.isConstant():
  	#xframe=mass.frame(RooFit.Title("m="+str(int((meanW.getValV())*1000.)/1000.)+"#pm"+str(int(meanW.getError()*1000.)/1000.)+" GeV, #mu_{#sigma}="+str(int(musigv*1000.)/1000.)+"#pm"+str(int(musige*1000.)/1000.)+", #chi^{2}/N="+str(int((chi2.getVal()/(nbins-nfree))*10.)/10.)))
  	xframe=mass.frame(RooFit.Title("            m="+str(int((meanW.getValV())*1000.)/1000.)+"#pm"+str(int(meanW.getError()*1000.)/1000.)+" GeV, #chi^{2}/N="+str(int((chi2.getVal()/(nbins-nfree))*10.)/10.)))
      else:
  	#xframe=mass.frame(RooFit.Title("#Delta m="+str(int((meanWZ.getValV()-refmass)*1000.)/1000.)+"#pm"+str(int(meanWZ.getError()*1000.)/1000.)+" GeV, #mu_{#sigma}="+str(int(musigv*1000.)/1000.)+"#pm"+str(int(musige*1000.)/1000.)+", #chi^{2}/N="+str(int((chi2.getVal()/(nbins-nfree))*10.)/10.)))
  	xframe=mass.frame(RooFit.Title("            #Delta m="+str(int((meanWZ.getValV()-refmass)*1000.)/1000.)+"#pm"+str(int(meanWZ.getError()*1000.)/1000.)+" GeV, #chi^{2}/N="+str(int((chi2.getVal()/(nbins-nfree))*10.)/10.)))
      if fit=="data":
  	data.plotOn(xframe,RooFit.MarkerSize(1))
      else:
  	data.plotOn(xframe,RooFit.DataError(RooAbsData.SumW2),RooFit.MarkerSize(1))
      model.plotOn(xframe,RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
      model.plotOn(xframe,RooFit.Components("bkg"+name),RooFit.LineStyle(kDashed),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
      model.plotOn(xframe,RooFit.Components("sigW"),RooFit.LineStyle(kDotted),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
      model.plotOn(xframe,RooFit.Components("sigZ"),RooFit.LineStyle(kDashDotted),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
      canvas=TCanvas("c2","c2",0,0,600,600)
      xframe.GetYaxis().SetTitle("Events")
      xframe.Draw()
      canvas.SaveAs(prefix+"_"+plot[0]+name+"_fit"+fit+".pdf")
      canvas.SaveAs(prefix+"_"+plot[0]+name+"_fit"+fit+".root")

     if Wonly: continue

     if fit=="data":
      sample=RooCategory("sample","sample")
      datasets=[]
      for category in ["anti-btag","btag"]:
  	if category=="btag":
  	  altscenario=btagscenario
  	else:
  	  altscenario=scenario
  	name=str(altscenario)+category
        name+="WvsZ"
  	sample.defineType(name)
  	datasets+=[RooFit.Import(name,datalist[name])]
      combData=RooDataHist("combData","combined data",RooArgList(mass),RooFit.Index(sample),*datasets)
      simPdf=RooSimultaneous("simPdf","simultaneous pdf",sample)
      for category in ["anti-btag","btag"]:
  	if category=="btag":
  	  altscenario=btagscenario
  	else:
  	  altscenario=scenario
  	name=str(altscenario)+category
        name+="WvsZ"
  	simPdf.addPdf(modellist[name],name) 
      simPdf.fitTo(combData)
      simPdf.fitTo(combData)
      simPdf.fitTo(combData)

      #xframe=mass.frame(RooFit.Title("#Delta m="+str(int((meanWZ.getValV())*1000.)/1000.)+"#pm"+str(int(meanWZ.getError()*1000.)/1000.)+" GeV, #mu_{#sigma}="+str(int(musigv*1000.)/1000.)+"#pm"+str(int(musige*1000.)/1000.)+", #chi^{2}/N="+str(int((chi2.getVal()/(nbins-nfree))*10.)/10.)))
      xframe=mass.frame(RooFit.Title("             #Delta m="+str(int((meanWZ.getValV())*1000.)/1000.)+"#pm"+str(int(meanWZ.getError()*1000.)/1000.)+" GeV, #chi^{2}/N="+str(int((chi2.getVal()/(nbins-nfree))*10.)/10.)))
      for category in ["anti-btag","btag"]:
  	if category=="btag":
  	  altscenario=btagscenario
	  color=kRed
  	else:
  	  altscenario=scenario
	  color=kBlue
  	name=str(altscenario)+category
        name+="WvsZ"
  	datalist[name].plotOn(xframe,RooFit.MarkerSize(1))
  	modellist[name].plotOn(xframe,RooFit.Normalization(1.0,RooAbsReal.RelativeExpected),RooFit.LineColor(color))
  	modellist[name].plotOn(xframe,RooFit.Components("bkg"+name),RooFit.LineStyle(kDashed),RooFit.LineColor(color),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
  	modellist[name].plotOn(xframe,RooFit.Components("sigW"),RooFit.LineStyle(kDotted),RooFit.LineColor(color),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
  	modellist[name].plotOn(xframe,RooFit.Components("sigZ"),RooFit.LineStyle(kDashDotted),RooFit.LineColor(color),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
      canvas=TCanvas("c2","c2",0,0,600,600)
      canvas.SetLogy()
      xframe.GetYaxis().SetTitle("Events")
      xframe.Draw()
      canvas.SaveAs(prefix+"_"+plot[0]+str(scenario)+str(btagscenario)+"combined_fit"+fit+".pdf")
      canvas.SaveAs(prefix+"_"+plot[0]+str(scenario)+str(btagscenario)+"combined_fit"+fit+".root")
