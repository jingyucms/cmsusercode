// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Projections/FastJets.hh"
#include "fastjet/tools/Pruner.hh"
#include "GeneratorInterface/RivetInterface/src/Njettiness.hh"

namespace Rivet {

  class CMS_JME_13_006 : public Analysis {
  public:
    CMS_JME_13_006() : Analysis("CMS_JME_13_006") {
       setBeams(PROTON, PROTON);
    }
//=====================================================INIT
    void init() {
      FinalState fs;
      FastJets jets(fs, FastJets::CAM, 0.8);
      addProjection(jets, "jets");
      _h_tau21 = bookHistogram1D(1, 1, 1);
      _h_tau21_masscut = bookHistogram1D(2, 1, 1);
      _h_tau21_prunedmasscut = bookHistogram1D(3, 1, 1);
    }
//=====================================================ANALYZE
    void analyze(const Event& event) {
      const double weight = event.weight();
      const PseudoJets& jets = applyProjection<FastJets>(event, "jets").pseudoJetsByPt();
      if (jets.size() < 2) vetoEvent;
      double mjj = (jets[0]+jets[1]).m();
      if (mjj < 890) vetoEvent;
      if (fabs(jets[0].eta()-jets[1].eta()) > 1.3) vetoEvent;
      if (fabs(jets[0].eta()) > 2.4) vetoEvent;
      if (jets[0].pt() < 400) vetoEvent;
      if (jets[0].pt() > 600) vetoEvent;
      fastjet::Pruner pruner(fastjet::cambridge_algorithm, 0.1, 0.5);      
      NsubParameters paraNsub = NsubParameters(1.0, 0.8); //assume R=0.8 jet clusering used
      Njettiness routine(Njettiness::onepass_kt_axes, paraNsub);
      const double tau1 = routine.getTau(1, jets[0].constituents());
      const double tau2 = routine.getTau(2, jets[0].constituents());
      const double jetMass = jets[0].m();
      const double prunedJetMass = pruner(jets[0]).m();
      _h_tau21->fill(tau2/tau1, weight);
      if((jetMass>60)&&(jetMass<100))
        _h_tau21_masscut->fill(tau2/tau1, weight);
      if((prunedJetMass>60)&&(prunedJetMass<100))
        _h_tau21_prunedmasscut->fill(tau2/tau1, weight);
    }
//=====================================================FINALIZE
    void finalize() {
      normalize(_h_tau21,1./double(_nBins));
      normalize(_h_tau21_masscut,1./double(_nBins));
      normalize(_h_tau21_prunedmasscut,1./double(_nBins));
    }
//=====================================================DECLARATIONS
  private:
      AIDA::IHistogram1D * _h_tau21;
      AIDA::IHistogram1D * _h_tau21_masscut;
      AIDA::IHistogram1D * _h_tau21_prunedmasscut;
      static const unsigned _nBins = 20;
  };
  // This global object acts as a hook for the plugin system
  AnalysisBuilder<CMS_JME_13_006> plugin_CMS_JME_13_006;
}
