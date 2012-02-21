import os, sys
import array
from ROOT import * 
from CMGTools.RootTools.RootTools import *

hists=[]
colors=[1,2,4,6,7,8,9,10,11,12,13,14]
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
    if ratio and "trigger" in name:
        legend=TLegend(0.6,0.8,0.95,0.95,"")
    else:
        legend=TLegend(0.6,0.65,0.95,0.95,"")
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

	fullformula1tag=fullformula.replace("/","1tag/")
	fullformula2tag=fullformula.replace("/","2tag/")


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
	if "data"==samples[i][2]:
	    norm=hist1.Integral()
	relnorm=hist1.Integral()
	if 'norm-data' in name and relnorm>0:
	    hist1.Scale(norm/relnorm)
	if 'norm-events' in name:
	    hist1.Scale(1./events[i]/weights[i])
	    massmin=samples[i][3]-200
	    massmax=samples[i][3]+200
            print "all "+str(massmin)+"-"+str(massmax), hist1.Integral(hist1.FindBin(massmin),hist1.FindBin(massmax))
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
            hist1.Draw(options)
            hists+=[hist1]
	    if i==0 or (ratio and i==1):
                firsthist=hist1
            hist1.GetXaxis().SetRangeUser(xmin,xmax)
	    legend.AddEntry(hist1,samples[i][2],"l")
            maxy=max(maxy,hist1.GetMaximum())
	
	if not "same" in options: options+='same'
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
	if 'norm-data' in name and relnorm>0:
	    hist2.Scale(norm/relnorm*dataMCtagEffScale)
	if 'norm-events' in name:
	    hist2.Scale(1./events[i]/weights[i])
	    massmin=samples[i][3]-200
	    massmax=samples[i][3]+200
            print "1tag "+str(massmin)+"-"+str(massmax), hist2.Integral(hist2.FindBin(massmin),hist2.FindBin(massmax))
            if samples[i][3]>0 and signal and not ratio:
	        fit_gaus=TF1('fit '+str(i)+'gaus','gaus',samples[i][3]*0.8, samples[i][3]*1.2)
                hist2.Fit(fit_gaus,"R0N")
	        fit=TF1('fit '+str(i),fnc_dscb,samples[i][3]*0.3, samples[i][3]*1.3,7)
		fit.SetParameter(0,fit_gaus.GetParameter(0))
		fit.SetParameter(1,fit_gaus.GetParameter(1))
		fit.SetParameter(2,fit_gaus.GetParameter(2))
		fit.SetParameter(3,2)
		fit.SetParameter(4,1)
		fit.SetParameter(5,2)
		fit.SetParameter(6,1)
                fit.SetLineWidth(1)
                fit.SetLineColor(colors[i])
		#if samples[i][3]*0.8<bins[0]:
                #    fit.FixParameter(3,100)
                #    fit.FixParameter(4,0)
                hist2.Fit(fit,"R0")
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
	        f.write("acceptance="+str(hist1.Integral(hist1.FindBin(890),hist1.FindBin(xmax)))+"\n") #hist1.FindBin(samples[i][3]*0.3), hist1.FindBin(samples[i][3]*1.3)
	        f.write("efficiency="+str(hist2.Integral(hist1.FindBin(890),hist1.FindBin(xmax))/hist1.Integral(hist1.FindBin(890),hist1.FindBin(xmax)))+"\n")
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
            hist2.Draw(options)
            hists+=[hist2]
	    legend.AddEntry(hist2,"1tag","l")
            maxy=max(maxy,hist2.GetMaximum())
	
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
	if 'norm-data' in name and relnorm>0:
	    hist3.Scale(norm/relnorm*dataMCtagEffScale*dataMCtagEffScale)
	if 'norm-events' in name:
	    hist3.Scale(1./events[i]/weights[i])
	    massmin=samples[i][3]-200
	    massmax=samples[i][3]+200
            print "2tag "+str(massmin)+"-"+str(massmax), hist3.Integral(hist3.FindBin(massmin),hist3.FindBin(massmax))
            if samples[i][3]>0 and signal in [1,2,3] and not ratio:
	        fit_gaus=TF1('fit2 '+str(i)+'gaus','gaus',samples[i][3]*0.8, samples[i][3]*1.2)
                hist3.Fit(fit_gaus,"R0N")
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
		#if samples[i][3]*0.8<bins[0]:
                #    fit.FixParameter(3,100)
                #    fit.FixParameter(4,0)
                hist3.Fit(fit,"R0")
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
	        f.write("acceptance="+str(hist1.Integral(hist1.FindBin(890),hist1.FindBin(xmax)))+"\n")
	        f.write("efficiency="+str(hist3.Integral(hist1.FindBin(890),hist1.FindBin(xmax))/hist1.Integral(hist1.FindBin(890),hist1.FindBin(xmax)))+"\n")
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
            hist3.Draw(options)
            hists+=[hist3]
            legend.AddEntry(hist3,"2tags","l")
            maxy=max(maxy,hist3.GetMaximum())

	if "data"==samples[i][2]:
	    normhistos+=[(hist1,hist2,hist3)]

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
       l2.Draw("same")
       hists+=[l2]
       if "trigger" in name:
           l3=TF1("line3","-1",xmin,xmax)
       else:
           l3=TF1("line3","0.01",xmin,xmax)
       l3.SetLineWidth(1)
       l3.SetLineStyle(3)
       l3.Draw("same")
       hists+=[l3]

    if "trigger" in name and ratio:
        firsthist.GetYaxis().SetRangeUser(ymin,ymax)
    elif ratio:
        firsthist.GetYaxis().SetRangeUser(1e-3,1e+1)
    elif ymin>0:
        firsthist.GetYaxis().SetRangeUser(ymin,max(ymax,maxy)*3.0)
    else:
        firsthist.GetYaxis().SetRangeUser(ymin,max(ymax,maxy)*1.2)
	
    legend.SetTextSize(0.04)
    legend.SetFillStyle(0)
    if showLegend and (not ratio or "trigger" in name):
        legend.Draw("same")
    hists+=[legend]
    
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
    print 'plotDataMCKinematics'

    for ratio in [False,True]:
     if ratio:
         filename=prefix + '_dijet_norm_ratio'
     else:
         filename=prefix + '_dijet_norm'
     canvas = TCanvas("","",0,0,200,200)
     canvas.SetLogy()
     plotVariable('mjj norm-data','cmgPFDiJetHistograms/mass', 'm_{jj}','N',1,0,4500,5e-1,0, ratio, True)
     canvas.SaveAs(filename+'_mass.root')
     canvas.SaveAs(filename+'_mass.pdf')
     canvas.SaveAs(filename+'_mass.eps')
     if wait:
         os.system("ghostview "+filename+'_mass.eps')
     canvas = TCanvas("","",0,0,200,200)
     canvas.SetLogy()
     plotVariable('mjjfat norm-data','cmgPFFatDiJetHistograms/mass', 'm_{jj}','N',1,0,4500,5e-1,0, ratio, True)
     canvas.SaveAs(filename+'_fatmass.root')
     canvas.SaveAs(filename+'_fatmass.pdf')
     canvas.SaveAs(filename+'_fatmass.eps')
     if wait:
         os.system("ghostview "+filename+'_fatmass.eps')
     canvas = TCanvas("","",0,0,200,200)
     canvas.SetLogy()
     plotVariable('deltaEta norm-data','cmgPFDiJetHistograms/deltaEta', 'd#eta','N',20,-2,2,5e-1,0, ratio,False)
     canvas.SaveAs(filename+'_deta.root')
     canvas.SaveAs(filename+'_deta.pdf')
     canvas.SaveAs(filename+'_deta.eps')
     if wait:
         os.system("ghostview "+filename+'_deta.eps')
     canvas = TCanvas("","",0,0,200,200)
     canvas.SetLogy()
     plotVariable('deltaPhi norm-data','cmgPFDiJetHistograms/deltaPhi', 'd#phi','N',50,0,3.15,5e-1,0, ratio,False)
     canvas.SaveAs(filename+'_dphi.root')
     canvas.SaveAs(filename+'_dphi.pdf')
     canvas.SaveAs(filename+'_dphi.eps')
     if wait:
         os.system("ghostview "+filename+'_dphi.eps')

    for ratio in [False,True]:
     if ratio:
         filename=prefix + '_jet_norm_ratio'
     else:
         filename=prefix + '_jet_norm'
     canvas = TCanvas("","",0,0,200,200)
     canvas.SetLogy()
     plotVariable('pT1 norm-data','cmgPFDiJetHistograms/pt1', 'p_{T,1}','N',50,0,2000,5e-1,0, ratio,True)
     canvas.SaveAs(filename+'_pt1.root')
     canvas.SaveAs(filename+'_pt1.pdf')
     canvas.SaveAs(filename+'_pt1.eps')
     if wait:
         os.system("ghostview "+filename+'_pt1.eps')
     canvas = TCanvas("","",0,0,200,200)
     canvas.SetLogy()
     plotVariable('pT2 norm-data','cmgPFDiJetHistograms/pt2', 'p_{T,2}','N',50,0,2000,5e-1,0, ratio,True)
     canvas.SaveAs(filename+'_pt2.root')
     canvas.SaveAs(filename+'_pt2.pdf')
     canvas.SaveAs(filename+'_pt2.eps')
     if wait:
         os.system("ghostview "+filename+'_pt2.eps')
     canvas = TCanvas("","",0,0,200,200)
     canvas.SetLogy()
     plotVariable('eta1 norm-data','cmgPFDiJetHistograms/eta1', '#eta_{1}','N',30,-3,3,5e-1,0, ratio,False)
     canvas.SaveAs(filename+'_eta1.root')
     canvas.SaveAs(filename+'_eta1.pdf')
     canvas.SaveAs(filename+'_eta1.eps')
     if wait:
         os.system("ghostview "+filename+'_eta1.eps')
     canvas = TCanvas("","",0,0,200,200)
     canvas.SetLogy()
     plotVariable('eta2 norm-data','cmgPFDiJetHistograms/eta2', '#eta_{2}','N',30,-3,3,5e-1,0, ratio,False)
     canvas.SaveAs(filename + '_eta2.root')
     canvas.SaveAs(filename + '_eta2.pdf')
     canvas.SaveAs(filename + '_eta2.eps')
     if wait:
         os.system("ghostview "+filename + '_eta2.eps')

