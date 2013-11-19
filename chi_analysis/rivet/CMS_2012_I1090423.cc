// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Tools/BinnedHistogram.hh"

namespace Rivet {

  class CMS_2012_I1090423 : public Analysis {
  public:
    CMS_2012_I1090423() : Analysis("CMS_2012_I1090423") {
       setBeams(PROTON, PROTON);
    }
//=====================================================INIT
    void init() {
      FinalState fs;
      FastJets antikt(fs, FastJets::ANTIKT, 0.5);
      addProjection(antikt, "ANTIKT");
      _h_chi_dijet.addHistogram(3000., 7000., bookHistogram1D(1, 1, 1));
      _h_chi_dijet.addHistogram(2400., 3000., bookHistogram1D(2, 1, 1));
      _h_chi_dijet.addHistogram(1900., 2400., bookHistogram1D(3, 1, 1));
      _h_chi_dijet.addHistogram(1500., 1900., bookHistogram1D(4, 1, 1));
      _h_chi_dijet.addHistogram(1200., 1500., bookHistogram1D(5, 1, 1));
      _h_chi_dijet.addHistogram(1000., 1200., bookHistogram1D(6, 1, 1));
      _h_chi_dijet.addHistogram(800., 1000., bookHistogram1D(7, 1, 1));
      _h_chi_dijet.addHistogram(600., 800., bookHistogram1D(8, 1, 1));
      _h_chi_dijet.addHistogram(400., 600., bookHistogram1D(9, 1, 1));
    }
//=====================================================ANALYZE
    void analyze(const Event& event) {
      const double weight = event.weight();
      const Jets& jets = applyProjection<JetAlg>(event, "ANTIKT").jetsByPt();
      if (jets.size() < 2) vetoEvent;
      FourMomentum j0(jets[0].momentum());
      FourMomentum j1(jets[1].momentum());
      double y0 = j0.rapidity();
      double y1 = j1.rapidity();
      if (fabs(y0+y1)/2. > 1.11) vetoEvent;
      if (exp(fabs(y0-y1)) > 16.) vetoEvent;
      double mjj = FourMomentum(j0+j1).mass();
      double chi = exp(fabs(y0-y1));
      _h_chi_dijet.fill(mjj, chi, weight);

    }
//=====================================================FINALIZE
    void finalize() {
      foreach (AIDA::IHistogram1D* hist, _h_chi_dijet.getHistograms()) {
        normalize(hist);
      }
    }
//=====================================================DECLARATIONS
  private:
    BinnedHistogram<double> _h_chi_dijet;
   };
  // This global object acts as a hook for the plugin system
  AnalysisBuilder<CMS_2012_I1090423> plugin_CMS_2012_I1090423;
}
