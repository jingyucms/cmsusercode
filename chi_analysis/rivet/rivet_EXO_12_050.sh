cvs co -r 1.3 Configuration/GenProduction/python/EightTeV/QCD_Pt_15to3000_TuneZ2star_Flat_8TeV_pythia6_cff.py
cvs co Configuration/GenProduction/python/rivet_customize.py
cvs co GeneratorInterface/RivetInterface
source GeneratorInterface/RivetInterface/test/rivetSetup.sh

flat2aida cmsusercode/chi_analysis/rivet/CMS_EXO_12_050.dat -o cmsusercode/chi_analysis/rivet/CMS_EXO_12_050.aida

cp cmsusercode/chi_analysis/rivet/CMS_EXO_12_050.cc GeneratorInterface/RivetInterface/src/
cp cmsusercode/chi_analysis/rivet/CMS_EXO_12_050.aida GeneratorInterface/RivetInterface/data/
cp cmsusercode/chi_analysis/rivet/CMS_EXO_12_050.info GeneratorInterface/RivetInterface/data/
cp cmsusercode/chi_analysis/rivet/CMS_EXO_12_050.plot GeneratorInterface/RivetInterface/data/

scram b -j5

cmsDriver.py Configuration/GenProduction/python/EightTeV/QCD_Pt_15to3000_TuneZ2star_Flat_8TeV_pythia6_cff.py -s GEN --datatier=GEN-SIM-RAW --conditions auto:mc --eventcontent RAWSIM --no_exec -n 10000 --python_filename=rivet_cfg.py --customise=Configuration/GenProduction/rivet_customize.py

cmsRun cmsusercode/chi_analysis/rivet/rivet_EXO_12_050_pythia6_cfg.py &

rivet-mkhtml -c GeneratorInterface/RivetInterface/data/CMS_EXO_12_050.plot --mc-errs EXO12050pythia6.aida GeneratorInterface/RivetInterface/data/CMS_EXO_12_050.aida