def plotDataMCTagging():
    print 'plotDataMCTagging'

    for ratio in [False,True]:
     if ratio:
         filename=prefix + '_ca8jet_norm_ratio'
     else:
         filename=prefix + '_ca8jet_norm'
     canvas = TCanvas("","",0,0,200,200)
     canvas.SetLogy()
     plotVariable('m1 norm-data','cmgPFDiJetCA8PrunedHistograms/mass1', 'm_{1}','N',50,0,500,5e-1,0,ratio, True)
     canvas.SaveAs(filename+'_m1.root')
     canvas.SaveAs(filename+'_m1.pdf')
     canvas.SaveAs(filename+'_m1.eps')
     if wait:
         os.system("ghostview "+filename+'_m1.eps')
     canvas = TCanvas("","",0,0,200,200)
     canvas.SetLogy()
     plotVariable('m2 norm-data','cmgPFDiJetCA8PrunedHistograms/mass2', 'm_{2}','N',50,0,500,5e-1,0,ratio, True)
     canvas.SaveAs(filename+'_m2.root')
     canvas.SaveAs(filename+'_m2.pdf')
     canvas.SaveAs(filename+'_m2.eps')
     if wait:
         os.system("ghostview "+filename+'_m2.eps')
     canvas = TCanvas("","",0,0,200,200)
     canvas.SetLogy()
     plotVariable('massdrop1 norm-data','cmgPFDiJetCA8PrunedHistograms/massdrop1', 'massdrop_{1}','N',30,0,1,5e-1,0,ratio,False)
     canvas.SaveAs(filename+'_massdrop1.root')
     canvas.SaveAs(filename+'_massdrop1.pdf')
     canvas.SaveAs(filename+'_massdrop1.eps')
     if wait:
         os.system("ghostview "+filename+'_massdrop1.eps')
     canvas = TCanvas("","",0,0,200,200)
     canvas.SetLogy()
     plotVariable('massdrop2 norm-data','cmgPFDiJetCA8PrunedHistograms/massdrop2', 'massdrop_{2}','N',30,0,1,5e-1,0,ratio,False)
     canvas.SaveAs(filename+'_massdrop2.root')
     canvas.SaveAs(filename+'_massdrop2.pdf')
     canvas.SaveAs(filename+'_massdrop2.eps')
     if wait:
         os.system("ghostview "+filename+'_massdrop2.eps')

