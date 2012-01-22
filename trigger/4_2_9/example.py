

process.HLT_IsoMu15_eta2p1_LooseIsoPFTau20_v4 = cms.Path( process.HLTBeginSequence + process.HLTRecoJetSequencePrePF + process.HLTPFJetTriggerSequenceForTaus + process.HLTPFTauSequence + process.HLTPFTauTightIsoSequence+   process.HLTEndSequence )



process.offlineSelectedPFTausLooseIsoTrackFinding = cms.EDFilter( "PFTauSelector",
                                                                      src = cms.InputTag( "hpsPFTauProducer" ),
                                                                      discriminators = cms.VPSet(
          cms.PSet(  discriminator = cms.InputTag( "hpsPFTauDiscriminationByDecayModeFinding" ),
                             selectionCut = cms.double( 0.5 )
                           ),
#                cms.PSet(  discriminator = cms.InputTag( "hpsPFTauDiscriminationByMediumIsolation" ),
                          cms.PSet(  discriminator = cms.InputTag( "hpsPFTauDiscriminationByLooseIsolation" ),
                                   selectionCut = cms.double( 0.5 )
                                 ),
                cms.PSet(  discriminator = cms.InputTag( "hpsPFTauDiscriminationByLooseMuonRejection" ),
                                   selectionCut = cms.double( 0.5 )
                                 ),
                cms.PSet(  discriminator = cms.InputTag( "hpsPFTauDiscriminationByMediumElectronRejection" ),
                                   selectionCut = cms.double( 0.5 )
                                 ),

              )
                                                                  )

process.offlineSelectedPFTausMediumIsoTrackFinding = cms.EDFilter( "PFTauSelector",
                                                                      src = cms.InputTag( "hpsPFTauProducer" ),
                                                                      discriminators = cms.VPSet(
          cms.PSet(  discriminator = cms.InputTag( "hpsPFTauDiscriminationByDecayModeFinding" ),
                             selectionCut = cms.double( 0.5 )
                           ),
                cms.PSet(  discriminator = cms.InputTag( "hpsPFTauDiscriminationByMediumIsolation" ),
                                   selectionCut = cms.double( 0.5 )
                                 ),
                cms.PSet(  discriminator = cms.InputTag( "hpsPFTauDiscriminationByLooseMuonRejection" ),
                                   selectionCut = cms.double( 0.5 )
                                 ),
                cms.PSet(  discriminator = cms.InputTag( "hpsPFTauDiscriminationByMediumElectronRejection" ),
                                   selectionCut = cms.double( 0.5 )
                                 ),

              )
                                                                  )


process.tauGenJetsSelectorAllHadrons = cms.EDFilter("TauGenJetDecayModeSelector",
      src = cms.InputTag("tauGenJets"),
      select = cms.vstring('oneProng0Pi0', 
                           'oneProng1Pi0', 
                           'oneProng2Pi0', 
                           'oneProngOther',
                          'threeProng0Pi0', 
                           'threeProng1Pi0', 
                           'threeProngOther', 
                           'rare'),
      filter = cms.bool(True)
 )



process.test = cms.Path(process.offlineSelectedPFTausMediumIsoTrackFinding+process.offlineSelectedPFTausLooseIsoTrackFinding)
#process.tauHadr = cms.Path(process.tauGenJetsSelectorAllHadrons)


process.source.fileNames = (


   'file:/build/gennai/RelVal_Reco_PU/2867C622-00F0-E011-825B-0018F3D09620.root',
   'file:/build/gennai/RelVal_Reco_PU/542E75FD-F8F2-E011-B3B8-002618943831.root',
   'file:/build/gennai/RelVal_Reco_PU/A4760ED8-C0F1-E011-B375-002354EF3BE2.root',
   'file:/build/gennai/RelVal_Reco_PU/CA02B012-FEEE-E011-B8CE-0018F3D0968A.root',
'file:/build/gennai/RelVal_Reco_PU/50AFD7B2-56F1-E011-B0DE-003048679150.root',
'file:/build/gennai/RelVal_Reco_PU/6AF8465D-4FEF-E011-A399-002354EF3BDC.root',
'file:/build/gennai/RelVal_Reco_PU/B4D788ED-9FEE-E011-A91E-001BFCDBD11E.root'

     )

