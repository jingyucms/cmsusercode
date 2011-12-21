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

prefix = "plots/genstudy_compare"
wait=True

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

def createPlots(sample,prefix):
    plots=[]
    plots += [TH1F(prefix+'M(X)',';m(X) [GeV];N',40,920,1080)]
    plots += [TH1F(prefix+'M(Z1)',';m(Z1) [GeV];N',40,70,110)]
    plots += [TH1F(prefix+'M(Z2)',';m(Z2) [GeV];N',40,70,110)]
    plots += [TH1F(prefix+'#Delta #eta',';#Delta #eta;N',15,0,3)]
    plots += [TH1F(prefix+'cos(#theta_{1})',';cos(#theta_{1});N',15,-1,1)]
    plots += [TH1F(prefix+'cos(#theta_{2})',';cos(#theta_{2});N',15,-1,1)]
    plots += [TH1F(prefix+'#phi',';#phi;N',15,-3.1416,3.1416)]
    plots += [TH1F(prefix+'cos(#theta*)',';cos(#theta*);N',15,-1,1)]
    plots += [TH1F(prefix+'#phi_{1}*',';#phi_{1}*;N',15,-3.1416,3.1416)]
    plots += [TH1F(prefix+'#phi_{2}*',';#phi_{2}*;N',15,-3.1416,3.1416)]
    plots += [TH1F(prefix+'#phi_{1}',';#phi_{1};N',15,-3.1416,3.1416)]
    plots += [TH1F(prefix+'#phi_{2}',';#phi_{2};N',15,-3.1416,3.1416)]
    
    for plot in plots:
        plot.Sumw2()

    events=Events(sample[0])
    particles_handle=Handle("std::vector<reco::GenParticle>")
    particles_label="genParticlesStatus3"
    event_count=0
    for event in events:
        event_count+=1
	if event_count>1000:
	    break
	#print "Event:",event_count
        events.getByLabel(particles_label,particles_handle)
        particles=particles_handle.product()
	#for i_particle in range(len(particles)):
	#    print i_particle, particles[i_particle].pdgId()
        x=particles[sample[1]]
	z1=particles[sample[2]]
	z2=particles[sample[3]]
	assert(z1.pdgId()==23)
	assert(z2.pdgId()==23)
	assert(z1.mother(0)==x)
	assert(z2.mother(0)==x)
	q11=z1.daughter(0)
	q12=z1.daughter(1)
	q21=z2.daughter(0)
	q22=z2.daughter(1)
	if abs(q11.eta())>5.0: continue
	if abs(q12.eta())>5.0: continue
	if abs(q21.eta())>5.0: continue
	if abs(q22.eta())>5.0: continue
	if q11.pt()<10: continue
	if q12.pt()<10: continue
	if q21.pt()<10: continue
	if q22.pt()<10: continue
        plots[0].Fill(x.mass())		
        plots[1].Fill(z1.mass())		
        plots[2].Fill(z2.mass())
        plots[3].Fill(abs(z1.eta()-z2.eta()))
	angles=calculateAngles(lv(x),lv(z1),lv(q11),lv(q12),lv(z2),lv(q21),lv(q22))
        plots[4].Fill(angles[0])		
        plots[5].Fill(angles[1])		
        plots[6].Fill(angles[2])		
        plots[7].Fill(angles[3])		
        plots[8].Fill(angles[4])		
        plots[9].Fill(angles[5])		
        plots[10].Fill(angles[6])		
        plots[11].Fill(angles[7])
    for plot in plots:
        if plot.Integral()>0:
            plot.Scale(1./plot.Integral())
        plot.GetYaxis().SetRangeUser(0,plot.GetMaximum()*1.3)
    return plots