def plotSignalKinematics():
     print 'plotSignalKinematics'

     filename=prefix + '_dijet_norm'
     canvas = TCanvas("","",0,0,200,200)
     plotVariable('mjj norm-events','cmgPFDiJetHistogramsReference/mass', 'm_{jj}','N',1,0,3500,0,0.05)
     canvas.SaveAs(filename+'_mass.root')
     canvas.SaveAs(filename+'_mass.pdf')
     canvas.SaveAs(filename+'_mass.eps')
     if wait:
         os.system("ghostview "+filename+'_mass.eps')

     canvas = TCanvas("","",0,0,200,200)
     plotVariable('deltaEta norm-data','cmgPFDiJetHistograms/deltaEta', 'd#eta','N',20,-2,2,0,0.05)
     canvas.SaveAs(filename+'_deta.root')
     canvas.SaveAs(filename+'_deta.pdf')
     canvas.SaveAs(filename+'_deta.eps')
     if wait:
         os.system("ghostview "+filename+'_deta.eps')

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

wait=True
trigger=False

samples=[[["file:/tmp/hinzmann/428_HT_Run2011A-May10ReReco-v1_vv9_histograms.root",
           "file:/tmp/hinzmann/428_HT_Run2011A-PromptReco-v4_vv9_histograms.root",
           "file:/tmp/hinzmann/428_HT_Run2011A-05Aug2011-v1_vv9_histograms.root",
           "file:/tmp/hinzmann/428_HT_Run2011A-PromptReco-v6_vv9_histograms.root",
           "file:/tmp/hinzmann/428_HT_Run2011B-PromptReco-v1_vv9_histograms.root",
           ],1,'data',0],
        ]
