import os, sys
import array
from ROOT import * 
from CMGTools.RootTools.RootTools import *

hists=[]
colors=[1,2,4,6,7,8,9,11,12,13,14]
ymin=0.001

def fnc_dscb(xx,pp):
  x   = xx[0];
  N   = pp[0];
  mu  = pp[1];
  sig = pp[2];
  a1  = pp[3];
  p1  = pp[4];
  a2  = pp[5];
  p2  = pp[6];

  u   = (x-mu)/sig;
  A1  = TMath.Power(p1/TMath.Abs(a1),p1)*TMath.Exp(-a1*a1/2);
  A2  = TMath.Power(p2/TMath.Abs(a2),p2)*TMath.Exp(-a2*a2/2);
  B1  = p1/TMath.Abs(a1) - TMath.Abs(a1);
  B2  = p2/TMath.Abs(a2) - TMath.Abs(a2);

  result=N;
  if (u<-a1):
      result *= A1*TMath.Power(B1-u,-p1);
  elif (u<a2):
      result *= TMath.Exp(-u*u/2);
  else:
      result *= A2*TMath.Power(B2+u,-p2);
  return result;

def makeEfficiency(passing, all):
    gragh=TGraphAsymmErrors(passing, all)
    gragh.GetXaxis().SetTitle(passing.GetXaxis().GetTitle())
    gragh.GetYaxis().SetTitle(passing.GetYaxis().GetTitle())
    gragh.GetXaxis().SetRangeUser(passing.GetXaxis().GetBinLowEdge(1),passing.GetXaxis().GetBinUpEdge(passing.GetNbinsX()))
    gragh.GetYaxis().SetRangeUser(0,1)
    return gragh

