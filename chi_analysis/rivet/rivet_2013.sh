cvs co -r 1.8 Configuration/GenProduction/python/QCD_Pt_15to3000_TuneZ2_Flat_7TeV_pythia6_cff.py
cvs co -r 1.7 Configuration/GenProduction/python/QCD_Pt_15to3000_Tune23_Flat_7TeV_herwigpp_cff.py
cmsDriver.py Configuration/GenProduction/python/QCD_Pt_15to3000_TuneZ2_Flat_7TeV_pythia6_cff.py -s GEN --datatier=GEN-SIM-RAW --conditions auto:mc --eventcontent RAWSIM --no_exec -n 10000 --python_filename=rivet_cfg.py --customise=Configuration/GenProduction/rivet_customize.py
rivet-mkhtml -c GeneratorInterface/RivetInterface/data/CMS_2012_I1090423.plot pythia6.aida herwigpp.aida GeneratorInterface/RivetInterface/data/CMS_2012_I1090423.aida
