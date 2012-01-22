import FWCore.ParameterSet.Config as cms

# Services

hltESPElectronTrajectoryCleanerBySharedHits = cms.ESProducer("TrajectoryCleanerESProducer",
  ComponentName = cms.string('hltESPElectronTrajectoryCleanerBySharedHits'),
  ComponentType = cms.string('TrajectoryCleanerBySharedHits'),
  fractionShared = cms.double('0.19'),
  allowSharedFirstHit = cms.bool(True)
)

hltESPElectronChi2 = cms.ESProducer("Chi2MeasurementEstimatorESProducer",
  ComponentName = cms.string('hltESPElectronChi2'),
  nSigma = cms.double(3.0),
  MaxChi2 = cms.double(100000.0)
)

hltESPTrajectoryBuilderForElectrons = cms.ESProducer("CkfTrajectoryBuilderESProducer",
  ComponentName = cms.string('hltESPTrajectoryBuilderForElectrons'),
  trajectoryFilterName = cms.string('hltESPTrajectoryFilterForElectrons'),
  maxCand = cms.int32(3),
  intermediateCleaning = cms.bool(False),
  propagatorAlong = cms.string('hltESPFwdGsfElectronPropagator'),
  propagatorOpposite = cms.string('hltESPBwdGsfElectronPropagator'),
  estimator = cms.string('hltESPElectronChi2'),
  MeasurementTrackerName = cms.string('hltESPMeasurementTracker'),
  lostHitPenalty = cms.double(30.),
  alwaysUseInvalidHits = cms.bool(True),
  TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
  updator = cms.string('hltESPKFUpdator')
)

hltESPTrajectoryFilterForElectrons = cms.ESProducer("TrajectoryFilterESProducer",
  ComponentName = cms.string('hltESPTrajectoryFilterForElectrons'),
  filterPset = cms.PSet(
  chargeSignificance = cms.double(-1.0),
  minPt = cms.double(3.0),
  minHitsMinPt = cms.int32(-1),
  ComponentType = cms.string('CkfBaseTrajectoryFilter'),
  maxLostHits = cms.int32(1),
  maxNumberOfHits = cms.int32(-1),
  maxConsecLostHits = cms.int32(1),
  nSigmaMinPt = cms.double(5.0),
  minimumNumberOfHits = cms.int32(5)
  )
)


hltESPTrajectoryBuilderForElectrons3Hit = cms.ESProducer("CkfTrajectoryBuilderESProducer",
  ComponentName = cms.string('hltESPTrajectoryBuilderForElectrons3Hit'),
  trajectoryFilterName = cms.string('hltESPTrajectoryFilterForElectrons3Hit'),
  maxCand = cms.int32(3),
  intermediateCleaning = cms.bool(False),
  propagatorAlong = cms.string('hltESPFwdGsfElectronPropagator'),
  ropagatorOpposite = cms.string('hltESPBwdGsfElectronPropagator'),
  estimator = cms.string('hltESPElectronChi2'),
  MeasurementTrackerName = cms.string('hltESPMeasurementTracker'),
  lostHitPenalty = cms.double(30.),
  alwaysUseInvalidHits = cms.bool(True),
  TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
  updator = cms.string('hltESPKFUpdator')
)

hltESPTrajectoryFilterForElectrons3Hit = cms.ESProducer("TrajectoryFilterESProducer",
  ComponentName = cms.string('hltESPTrajectoryFilterForElectrons3Hit'),
  filterPset = cms.PSet(
  chargeSignificance = cms.double(-1.0),
  minPt = cms.double(3.0),
  minHitsMinPt = cms.int32(-1),
  ComponentType = cms.string('CkfBaseTrajectoryFilter'),
  maxLostHits = cms.int32(1),
  maxNumberOfHits = cms.int32(-1),
  maxConsecLostHits = cms.int32(1),
  nSigmaMinPt = cms.double(5.0),
  minimumNumberOfHits = cms.int32(3)
  )
)


hltESPFwdGsfElectronPropagator = cms.ESProducer("PropagatorWithMaterialESProducer",
    MaxDPhi = cms.double(1.6),
    ComponentName = cms.string('hltESPFwdGsfElectronPropagator'),
    Mass = cms.double(0.000511),
    PropagationDirection = cms.string('alongMomentum'),
    useRungeKutta = cms.bool(False),
    ptMin = cms.double(-1.)
)

hltESPBwdGsfElectronPropagator = cms.ESProducer("PropagatorWithMaterialESProducer",
    MaxDPhi = cms.double(1.6),
    ComponentName = cms.string('hltESPBwdGsfElectronPropagator'),
    Mass = cms.double(0.000511),
    PropagationDirection = cms.string('oppositeToMomentum'),
    useRungeKutta = cms.bool(False),
    ptMin = cms.double(-1.)
)

hltESPKullbackLeiblerDistance5D = cms.ESProducer("DistanceBetweenComponentsESProducer5D",
    ComponentName = cms.string('hltESPKullbackLeiblerDistance5D'),
    DistanceMeasure = cms.string('KullbackLeibler')
)