if trigger:
    samples+=[samples[-1][:]]
    samples[-1][2]='data reference'
else:
    samples+=[
         (["file:/tmp/hinzmann/QCD_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv5_0_histograms.root",
	   ],3.326e-04*1e9*6e4,'QCD Pythia6 Z2',0),
         (["file:/tmp/hinzmann/428_QCD_Pt-15to3000_Tune23_Flat_7TeV_herwigpp_Fall11-PU_S6_START42_V14B-v2_vv9_3_0_histograms.root",
	   ],3.326e-04*1e9*6e4,'QCD Herwig++',0),
         #(["file:/tmp/hinzmann/428_W1Jet_TuneZ2_7TeV-madgraph-tauola_Fall11-PU_S6_START42_V14B-v1_vv9_4_0_histograms.root",
	 #  ],3.326e-04*1e9*6e4,'QCD',0),
         ]

if len(sys.argv)>1:
    signal=int(sys.argv[1])
else:
    signal=0

if signal==1:
    samples=[(["file:/tmp/hinzmann/RSGravitonToWW_kMpl_01_M_1000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5_0_histograms.root"],1,'G*->WW (0.1)',1000),
             (["file:/tmp/hinzmann/RSGravitonToWW_kMpl_01_M_2000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5_0_histograms.root"],1,'G*->WW (0.1)',2000),
             ]

if signal==2:
    samples=[(["file:/tmp/hinzmann/RSGravitonToZZ_kMpl_01_M_1000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5_0_histograms.root"],1,'G*->ZZ (0.1)',1000),
             (["file:/tmp/hinzmann/RSGravitonToZZ_kMpl_01_M_2000_Tune23_7TeV_herwiggpp_cff_py_GEN_FASTSIM_HLT_PU_vv5_0_histograms.root"],1,'G*->ZZ (0.1)',2000),
             ]

if signal==3:
    samples=[(["file:/tmp/hinzmann/pythia6_Wprime_WZ_1000_vv5_0_histograms.root"],1,"W'->WZ",1000),
             (["file:/tmp/hinzmann/pythia6_Wprime_WZ_2000_vv5_0_histograms.root"],1,"W'->WZ",2000),
             ]

