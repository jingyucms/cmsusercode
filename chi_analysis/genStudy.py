import os, sys
from ROOT import * 
from DataFormats.FWLite import Events,Handle

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

def calculateAngles(thep4H, thep4Z1, thep4M11, thep4M12, thep4Z2, thep4M21, thep4M22):
	
	#std::cout << "In calculate angles..." << std::endl;
	boostX = -(thep4H.BoostVector());
	thep4Z1inXFrame = TLorentzVector( thep4Z1 );
	thep4Z2inXFrame = TLorentzVector( thep4Z2 );	
	thep4Z1inXFrame.Boost( boostX );
	thep4Z2inXFrame.Boost( boostX );
	theZ1X_p3 = TVector3( thep4Z1inXFrame.X(), thep4Z1inXFrame.Y(), thep4Z1inXFrame.Z() );
	theZ2X_p3 = TVector3( thep4Z2inXFrame.X(), thep4Z2inXFrame.Y(), thep4Z2inXFrame.Z() );
	
	# calculate phi1, phi2, costhetastar
	phi1 = theZ1X_p3.Phi();
	phi2 = theZ2X_p3.Phi();
	#######################/
	# check for z1/z2 convention
	#######################/		
	p4Z1 = thep4Z1; p4M11 = thep4M11; p4M12 = thep4M12;
	p4Z2 = thep4Z2; p4M21 = thep4M21; p4M22 = thep4M22;
	costhetastar = theZ1X_p3.CosTheta();
	
	# now helicity angles................................
	boostZ1 = -(p4Z1.BoostVector());
	p4Z2Z1 = TLorentzVector(p4Z2);
	p4Z2Z1.Boost(boostZ1);
	#find the decay axis
	##/TVector3 unitx_1 = -Hep3Vector(p4Z2Z1);
	unitx_1 = TVector3( -p4Z2Z1.X(), -p4Z2Z1.Y(), -p4Z2Z1.Z() );
	norm=1
	if unitx_1.Mag()>0:
            norm = 1/(unitx_1.Mag());
	unitx_1*=norm;
	#boost daughters of z2
	p4M21Z1 = TLorentzVector(p4M21);
	p4M22Z1 = TLorentzVector(p4M22);
	p4M21Z1.Boost(boostZ1);
	p4M22Z1.Boost(boostZ1);
	#create z and y axes
	##/TVector3 unitz_1 = Hep3Vector(p4M21Z1).cross(Hep3Vector(p4M22Z1));
	p4M21Z1_p3 = TVector3( p4M21Z1.X(), p4M21Z1.Y(), p4M21Z1.Z() );
	p4M22Z1_p3 = TVector3( p4M22Z1.X(), p4M22Z1.Y(), p4M22Z1.Z() );
	unitz_1 = p4M21Z1_p3.Cross( p4M22Z1_p3 );
	if unitz_1.Mag()>0:
            norm = 1/(unitz_1.Mag());
	unitz_1 *= norm;
	unity_1 = unitz_1.Cross(unitx_1);
	
	#caculate theta1
	p4M11Z1 = TLorentzVector(p4M11);
	p4M11Z1.Boost(boostZ1);
	p3M11 = TVector3( p4M11Z1.X(), p4M11Z1.Y(), p4M11Z1.Z() );
	unitM11 = p3M11.Unit();
	x_m11 = unitM11.Dot(unitx_1); y_m11 = unitM11.Dot(unity_1); z_m11 = unitM11.Dot(unitz_1);
	M11_Z1frame = TVector3 (y_m11, z_m11, x_m11);
	costheta1 = M11_Z1frame.CosTheta();
	#std::cout << "theta1: " << M11_Z1frame.Theta() << std::endl;
	###-----------------------old way of calculating phi---------------####/
	phi = M11_Z1frame.Phi();
	
	#set axes for other system
	boostZ2 = -(p4Z2.BoostVector());
	p4Z1Z2 = TLorentzVector(p4Z1);
	p4Z1Z2.Boost(boostZ2);
	unitx_2 = TVector3( -p4Z1Z2.X(), -p4Z1Z2.Y(), -p4Z1Z2.Z() );
	if unitx_2.Mag()>0:
            norm = 1/(unitx_2.Mag());
	unitx_2*=norm;
	#boost daughters of z2
	p4M11Z2 = TLorentzVector(p4M11);
	p4M12Z2 = TLorentzVector(p4M12);
	p4M11Z2.Boost(boostZ2);
	p4M12Z2.Boost(boostZ2);
	p4M11Z2_p3 = TVector3( p4M11Z2.X(), p4M11Z2.Y(), p4M11Z2.Z() );
	p4M12Z2_p3 = TVector3( p4M12Z2.X(), p4M12Z2.Y(), p4M12Z2.Z() );
	unitz_2 = p4M11Z2_p3.Cross( p4M12Z2_p3 );
	if unitz_2.Mag()>0:
            norm = 1/(unitz_2.Mag());
	unitz_2*=norm;
	unity_2 = unitz_2.Cross(unitx_2);
	#calcuate theta2
	p4M21Z2 = TLorentzVector(p4M21);
	p4M21Z2.Boost(boostZ2);
	p3M21 = TVector3( p4M21Z2.X(), p4M21Z2.Y(), p4M21Z2.Z() );
	unitM21 = p3M21.Unit();
	x_m21 = unitM21.Dot(unitx_2); y_m21 = unitM21.Dot(unity_2); z_m21 = unitM21.Dot(unitz_2);
	M21_Z2frame = TVector3(y_m21, z_m21, x_m21);
	costheta2 = M21_Z2frame.CosTheta();
	
	# calculate phi
	#calculating phi_n
	n_p4Z1inXFrame = TLorentzVector( p4Z1 );
	n_p4M11inXFrame = TLorentzVector( p4M11 );
	n_p4Z1inXFrame.Boost( boostX );
	n_p4M11inXFrame.Boost( boostX );        
	n_p4Z1inXFrame_unit = n_p4Z1inXFrame.Vect().Unit();
	n_p4M11inXFrame_unit = n_p4M11inXFrame.Vect().Unit();  
	n_unitz_1 = TVector3( n_p4Z1inXFrame_unit );
	## y-axis is defined by neg lepton cross z-axis
	## the subtle part is here...
	#####TVector3 n_unity_1 = n_p4M11inXFrame_unit.Cross( n_unitz_1 );
	n_unity_1 = n_unitz_1.Cross( n_p4M11inXFrame_unit );
	n_unitx_1 = n_unity_1.Cross( n_unitz_1 );
	
	n_p4M21inXFrame = TLorentzVector( p4M21 );
	n_p4M21inXFrame.Boost( boostX );
	n_p4M21inXFrame_unit = n_p4M21inXFrame.Vect().Unit();
	#rotate into other plane
	n_p4M21inXFrame_unitprime = TVector3 ( n_p4M21inXFrame_unit.Dot(n_unitx_1), n_p4M21inXFrame_unit.Dot(n_unity_1), n_p4M21inXFrame_unit.Dot(n_unitz_1) );
	
	#/ and then calculate phistar1
	n_p4PartoninXFrame_unit = TVector3( 0.0, 0.0, 1.0 );
	n_p4PartoninXFrame_unitprime = TVector3( n_p4PartoninXFrame_unit.Dot(n_unitx_1), n_p4PartoninXFrame_unit.Dot(n_unity_1), n_p4PartoninXFrame_unit.Dot(n_unitz_1) );
	# negative sign is for arrow convention in paper
	phistar1 = (n_p4PartoninXFrame_unitprime.Phi());
	
	# and the calculate phistar2
	n_p4Z2inXFrame = TLorentzVector( p4Z2 );
	n_p4Z2inXFrame.Boost( boostX );
	n_p4Z2inXFrame_unit = n_p4Z2inXFrame.Vect().Unit();
	###/TLorentzVector n_p4M21inXFrame( p4M21 );
	###n_p4M21inXFrame.Boost( boostX );        
	##TVector3 n_p4M21inXFrame_unit = n_p4M21inXFrame.Vect().Unit();  
	n_unitz_2 = TVector3( n_p4Z2inXFrame_unit );
	## y-axis is defined by neg lepton cross z-axis
	## the subtle part is here...
	###TVector3 n_unity_2 = n_p4M21inXFrame_unit.Cross( n_unitz_2 );
	n_unity_2 = n_unitz_2.Cross( n_p4M21inXFrame_unit );
	n_unitx_2 = n_unity_2.Cross( n_unitz_2 );
	n_p4PartoninZ2PlaneFrame_unitprime = TVector3( n_p4PartoninXFrame_unit.Dot(n_unitx_2), n_p4PartoninXFrame_unit.Dot(n_unity_2), n_p4PartoninXFrame_unit.Dot(n_unitz_2) );
	phistar2 = (n_p4PartoninZ2PlaneFrame_unitprime.Phi());

        return (costheta1, costheta2, phi, costhetastar, phistar1, phistar2, phi1, phi2)