def plotVariable(name,formula,labelx,labely,xbins,xmin,xmax,ymin=0,ymax=0,ratio=False, showLegend=True):
    print 'plotVariable:', name
    global hists
    if "data"==samples[0][2]:
        legend_title="CMS Preliminary"
    else:
        legend_title="CMS Simulation"
    if ratio and "trigger" in name:
        legend=TLegend(0.58,0.8,0.95,0.95,legend_title)
    else:
        legend=TLegend(0.58,0.6,0.95,0.95,legend_title)
    firsthist=None
    if ratio:
        labely=labely+'(data) / '+labely+'(MC)'

    efficiency_cut=0.99
    if "mjjtrig1" in name:
        efficiency_cut=0.99
        labely='eff (HLT_HT600 || HLT_Fat850)'
    elif "mjjtrig2" in name:
        efficiency_cut=(4.66*0.99-(4.66-0.8)*0.9999)/0.8
        labely='eff (HLT_HT650 || HLT_Fat850)'
    elif "mjjtrig3" in name:
        efficiency_cut=(4.66*0.99-(4.66-0.8-0.15)*0.9999-0.8*0.987)/0.15
        labely='eff (HLT_HT700 || HLT_Fat850)'
    elif "mjjtrig4" in name:
        efficiency_cut=(4.66*0.99-(4.66-0.8-0.15)*0.9999-0.8*0.987)/0.15
        labely='eff (HLT_Fat850)'
    print efficiency_cut
	 
    maxy=0
    norm=1
    normhistos=[]
    datapoints_all=[]
    datapoints_1tag=[]
    datapoints_2tag=[]
    for i in range(len(samples)):
        print i
	if "data"==samples[i][2]:
            options='le'
	elif "QCD" in samples[i][2]:
            options='h'
	elif tagging_variables:
            options='histc'
	else:
            options='h'
	if not "same" in options and ((i>0 and not ratio) or i>1): options+='same'
	if "mjj" in name:
	     bins=[]
             #bins+=[1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, ]
	     if "mjjtrig" in name or signal:
                 bins+=[419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, ]
             bins+=[890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808, 7000]
        else:
	     bins=[xmin+float(xmax-xmin)/float(xbins)*b for b in range(xbins)]+[xmax]
        binning=array.array('d')
        for bin in bins:
            binning.append(bin)

        if "data"==samples[i][2]:
            dataMCtagEffScale=1.0
	else:
            dataMCtagEffScale=1.0#0.95

        fullformula=formula
        
        if "trigger" in name:
            if "reference" in samples[i][2]:
	        fullformula=formula.replace("Histograms","HistogramsReference")
            elif "mjjtrig1" in name:
                fullformula=formula.replace("Histograms","HistogramsAnalysis1")
            elif "mjjtrig2" in name:
                fullformula=formula.replace("Histograms","HistogramsAnalysis2")
            elif "mjjtrig3" in name:
                fullformula=formula.replace("Histograms","HistogramsAnalysis3")
            elif "mjjtrig4" in name:
                fullformula=formula.replace("Histograms","HistogramsAnalysis4")

        if no_tagging:
            fullformula1tag=fullformula
            fullformula2tag=fullformula
	else:
            fullformula1tag=fullformula.replace("/","1tag/")
            fullformula2tag=fullformula.replace("/","2tag/")

        if use_loose_massdrop:
	    fullformula1tag=fullformula1tag.replace("tag","ltag")
	    fullformula2tag=fullformula2tag.replace("tag","ltag")
        if use_tight_massdrop:
	    fullformula1tag=fullformula1tag.replace("tag","ttag")
	    fullformula2tag=fullformula2tag.replace("tag","ttag")

        hist1 = TH1F(name+' '+str(i)+str(ratio),';'+labelx+';'+labely,len(binning)-1,binning)
	hist1.Sumw2()
        for j in range(len(files[i])):
	    h1=files[i][j].Get(fullformula).Clone()
            if "data"==samples[i][2] and "mjj " in name and not ratio:
	        for b in range(h1.GetXaxis().GetNbins()):
	            for c in range(int(round(h1.GetBinContent(b+1)))):
		        datapoints_all+=[h1.GetBinCenter(b+1)]
            h1=h1.Rebin(len(binning)-1,h1.GetName()+"_rebin",binning)
            hist1.Add(h1,weights[i])
	    if "/mass1" in fullformula or "/massdrop1" in fullformula or "/dR1" in fullformula:
	        h1=files[i][j].Get(fullformula.replace("/mass1","/mass2").replace("/massdrop1","/massdrop2").replace("/dR1","/dR2")).Clone()
                h1=h1.Rebin(len(binning)-1,h1.GetName()+"_rebin",binning)
                hist1.Add(h1,weights[i])
        if "data"==samples[i][2] and "mjj " in name and not ratio:
                print "inclusive & mass & events"
	        for b in range(hist1.GetXaxis().GetNbins()):
		    print int(hist1.GetXaxis().GetBinLowEdge(b+1)), "&", int(hist1.GetBinContent(b+1))
	if "data"==samples[i][2]:
	    norm=hist1.Integral()
	relnorm=hist1.Integral()
        if 'norm-data-tagged' in name:
            if "data"==samples[i][2]:
	        norm1=norm
	    else:
	        norm=norm1
	if 'norm-data' in name and relnorm>0:
	    hist1.Scale(norm/relnorm)
	if 'norm-one' in name:
	    hist1.Scale(1./relnorm)
	if 'norm-events' in name:
	    hist1.Scale(1./events[i]/weights[i])
	if ratio and not "data"==samples[i][2]:
            if "trigger" in name:
                hist1.Divide(normhistos[-1][0],hist1,1,1,'B')
		turnon=0
		efficiency=0
	        for b in range(hist1.GetXaxis().GetNbins()):
                    if hist1.GetXaxis().GetBinLowEdge(b+1)==890:
 			efficiency=hist1.GetBinContent(b+1)
	        for b in range(hist1.GetXaxis().GetNbins()):
		    if hist1.GetBinContent(b+1)>efficiency_cut:
		        turnon=hist1.GetXaxis().GetBinLowEdge(b+1)
			break
                print "turn-on:", turnon,efficiency
	    else:
                hist1.Divide(normhistos[-1][0],hist1)
	if not ratio or not "data"==samples[i][2]:
            hist1.SetLineColor(colors[i])
            if not (not "data"==samples[i][2] and not signal and not ratio and "mjj" in name) and not only_fits:
                hist1.Draw(options)
            hists+=[hist1]
	    if i==0 or (ratio and i==1):
                firsthist=hist1
            hist1.GetXaxis().SetRangeUser(xmin,xmax)
            maxy=max(maxy,hist1.GetMaximum())
	if "data"==samples[i][2]:
            hist1.SetMarkerStyle(20)
            hist1.SetMarkerSize(0.5)
	    if not only_fits:
                legend.AddEntry(hist1,samples[i][2],"ple")
	else:
	    if not only_fits:
                legend.AddEntry(hist1,samples[i][2],"l")
        if not "data"==samples[i][2] and not signal and not ratio and "mjj" in name:
	    fit=TF1('fit '+str(i)+samples[i][2],'[0]*pow(1.0-x/7000.0,[1])/pow(x/7000.0,[2]+[3]*log(x/7000.0))',bins[0],bins[-1])
	    fit.SetParameter(0,hist1.Integral())
	    fit.SetParameter(1,5)
	    fit.SetParameter(2,5)
	    fit.SetParameter(3,-0.5)
            fit.SetLineWidth(1)
            fit.SetLineColor(colors[i])
            hist1.Fit(fit,"R0")
            fit.Draw('lsame')
            hists+=[fit]

        if "data"==samples[i][2] and "dPhi" in name:
             print "Events with dPhi<0.5:",hist1.Integral(hist1.FindBin(0),hist1.FindBin(0.5))
             print "Events with 0.5<dPhi<2.0:",hist1.Integral(hist1.FindBin(0.5),hist1.FindBin(2.0))
             print "Events with 2.0<dPhi:",hist1.Integral(hist1.FindBin(2.0),hist1.FindBin(3.15))
	
	if not only_fits and not "same" in options: options+='same'

	if not ratio and "mjj" in name and not "Fat" in fullformula and "1tag" in fullformula1tag:
            hist2m = TH1F(name+' '+str(i)+str(ratio)+' 1mtag',';'+labelx+';'+labely,len(binning)-1,binning)
	    hist2m.Sumw2()
            for j in range(len(files[i])):
                try:
		    h2m=files[i][j].Get(fullformula1tag.replace("tag","mtag")).Clone()
		except: break
                h2m=h2m.Rebin(len(binning)-1,h2m.GetName()+"_rebin",binning)
                hist2m.Add(h2m,weights[i])
                if 'norm-data-tagged' in name:
                    if "data"==samples[i][2]:
	                norm2=hist2m.Integral()
                    relnorm=hist2m.Integral()
		    norm=norm2
                if 'norm-one-tagged' in name:
                    relnorm=hist2m.Integral()
                if 'norm-data' in name and relnorm>0:
                    hist2m.Scale(norm/relnorm*dataMCtagEffScale)
                if 'norm-one' in name:
                    hist2m.Scale(1./relnorm)
                if 'norm-events' in name:
                    hist2m.Scale(1./events[i]/weights[i])
	
        hist2 = TH1F(name+' '+str(i)+str(ratio)+' 1tag',';'+labelx+';'+labely,len(binning)-1,binning)
	hist2.Sumw2()
        for j in range(len(files[i])):
            h2=files[i][j].Get(fullformula1tag).Clone()
            if "data"==samples[i][2] and "mjj " in name and not ratio:
	        for b in range(h2.GetXaxis().GetNbins()):
	            for c in range(int(round(h2.GetBinContent(b+1)))):
		        datapoints_1tag+=[h2.GetBinCenter(b+1)]
            h2=h2.Rebin(len(binning)-1,h2.GetName()+"_rebin",binning)
            hist2.Add(h2,weights[i])
	if 'norm-data-tagged' in name:
            if "data"==samples[i][2]:
	        norm2=hist2.Integral()
            relnorm=hist2.Integral()
	    norm=norm2
        if "data"==samples[i][2] and "mjj " in name and not ratio:
                print "1-tag & mass & events"
	        for b in range(hist2.GetXaxis().GetNbins()):
		    print int(hist2.GetXaxis().GetBinLowEdge(b+1)), "&", int(hist2.GetBinContent(b+1))
        if 'norm-one-tagged' in name:
            relnorm=hist2.Integral()
	if 'norm-data' in name and relnorm>0:
	    hist2.Scale(norm/relnorm*dataMCtagEffScale)
	if 'norm-one' in name:
	    hist2.Scale(1./relnorm)
	if 'norm-events' in name:
	    hist2.Scale(1./events[i]/weights[i])
        if samples[i][3]>0 and signal and not ratio and "mjj" in name:
	    fit_gaus=TF1('fit '+str(i)+'gaus','gaus',samples[i][3]*0.8, samples[i][3]*1.2)
            hist2.Fit(fit_gaus,"R0N")
	    print "fit mean, width", fit_gaus.GetParameter(1), fit_gaus.GetParameter(2)
	    fit=TF1('fit '+str(i),fnc_dscb,samples[i][3]*0.3, samples[i][3]*1.3,7)
	    fit.SetTitle("")
	    fit.SetParameter(0,fit_gaus.GetParameter(0))
	    fit.SetParameter(1,fit_gaus.GetParameter(1))
	    fit.SetParameter(2,fit_gaus.GetParameter(2))
	    fit.SetParameter(3,2)
	    fit.SetParameter(4,1)
	    fit.SetParameter(5,2)
	    fit.SetParameter(6,1)
            fit.SetLineWidth(1)
            fit.SetLineColor(colors[i])
            fit.SetLineStyle(1)
	    #if samples[i][3]*0.8<bins[0]:
            #	 fit.FixParameter(3,100)
            #	 fit.FixParameter(4,0)
            hist2.Fit(fit,"R0")
            maxy=max(maxy,fit.GetMaximum())
	    if only_fits:
              fit.SetLineStyle(i+1)
	      if i==0:
                firsthist=fit
              if not "same" in options:
                if ("qW" in samples[i][2] or "qZ" in samples[i][2]):
                    fit.Draw('l')
	      else:
                if ("qW" in samples[i][2] or "qZ" in samples[i][2]):
        	   fit.Draw('lsame')
            elif not no_tagging:
        	fit.Draw('lsame')
            f=file(prefix+"_"+samples[i][2]+"_"+str(samples[i][3])+"_1tag.txt","w")
            bincenter=[\
  0.31,  0.33,  0.35,  0.37,  0.39,  0.41,  0.43,  0.45,  0.47,  0.49,\
  0.51,  0.53,  0.55,  0.57,  0.59,  0.61,  0.63,  0.65,  0.67,  0.69,\
  0.71,  0.73,  0.75,  0.77,  0.79,  0.81,  0.83,  0.85,  0.87,  0.89,\
  0.91,  0.93,  0.95,  0.97,  0.99,  1.01,  1.03,  1.05,  1.07,  1.09,\
  1.11,  1.13,  1.15,  1.17,  1.19,  1.21,  1.23,  1.25,  1.27,  1.29]
	    f.write("double yvalues[50] = {")
	    for b in range(len(bincenter)):
            	#f.write(str(10000.*hist3.GetBinContent(hist3.FindBin(bincenter[b]*samples[i][3])))+",")
	    	if fit.Eval(bincenter[b]*samples[i][3])>0:
            	    f.write(str(10000.*fit.Eval(bincenter[b]*samples[i][3])))
	    	else:
            	    f.write(str(10000.*fit_gaus.Eval(bincenter[b]*samples[i][3])))
	    	if b<len(bincenter)-1:
	    	   f.write(", ")
	    f.write("};")
            f.close()
            print "stored", len(bincenter), "signal shape points"
            f=file(prefix+"_"+samples[i][2]+"_"+str(samples[i][3])+"_1tag_eff.txt","w")
	    f.write("acceptance(>890)="+str(hist1.Integral(hist1.FindBin(890),hist1.FindBin(xmax)))+"\n")
	    f.write("acceptance(1sigma)="+str(hist1.Integral(hist1.FindBin(samples[i][3]*0.8), hist1.FindBin(samples[i][3]*1.2)))+"\n")
	    if "1tag" in fullformula1tag:
                f.write("efficiency(m-only,>890)="+str(hist2m.Integral(hist1.FindBin(890),hist1.FindBin(xmax))/hist1.Integral(hist1.FindBin(890),hist1.FindBin(xmax)))+"\n")
                f.write("efficiency(m-only,1sigma)="+str(hist2m.Integral(hist1.FindBin(samples[i][3]*0.8), hist1.FindBin(samples[i][3]*1.2))/hist1.Integral(hist1.FindBin(samples[i][3]*0.8), hist1.FindBin(samples[i][3]*1.2)))+"\n")
	    f.write("efficiency(>890)="+str(hist2.Integral(hist1.FindBin(890),hist1.FindBin(xmax))/hist1.Integral(hist1.FindBin(890),hist1.FindBin(xmax)))+"\n")
	    f.write("efficiency(1sigma)="+str(hist2.Integral(hist1.FindBin(samples[i][3]*0.8), hist1.FindBin(samples[i][3]*1.2))/hist1.Integral(hist1.FindBin(samples[i][3]*0.8), hist1.FindBin(samples[i][3]*1.2)))+"\n")
	    f.close()
            print "stored acceptance and efficiency"
	if ratio and not "data"==samples[i][2]:
	    if "trigger" in name:
                hist2.Divide(normhistos[-1][1],hist2,1,1,'B')
		turnon=0
		efficiency=0
	        for b in range(hist2.GetXaxis().GetNbins()):
                    if hist2.GetXaxis().GetBinLowEdge(b+1)==890:
 			efficiency=hist2.GetBinContent(b+1)
	        for b in range(hist2.GetXaxis().GetNbins()):
		    if hist2.GetBinContent(b+1)>efficiency_cut:
		        turnon=hist2.GetXaxis().GetBinLowEdge(b+1)
			break
                print "turn-on:", turnon,efficiency
	        hist2.Add(TF1("add1","-1",xmin,xmax))
	    else:
                hist2.Divide(normhistos[-1][1],hist2)
                hist2.Scale(0.1)
	if not ratio or not "data"==samples[i][2]:
            #if not "data"==samples[i][2] and 'norm-data' in name:
	    #    hist2.SetLineColor(colors[i+1])
	    #else:
            hist2.SetLineColor(colors[i])
            hist2.SetLineStyle(2)
            if not no_tagging and not (not "data"==samples[i][2] and not signal and not ratio and "mjj" in name) and not only_fits:
                hist2.Draw(options)
            hists+=[hist2]
            maxy=max(maxy,hist2.GetMaximum())
	if "data"==samples[i][2]:
            hist2.SetMarkerStyle(21)
            hist2.SetMarkerSize(0.5)
	    if only_fits:
	      if ("qW" in samples[i][2] or "qZ" in samples[i][2]):
	        legend.AddEntry(fit,samples[i][2],"ple")
            elif not no_tagging:
                legend.AddEntry(hist2,"1tag","ple")
	else:
	    if only_fits:
	      if ("qW" in samples[i][2] or "qZ" in samples[i][2]):
                legend.AddEntry(fit,samples[i][2],"l")
            elif not no_tagging:
                legend.AddEntry(hist2,"1tag","l")
        if not "data"==samples[i][2] and not signal and not ratio and "mjj" in name:
	    fit=TF1('fit '+str(i)+samples[i][2]+"2tag",'[0]*pow(1.0-x/7000.0,[1])/pow(x/7000.0,[2]+[3]*log(x/7000.0))',bins[0],bins[-1])
	    fit.SetParameter(0,hist2.Integral())
	    fit.SetParameter(1,5)
	    fit.SetParameter(2,5)
	    fit.SetParameter(3,-0.5)
            fit.SetLineWidth(1)
            fit.SetLineStyle(2)
            fit.SetLineColor(colors[i])
            hist2.Fit(fit,"R0")
	    if only_fits:
              fit.SetLineStyle(i+1)
	    if not only_fits or ("qW" in samples[i][2] or "qZ" in samples[i][2]):
                fit.Draw('lsame')
            hists+=[fit]

	if only_fits and ("qW" in samples[i][2] or "qZ" in samples[i][2]) and not "same" in options: options+='same'

	if not ratio and "mjj" in name and not "Fat" in fullformula and "1tag" in fullformula1tag:
            hist3m = TH1F(name+' '+str(i)+str(ratio)+' 2mtag',';'+labelx+';'+labely,len(binning)-1,binning)
	    hist3m.Sumw2()
            for j in range(len(files[i])):
                try:
                    h3m=files[i][j].Get(fullformula2tag.replace("tag","mtag")).Clone()
		except: break
                h3m=h3m.Rebin(len(binning)-1,h3m.GetName()+"_rebin",binning)
                hist3m.Add(h3m,weights[i])
                if 'norm-data-tagged' in name:
                    if "data"==samples[i][2]:
	                norm3=hist3m.Integral()
                    relnorm=hist3m.Integral()
		    norm=norm3
                if 'norm-one-tagged' in name:
                    relnorm=hist3m.Integral()
                if 'norm-data' in name and relnorm>0:
                    hist3m.Scale(norm/relnorm*dataMCtagEffScale)
                if 'norm-one' in name:
                    hist3m.Scale(1./relnorm)
                if 'norm-events' in name:
                    hist3m.Scale(1./events[i]/weights[i])
	
        hist3 = TH1F(name+' '+str(i)+str(ratio)+' 2tags',';'+labelx+';'+labely,len(binning)-1,binning)
	hist3.Sumw2()
        for j in range(len(files[i])):
            h3=files[i][j].Get(fullformula2tag).Clone()
            if "data"==samples[i][2] and "mjj " in name and not ratio:
	        for b in range(h3.GetXaxis().GetNbins()):
	            for c in range(int(round(h3.GetBinContent(b+1)))):
		        datapoints_2tag+=[h3.GetBinCenter(b+1)]
            h3=h3.Rebin(len(binning)-1,h3.GetName()+"_rebin",binning)
            hist3.Add(h3,weights[i])
	if 'norm-data-tagged' in name:
            if "data"==samples[i][2]:
	        norm3=hist3.Integral()
            relnorm=hist3.Integral()
	    norm=norm3
        if "data"==samples[i][2] and "mjj " in name and not ratio:
                print "2-tag & mass & events"
	        for b in range(hist3.GetXaxis().GetNbins()):
		    print int(hist3.GetXaxis().GetBinLowEdge(b+1)), "&", int(hist3.GetBinContent(b+1))
        if 'norm-one-tagged' in name:
            relnorm=hist3.Integral()
	if 'norm-data' in name and relnorm>0:
	    hist3.Scale(norm/relnorm*dataMCtagEffScale*dataMCtagEffScale)
	if 'norm-one' in name:
	    hist3.Scale(1./relnorm)
	if 'norm-events' in name:
	    hist3.Scale(1./events[i]/weights[i])
        if samples[i][3]>0 and signal in [1,2,3,11,12,111,112,100] and ("WW" in samples[i][2] or "WZ" in samples[i][2] or "ZZ" in samples[i][2]) and not ratio and "mjj" in name:
	    fit_gaus=TF1('fit2 '+str(i)+'gaus','gaus',samples[i][3]*0.8, samples[i][3]*1.2)
            hist3.Fit(fit_gaus,"R0N")
	    print "fit mean, width", fit_gaus.GetParameter(1), fit_gaus.GetParameter(2)
	    fit=TF1('fit2 '+str(i),fnc_dscb,samples[i][3]*0.3, samples[i][3]*1.3,7)
	    fit.SetParameter(0,fit_gaus.GetParameter(0))
	    fit.SetParameter(1,fit_gaus.GetParameter(1))
	    fit.SetParameter(2,fit_gaus.GetParameter(2))
	    fit.SetParameter(3,2)
	    fit.SetParameter(4,0.1)
	    fit.SetParameter(5,2)
	    fit.SetParameter(6,0.1)
            fit.SetLineWidth(1)
            fit.SetLineColor(colors[i])
            fit.SetLineStyle(3)
	    #if samples[i][3]*0.8<bins[0]:
            #	 fit.FixParameter(3,100)
            #	 fit.FixParameter(4,0)
            hist3.Fit(fit,"R0")
	    if only_fits:
              fit.SetLineStyle(i+1)
            maxy=max(maxy,fit.GetMaximum())
            if not no_tagging:
        	fit.Draw('lsame')
            f=file(prefix+"_"+samples[i][2]+"_"+str(samples[i][3])+"_2tag.txt","w")
            bincenter=[\
  0.31,  0.33,  0.35,  0.37,  0.39,  0.41,  0.43,  0.45,  0.47,  0.49,\
  0.51,  0.53,  0.55,  0.57,  0.59,  0.61,  0.63,  0.65,  0.67,  0.69,\
  0.71,  0.73,  0.75,  0.77,  0.79,  0.81,  0.83,  0.85,  0.87,  0.89,\
  0.91,  0.93,  0.95,  0.97,  0.99,  1.01,  1.03,  1.05,  1.07,  1.09,\
  1.11,  1.13,  1.15,  1.17,  1.19,  1.21,  1.23,  1.25,  1.27,  1.29]
	    f.write("double yvalues[50] = {")
	    for b in range(len(bincenter)):
            	#f.write(str(10000.*hist3.GetBinContent(hist3.FindBin(bincenter[b]*samples[i][3])))+",")
	    	if fit.Eval(bincenter[b]*samples[i][3])>0:
            	    f.write(str(10000.*fit.Eval(bincenter[b]*samples[i][3])))
	    	else:
            	    f.write(str(10000.*fit_gaus.Eval(bincenter[b]*samples[i][3])))
	    	if b<len(bincenter)-1:
	    	   f.write(", ")
	    f.write("};")
            f.close()
            print "stored", len(bincenter), "signal shape points"
            f=file(prefix+"_"+samples[i][2]+"_"+str(samples[i][3])+"_2tag_eff.txt","w")
	    f.write("acceptance(>890)="+str(hist1.Integral(hist1.FindBin(890),hist1.FindBin(xmax)))+"\n")
	    f.write("acceptance(1sigma)="+str(hist1.Integral(hist1.FindBin(samples[i][3]*0.8), hist1.FindBin(samples[i][3]*1.2)))+"\n")
	    if "1tag" in fullformula1tag:
                f.write("efficiency(m-only,>890)="+str(hist3m.Integral(hist1.FindBin(890),hist1.FindBin(xmax))/hist1.Integral(hist1.FindBin(890),hist1.FindBin(xmax)))+"\n")
                f.write("efficiency(m-only,1sigma)="+str(hist3m.Integral(hist1.FindBin(samples[i][3]*0.8), hist1.FindBin(samples[i][3]*1.2))/hist1.Integral(hist1.FindBin(samples[i][3]*0.8), hist1.FindBin(samples[i][3]*1.2)))+"\n")
	    f.write("efficiency(>890)="+str(hist3.Integral(hist1.FindBin(890),hist1.FindBin(xmax))/hist1.Integral(hist1.FindBin(890),hist1.FindBin(xmax)))+"\n")
	    f.write("efficiency(1sigma)="+str(hist3.Integral(hist1.FindBin(samples[i][3]*0.8), hist1.FindBin(samples[i][3]*1.2))/hist1.Integral(hist1.FindBin(samples[i][3]*0.8), hist1.FindBin(samples[i][3]*1.2)))+"\n")
	    f.close()
            print "stored acceptance and efficiency"
	if ratio and not "data"==samples[i][2]:
	    if "trigger" in name:
                hist3.Divide(normhistos[-1][2],hist3,1,1,'B')
		turnon=0
		efficiency=0
	        for b in range(hist3.GetXaxis().GetNbins()):
                    if hist3.GetXaxis().GetBinLowEdge(b+1)==890:
 			efficiency=hist3.GetBinContent(b+1)
	        for b in range(hist3.GetXaxis().GetNbins()):
		    if hist3.GetBinContent(b+1)>efficiency_cut:
		        turnon=hist3.GetXaxis().GetBinLowEdge(b+1)
			break
                print "turn-on:", turnon,efficiency
	        hist3.Add(TF1("add1","-2",xmin,xmax))
	    else:
                hist3.Divide(normhistos[-1][2],hist3)
                hist3.Scale(0.01)
	if not ratio or not "data"==samples[i][2]:
            #if not "data"==samples[i][2] and 'norm-data' in name:
	    #    hist3.SetLineColor(colors[i+2])
	    #else:
            hist3.SetLineColor(colors[i])
            hist3.SetLineStyle(3)
            if not no_tagging and not only_fits:# and not (not "data"==samples[i][2] and not signal and not ratio and "mjj" in name):
                hist3.Draw(options)
            hists+=[hist3]
            maxy=max(maxy,hist3.GetMaximum())
	if "data"==samples[i][2]:
            hist3.SetMarkerStyle(22)
            hist3.SetMarkerSize(0.5)
	    if only_fits:
	      if ("WW" in samples[i][2] or "WZ" in samples[i][2] or "ZZ" in samples[i][2]):
	        legend.AddEntry(fit,samples[i][2],"ple")
            elif not no_tagging:
                legend.AddEntry(hist3,"2tags","ple")
	else:
	    if only_fits:
	      if ("WW" in samples[i][2] or "WZ" in samples[i][2] or "ZZ" in samples[i][2]):
	        legend.AddEntry(fit,samples[i][2],"l")
            elif not no_tagging:
                legend.AddEntry(hist3,"2tags","l")
        if not "data"==samples[i][2] and not signal and not ratio and "mjj" in name:
	    fit=TF1('fit '+str(i)+samples[i][2]+"2tag",'[0]*pow(1.0-x/7000.0,[1])/pow(x/7000.0,[2]+[3]*log(x/7000.0))',bins[0],bins[-1])
	    fit.SetParameter(0,hist3.Integral())
	    fit.SetParameter(1,5)
	    fit.SetParameter(2,5)
	    fit.FixParameter(3,0)
            fit.SetLineWidth(1)
            fit.SetLineStyle(3)
            fit.SetLineColor(colors[i])
            hist3.Fit(fit,"R0")
            #fit.Draw('lsame')
            hists+=[fit]

	if "data"==samples[i][2]:
	    normhistos+=[(hist1,hist2,hist3)]

        if "mjj" in name and not ratio and not "Fat" in fullformula and "1tag" in fullformula1tag:
            hist2m=hist2m.Clone()
            hist2m.Divide(hist2m,hist1,1,1,'B')
            hist2m.SaveAs(prefix+"_"+samples[i][2]+"_"+str(samples[i][3])+"_eff_1mtag.root")
            hist3m=hist3m.Clone()
            hist3m.Divide(hist3m,hist1,1,1,'B')
            hist3m.SaveAs(prefix+"_"+samples[i][2]+"_"+str(samples[i][3])+"_eff_2mtag.root")
        if "mjj" in name and not ratio and not "Fat" in fullformula:
            hist2=hist2.Clone()
            hist2.Divide(hist2,hist1,1,1,'B')
            if use_loose_massdrop:
                hist2.SaveAs(prefix+"_"+samples[i][2]+"_"+str(samples[i][3])+"_eff_1ltag.root")
            elif use_tight_massdrop:
                hist2.SaveAs(prefix+"_"+samples[i][2]+"_"+str(samples[i][3])+"_eff_1ttag.root")
            else:
                hist2.SaveAs(prefix+"_"+samples[i][2]+"_"+str(samples[i][3])+"_eff_1tag.root")
            hist3=hist3.Clone()
            hist3.Divide(hist3,hist1,1,1,'B')
            if use_loose_massdrop:
                hist3.SaveAs(prefix+"_"+samples[i][2]+"_"+str(samples[i][3])+"_eff_2ltag.root")
            elif use_tight_massdrop:
                hist3.SaveAs(prefix+"_"+samples[i][2]+"_"+str(samples[i][3])+"_eff_2ttag.root")
            else:
                hist3.SaveAs(prefix+"_"+samples[i][2]+"_"+str(samples[i][3])+"_eff_2tag.root")

	if only_fits and ("WW" in samples[i][2] or "ZZ" in samples[i][2] or "WZ" in samples[i][2]) and not "same" in options: options+='same'

    if "mjj " in name and not ratio and not signal:
     	f=file(prefix+"_data_all.txt","w")
     	for point in sorted(datapoints_all):
     	    f.write(str(point)+"\n")
     	f.close()
     	print "stored", len(datapoints_all), "data points"
     	f=file(prefix+"_data_1tag.txt","w")
     	for point in sorted(datapoints_1tag):
     	    f.write(str(point)+"\n")
     	f.close()
     	print "stored", len(datapoints_1tag), "data points"
     	normhistos[0][1].SaveAs(prefix+"_data_1tag.root")
     	f=file(prefix+"_data_2tag.txt","w")
     	for point in sorted(datapoints_2tag):
     	    f.write(str(point)+"\n")
     	f.close()
     	print "stored", len(datapoints_2tag), "data points"
     	normhistos[0][2].SaveAs(prefix+"_data_2tag.root")


    if ratio:
       l1=TF1("line1","1",xmin,xmax)
       l1.SetLineWidth(1)
       l1.SetLineStyle(1)
       l1.Draw("same")
       hists+=[l1]
       if "trigger" in name:
           l2=TF1("line2","0",xmin,xmax)
       else:
           l2=TF1("line2","0.1",xmin,xmax)
       l2.SetLineWidth(1)
       l2.SetLineStyle(2)
       if not no_tagging:
           l2.Draw("same")
       hists+=[l2]
       if "trigger" in name:
           l3=TF1("line3","-1",xmin,xmax)
       else:
           l3=TF1("line3","0.01",xmin,xmax)
       l3.SetLineWidth(1)
       l3.SetLineStyle(3)
       if not no_tagging:
           l3.Draw("same")
       hists+=[l3]

    if "trigger" in name and ratio:
        firsthist.GetYaxis().SetRangeUser(ymin,ymax)
    elif ratio:
      if ymin>0:
        if no_tagging:
            firsthist.GetYaxis().SetRangeUser(1e-1,1e+1)
	else:
            firsthist.GetYaxis().SetRangeUser(1e-3,1e+1)
      else:
        if no_tagging:
            firsthist.GetYaxis().SetRangeUser(0.5,1.5)
	else:
            firsthist.GetYaxis().SetRangeUser(-1.5,1.5)
    elif ymin>0:
        firsthist.GetYaxis().SetRangeUser(ymin,max(ymax,maxy)*3.0)
    else:
      if only_fits:
        firsthist.GetYaxis().SetRangeUser(ymin,0.5)
        firsthist.GetXaxis().SetRangeUser(890,2000)
	firsthist.GetXaxis().SetTitle(labelx)
	firsthist.GetYaxis().SetTitle(labely)
	legend.SetX1(0.2)
	legend.SetHeader("1.5 TeV resonances            CMS Simulation")
      else:
        firsthist.GetYaxis().SetRangeUser(ymin,max(ymax,maxy)*1.2)
	
    legend.SetTextSize(0.04)
    legend.SetFillStyle(0)
    if showLegend and (not ratio or "trigger" in name):
        legend.Draw("same")
    hists+=[legend]

    if "data"==samples[0][2]:
        legend3=TLegend(0.3,0.9,0.6,0.95,"L = 5.0 fb^{-1}")
        legend3.SetTextSize(0.04)
        legend3.SetFillStyle(0)
        legend3.Draw("same")
        hists+=[legend3]
 
        legend4=TLegend(0.3,0.85,0.6,0.9,"#sqrt{s} = 7 TeV")
        legend4.SetTextSize(0.04)
        legend4.SetFillStyle(0)
        legend4.Draw("same")
        hists+=[legend4]
    