if signal==4:
    samples=[(["file:/tmp/hinzmann/pythia6_qstar_qW_1000_vv5_0_histograms.root"],1,'q*->qW',1000),
             (["file:/tmp/hinzmann/pythia6_qstar_qW_2000_vv5_0_histograms.root"],1,'q*->qW',2000),
             ]

if signal==5:
    samples=[(["file:/tmp/hinzmann/pythia6_qstar_qZ_1000_vv5_0_histograms.root"],1,'q*->qZ',1000),
             (["file:/tmp/hinzmann/pythia6_qstar_qZ_2000_vv5_0_histograms.root"],1,'q*->qZ',2000),
             ]

if signal==1:
    samples=[#(["file:/tmp/hinzmann/428_RSGravitonToWW_kMpl01_M_750_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1,'G*->WW',750),
             (["file:/tmp/hinzmann/428_RSGravitonToWW_kMpl01_M_1000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1,'G*->WW',1000),
             (["file:/tmp/hinzmann/428_RSGravitonToWW_kMpl01_M_1500_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1,'G*->WW',1500),
             (["file:/tmp/hinzmann/428_RSGravitonToWW_kMpl01_M_2000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1,'G*->WW',2000),
             #(["file:/tmp/hinzmann/428_RSGravitonToWW_kMpl01_M_3000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1,'G*->WW',3000),
             ]

if signal==2:
    samples=[#(["file:/tmp/hinzmann/428_RSGravitonToZZ_kMpl01_M_750_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1,'G*->ZZ',750),
             (["file:/tmp/hinzmann/428_RSGravitonToZZ_kMpl01_M_1000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1,'G*->ZZ',1000),
             (["file:/tmp/hinzmann/428_RSGravitonToZZ_kMpl01_M_1500_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1,'G*->ZZ',1500),
             (["file:/tmp/hinzmann/428_RSGravitonToZZ_kMpl01_M_2000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1,'G*->ZZ',2000),
             #(["file:/tmp/hinzmann/428_RSGravitonToZZ_kMpl01_M_3000_Tune23_7TeV_herwiggpp_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1,'G*->ZZ',3000),
             ]

if signal==3:
    samples=[#(["file:/tmp/hinzmann/428_WprimeToWZ_M_750_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1,"W'->WZ",750),
             (["file:/tmp/hinzmann/428_WprimeToWZ_M_1000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1,"W'->WZ",1000),
             (["file:/tmp/hinzmann/428_WprimeToWZ_M_1500_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1,"W'->WZ",1500),
             (["file:/tmp/hinzmann/428_WprimeToWZ_M_2000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1,"W'->WZ",2000),
             #(["file:/tmp/hinzmann/428_WprimeToWZ_M_3000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1,"W'->WZ",3000),
             ]

if signal==4:
    samples=[(["file:/tmp/hinzmann/428_QstarToQW_M_750_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1,'q*->qW',750),
             #(["file:/tmp/hinzmann/428_QstarToQW_M_1000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_4_0_histograms.root"],1,'q*->qW',1000),
             (["file:/tmp/hinzmann/428_QstarToQW_M_1500_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1,'q*->qW',1500),
             #(["file:/tmp/hinzmann/428_QstarToQW_M_2000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1,'q*->qW',2000),
             (["file:/tmp/hinzmann/428_QstarToQW_M_3000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1,'q*->qW',3000),
             ]

if signal==5:
    samples=[(["file:/tmp/hinzmann/428_QstarToQZ_M_750_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1,'q*->qZ',750),
             #(["file:/tmp/hinzmann/428_QstarToQZ_M_1000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1,'q*->qZ',1000),
             (["file:/tmp/hinzmann/428_QstarToQZ_M_1500_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1,'q*->qZ',1500),
             #(["file:/tmp/hinzmann/428_QstarToQZ_M_2000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1,'q*->qZ',2000),
             (["file:/tmp/hinzmann/428_QstarToQZ_M_3000_TuneZ2_7TeV_pythia6_Fall11-PU_S6_START42_V14B-v1_vv9_3_0_histograms.root"],1,'q*->qZ',3000),
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
    if signal:
        nevents=30240.
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

if __name__ == '__main__':
    if trigger:
	plotTriggerEff()
    elif signal:
        plotSignalKinematics()
    else:
        plotDataMCKinematics()
	plotDataMCTagging()
