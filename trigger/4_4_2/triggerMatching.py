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

prefix = "plots/tauisolation_original"
wait=True

def makeEfficiency(passing, all):
    gragh=TGraphAsymmErrors(passing, all)
    gragh.GetXaxis().SetTitle(passing.GetXaxis().GetTitle())
    gragh.GetYaxis().SetTitle(passing.GetYaxis().GetTitle())
    gragh.GetXaxis().SetRangeUser(passing.GetXaxis().GetBinLowEdge(1),passing.GetXaxis().GetBinUpEdge(passing.GetNbinsX()))
    gragh.GetYaxis().SetRangeUser(0,1)
    return gragh

if __name__ == '__main__':

    legend=TLegend(0.7,0.6,0.9,0.9,"")
    tau_pt = TH1F('tau pT',';pT [GeV];N',20,10,50)
    tau_pt.Sumw2()

    filter_tau_pt = TH1F('tau pT eff',';pT [GeV];Trigger efficiency',20,10,50)
    filter_tau_pt.Sumw2()

    filter2_tau_pt = TH1F('tau pT eff2',';pT [GeV];Trigger efficiency',20,10,50)
    filter2_tau_pt.Sumw2()
    filter2_tau_pt.SetLineColor(2)

    filter3_tau_pt = TH1F('tau pT eff3',';pT [GeV];Trigger efficiency',20,10,50)
    filter3_tau_pt.Sumw2()
    filter3_tau_pt.SetLineColor(4)

    filter4_tau_pt = TH1F('tau pT eff4',';pT [GeV];Trigger efficiency',20,10,50)
    filter4_tau_pt.Sumw2()
    filter4_tau_pt.SetLineColor(3)

    ele_pt = TH1F('ele pT',';pT [GeV];N',20,10,50)
    ele_pt.Sumw2()
    
    filter_ele_pt = TH1F('ele pT eff',';pT [GeV];Trigger efficiency',20,10,50)
    filter_ele_pt.Sumw2()

    vertex_n = TH1F('tau pT 20 vertex n',';N(vertices);N',35,0,34)
    vertex_n.Sumw2()

    filter_vertex_n = TH1F('tau pT 20 vertex n eff',';N(vertices);Trigger efficiency',35,0,34)
    filter_vertex_n.Sumw2()

    filter2_vertex_n = TH1F('tau pT 20 vertex n eff2',';N(vertices);Trigger efficiency',35,0,34)
    filter2_vertex_n.Sumw2()
    filter2_vertex_n.SetLineColor(2)

    filter3_vertex_n = TH1F('tau pT 20 vertex n eff3',';N(vertices);Trigger efficiency',35,0,34)
    filter3_vertex_n.Sumw2()
    filter3_vertex_n.SetLineColor(4)

    filter4_vertex_n = TH1F('tau pT 20 vertex n eff4',';N(vertices);Trigger efficiency',35,0,34)
    filter4_vertex_n.Sumw2()
    filter4_vertex_n.SetLineColor(3)

    ele_vertex_n = TH1F('ele pT 20 vertex n',';N(vertices);Trigger efficiency',35,0,34)
    ele_vertex_n.Sumw2()

    filterele_vertex_n = TH1F('ele pT 20 vertex n eff',';N(vertices);Trigger efficiency',35,0,34)
    filterele_vertex_n.Sumw2()

    veff_vertex_n = TH1F('tau pT 20 vertex 1 eff',';N(vertices);Primary vertex matched',35,0,34)
    veff_vertex_n.Sumw2()

    vreco_vertex_n = TH1F('tau pT 20 vertex 1 reco',';N(vertices);Primary vertex reconstructed',35,0,34)
    vreco_vertex_n.Sumw2()

    hltvertex_n = TH1F('tau pT 20 hltvertex n',';N(HLT-vertices);N',20,0,19)
    hltvertex_n.Sumw2()

    filter_hltvertex_n = TH1F('tau pT 20 hltvertex n eff',';N(vertices);Trigger efficiency',20,0,19)
    filter_hltvertex_n.Sumw2()

    matched_vertex_n = TH2F('vertex n eff',';N(vertices);N(HLT-vertices)',30,0,29,20,0,19)
    matched_vertex_n.Sumw2()

    #events=Events("/tmp/hinzmann/trigger_study_original.root")
    #events=Events("/tmp/hinzmann/trigger_study_isolation_PV_off.root")
    #events=Events("/tmp/hinzmann/trigger_study_noiso_nodZ_primaryvertex_everywhere_debug.root")
    #events=Events("/tmp/hinzmann/trigger_study_offlineVertex_mu.root")
    #events=Events("/tmp/hinzmann/trigger_study_offlineVertex_e.root")
    #events=Events("/tmp/hinzmann/trigger_study_offlineVertex_pix.root")
    #events=Events("/tmp/hinzmann/trigger_study_offlineVertex_off.root")
    #events=Events("/tmp/hinzmann/trigger_study_offlineVertex_off_iso1.root")
    #events=Events("/tmp/hinzmann/trigger_study_offlineVertex_off_sumpt.root")
    #events=Events("/tmp/hinzmann/trigger_study_offlineVertex_off_relsumpt.root")
    events=Events("/tmp/hinzmann/trigger_study_all.root")
    #events=Events("/tmp/hinzmann/trigger_study_trackmaxdz02_nousepvconstraint.root")

    tau_handle=Handle("std::vector<reco::PFTau>")
    tau_label="offlineSelectedPFTausLooseIsoTrackFinding"
    #tau_label="offlineSelectedPFTausMediumIsoTrackFinding"
    #tau_label="offlineSelectedPFTausTightIsoTrackFinding"

    hlttau_handle=Handle("std::vector<reco::PFTau>")
    hlttau_label="hltPFTausMediumIso"

    ele_handle=Handle("std::vector<reco::GsfElectron>")
    ele_label="gsfElectrons"

    hltele_handle=Handle("std::vector<reco::Electron>")
    hltele_label="hltPixelMatchElectronsL1Iso"

    #l1filter_handle=Handle("trigger::TriggerFilterObjectWithRefs")
    #l1filter_label="hltL1sL1SingleEG18orL1SingleEG20"

    #elefilter_handle=Handle("trigger::TriggerFilterObjectWithRefs")
    #elefilter_label="hltOverlapFilterIsoEle20CaloJet5"

    isolationfilter_handle=Handle("trigger::TriggerFilterObjectWithRefs")
    isolationfilter_label="hltPFTauTightIso20TrackTightIso"

    isolation2filter_handle=Handle("trigger::TriggerFilterObjectWithRefs")
    isolation2filter_label="hltPFTauMediumIso20TrackMediumIso"

    isolation3filter_handle=Handle("trigger::TriggerFilterObjectWithRefs")
    isolation3filter_label="hltPFTauMediumIso20Track"

    isolation4filter_handle=Handle("trigger::TriggerFilterObjectWithRefs")
    isolation4filter_label="hltPFTau20TrackLooseIso"

    electronfilter_handle=Handle("trigger::TriggerFilterObjectWithRefs")
    electronfilter_label="hltEle20CaloIdVTCaloIsoTTrkIdTTrkIsoTTrackIsoFilterL1SingleEG18orL1SingleEG20"

    muonfilter_handle=Handle("trigger::TriggerFilterObjectWithRefs")
    muonfilter_label="hltSingleMuIsoL3IsoFiltered15"

    vertex_handle=Handle("std::vector<reco::Vertex>")
    vertex_label="offlinePrimaryVertices"

    hltvertex_handle=Handle("std::vector<reco::Vertex>")
    #hltvertex_label="offlinePrimaryVertices"
    #hltvertex_label="hltPixelVertices"
    #hltvertex_label="hltPixelVertices3DbbPhi"
    #hltvertex_label="hltPrimaryVertices"
    #hltvertex_label="hltPrimaryVertices2"
    #hltvertex_label="vertexFromMuon"
    #hltvertex_label="vertexFromElectron"
    #hltvertex_label="verticesFromGsfTracks"
    hltvertex_label="vertexFromTrack"

    event_count=0
    for event in events:
        event_count+=1
	if str(event_count).replace("0","") in ["1","3"]:
            print "Event:",event_count
        events.getByLabel(tau_label,tau_handle)
        taus=tau_handle.product()
        events.getByLabel(hlttau_label,hlttau_handle)
        hlttaus=hlttau_handle.product()
        events.getByLabel(ele_label,ele_handle)
        eles=ele_handle.product()
	try:
            events.getByLabel(hltele_label,hltele_handle)
            hlteles=hltele_handle.product()
	except: hlteles=()
        #events.getByLabel(l1filter_label,l1filter_handle)
        #l1filter=l1filter_handle.product()
        #events.getByLabel(elefilter_label,elefilter_handle)
        #elefilter=elefilter_handle.product()
        events.getByLabel(isolationfilter_label,isolationfilter_handle)
        isolationfilter=isolationfilter_handle.product()
        events.getByLabel(isolation2filter_label,isolation2filter_handle)
        isolation2filter=isolation2filter_handle.product()
        events.getByLabel(isolation3filter_label,isolation3filter_handle)
        isolation3filter=isolation3filter_handle.product()
        events.getByLabel(isolation4filter_label,isolation4filter_handle)
        isolation4filter=isolation4filter_handle.product()
	try:
	    electronfilter=None
            events.getByLabel(electronfilter_label,electronfilter_handle)
            electronfilter=electronfilter_handle.product()
	except: pass #continue
	try:
	    muonfilter=None
            events.getByLabel(muonfilter_label,muonfilter_handle)
            muonfilter=muonfilter_handle.product()
	except: pass #continue
	try:
	    hltvertices=()
            events.getByLabel(hltvertex_label,"","TEST",hltvertex_handle)
            hltvertices=hltvertex_handle.product()
	except: pass #continue
        events.getByLabel(vertex_label,"","RECO",vertex_handle)
        vertices=vertex_handle.product()
        
        num_taus=len(taus)
        num_hlttaus=len(hlttaus)
        num_eles=len(eles)
        num_hlteles=len(hlteles)
        num_vertices=len(vertices)
        num_hltvertices=len(hltvertices)
        #print "Taus:",num_taus
        #print "HLT-Taus:",num_hlttaus
        #print "Es:",num_eles
        #print "HLT-Es:",num_hlteles
        #print "Vertices:",num_vertices
        #print "HLT-Vertices:",num_hltvertices

        #if not l1filter.l1emSize()>0:
	#    continue
        
	matched_tau_20=False
	matched_tau_20_filter=False
	matched_tau_20_filter2=False
	matched_tau_20_filter3=False
	matched_tau_20_filter4=False
        for i_tau in range(num_taus):
            tau=taus[i_tau]
	    matched_hlttau=None
            for i_hlttau in range(num_hlttaus):
        	hlttau=hlttaus[i_hlttau]
        	dPhi=fabs(fmod(tau.phi()-hlttau.phi()+3.0*TMath.Pi(),2.0*TMath.Pi())-TMath.Pi())
        	dEta=fabs(tau.eta()-hlttau.eta())
  	    	dR=sqrt(dPhi*dPhi+dEta*dEta)
		if dR<0.1:
		    matched_hlttau=hlttau
		    break
            if matched_hlttau:
                tau_pt.Fill(tau.pt())		
                if tau.pt()>22:
                    matched_tau_20=True
	        #l1pass=l1filter.l1emSize()>0
		#elepass=elefilter.electronSize()>0
		isolationpass=isolationfilter.jetSize()>0
		isolation2pass=isolation2filter.jetSize()>0
		isolation3pass=isolation3filter.jetSize()>0
		isolation4pass=isolation4filter.jetSize()>0
	        if isolationpass:
                    filter_tau_pt.Fill(tau.pt())
		    if tau.pt()>22:
		        matched_tau_20_filter=True
	        if isolation2pass:
                    filter2_tau_pt.Fill(tau.pt())
		    if tau.pt()>22:
		        matched_tau_20_filter2=True
	        if isolation3pass:
                    filter3_tau_pt.Fill(tau.pt())
		    if tau.pt()>22:
		        matched_tau_20_filter3=True
	        if isolation4pass:
                    filter4_tau_pt.Fill(tau.pt())
		    if tau.pt()>22:
		        matched_tau_20_filter4=True

	matched_ele_20=False
	matched_ele_20_filter=False
        for i_ele in range(num_eles):
            ele=eles[i_ele]
	    matched_hltele=None
            for i_hltele in range(num_hlteles):
        	hltele=hlteles[i_hltele]
        	dPhi=fabs(fmod(ele.phi()-hltele.phi()+3.0*TMath.Pi(),2.0*TMath.Pi())-TMath.Pi())
        	dEta=fabs(ele.eta()-hltele.eta())
  	    	dR=sqrt(dPhi*dPhi+dEta*dEta)
		if dR<0.1:
		    matched_hltele=hltele
		    break
            if matched_hltele:
                ele_pt.Fill(ele.pt())
                if ele.pt()>20:
                    matched_ele_20=True
		elepass=electronfilter and electronfilter.electronSize()>0 and num_hltvertices>0
	        if elepass:
                    filter_ele_pt.Fill(ele.pt())
		    if ele.pt()>20:
		        matched_ele_20_filter=True

        # check lepton vertex reco only
	#matched_tau_20=num_hltvertices>0
	#matched_tau_20=num_hltvertices>0 and electronfilter.electronSize()>0
	#matched_tau_20=muonfilter.muonSize()>0 and num_hltvertices>0
	
        matched_first_vertex=False
        reconstructed_first_vertex=False
        matched_hltvertices=[]
        for i_vertex in range(num_vertices):
            vertex=vertices[i_vertex]
            first_hltvertex=True
	    #max_ntracks=0
            #for i_hltvertex in range(num_hltvertices):
            #    hltvertex=hltvertices[i_hltvertex]
	    #    if hltvertex.nTracks()>max_ntracks:
	    #    max_ntracks=hltvertex.nTracks()
            for i_hltvertex in range(num_hltvertices):
        	hltvertex=hltvertices[i_hltvertex]
	        #if hltvertex.nTracks()<max_ntracks and hltvertex.nTracks()<5:
		#    continue
        	dZ=fabs(vertex.z()-hltvertex.z())
		#if i_vertex==0 and i_hltvertex==0:
		#    print dZ, electronfilter.electronRefs()[0].product()[0].vz()
		if dZ<0.2:
		    matched_hltvertices+=[hltvertex]
		    if i_vertex==0 and first_hltvertex:
		       matched_first_vertex=True
		    if i_vertex==0:
		       reconstructed_first_vertex=True
		    break
		first_hltvertex=False
	if matched_tau_20:
            vertex_n.Fill(num_vertices)
            hltvertex_n.Fill(len(matched_hltvertices))
            if matched_first_vertex:
                veff_vertex_n.Fill(num_vertices)
            if reconstructed_first_vertex:
                vreco_vertex_n.Fill(num_vertices)
	if matched_tau_20_filter:
            filter_vertex_n.Fill(num_vertices)
            filter_hltvertex_n.Fill(len(matched_hltvertices))
	if matched_tau_20_filter2:
            filter2_vertex_n.Fill(num_vertices)
	if matched_tau_20_filter3:
            filter3_vertex_n.Fill(num_vertices)
	if matched_tau_20_filter4:
            filter4_vertex_n.Fill(num_vertices)
	if matched_ele_20:
            ele_vertex_n.Fill(num_vertices)
	if matched_ele_20_filter:
            filterele_vertex_n.Fill(num_vertices)
        matched_vertex_n.Fill(num_vertices,len(matched_hltvertices))		
	    
    canvas = TCanvas("","",0,0,600,400)
    canvas.Divide(3,2)
    canvas.cd(1)
    legend=TLegend(0.4,0.3,0.9,0.5,"")
    graph=makeEfficiency(filter_ele_pt,ele_pt)
    graph.Draw("apz")
    #filterele_ele_pt.Divide(filter_ele_pt,ele_pt,1,1,'B')
    #filterele_ele_pt.Draw("he")
    legend.AddEntry(filter_ele_pt,"reco","l")
    legend.SetTextSize(0.04)
    legend.SetFillStyle(0)
    legend.Draw("same")
    canvas.cd(3)
    legend2=TLegend(0.4,0.3,0.9,0.5,"")
    graphv=makeEfficiency(filterele_vertex_n,vertex_n)
    graphv.Draw("apz")
    fit=TF1('fit graphv','[0]+[1]*x',5,31)
    fit.SetLineColor(1)
    graphv.Fit(fit,"R0")
    fit.Draw('lsame')
    print fit.Eval(15),fit.Eval(30)
    #filterele_vertex_n.Divide(filterele_vertex_n,vertex_n,1,1,'B')
    #filterele_vertex_n.Draw("le")
    legend2.AddEntry(filter_ele_pt,"reco","l")
    legend2.SetTextSize(0.04)
    legend2.SetFillStyle(0)
    legend2.Draw("same")

    canvas.SaveAs(prefix + '_ele.root')
    canvas.SaveAs(prefix + '_ele.pdf')
    canvas.SaveAs(prefix + '_ele.eps')
    if wait:
        os.system("ghostview "+prefix + '_ele.eps')
	    
    canvas = TCanvas("","",0,0,600,400)
    canvas.Divide(3,2)
    canvas.cd(1)
    legend=TLegend(0.4,0.3,0.9,0.5,"")
    graph3=makeEfficiency(filter3_tau_pt,tau_pt)
    graph3.Draw("apz")
    graph4=makeEfficiency(filter4_tau_pt,tau_pt)
    graph4.Draw("pzsame")
    graph2=makeEfficiency(filter2_tau_pt,tau_pt)
    graph2.Draw("pzsame")
    graph=makeEfficiency(filter_tau_pt,tau_pt)
    graph.Draw("pzsame")
    #filter_tau_pt.Divide(filter_tau_pt,tau_pt,1,1,'B')
    #filter_tau_pt.Draw("he")
    #filter2_tau_pt.Divide(filter2_tau_pt,tau_pt,1,1,'B')
    #filter2_tau_pt.Draw("hesame")
    #filter3_tau_pt.Divide(filter3_tau_pt,tau_pt,1,1,'B')
    #filter3_tau_pt.Draw("hesame")
    legend.AddEntry(filter3_tau_pt,"Track","l")
    legend.AddEntry(filter4_tau_pt,"LooseIso","l")
    legend.AddEntry(filter2_tau_pt,"MediumIso","l")
    legend.AddEntry(filter_tau_pt,"TightIso","l")
    legend.SetTextSize(0.04)
    legend.SetFillStyle(0)
    legend.Draw("same")
    canvas.cd(2)
    canvas.GetPad(2).SetRightMargin(0.12)
    gStyle.SetPalette(1)
    matched_vertex_n.Draw("colz")
    canvas.cd(3)
    legend2=TLegend(0.4,0.3,0.9,0.5,"")
    graphv3=makeEfficiency(filter3_vertex_n,vertex_n)
    graphv3.Draw("apz")
    fit3=TF1('fit graphv3','[0]+[1]*x',5,31)
    fit3.SetLineColor(4)
    graphv3.Fit(fit3,"R0")
    graphv4=makeEfficiency(filter4_vertex_n,vertex_n)
    graphv4.Draw("pzsame")
    fit4=TF1('fit graphv4','[0]+[1]*x',5,31)
    fit4.SetLineColor(3)
    graphv4.Fit(fit4,"R0")
    graphv2=makeEfficiency(filter2_vertex_n,vertex_n)
    graphv2.Draw("pzsame")
    fit2=TF1('fit graphv2','[0]+[1]*x',5,31)
    fit2.SetLineColor(2)
    graphv2.Fit(fit2,"R0")
    graphv=makeEfficiency(filter_vertex_n,vertex_n)
    graphv.Draw("pzsame")
    fit=TF1('fit graphv','[0]+[1]*x',5,31)
    fit.SetLineColor(1)
    graphv.Fit(fit,"R0")
    fit3.Draw('lsame')
    fit4.Draw('lsame')
    fit2.Draw('lsame')
    fit.Draw('lsame')
    print fit3.Eval(15),fit3.Eval(30)
    print fit4.Eval(15),fit4.Eval(30)
    print fit2.Eval(15),fit2.Eval(30)
    print fit.Eval(15),fit.Eval(30)
    #filter_vertex_n.Divide(filter_vertex_n,vertex_n,1,1,'B')
    #filter_vertex_n.Draw("le")
    #filter2_vertex_n.Divide(filter2_vertex_n,vertex_n,1,1,'B')
    #filter2_vertex_n.Draw("lesame")
    #filter3_vertex_n.Divide(filter3_vertex_n,vertex_n,1,1,'B')
    #filter3_vertex_n.Draw("lesame")
    legend2.AddEntry(filter3_tau_pt,"Track","l")
    legend2.AddEntry(filter4_tau_pt,"LooseIso","l")
    legend2.AddEntry(filter2_tau_pt,"MediumIso","l")
    legend2.AddEntry(filter_tau_pt,"TightIso","l")
    legend2.SetTextSize(0.04)
    legend2.SetFillStyle(0)
    legend2.Draw("same")
    canvas.cd(4)
    graphhv=makeEfficiency(filter_hltvertex_n,hltvertex_n)
    graphhv.Draw("apz")
    #filter_hltvertex_n.Divide(filter_hltvertex_n,hltvertex_n,1,1,'B')
    #filter_hltvertex_n.Draw("le")
    canvas.cd(5)
    graphvv=makeEfficiency(veff_vertex_n,vertex_n)
    graphvv.Draw("apz")
    #veff_vertex_n.Divide(veff_vertex_n,vertex_n,1,1,'B')
    #veff_vertex_n.Draw("le")
    canvas.cd(6)
    graphfv=makeEfficiency(vreco_vertex_n,vertex_n)
    graphfv.Draw("apz")
    #vreco_vertex_n.Divide(vreco_vertex_n,vertex_n,1,1,'B')
    #vreco_vertex_n.Draw("le")

    canvas.SaveAs(prefix + '_pt.root')
    canvas.SaveAs(prefix + '_pt.pdf')
    canvas.SaveAs(prefix + '_pt.eps')
    if wait:
        os.system("ghostview "+prefix + '_pt.eps')