def lv(p):
    return TLorentzVector(p.p4().Px(),p.p4().Py(),p.p4().Pz(),p.p4().E())

def createPlots(sample,prefix,jets=0):
    if sample.endswith(".txt"):
        files=[]
        filelist=open(sample)
	for line in filelist.readlines():
	    if ".root" in line:
	        files+=[line.strip()]
    else:
        files=[sample]
    #generator_handle=Handle("GenEventInfoProduct")
    #generator_label="generator"
    #particles_handle=Handle("std::vector<reco::GenParticle>")
    #particles_label="genParticles"
    prunedgenjets_handle=Handle("std::vector<reco::GenJet>")
    prunedgenjets_label="ak5GenJets"
    #vertices_handle=Handle("std::vector<reco::Vertex>")
    #vertices_label="offlinePrimaryVertices"

    plots=[]
    plots += [TH1F(prefix+'M(X)',';m(X) [GeV];N',50,0,5000)]
    plots += [TH1F(prefix+'y_{boost}',';y_{boost};N',15,0,3)]
    plots += [TH1F(prefix+'#Chi',';#Chi;N',15,1,16)]
    plots += [TH1F(prefix+'#Chi',';#Chi;N',15,1,16)]
    plots += [TH1F(prefix+'#Chi',';#Chi;N',15,1,16)]
    plots += [TH1F(prefix+'#Chi',';#Chi;N',15,1,16)]
    
    for plot in plots:
        plot.Sumw2()

    event_count=0
    events=Events(files)
    for event in events:
        event_count+=1
	if event_count%10000==1:
	    print "Event:",event_count
        #events.getByLabel(generator_label,generator_handle)
        #generator=generator_handle.product()
        #weight=generator.weight()
	weight=1
	try:
            events.getByLabel(prunedgenjets_label,prunedgenjets_handle)
            prunedgenjets=prunedgenjets_handle.product()
	except: continue
	if len(prunedgenjets)<2: continue
        z1=lv(prunedgenjets[0])
        z2=lv(prunedgenjets[1])
	if abs(z1.Rapidity())>2.5 or abs(z2.Rapidity())>2.5 or abs(z1.Rapidity()+z2.Rapidity())>1.11 or exp(abs(z1.Rapidity()-z2.Rapidity()))>16: continue
        q11=z1
        q12=z1
        q21=z2
        q22=z2
	x=z1+z2

	#if event_count>100:
	#    break

	if abs(q11.Eta())>5.0: continue
	if abs(q12.Eta())>5.0: continue
	if abs(q21.Eta())>5.0: continue
	if abs(q22.Eta())>5.0: continue
	if q11.Pt()<10: continue
	if q12.Pt()<10: continue
	if q21.Pt()<10: continue
	if q22.Pt()<10: continue
        plots[0].Fill(x.M(),weight)		
	if x.M()<1900: continue
        plots[1].Fill(abs(z1.Rapidity()+z2.Rapidity()),weight)
	if x.M()>=1900 and x.M()<2400:
            plots[2].Fill(exp(abs(z1.Rapidity()-z2.Rapidity())),weight)
	if x.M()>=2400 and x.M()<3000:
            plots[3].Fill(exp(abs(z1.Rapidity()-z2.Rapidity())),weight)
	if x.M()>=3000 and x.M()<4000:
            plots[4].Fill(exp(abs(z1.Rapidity()-z2.Rapidity())),weight)
	if x.M()>=4000:
            plots[5].Fill(exp(abs(z1.Rapidity()-z2.Rapidity())),weight)
    print "Event:",event_count
    for plot in plots:
        if plot.Integral()>0:
            plot.Scale(1./plot.Integral())
        plot.GetYaxis().SetRangeUser(plot.GetMaximum()/10000,plot.GetMaximum()*1.4)
    return plots