if __name__ == '__main__':

    plotsJHU=createPlots(["/tmp/hinzmann/JHU_graviton_ZZ_1000.root",6,7,8],"JHU")
    plotsPy6=createPlots(["/tmp/hinzmann/pythia6_gravitonZZ_1000_noMPI_noHAD_noSHOWER_PFAOD.root",6,7,8],"Py6")
    plotsHpp=createPlots(["/tmp/hinzmann/herwigpp_graviton_ZZ_1000_noMPI_noHAD_noSHOWER_PFAOD.root",4,5,6,],"Hpp")
    #plotsPy6=createPlots(["/tmp/hinzmann/herwigpp_graviton_ZZ_1000_l1851_noMPI_noHAD_noSHOWER_PFAOD.root",4,5,6,],"Hpp01")

    canvas = TCanvas("","",0,0,600,400)
    canvas.Divide(3,2)

    canvas.cd(1)
    #canvas.GetPad(1).SetLogy()
    plotsJHU[0].Draw("")
    plotsPy6[0].SetLineColor(2)
    plotsPy6[0].Draw("same")
    plotsHpp[0].SetLineColor(4)
    plotsHpp[0].Draw("same")
    legend1=TLegend(0.6,0.6,0.9,0.9,"")
    legend1.AddEntry(plotsJHU[0],"JHU","l")
    legend1.AddEntry(plotsPy6[0],"Py6","l")
    #legend1.AddEntry(plotsPy6[0],"H++ 0.1","l")
    legend1.AddEntry(plotsHpp[0],"H++ 0.02","l")
    legend1.SetTextSize(0.04)
    legend1.SetFillStyle(0)
    legend1.Draw("same")

    canvas.cd(2)
    plotsJHU[1].Draw("")
    plotsPy6[1].SetLineColor(2)
    plotsPy6[1].Draw("same")
    plotsHpp[1].SetLineColor(4)
    plotsHpp[1].Draw("same")

    canvas.cd(3)
    plotsJHU[2].Draw("")
    plotsPy6[2].SetLineColor(2)
    plotsPy6[2].Draw("same")
    plotsHpp[2].SetLineColor(4)
    plotsHpp[2].Draw("same")

    canvas.cd(4)
    plotsJHU[3].Draw("")
    plotsPy6[3].SetLineColor(2)
    plotsPy6[3].Draw("same")
    plotsHpp[3].SetLineColor(4)
    plotsHpp[3].Draw("same")

    canvas.cd(5)
    plotsJHU[4].Draw("")
    plotsPy6[4].SetLineColor(2)
    plotsPy6[4].Draw("same")
    plotsHpp[4].SetLineColor(4)
    plotsHpp[4].Draw("same")

    canvas.cd(6)
    plotsJHU[5].Draw("")
    plotsPy6[5].SetLineColor(2)
    plotsPy6[5].Draw("same")
    plotsHpp[5].SetLineColor(4)
    plotsHpp[5].Draw("same")

    canvas.SaveAs(prefix + '_x.root')
    canvas.SaveAs(prefix + '_x.pdf')
    canvas.SaveAs(prefix + '_x.eps')
    if wait:
        os.system("ghostview "+prefix + '_x.eps')

    canvas = TCanvas("","",0,0,600,400)
    canvas.Divide(3,2)

    canvas.cd(1)
    plotsJHU[6].Draw("")
    plotsPy6[6].SetLineColor(2)
    plotsPy6[6].Draw("same")
    plotsHpp[6].SetLineColor(4)
    plotsHpp[6].Draw("same")

    canvas.cd(2)
    plotsJHU[7].Draw("")
    plotsPy6[7].SetLineColor(2)
    plotsPy6[7].Draw("same")
    plotsHpp[7].SetLineColor(4)
    plotsHpp[7].Draw("same")
    legend2=TLegend(0.6,0.6,0.9,0.9,"")
    legend2.AddEntry(plotsJHU[0],"JHU","l")
    legend1.AddEntry(plotsPy6[0],"Py6","l")
    #legend2.AddEntry(plotsPy6[0],"H++ 0.1","l")
    legend2.AddEntry(plotsHpp[0],"H++ 0.02","l")
    legend2.SetTextSize(0.04)
    legend2.SetFillStyle(0)
    legend2.Draw("same")

    canvas.cd(3)
    plotsJHU[8].Draw("")
    plotsPy6[8].SetLineColor(2)
    plotsPy6[8].Draw("same")
    plotsHpp[8].SetLineColor(4)
    plotsHpp[8].Draw("same")

    canvas.cd(4)
    plotsJHU[9].Draw("")
    plotsPy6[9].SetLineColor(2)
    plotsPy6[9].Draw("same")
    plotsHpp[9].SetLineColor(4)
    plotsHpp[9].Draw("same")

    canvas.cd(5)
    plotsJHU[10].Draw("")
    plotsPy6[10].SetLineColor(2)
    plotsPy6[10].Draw("same")
    plotsHpp[10].SetLineColor(4)
    plotsHpp[10].Draw("same")

    canvas.cd(6)
    plotsJHU[11].Draw("")
    plotsPy6[11].SetLineColor(2)
    plotsPy6[11].Draw("same")
    plotsHpp[11].SetLineColor(4)
    plotsHpp[11].Draw("same")

    canvas.SaveAs(prefix + '_z.root')
    canvas.SaveAs(prefix + '_z.pdf')
    canvas.SaveAs(prefix + '_z.eps')
    if wait:
        os.system("ghostview "+prefix + '_z.eps')

