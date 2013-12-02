cvs co -r 1.8 Configuration/GenProduction/python/QCD_Pt_15to3000_TuneZ2_Flat_7TeV_pythia6_cff.py
cvs co Configuration/GenProduction/python/rivet_customize.py
cvs co GeneratorInterface/RivetInterface

flat2aida cmsusercode/chi_analysis/rivet/CMS_2012_I1090423.dat -o cmsusercode/chi_analysis/rivet/CMS_2012_I1090423.aida

cp cmsusercode/chi_analysis/rivet/CMS_2012_I1090423.cc GeneratorInterface/RivetInterface/src/
cp cmsusercode/chi_analysis/rivet/CMS_2012_I1090423.aida GeneratorInterface/RivetInterface/data/
cp cmsusercode/chi_analysis/rivet/CMS_2012_I1090423.info GeneratorInterface/RivetInterface/data/
cp cmsusercode/chi_analysis/rivet/CMS_2012_I1090423.plot GeneratorInterface/RivetInterface/data/

scram b -j5

cmsDriver.py Configuration/GenProduction/python/QCD_Pt_15to3000_TuneZ2_Flat_7TeV_pythia6_cff.py -s GEN --datatier=GEN-SIM-RAW --conditions auto:mc --eventcontent RAWSIM --no_exec -n 10000 --python_filename=rivet_cfg.py --customise=Configuration/GenProduction/rivet_customize.py

cmsRun cmsusercode/chi_analysis/rivet/rivet_2012_I1090423_pythia6_cfg.py &

rivet-mkhtml -c GeneratorInterface/RivetInterface/data/CMS_2012_I1090423.plot --mc-errs 2012I1090423pythia6.aida GeneratorInterface/RivetInterface/data/CMS_2012_I1090423.aida