def plotTriggerEff():
    print 'plotTriggerEff'

    for ratio in [False,True]:
     if ratio:
    	 filename=prefix + '_ca8dijet_trigger_ratio'
     else:
    	 filename=prefix + '_ca8dijet_trigger'
     canvas = TCanvas("","",0,0,200,200)
     #canvas.GetPad(1).SetLogy()
     plotVariable('mjjtrig1 trigger ca8','cmgPFDiJetCA8PrunedHistograms/mass', 'm_{jj}','N',1,0,1500,-2,1, ratio, True)
     canvas.SaveAs(filename+'1.root')
     canvas.SaveAs(filename+'1.pdf')
     canvas.SaveAs(filename+'1.eps')
     if wait:
    	 os.system("ghostview "+filename+'1.eps')
     canvas = TCanvas("","",0,0,200,200)
     #canvas.GetPad(2).SetLogy()
     plotVariable('mjjtrig2 trigger ca8','cmgPFDiJetCA8PrunedHistograms/mass', 'm_{jj}','N',1,0,1500,-2,1, ratio, True)
     canvas.SaveAs(filename+'2.root')
     canvas.SaveAs(filename+'2.pdf')
     canvas.SaveAs(filename+'2.eps')
     if wait:
    	 os.system("ghostview "+filename+'2.eps')
     canvas = TCanvas("","",0,0,200,200)
     #canvas.GetPad(3).SetLogy()
     plotVariable('mjjtrig3 trigger ca8','cmgPFDiJetCA8PrunedHistograms/mass', 'm_{jj}','N',1,0,1500,-2,1, ratio, True)
     canvas.SaveAs(filename+'3.root')
     canvas.SaveAs(filename+'3.pdf')
     canvas.SaveAs(filename+'3.eps')
     if wait:
    	 os.system("ghostview "+filename+'3.eps')
     canvas = TCanvas("","",0,0,200,200)
     #canvas.GetPad(4).SetLogy()
     plotVariable('mjjtrig4 trigger ca8','cmgPFDiJetCA8PrunedHistograms/mass', 'm_{jj}','N',1,0,1500,-2,1, ratio, True)
     canvas.SaveAs(filename+'4.root')
     canvas.SaveAs(filename+'4.pdf')
     canvas.SaveAs(filename+'4.eps')
     if wait:
    	 os.system("ghostview "+filename+'4.eps')

    for ratio in [False,True]:
     if ratio:
         filename=prefix + '_dijet_trigger_ratio'
     else:
         filename=prefix + '_dijet_trigger'
     canvas = TCanvas("","",0,0,200,200)
     #canvas.GetPad(1).SetLogy()
     plotVariable('mjjtrig1 trigger','cmgPFDiJetHistograms/mass', 'm_{jj}','N',1,0,1500,-2,1, ratio, True)
     canvas.SaveAs(filename+'1.root')
     canvas.SaveAs(filename+'1.pdf')
     canvas.SaveAs(filename+'1.eps')
     if wait:
         os.system("ghostview "+filename+'1.eps')
     canvas = TCanvas("","",0,0,200,200)
     #canvas.GetPad(2).SetLogy()
     plotVariable('mjjtrig2 trigger','cmgPFDiJetHistograms/mass', 'm_{jj}','N',1,0,1500,-2,1, ratio, True)
     canvas.SaveAs(filename+'2.root')
     canvas.SaveAs(filename+'2.pdf')
     canvas.SaveAs(filename+'2.eps')
     if wait:
         os.system("ghostview "+filename+'2.eps')
     canvas = TCanvas("","",0,0,200,200)
     #canvas.GetPad(3).SetLogy()
     plotVariable('mjjtrig3 trigger','cmgPFDiJetHistograms/mass', 'm_{jj}','N',1,0,1500,-2,1, ratio, True)
     canvas.SaveAs(filename+'3.root')
     canvas.SaveAs(filename+'3.pdf')
     canvas.SaveAs(filename+'3.eps')
     if wait:
         os.system("ghostview "+filename+'3.eps')
     canvas = TCanvas("","",0,0,200,200)
     #canvas.GetPad(4).SetLogy()
     plotVariable('mjjtrig4 trigger','cmgPFDiJetHistograms/mass', 'm_{jj}','N',1,0,1500,-2,1, ratio, True)
     canvas.SaveAs(filename+'4.root')
     canvas.SaveAs(filename+'4.pdf')
     canvas.SaveAs(filename+'4.eps')
     if wait:
         os.system("ghostview "+filename+'4.eps')

