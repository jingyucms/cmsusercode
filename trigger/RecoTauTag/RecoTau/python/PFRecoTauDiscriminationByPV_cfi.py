import FWCore.ParameterSet.Config as cms
from RecoTauTag.RecoTau.TauDiscriminatorTools import noPrediscriminants

pfRecoTauDiscriminationByPV = cms.EDProducer("PFRecoTauDiscriminationByPV",
    # Tau collection to discriminate
    PFTauProducer = cms.InputTag('pfRecoTauProducer'),

    Prediscriminants = noPrediscriminants,

    # Vertex from primary vertex collection
    vertexSrc = cms.InputTag("offlinePrimaryVerticesWithBS"),
    
    # use leading track instead of primary vertex collection
    useLeadingTrack = cms.bool(False),
    
    # Vertex from leading track to be used
    trackSrc = cms.InputTag("globalTracks"),
    
    # use leading RecoCandidate instead of primary vertex collection
    useLeadingRecoCandidate = cms.bool(False),
    
    # Vertex from RecoCandidate(e.g. lepton) track to be used
    recoCandidateSrc = cms.InputTag("gsfElectrons"),
    
    # max dZ distance to primary vertex
    dZ = cms.double(0.2),
)