#process.source.fileNames = (
process.source.secondaryFileNames = cms.untracked.vstring(
    'file:/build/gennai/RelVal_Raw_PU/029F37C9-57F1-E011-A813-0030486791BA.root',
'file:/build/gennai/RelVal_Raw_PU/040CF5D8-C0F1-E011-9648-00261894386F.root',
'file:/build/gennai/RelVal_Raw_PU/16CC9E64-E9EE-E011-B801-001A92971B1A.root',
'file:/build/gennai/RelVal_Raw_PU/18AE0AE6-9FEE-E011-AA24-003048679228.root',
'file:/build/gennai/RelVal_Raw_PU/2AFEF247-9EEE-E011-A6AD-00304867BFBC.root',
'file:/build/gennai/RelVal_Raw_PU/303798D9-C0F1-E011-BC5C-003048678BE8.root',
'file:/build/gennai/RelVal_Raw_PU/366C2997-6BEF-E011-9838-0018F3D096D2.root',
'file:/build/gennai/RelVal_Raw_PU/3C749FC3-9DEE-E011-A67C-003048678B84.root',
'file:/build/gennai/RelVal_Raw_PU/501BBC0A-36F1-E011-97EB-003048679076.root',
'file:/build/gennai/RelVal_Raw_PU/5E4527AC-20EF-E011-A980-003048679168.root',
'file:/build/gennai/RelVal_Raw_PU/5EB7FAE7-E5EE-E011-8224-00304867916E.root',
'file:/build/gennai/RelVal_Raw_PU/6202307B-B6F2-E011-AD04-003048678FA6.root',
'file:/build/gennai/RelVal_Raw_PU/74848E23-59F1-E011-BFB0-003048678FF2.root',
'file:/build/gennai/RelVal_Raw_PU/7EE667B6-50EF-E011-AD0D-0018F3D09678.root',
'file:/build/gennai/RelVal_Raw_PU/7EF47BE1-78F2-E011-AE50-003048678FDE.root',
'file:/build/gennai/RelVal_Raw_PU/80F272D4-44F1-E011-9CB6-003048678A88.root',
'file:/build/gennai/RelVal_Raw_PU/883765AF-C3EE-E011-8125-001A92810ABA.root',
'file:/build/gennai/RelVal_Raw_PU/92983CFD-67F1-E011-B7B2-0018F3D0967E.root',
'file:/build/gennai/RelVal_Raw_PU/9428E7D6-BFF1-E011-A0EB-003048678F06.root',
'file:/build/gennai/RelVal_Raw_PU/AC875411-FEEE-E011-A65C-0018F3D09654.root',
'file:/build/gennai/RelVal_Raw_PU/B61410FE-DEF1-E011-AC31-001A9281172A.root',
'file:/build/gennai/RelVal_Raw_PU/BAF87771-12F1-E011-8ED0-003048678AC0.root',
'file:/build/gennai/RelVal_Raw_PU/BAF9FF53-9FEE-E011-BD65-002618943978.root',
'file:/build/gennai/RelVal_Raw_PU/D24BCC4A-9FEE-E011-AC95-003048D15DB6.root',
'file:/build/gennai/RelVal_Raw_PU/E2E0145A-4CEF-E011-8796-003048679046.root',
'file:/build/gennai/RelVal_Raw_PU/F21C0185-37F1-E011-9B15-001A92971AAA.root',
'file:/build/gennai/RelVal_Raw_PU/F62FBA4E-27EF-E011-ACB8-003048679012.root',



            )