def plotDataMCKinematics():
    global no_tagging
    print 'plotDataMCKinematics'

    jettypes=[""]
    if no_tagging:
        jettypes+=["Fat"]

    for ratio in [False,True]:
      for fat in jettypes:
    	 if ratio:
    	     filename=prefix + '_dijet_norm_ratio'
    	 else:
    	     filename=prefix + '_dijet_norm'
    	 canvas = TCanvas("","",0,0,200,200)
    	 canvas.SetLogy()
    	 plotVariable('mjj norm-data-tagged','cmgPF'+fat+'DiJetHistograms/mass', 'm_{jj}','N',1,0,4500,5e-1,0, ratio, True)
    	 canvas.SaveAs(filename + fat + '_mass.root')
    	 canvas.SaveAs(filename + fat + '_mass.pdf')
    	 canvas.SaveAs(filename + fat + '_mass.eps')
    	 if wait:
    	     os.system("ghostview "+filename + fat + '_mass.eps')

    	 canvas = TCanvas("","",0,0,200,200)
    	 canvas.SetLogy()
    	 plotVariable('mjj norm-data','cmgPF'+fat+'DiJetHistograms/mass', 'm_{jj}','N',1,0,4500,5e-1,0, ratio, True)
    	 canvas.SaveAs(filename + fat + '_mass_rel.root')
    	 canvas.SaveAs(filename + fat + '_mass_rel.pdf')
    	 canvas.SaveAs(filename + fat + '_mass_rel.eps')
    	 if wait:
    	     os.system("ghostview "+filename + fat + '_mass_rel.eps')

    	 canvas = TCanvas("","",0,0,200,200)
    	 canvas.SetLogy()
    	 plotVariable('deltaEta norm-data-tagged','cmgPF'+fat+'DiJetHistograms/deltaEta', 'd#eta','N',20,-2,2,5e-1,0, ratio,False)
    	 canvas.SaveAs(filename + fat + '_deta.root')
    	 canvas.SaveAs(filename + fat + '_deta.pdf')
    	 canvas.SaveAs(filename + fat + '_deta.eps')
    	 if wait:
    	     os.system("ghostview "+filename + fat + '_deta.eps')

    	 canvas = TCanvas("","",0,0,200,200)
    	 canvas.SetLogy()
    	 plotVariable('deltaPhi norm-data-tagged','cmgPF'+fat+'DiJetHistograms/deltaPhi', 'd#phi','N',50,0,3.15,5e-1,0, ratio,False)
    	 canvas.SaveAs(filename + fat + '_dphi.root')
    	 canvas.SaveAs(filename + fat + '_dphi.pdf')
    	 canvas.SaveAs(filename + fat + '_dphi.eps')
    	 if wait:
    	     os.system("ghostview "+filename + fat + '_dphi.eps')
    
    	 canvas = TCanvas("","",0,0,200,200)
    	 canvas.SetLogy()
    	 plotVariable('metSumPt norm-data-tagged','cmgPF'+fat+'DiJetHistograms/metSumPt', '|#sum #vec{p}_{T}| / #sum p_{T}','N',50,0,1,5e-2,0, ratio,True)
    	 canvas.SaveAs(filename + fat + '_metSumPt.root')
    	 canvas.SaveAs(filename + fat + '_metSumPt.pdf')
    	 canvas.SaveAs(filename + fat + '_metSumPt.eps')
    	 if wait:
    	     os.system("ghostview "+filename + fat + '_metSumPt.eps')
    
    for ratio in [False,True]:
      for fat in jettypes:
    	 if ratio:
    	     filename=prefix + '_jet_norm_ratio'
    	 else:
    	     filename=prefix + '_jet_norm'
    	 canvas = TCanvas("","",0,0,200,200)
    	 canvas.SetLogy()
    	 plotVariable('pT1 norm-data-tagged','cmgPF'+fat+'DiJetHistograms/pt1', 'p_{T,1}','N',50,0,2000,5e-1,0, ratio,True)
    	 canvas.SaveAs(filename + fat + '_pt1.root')
    	 canvas.SaveAs(filename + fat + '_pt1.pdf')
    	 canvas.SaveAs(filename + fat + '_pt1.eps')
    	 if wait:
    	     os.system("ghostview "+filename + fat + '_pt1.eps')
    	 canvas = TCanvas("","",0,0,200,200)
    	 canvas.SetLogy()
    	 plotVariable('pT2 norm-data-tagged','cmgPF'+fat+'DiJetHistograms/pt2', 'p_{T,2}','N',50,0,2000,5e-1,0, ratio,True)
    	 canvas.SaveAs(filename + fat + '_pt2.root')
    	 canvas.SaveAs(filename + fat + '_pt2.pdf')
    	 canvas.SaveAs(filename + fat + '_pt2.eps')
    	 if wait:
    	     os.system("ghostview "+filename + fat + '_pt2.eps')
    	 canvas = TCanvas("","",0,0,200,200)
    	 canvas.SetLogy()
    	 plotVariable('eta1 norm-data-tagged','cmgPF'+fat+'DiJetHistograms/eta1', '#eta_{1}','N',30,-3,3,5e-1,0, ratio,False)
    	 canvas.SaveAs(filename + fat + '_eta1.root')
    	 canvas.SaveAs(filename + fat + '_eta1.pdf')
    	 canvas.SaveAs(filename + fat + '_eta1.eps')
    	 if wait:
    	     os.system("ghostview "+filename + fat + '_eta1.eps')
    	 canvas = TCanvas("","",0,0,200,200)
    	 canvas.SetLogy()
    	 plotVariable('eta2 norm-data-tagged','cmgPF'+fat+'DiJetHistograms/eta2', '#eta_{2}','N',30,-3,3,5e-1,0, ratio,False)
    	 canvas.SaveAs(filename + fat + '_eta2.root')
    	 canvas.SaveAs(filename + fat + '_eta2.pdf')
    	 canvas.SaveAs(filename + fat + '_eta2.eps')
    	 if wait:
    	     os.system("ghostview "+filename + fat + '_eta2.eps')

    no_tagging=True

    for ratio in [False,True]:
      for fat in jettypes:
    	 if ratio:
    	     filename=prefix + '_met_norm_ratio'
    	 else:
    	     filename=prefix + '_met_norm'
    	 canvas = TCanvas("","",0,0,200,200)
    	 canvas.SetLogy()
    	 plotVariable('metsumet norm-data-tagged','baseMETHistograms/metSumEt', 'ME_{T} / #sum E_{T}','N',50,0,1,5e-2,0, ratio,True)
    	 canvas.SaveAs(filename + fat + '_metsumet.root')
    	 canvas.SaveAs(filename + fat + '_metsumet.pdf')
    	 canvas.SaveAs(filename + fat + '_metsumet.eps')
    	 if wait:
    	     os.system("ghostview "+filename + fat + '_metsumet.eps')
    	 canvas = TCanvas("","",0,0,200,200)

