#include "RecoTauTag/RecoTau/interface/TauDiscriminationProducerBase.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/RecoCandidate/interface/RecoCandidate.h"
#include "DataFormats/Math/interface/Point3D.h"
#include "DataFormats/Math/interface/Error.h"

/* 
 * class PFRecoTauDiscriminationByPV
 * created : January 26 2012,
 * revised : Wed Jan 26 11:13:04 PDT 2012
 * Authors : Andreas Hinzmann (CERN)
 */

using namespace reco;

class PFRecoTauDiscriminationByPV : public PFTauDiscriminationProducerBase  {
   public:
      explicit PFRecoTauDiscriminationByPV(const edm::ParameterSet& iConfig):PFTauDiscriminationProducerBase(iConfig){   
         vertexSrc_ = iConfig.getParameter<edm::InputTag>("vertexSrc");
         useLeadingTrack_ = iConfig.getParameter<bool>("useLeadingTrack");
         trackSrc_ = iConfig.getParameter<edm::InputTag>("trackSrc");
         useLeadingRecoCandidate_ = iConfig.getParameter<bool>("useLeadingRecoCandidate");
         recoCandidateSrc_ = iConfig.getParameter<edm::InputTag>("recoCandidateSrc");
         dZ_ = iConfig.getParameter<double>("dZ");
      }
      ~PFRecoTauDiscriminationByPV(){} 
      void beginEvent(const edm::Event& evt, const edm::EventSetup& evtSetup);
      double discriminate(const PFTauRef& pfTau);
   private:
      edm::InputTag vertexSrc_;
      bool useLeadingTrack_;
      edm::InputTag trackSrc_;
      bool useLeadingRecoCandidate_;
      edm::InputTag recoCandidateSrc_;
      double dZ_;
      edm::Handle<edm::View<reco::Vertex> > vertices;
      edm::Handle<edm::View<reco::Track> > tracks;
      edm::Handle<edm::View<reco::RecoCandidate> > recocandidates;
};

void PFRecoTauDiscriminationByPV::beginEvent(const edm::Event& event,
    const edm::EventSetup& eventSetup) {
   event.getByLabel(vertexSrc_, vertices);
   if (useLeadingTrack_)
   event.getByLabel(trackSrc_, tracks);
   if (useLeadingRecoCandidate_)
   event.getByLabel(recoCandidateSrc_, recocandidates);
}

double PFRecoTauDiscriminationByPV::discriminate(const PFTauRef& pfTau)
{
   double isFromPV=0.;
   // if no vertex in vertex collection or no leading track in tau return false
   if((!vertices.isValid())||
      (vertices->size()==0)||
      (pfTau->leadPFChargedHadrCand().isNull())||
      (pfTau->leadPFChargedHadrCand()->trackRef().isNull()))
      return 0.;

   // discriminate by z position of leading track at vertex
   if (useLeadingTrack_)
   {
       if ((tracks.isValid())&&(tracks->size()>0)){
       double maxpt=0.;
       unsigned i_maxpt=0;
       for (unsigned i = 0; i < tracks->size(); ++i) {
         double pt=tracks->ptrAt(i)->pt();
         if(pt>maxpt)
         {
 	   i_maxpt=i;
 	   maxpt=pt;
         }
       }
       if(fabs(pfTau->leadPFChargedHadrCand()->trackRef()->dz(vertices->at(0).position()) - tracks->ptrAt(i_maxpt)->dz(vertices->at(0).position()) < dZ_))
          isFromPV=1.;
       }
   }

   // discriminate by z position of track of recocandidate at vertex
   else if (useLeadingRecoCandidate_)
   {
       if ((recocandidates.isValid())&&(recocandidates->size()>0)){
       double maxpt=0.;
       unsigned i_maxpt=0;
       for (unsigned i = 0; i < recocandidates->size(); ++i) {
         double pt=recocandidates->ptrAt(i)->pt();
         if(pt>maxpt)
         {
  	   i_maxpt=i;
  	   maxpt=pt;
         }
       }
       if(fabs(pfTau->leadPFChargedHadrCand()->trackRef()->dz(vertices->at(0).position()) - recocandidates->ptrAt(i_maxpt)->bestTrack()->dz(vertices->at(0).position()) < dZ_))
          isFromPV=1.;
       }
   }
    
   // discriminate by z position of leading vertex
   else
   {
       if (fabs(pfTau->leadPFChargedHadrCand()->trackRef()->dz(vertices->at(0).position()))<dZ_)
          isFromPV=1.;
   }
   return isFromPV;
}

DEFINE_FWK_MODULE(PFRecoTauDiscriminationByPV);
