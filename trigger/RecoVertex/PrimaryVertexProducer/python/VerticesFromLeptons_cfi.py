import FWCore.ParameterSet.Config as cms

verticesFromElectrons = cms.EDProducer("VertexFromTrackProducer",
    verbose = cms.untracked.bool(False),
    candidateLabel = cms.InputTag("gsfElectrons"),
    useBeamSpot = cms.bool(True),
    beamSpotLabel = cms.InputTag("offlineBeamSpot"),
    useVertex = cms.bool(True),
    vertexLabel = cms.InputTag("offlinePrimaryVertices"),
)

verticesFromMuons = cms.EDProducer("VertexFromTrackProducer",
    verbose = cms.untracked.bool(False),
    candidateLabel = cms.InputTag("muons"),
    useBeamSpot = cms.bool(True),
    beamSpotLabel = cms.InputTag("offlineBeamSpot"),
    useVertex = cms.bool(True),
    vertexLabel = cms.InputTag("offlinePrimaryVertices"),
)