if __name__ == '__main__':

   wait=False
 
   for jets in [1]:#0,1,2,3,100,101,102

    l1="Py8 QCD 7 TeV"
    l2="Py8 QCD 8 TeV"
    
    if jets==1:
       prefix = "GEN_genjetstudyhigh"
       #plotsHpp=createPlots("/tmp/hinzmann/pythia8_qcd7TeV_genStudy2_PFAOD.root",l1,jets)
       #plotsPy6=createPlots("/tmp/hinzmann/pythia8_qcd8TeV_genStudy2_PFAOD.root",l2,jets)
       plotsHpp=createPlots("fileList_pythia8_qcd7TeV_2500_grid.txt",l1,jets)
       plotsPy6=createPlots("fileList_pythia8_qcd8TeV_2500_grid.txt",l2,jets)

    canvas = TCanvas("","",0,0,600,400)
    canvas.Divide(3,2)

    canvas.cd(1)
    canvas.GetPad(1).SetLogy()
    plotsPy6[0].Draw("")
    #plotsPy6[0].SetLineColor(2)
    #plotsPy6[0].Draw("same")
    plotsHpp[0].SetLineColor(4)
    plotsHpp[0].Draw("same")
    #plotsHpp[0].SetLineColor(6)
    #plotsHpp[0].Draw("same")
    legend1=TLegend(0.6,0.6,0.9,0.9,"")
    legend1.AddEntry(plotsHpp[0],l1,"l")
    legend1.AddEntry(plotsPy6[0],l2,"l")
    legend1.SetTextSize(0.04)
    legend1.SetFillStyle(0)
    legend1.Draw("same")
    print "number of events passed:",plotsHpp[0].GetEntries()
    print "number of events passed:",plotsPy6[0].GetEntries()

    canvas.cd(2)
    plotsPy6[1].Draw("")
    #plotsPy6[1].SetLineColor(2)
    #plotsPy6[1].Draw("same")
    plotsHpp[1].SetLineColor(4)
    plotsHpp[1].Draw("same")
    #plotsHpp[1].SetLineColor(6)
    #plotsHpp[1].Draw("same")

    canvas.cd(3)
    plotsPy6[2].Draw("")
    #plotsPy6[2].SetLineColor(2)
    #plotsPy6[2].Draw("same")
    plotsHpp[2].SetLineColor(4)
    plotsHpp[2].Draw("same")
    #plotsHpp[2].SetLineColor(6)
    #plotsHpp[2].Draw("same")

    canvas.cd(4)
    plotsPy6[3].Draw("")
    #plotsPy6[3].SetLineColor(2)
    #plotsPy6[3].Draw("same")
    plotsHpp[3].SetLineColor(4)
    plotsHpp[3].Draw("same")
    #plotsHpp[3].SetLineColor(6)
    #plotsHpp[3].Draw("same")

    canvas.cd(5)
    plotsPy6[4].Draw("")
    #plotsPy6[4].SetLineColor(2)
    #plotsPy6[4].Draw("same")
    plotsHpp[4].SetLineColor(4)
    plotsHpp[4].Draw("same")
    #plotsHpp[4].SetLineColor(6)
    #plotsHpp[4].Draw("same")

    canvas.cd(6)
    plotsPy6[5].Draw("")
    #plotsPy6[5].SetLineColor(2)
    #plotsPy6[5].Draw("same")
    plotsHpp[5].SetLineColor(4)
    plotsHpp[5].Draw("same")
    #plotsHpp[5].SetLineColor(6)
    #plotsHpp[5].Draw("same")

    canvas.SaveAs(prefix + '_x.root')
    canvas.SaveAs(prefix + '_x.pdf')
    canvas.SaveAs(prefix + '_x.eps')
    if wait:
        os.system("ghostview "+prefix + '_x.eps')