def plotDataMCTagging():
    global no_tagging
    print 'plotDataMCTagging'

    no_tagging=True

    for ratio in [False,True]:
     if ratio:
         filename=prefix + '_ca8jet_norm_ratio'
     else:
         filename=prefix + '_ca8jet_norm'

     miny=5e-1

     canvas = TCanvas("","",0,0,200,200)
     if miny!=0:
         canvas.SetLogy()
     plotVariable('m1 norm-data','cmgPFDiJetCA8PrunedHistograms/mass1', 'm_{jet}','N',50,0,600,miny,0,ratio, True)
     canvas.SaveAs(filename+'_m1log.root')
     canvas.SaveAs(filename+'_m1log.pdf')
     canvas.SaveAs(filename+'_m1log.eps')
     if wait:
         os.system("ghostview "+filename+'_m1log.eps')

     miny=0

     canvas = TCanvas("","",0,0,200,200)
     if miny!=0:
         canvas.SetLogy()
     plotVariable('m1 norm-data','cmgPFDiJetCA8PrunedHistograms/mass1', 'm_{jet}','N',50,0,200,miny,0,ratio, True)
     canvas.SaveAs(filename+'_m1.root')
     canvas.SaveAs(filename+'_m1.pdf')
     canvas.SaveAs(filename+'_m1.eps')
     if wait:
         os.system("ghostview "+filename+'_m1.eps')
     #canvas = TCanvas("","",0,0,200,200)
     #if not tagging_variables:
     #    canvas.SetLogy()
     #plotVariable('m2 norm-data','cmgPFDiJetCA8PrunedHistograms/mass2', 'm_{2}','N',50,0,500,miny,0,ratio, True)
     #canvas.SaveAs(filename+'_m2.root')
     #canvas.SaveAs(filename+'_m2.pdf')
     #canvas.SaveAs(filename+'_m2.eps')
     #if wait:
     #    os.system("ghostview "+filename+'_m2.eps')

     canvas = TCanvas("","",0,0,200,200)
     if miny!=0:
         canvas.SetLogy()
     plotVariable('massdrop1 norm-data','cmgPFDiJetCA8PrunedHistograms/massdrop1', 'massdrop','N',25,0,1,miny,0,ratio,True)
     canvas.SaveAs(filename+'_massdrop1.root')
     canvas.SaveAs(filename+'_massdrop1.pdf')
     canvas.SaveAs(filename+'_massdrop1.eps')
     if wait:
         os.system("ghostview "+filename+'_massdrop1.eps')
     #canvas = TCanvas("","",0,0,200,200)
     #if not tagging_variables:
     #    canvas.SetLogy()
     #plotVariable('massdrop2 norm-data','cmgPFDiJetCA8PrunedHistograms/massdrop2', 'massdrop_{2}','N',30,0,1,miny,0,ratio,False)
     #canvas.SaveAs(filename+'_massdrop2.root')
     #canvas.SaveAs(filename+'_massdrop2.pdf')
     #canvas.SaveAs(filename+'_massdrop2.eps')
     #if wait:
     #    os.system("ghostview "+filename+'_massdrop2.eps')

     continue

     canvas = TCanvas("","",0,0,200,200)
     if miny!=0:
         canvas.SetLogy()
     plotVariable('dR1 norm-data','cmgPFDiJetCA8PrunedHistograms/dR1', '#Delta R','N',20,0,0.8,miny,0,ratio,True)
     canvas.SaveAs(filename+'_dR1.root')
     canvas.SaveAs(filename+'_dR1.pdf')
     canvas.SaveAs(filename+'_dR1.eps')
     if wait:
         os.system("ghostview "+filename+'_dR1.eps')

     miny=3e-1

     canvas = TCanvas("","",0,0,200,200)
     if miny!=0:
         canvas.SetLogy()
     plotVariable('dR norm-data','cmgPFDiJetAK5CA8PrunedHistograms/dR', '#Delta R','N',100,0,4,miny,0,ratio,True)
     canvas.SaveAs(filename+'_dR.root')
     canvas.SaveAs(filename+'_dR.pdf')
     canvas.SaveAs(filename+'_dR.eps')
     if wait:
         os.system("ghostview "+filename+'_dR.eps')

     canvas = TCanvas("","",0,0,200,200)
     if miny!=0:
         canvas.SetLogy()
     plotVariable('dEta norm-data','cmgPFDiJetAK5CA8PrunedHistograms/deta', '#Delta #eta','N',100,-2,2,miny,0,ratio,True)
     canvas.SaveAs(filename+'_dEta.root')
     canvas.SaveAs(filename+'_dEta.pdf')
     canvas.SaveAs(filename+'_dEta.eps')
     if wait:
         os.system("ghostview "+filename+'_dEta.eps')

     canvas = TCanvas("","",0,0,200,200)
     if miny!=0:
         canvas.SetLogy()
     plotVariable('dPhi norm-data','cmgPFDiJetAK5CA8PrunedHistograms/dphi', '#Delta #phi','N',100,0,3.15,miny,0,ratio,True)
     canvas.SaveAs(filename+'_dPhi.root')
     canvas.SaveAs(filename+'_dPhi.pdf')
     canvas.SaveAs(filename+'_dPhi.eps')
     if wait:
         os.system("ghostview "+filename+'_dPhi.eps')