hltESPCloseComponentsMerger5D = cms.ESProducer("CloseComponentsMergerESProducer5D",
    ComponentName = cms.string('hltESPCloseComponentsMerger5D'),
    MaxComponents = cms.int32(12),
    DistanceMeasure = cms.string('hltESPKullbackLeiblerDistance5D')
)

hltESPFwdAnalyticalPropagator = cms.ESProducer("AnalyticalPropagatorESProducer",
    MaxDPhi = cms.double(1.6),
    ComponentName = cms.string('hltESPFwdAnalyticalPropagator'),
    PropagationDirection = cms.string('alongMomentum')
)

hltESPBwdAnalyticalPropagator = cms.ESProducer("AnalyticalPropagatorESProducer",
    MaxDPhi = cms.double(1.6),
    ComponentName = cms.string('hltESPBwdAnalyticalPropagator'),
    PropagationDirection = cms.string('oppositeToMomentum')
)

hltESPElectronMaterialEffects = cms.ESProducer("GsfMaterialEffectsESProducer",
    BetheHeitlerParametrization = cms.string('BetheHeitler_cdfmom_nC6_O5.par'),
    EnergyLossUpdator = cms.string('GsfBetheHeitlerUpdator'),
    ComponentName = cms.string('hltESPElectronMaterialEffects'),
    MultipleScatteringUpdator = cms.string('MultipleScatteringUpdator'),
    Mass = cms.double(0.000511),
    BetheHeitlerCorrection = cms.int32(2)
)

hltGsfTrajectorySmoother = cms.ESProducer("GsfTrajectorySmootherESProducer",
    Merger = cms.string('hltESPCloseComponentsMerger5D'),
    ComponentName = cms.string('hltGsfTrajectorySmoother'),
    MaterialEffectsUpdator = cms.string('hltESPElectronMaterialEffects'),
    ErrorRescaling = cms.double(100.0),
    GeometricalPropagator = cms.string('hltESPBwdAnalyticalPropagator'),
    RecoGeometry = cms.string('hltESPGlobalDetLayerGeometry')                                
)

hltGsfTrajectoryFitter = cms.ESProducer("GsfTrajectoryFitterESProducer",
    Merger = cms.string('hltESPCloseComponentsMerger5D'),
    ComponentName = cms.string('hltGsfTrajectoryFitter'),
    MaterialEffectsUpdator = cms.string('hltESPElectronMaterialEffects'),
    GeometricalPropagator = cms.string('hltESPFwdAnalyticalPropagator'),
    RecoGeometry = cms.string('hltESPGlobalDetLayerGeometry')                                
)

hltESPGSFFittingSmoother = cms.ESProducer("KFFittingSmootherESProducer",
  ComponentName = cms.string('hltESPGSFFittingSmoother'),
  Fitter = cms.string('hltGsfTrajectoryFitter'),
  Smoother = cms.string('hltGsfTrajectorySmoother'),
  EstimateCut = cms.double(-1.0),
  LogPixelProbabilityCut = cms.double(-16.0),                               
  MinNumberOfHits = cms.int32(5),
  RejectTracks = cms.bool(True),
  BreakTrajWith2ConsecutiveMissing = cms.bool(True),
  NoInvalidHitsBeginEnd  = cms.bool(True)
)

# End of Services

hltCkfTrackCandidatesForGSF = cms.EDProducer("CkfTrackCandidateMaker",
    src = cms.InputTag("hltL1IsoStartUpElectronPixelSeeds"),
    TrajectoryBuilder = cms.string("hltESPTrajectoryBuilderForElectrons"),
    TrajectoryCleaner = cms.string("hltESPElectronTrajectoryCleanerBySharedHits"),
    NavigationSchool = cms.string("SimpleNavigationSchool"),
    RedundantSeedCleaner = cms.string( "CachingSeedCleanerBySharedInput" ),
    useHitsSplitting = cms.bool(True),
    doSeedingRegionRebuilding = cms.bool(True),
    TransientInitialStateEstimatorParameters = cms.PSet( 
      propagatorAlongTISE = cms.string( "PropagatorWithMaterial" ),
      numberMeasurementsForFit = cms.int32( 4 ),
      propagatorOppositeTISE = cms.string( "PropagatorWithMaterialOpposite" )
    ),
    cleanTrajectoryAfterInOut = cms.bool(True),
    maxNSeeds = cms.uint32(100000)
)

gsfTrackingForHLT = cms.EDProducer("GsfTrackProducer",
    src = cms.InputTag("hltCkfTrackCandidatesForGSF"),
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    producer = cms.string(''),
    Fitter = cms.string('hltESPGSFFittingSmoother'),
    useHitsSplitting = cms.bool(False),
    TrajectoryInEvent = cms.bool(True),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    Propagator = cms.string('hltESPFwdGsfElectronPropagator'),
    NavigationSchool = cms.string('SimpleNavigationSchool'),
    MeasurementTracker = cms.string('hltESPMeasurementTracker'),    
    AlgorithmName = cms.string('gsf')
)
