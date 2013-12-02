cvs co -r 1.3 Configuration/GenProduction/python/EightTeV/QCD_Pt_15to3000_TuneZ2star_Flat_8TeV_pythia6_cff.py
cvs co Configuration/GenProduction/python/rivet_customize.py
cvs co GeneratorInterface/RivetInterface

flat2aida cmsusercode/chi_analysis/rivet/CMS_JME_13_006.dat -o cmsusercode/chi_analysis/rivet/CMS_JME_13_006.aida

cp cmsusercode/chi_analysis/rivet/Njettiness.hh GeneratorInterface/RivetInterface/src/Njettiness.hh
cp cmsusercode/chi_analysis/rivet/CMS_JME_13_006.cc GeneratorInterface/RivetInterface/src/
cp cmsusercode/chi_analysis/rivet/CMS_JME_13_006.aida GeneratorInterface/RivetInterface/data/
cp cmsusercode/chi_analysis/rivet/CMS_JME_13_006.info GeneratorInterface/RivetInterface/data/
cp cmsusercode/chi_analysis/rivet/CMS_JME_13_006.plot GeneratorInterface/RivetInterface/data/

scram b -j5

cmsDriver.py Configuration/GenProduction/python/EightTeV/QCD_Pt_15to3000_TuneZ2star_Flat_8TeV_pythia6_cff.py -s GEN --datatier=GEN-SIM-RAW --conditions auto:mc --eventcontent RAWSIM --no_exec -n 10000 --python_filename=rivet_cfg.py --customise=Configuration/GenProduction/rivet_customize.py

source GeneratorInterface/RivetInterface/test/rivetSetup.sh

cmsRun cmsusercode/chi_analysis/rivet/rivet_JME_13_006_pythia6_cfg.py &
cmsRun cmsusercode/chi_analysis/rivet/rivet_JME_13_006_pythia8_cfg.py &
cmsRun cmsusercode/chi_analysis/rivet/rivet_JME_13_006_herwigpp_cfg.py &

rivet-mkhtml -c GeneratorInterface/RivetInterface/data/CMS_JME_13_006.plot --mc-errs JME13006pythia6.aida JME13006pythia8.aida JME13006herwigpp.aida GeneratorInterface/RivetInterface/data/CMS_JME_13_006.aida