def plotDataMCWide():
    global no_tagging
    print 'plotDataMCWide'

    no_tagging=True

    for ratio in [False,True]:
         fat="Fat"
    	 if ratio:
    	     filename=prefix + '_wide_norm_ratio'
    	 else:
    	     filename=prefix + '_wide_norm'
    	 canvas = TCanvas("","",0,0,200,200)
    	 canvas.SetLogy()
    	 plotVariable('dptrel1 norm-data','cmgPF'+fat+'DiJetHistograms/dptrel1', '#Delta p_{T,1} / p_{T,1}','N',100,-1,1,5e-1,0, ratio, True)
    	 canvas.SaveAs(filename + fat + '_dptrel1.root')
    	 canvas.SaveAs(filename + fat + '_dptrel1.pdf')
    	 canvas.SaveAs(filename + fat + '_dptrel1.eps')
    	 if wait:
    	     os.system("ghostview "+filename + fat + '_dptrel1.eps')
    	 canvas = TCanvas("","",0,0,200,200)
    	 canvas.SetLogy()
    	 plotVariable('dptrel2 norm-data','cmgPF'+fat+'DiJetHistograms/dptrel2', '#Delta p_{T,2} / p_{T,2}','N',100,-1,1,5e-1,0, ratio, True)
    	 canvas.SaveAs(filename + fat + '_dptrel2.root')
    	 canvas.SaveAs(filename + fat + '_dptrel2.pdf')
    	 canvas.SaveAs(filename + fat + '_dptrel2.eps')
    	 if wait:
    	     os.system("ghostview "+filename + fat + '_dptrel2.eps')
    	 canvas = TCanvas("","",0,0,200,200)
    	 canvas.SetLogy()
    	 plotVariable('dpt1 norm-data','cmgPF'+fat+'DiJetHistograms/dpt1', '#Delta p_{T,1}','N',100,-500,500,5e-1,0, ratio, True)
    	 canvas.SaveAs(filename + fat + '_dpt1.root')
    	 canvas.SaveAs(filename + fat + '_dpt1.pdf')
    	 canvas.SaveAs(filename + fat + '_dpt1.eps')
    	 if wait:
    	     os.system("ghostview "+filename + fat + '_dpt1.eps')
    	 canvas = TCanvas("","",0,0,200,200)
    	 canvas.SetLogy()
    	 plotVariable('dpt1 norm-data','cmgPF'+fat+'DiJetHistograms/dpt2', '#Delta p_{T,2}','N',100,-500,500,5e-1,0, ratio, True)
    	 canvas.SaveAs(filename + fat + '_dpt2.root')
    	 canvas.SaveAs(filename + fat + '_dpt2.pdf')
    	 canvas.SaveAs(filename + fat + '_dpt2.eps')
    	 if wait:
    	     os.system("ghostview "+filename + fat + '_dpt2.eps')
    	 canvas = TCanvas("","",0,0,200,200)
    	 canvas.SetLogy()
    	 plotVariable('deta1 norm-data','cmgPF'+fat+'DiJetHistograms/deta1', 'd#eta_{1}','N',100,-1,1,5e-1,0, ratio,True)
    	 canvas.SaveAs(filename + fat + '_deta1.root')
    	 canvas.SaveAs(filename + fat + '_deta1.pdf')
    	 canvas.SaveAs(filename + fat + '_deta1.eps')
    	 if wait:
    	     os.system("ghostview "+filename + fat + '_deta1.eps')
    	 canvas = TCanvas("","",0,0,200,200)
    	 canvas.SetLogy()
    	 plotVariable('deta2 norm-data','cmgPF'+fat+'DiJetHistograms/deta2', 'd#eta_{2}','N',100,-1,1,5e-1,0, ratio,True)
    	 canvas.SaveAs(filename + fat + '_deta2.root')
    	 canvas.SaveAs(filename + fat + '_deta2.pdf')
    	 canvas.SaveAs(filename + fat + '_deta2.eps')
    	 if wait:
    	     os.system("ghostview "+filename + fat + '_deta2.eps')
    	 canvas = TCanvas("","",0,0,200,200)
    	 canvas.SetLogy()
    	 plotVariable('dphi1 norm-data','cmgPF'+fat+'DiJetHistograms/dphi1', 'd#phi_{1}','N',100,0,3.15/2.,5e-1,0, ratio,True)
    	 canvas.SaveAs(filename + fat + '_dphi1.root')
    	 canvas.SaveAs(filename + fat + '_dphi1.pdf')
    	 canvas.SaveAs(filename + fat + '_dphi1.eps')
    	 if wait:
    	     os.system("ghostview "+filename + fat + '_dphi1.eps')
    	 canvas = TCanvas("","",0,0,200,200)
    	 canvas.SetLogy()
    	 plotVariable('dphi2 norm-data','cmgPF'+fat+'DiJetHistograms/dphi2', 'd#phi_{2}','N',100,0,3.15/2.,5e-1,0, ratio,True)
    	 canvas.SaveAs(filename + fat + '_dphi2.root')
    	 canvas.SaveAs(filename + fat + '_dphi2.pdf')
    	 canvas.SaveAs(filename + fat + '_dphi2.eps')
    	 if wait:
    	     os.system("ghostview "+filename + fat + '_dphi2.eps')
    	 canvas = TCanvas("","",0,0,200,200)
    	 canvas.SetLogy()
    	 plotVariable('n1 norm-data','cmgPF'+fat+'DiJetHistograms/njets1', 'n_{1}','N',20,0,20,5e-1,0, ratio,True)
    	 canvas.SaveAs(filename + fat + '_n1.root')
    	 canvas.SaveAs(filename + fat + '_n1.pdf')
    	 canvas.SaveAs(filename + fat + '_n1.eps')
    	 if wait:
    	     os.system("ghostview "+filename + fat + '_n1.eps')
    	 canvas = TCanvas("","",0,0,200,200)
    	 canvas.SetLogy()
    	 plotVariable('n2 norm-data','cmgPF'+fat+'DiJetHistograms/njets2', 'n_{2}','N',20,0,20,5e-1,0, ratio,True)
    	 canvas.SaveAs(filename + fat + '_n2.root')
    	 canvas.SaveAs(filename + fat + '_n2.pdf')
    	 canvas.SaveAs(filename + fat + '_n2.eps')
    	 if wait:
    	     os.system("ghostview "+filename + fat + '_n2.eps')
    
