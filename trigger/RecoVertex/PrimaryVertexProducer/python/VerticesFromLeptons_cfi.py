import FWCore.ParameterSet.Config as cms

vertexFromMuon = cms.EDProducer("VertexFromTrackProducer",
    verbose = cms.untracked.bool(False),
    trackLabel = cms.InputTag("muons"),
    isRecoCandidate = cms.bool(True),
    useBeamSpot = cms.bool(True),
    beamSpotLabel = cms.InputTag("offlineBeamSpot"),
    useVertex = cms.bool(True),
    vertexLabel = cms.InputTag("offlinePrimaryVertices"),
)

vertexFromElectron = cms.EDProducer("VertexFromTrackProducer",
    verbose = cms.untracked.bool(False),
    trackLabel = cms.InputTag("gsfElectrons"),
    isRecoCandidate = cms.bool(True),
    useBeamSpot = cms.bool(True),
    beamSpotLabel = cms.InputTag("offlineBeamSpot"),
    useVertex = cms.bool(True),
    vertexLabel = cms.InputTag("offlinePrimaryVertices"),
)

vertexFromTrack = cms.EDProducer("VertexFromTrackProducer",
    verbose = cms.untracked.bool(False),
    trackLabel = cms.InputTag("iterativeTracks"),
    isRecoCandidate = cms.bool(False),
    useBeamSpot = cms.bool(True),
    beamSpotLabel = cms.InputTag("offlineBeamSpot"),
    useVertex = cms.bool(True),
    vertexLabel = cms.InputTag("offlinePrimaryVertices"),
)