def plotSignalKinematics():
     global no_tagging
     print 'plotSignalKinematics'

     filename=prefix + '_dijet_norm'
     canvas = TCanvas("","",0,0,200,200)
     plotVariable('mjj','cmgPFDiJetHistogramsReference/mass', 'm_{jj}','N',1,0,3500,0,0.05, False, True)
     canvas.SaveAs(filename+'_mass.root')
     canvas.SaveAs(filename+'_mass.pdf')
     canvas.SaveAs(filename+'_mass.eps')
     if wait:
         os.system("ghostview "+filename+'_mass.eps')

     canvas = TCanvas("","",0,0,200,200)
     plotVariable('mjj norm-one-tagged','cmgPFDiJetHistogramsReference/mass', 'm_{jj}','N',1,0,3500,0,0.5, False, True)
     canvas.SaveAs(filename+'_mass1.root')
     canvas.SaveAs(filename+'_mass1.pdf')
     canvas.SaveAs(filename+'_mass1.eps')
     if wait:
         os.system("ghostview "+filename+'_mass1.eps')

     #filename=prefix + '_dijet_norm'
     #canvas = TCanvas("","",0,0,200,200)
     #plotVariable('mjj','cmgPFFatDiJetHistogramsReference/mass', 'm_{jj}','N',1,0,3500,0,0.05, False, True)
     #canvas.SaveAs(filename+'_fatmass.root')
     #canvas.SaveAs(filename+'_fatmass.pdf')
     #canvas.SaveAs(filename+'_fatmass.eps')
     #if wait:
     #    os.system("ghostview "+filename+'_fatmass.eps')

     canvas = TCanvas("","",0,0,200,200)
     plotVariable('deltaEta norm-one','cmgPFDiJetHistograms/deltaEta', 'd#eta','N',20,-2,2,0,0.05, False,False)
     canvas.SaveAs(filename+'_deta.root')
     canvas.SaveAs(filename+'_deta.pdf')
     canvas.SaveAs(filename+'_deta.eps')
     if wait:
         os.system("ghostview "+filename+'_deta.eps')

     canvas = TCanvas("","",0,0,200,200)
     canvas.SetLogy()
     plotVariable('deltaPhi norm-one','cmgPFDiJetHistograms/deltaPhi', 'd#phi','N',50,0,3.15,1e-4,0, False,False)
     canvas.SaveAs(filename + '_dphi.root')
     canvas.SaveAs(filename + '_dphi.pdf')
     canvas.SaveAs(filename + '_dphi.eps')
     if wait:
     	 os.system("ghostview "+filename + '_dphi.eps')

     no_tagging=True

     filename=prefix + '_ca8jet_norm'
     canvas = TCanvas("","",0,0,200,200)
     canvas.SetLogy()
     plotVariable('m1 norm-one','cmgPFDiJetCA8PrunedHistograms/mass1', 'm_{jet}','N',50,0,500,1e-4,0,False, True)
     canvas.SaveAs(filename+'_m1.root')
     canvas.SaveAs(filename+'_m1.pdf')
     canvas.SaveAs(filename+'_m1.eps')
     if wait:
         os.system("ghostview "+filename+'_m1.eps')
     #canvas = TCanvas("","",0,0,200,200)
     #canvas.SetLogy()
     #plotVariable('m2 norm-one','cmgPFDiJetCA8PrunedHistograms/mass2', 'm_{2}','N',50,0,500,1e-4,0,False, True)
     #canvas.SaveAs(filename+'_m2.root')
     #canvas.SaveAs(filename+'_m2.pdf')
     #canvas.SaveAs(filename+'_m2.eps')
     #if wait:
     #    os.system("ghostview "+filename+'_m2.eps')
     canvas = TCanvas("","",0,0,200,200)
     canvas.SetLogy()
     plotVariable('massdrop1 norm-one','cmgPFDiJetCA8PrunedHistograms/massdrop1', 'massdrop','N',30,0,1,1e-4,0,False,False)
     canvas.SaveAs(filename+'_massdrop1.root')
     canvas.SaveAs(filename+'_massdrop1.pdf')
     canvas.SaveAs(filename+'_massdrop1.eps')
     if wait:
         os.system("ghostview "+filename+'_massdrop1.eps')
     #canvas = TCanvas("","",0,0,200,200)
     #canvas.SetLogy()
     #plotVariable('massdrop2 norm-one','cmgPFDiJetCA8PrunedHistograms/massdrop2', 'massdrop_{2}','N',30,0,1,1e-4,0,False,False)
     #canvas.SaveAs(filename+'_massdrop2.root')
     #canvas.SaveAs(filename+'_massdrop2.pdf')
     #canvas.SaveAs(filename+'_massdrop2.eps')
     #if wait:
     #    os.system("ghostview "+filename+'_massdrop2.eps')


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
gStyle.SetMarkerSize(0.5)
gStyle.SetHistLineWidth(1)
gStyle.SetStatFontSize(0.020)
gStyle.SetTitleSize(0.06, "XYZ")
gStyle.SetLabelSize(0.05, "XYZ")
gStyle.SetNdivisions(510, "XYZ")
gStyle.SetLegendBorderSize(0)

wait=True
trigger=False
no_tagging=False
use_loose_massdrop=False
use_tight_massdrop=False
tagging_variables=False
only_fits=False

samples=[[["file:/tmp/hinzmann/428_HT_Run2011A-May10ReReco-v1_vv10_histograms.root",
           "file:/tmp/hinzmann/428_HT_Run2011A-PromptReco-v4_vv10_histograms.root",
           "file:/tmp/hinzmann/428_HT_Run2011A-05Aug2011-v1_vv10_histograms.root",
           "file:/tmp/hinzmann/428_HT_Run2011A-PromptReco-v6_vv10_histograms.root",
           "file:/tmp/hinzmann/428_HT_Run2011B-PromptReco-v1_vv11_histograms.root",
           #"file:/tmp/hinzmann/428_HT_Run2011A-May10ReReco-v1_vv10_metsumpt_histograms.root",
           #"file:/tmp/hinzmann/428_HT_Run2011A-PromptReco-v4_vv10_metsumpt_histograms.root",
           #"file:/tmp/hinzmann/428_HT_Run2011A-05Aug2011-v1_vv10_metsumpt_histograms.root",
           #"file:/tmp/hinzmann/428_HT_Run2011A-PromptReco-v6_vv10_metsumpt_histograms.root",
           #"file:/tmp/hinzmann/428_HT_Run2011B-PromptReco-v1_vv11_metsumpt_histograms.root",
           ],1,'data',0],
        ]
if trigger:
    samples+=[samples[-1][:]]
    samples[-1][2]='data reference'
else:
    samples+=[
         #(["file:/tmp/hinzmann/QCD_vv5_histograms.root",
	 #  ],3.326e-04*1e9*6e4,'QCD Pythia6 Z2',0),
         (["file:/tmp/hinzmann/QCD_vv5_metsumpt_histograms.root",
	   ],3.326e-04*1e9*6e4,'QCD Pythia6 Z2',0),
         #(["file:/tmp/hinzmann/QCD_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv5_0_histograms.root",
	 #  ],3.326e-04*1e9*6e4,'QCD Pythia6 Z2',0),
         #(["file:/tmp/hinzmann/428_QCD_Pt-300to470_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_0_histograms.root",
	 #  ],1170.,'QCD Pythia6 Z2',0),
         #(["file:/tmp/hinzmann/428_QCD_Pt-470to600_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_0_histograms.root",
	 #  ],70.2,'QCD Pythia6 Z2',0),
         #(["file:/tmp/hinzmann/428_QCD_Pt-600to800_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_0_histograms.root",
	 #  ],15.6,'QCD Pythia6 Z2',0),
         #(["file:/tmp/hinzmann/428_QCD_Pt-800to1000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_0_histograms.root",
	 #  ],1.84,'QCD Pythia6 Z2',0),
         #(["file:/tmp/hinzmann/428_QCD_Pt-1000to1400_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_0_histograms.root",
	 #  ],0.332,'QCD Pythia6 Z2',0),
         #(["file:/tmp/hinzmann/428_QCD_Pt-1400to1800_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_0_histograms.root",
	 #  ],0.0109,'QCD Pythia6 Z2',0),
         #(["file:/tmp/hinzmann/428_QCD_Pt-1800_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v2_vv9_0_histograms.root",
	 #  ],3.58e-4,'QCD Pythia6 Z2',0),
         #(["file:/tmp/hinzmann/428_QCD_Pt-15to3000_Tune23_Flat_7TeV_herwigpp_Fall11-PU_S6_START42_V14B-v2_vv9_3_histograms.root",
	 #  ],3.326e-04*1e9*6e4,'QCD Herwig++',0),
         (["file:/tmp/hinzmann/428_QCD_Pt-15to3000_Tune23_Flat_7TeV_herwigpp_Fall11-PU_S6_START42_V14B-v2_vv9_3_metsumpt_histograms.root",
	   ],3.326e-04*1e9*6e4,'QCD Herwig++',0),
         #(["file:/tmp/hinzmann/428_W1Jet_TuneZ2_7TeV-madgraph-tauola_Fall11-PU_S6_START42_V14B-v1_vv9_4_0_histograms.root",
	 #  ],3.326e-04*1e9*6e4,'QCD',0),
         ]

if tagging_variables:
    samples+=[
             (["file:/tmp/hinzmann/428_RSGravitonToWW_kMpl01_M_1500_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./30240.,'G*->WW (1.5 TeV)',1500),
             (["file:/tmp/hinzmann/428_RSGravitonToZZ_kMpl01_M_1500_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_4_0_histograms.root"],1./30240.,'G*->ZZ (1.5 TeV)',1500),
             (["file:/tmp/hinzmann/428_WprimeToWZ_M_1500_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./29952.,"W'->WZ (1.5 TeV)",1500),
             (["file:/tmp/hinzmann/428_QstarToQW_M_1500_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./29664.,'q*->qW (1.5 TeV)',1500),
             (["file:/tmp/hinzmann/428_QstarToQZ_M_1500_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./30240.,'q*->qZ (1.5 TeV)',1500),
         ]
    #samples+=[
    #         (["file:/tmp/hinzmann/pythia6_graviton_WW_1000_vv5_0_histograms.root"],1,"G*->WW Py6 fast",1000),
    #         (["file:/tmp/hinzmann/RSGravitonToWW_kMpl_01_M_1000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5_0_histograms.root"],1,'G*->WW H++ fast',1000),
    #         (["file:/tmp/hinzmann/428_RSGravitonToWW_kMpl01_M_1000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./30240.,'G*->WW H++ full',1500),
    #         (["file:/tmp/hinzmann/pythia6_graviton_ZZ_1000_vv5_0_histograms.root"],1,"G*->ZZ Py6 fast",1000),
    #         (["file:/tmp/hinzmann/RSGravitonToZZ_kMpl_01_M_1000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5_0_histograms.root"],1,'G*->ZZ H++ fast',1000),
    #         (["file:/tmp/hinzmann/428_RSGravitonToZZ_kMpl01_M_1000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./30240.,'G*->ZZ H++ full',1000),
    #     ]
	     
if len(sys.argv)>1:
    signal=int(sys.argv[1])
else:
    signal=0

if signal==11:
    samples=[(["file:/tmp/hinzmann/RSGravitonToWW_kMpl_01_M_750_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5_0_histograms.root"],1,'G*->WW (0.75 TeV)',750),
             (["file:/tmp/hinzmann/RSGravitonToWW_kMpl_01_M_1000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5_0_histograms.root"],1,'G*->WW (1 TeV)',1000),
             (["file:/tmp/hinzmann/RSGravitonToWW_kMpl_01_M_1500_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5_0_histograms.root"],1,'G*->WW (1.5 TeV)',1500),
             (["file:/tmp/hinzmann/RSGravitonToWW_kMpl_01_M_2000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5_0_histograms.root"],1,'G*->WW (2 TeV)',2000),
             (["file:/tmp/hinzmann/RSGravitonToWW_kMpl_01_M_3000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5_0_histograms.root"],1,'G*->WW (3 TeV)',3000),
             ]

if signal==111:
    samples=[(["file:/tmp/hinzmann/pythia6_graviton_WW_1000_vv5_0_histograms.root"],1,"G*->WW (1 TeV)",1000),
             (["file:/tmp/hinzmann/pythia6_graviton_WW_2000_vv5_0_histograms.root"],1,"G*->WW (2 TeV)",2000),
             ]

if signal==12:
    samples=[(["file:/tmp/hinzmann/RSGravitonToZZ_kMpl_01_M_750_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5_0_histograms.root"],1,'G*->ZZ (0.75 TeV)',750),
             (["file:/tmp/hinzmann/RSGravitonToZZ_kMpl_01_M_1000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5_0_histograms.root"],1,'G*->ZZ (1 TeV)',1000),
             (["file:/tmp/hinzmann/RSGravitonToZZ_kMpl_01_M_1500_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5_0_histograms.root"],1,'G*->ZZ (1.5 TeV)',1500),
             (["file:/tmp/hinzmann/RSGravitonToZZ_kMpl_01_M_2000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5_0_histograms.root"],1,'G*->ZZ (2 TeV)',2000),
             (["file:/tmp/hinzmann/RSGravitonToZZ_kMpl_01_M_3000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5_0_histograms.root"],1,'G*->ZZ (3 TeV)',3000),
             ]

if signal==112:
    samples=[(["file:/tmp/hinzmann/pythia6_graviton_ZZ_1000_vv5_0_histograms.root"],1,"G*->ZZ (1 TeV)",1000),
             (["file:/tmp/hinzmann/pythia6_graviton_ZZ_2000_vv5_0_histograms.root"],1,"G*->ZZ (2 TeV)",2000),
             ]

if signal==13:
    samples=[(["file:/tmp/hinzmann/pythia6_Wprime_WZ_1000_vv5_0_histograms.root"],1,"W'->WZ",1000),
             (["file:/tmp/hinzmann/pythia6_Wprime_WZ_2000_vv5_0_histograms.root"],1,"W'->WZ",2000),
             ]

if signal==14:
    samples=[(["file:/tmp/hinzmann/pythia6_qstar_qW_1000_vv5_0_histograms.root"],1,'q*->qW',1000),
             (["file:/tmp/hinzmann/pythia6_qstar_qW_2000_vv5_0_histograms.root"],1,'q*->qW',2000),
             ]

if signal==15:
    samples=[(["file:/tmp/hinzmann/pythia6_qstar_qZ_1000_vv5_0_histograms.root"],1,'q*->qZ',1000),
             (["file:/tmp/hinzmann/pythia6_qstar_qZ_2000_vv5_0_histograms.root"],1,'q*->qZ',2000),
             ]

if signal==1:
    samples=[#(["file:/tmp/hinzmann/428_RSGravitonToWW_kMpl01_M_750_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_4_0_histograms.root"],1./30240.,'G*->WW',750),
             (["file:/tmp/hinzmann/428_RSGravitonToWW_kMpl01_M_1000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./30240.,'G*->WW (1 TeV)',1000),
             (["file:/tmp/hinzmann/428_RSGravitonToWW_kMpl01_M_1500_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./30240.,'G*->WW (1.5 TeV)',1500),
             (["file:/tmp/hinzmann/428_RSGravitonToWW_kMpl01_M_2000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./30240.,'G*->WW (2 TeV)',2000),
             #(["file:/tmp/hinzmann/428_RSGravitonToWW_kMpl01_M_3000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./30240.,'G*->WW',3000),
             ]

if signal==2:
    samples=[#(["file:/tmp/hinzmann/428_RSGravitonToZZ_kMpl01_M_750_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./30240.,'G*->ZZ',750),
             (["file:/tmp/hinzmann/428_RSGravitonToZZ_kMpl01_M_1000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./30240.,'G*->ZZ (1 TeV)',1000),
             (["file:/tmp/hinzmann/428_RSGravitonToZZ_kMpl01_M_1500_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_4_0_histograms.root"],1./30240.,'G*->ZZ (1.5 TeV)',1500),
             (["file:/tmp/hinzmann/428_RSGravitonToZZ_kMpl01_M_2000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./30240.,'G*->ZZ (2 TeV)',2000),
             #(["file:/tmp/hinzmann/428_RSGravitonToZZ_kMpl01_M_3000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./30240.,'G*->ZZ',3000),
             ]

if signal==3:
    samples=[#(["file:/tmp/hinzmann/428_WprimeToWZ_M_750_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./29952.,"W'->WZ",750),
             (["file:/tmp/hinzmann/428_WprimeToWZ_M_1000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./30240.,"W'->WZ (1 TeV)",1000),
             (["file:/tmp/hinzmann/428_WprimeToWZ_M_1500_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./29952.,"W'->WZ (1.5 TeV)",1500),
             (["file:/tmp/hinzmann/428_WprimeToWZ_M_2000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./30240.,"W'->WZ (2 TeV)",2000),
             #(["file:/tmp/hinzmann/428_WprimeToWZ_M_3000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./30240.,"W'->WZ",3000),
             ]

if signal==4:
    samples=[#(["file:/tmp/hinzmann/428_QstarToQW_M_750_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./29664.,'q*->qW',750),
             (["file:/tmp/hinzmann/428_QstarToQW_M_1000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_4_0_histograms.root"],1./28224.,'q*->qW (1 TeV)',1000),
             (["file:/tmp/hinzmann/428_QstarToQW_M_1500_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./29664.,'q*->qW (1.5 TeV)',1500),
             (["file:/tmp/hinzmann/428_QstarToQW_M_2000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./30240.,'q*->qW (2 TeV)',2000),
             (["file:/tmp/hinzmann/428_QstarToQW_M_3000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./30240.,'q*->qW (3 TeV)',3000),
             ]

if signal==5:
    samples=[#(["file:/tmp/hinzmann/428_QstarToQZ_M_750_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./30240.,'q*->qZ',750),
             (["file:/tmp/hinzmann/428_QstarToQZ_M_1000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_4_0_histograms.root"],1./29952.,'q*->qZ (1 TeV)',1000),
             (["file:/tmp/hinzmann/428_QstarToQZ_M_1500_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./30240.,'q*->qZ (1.5 TeV)',1500),
             (["file:/tmp/hinzmann/428_QstarToQZ_M_2000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_4_0_histograms.root"],1./30240.,'q*->qZ (2 TeV)',2000),
             (["file:/tmp/hinzmann/428_QstarToQZ_M_3000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./30240.,'q*->qZ (3 TeV)',3000),
             ]


if signal==100:
    samples=[(["file:/tmp/hinzmann/428_QstarToQW_M_1500_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./29664.,'q*->qW',1500),
             (["file:/tmp/hinzmann/428_QstarToQZ_M_1500_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./30240.,'q*->qZ',1500),
             (["file:/tmp/hinzmann/428_RSGravitonToWW_kMpl01_M_1500_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./30240.,'G*->WW',1500),
             (["file:/tmp/hinzmann/428_RSGravitonToZZ_kMpl01_M_1500_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_4_0_histograms.root"],1./30240.,'G*->ZZ',1500),
             (["file:/tmp/hinzmann/428_WprimeToWZ_M_1500_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1./29952.,"W'->WZ",1500),
             ]

events=[]
weights=[]
files=[]
lumi=1 #/pb
for sample,weight,name,mass in samples:
    print name
    nevents=0
    files+=[[]]
    for f in sample:
        print f
        files[-1]+=[TFile.Open(f)]
        #if not "data" in name:
        #    runInfoAccounting=files[-1][-1].Get("runInfoAccounting/RunInfoAccounting")
        #    hist=TH1F("h1","h1",100001,0,100000)
        #    runInfoAccounting.Project("h1","initialEvents")
        #    for b in range(hist.GetXaxis().GetNbins()):
	#        nevents+=int(round(hist.GetXaxis().GetBinCenter(b+1)))*hist.GetBinContent(b+1)
        #else:
        nevents+=files[-1][-1].Get("baseMETHistograms/met").GetEntries()
        #nevents+=files[-1][-1].Get("cmgPFDiJetHistogramsReference/mass").GetEntries()
    if "428" in str(sample):
        nevents=1.
    if not "data" in name:
        events+=[nevents]
        weights+=[lumi*weight/nevents]
    else:
        weights+=[1]
    print "number of events:",nevents, "weight:", weights[-1]

if signal:
    prefix = "plots/signal"+str(signal)
elif trigger:
    prefix = "plots/lumi46fb"
else:
    prefix = "plots/lumi46fb_dataMC"

if use_loose_massdrop:
    prefix += "_loose_massdrop"
if use_tight_massdrop:
    prefix += "_tight_massdrop"
if tagging_variables:
    prefix += "_sgbg"

if __name__ == '__main__':
    if trigger:
	plotTriggerEff()
    elif signal:
        plotSignalKinematics()
    elif tagging_variables:
	plotDataMCTagging()
        plotDataMCKinematics()
    else:
        plotDataMCKinematics()
	plotDataMCTagging()
	#if no_tagging:
        #    plotDataMCWide()
