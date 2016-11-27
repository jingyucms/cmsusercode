Here is the list of all scripts to run the dijet angular analysis.
The order of the execution matters in some cases.

-------- MC production in CMSSW_7_1_X:

submit_ci_samples_13TeV.py # produce GEN samples for LO QCD and LO QCD+CI
submit_add_samples_13TeV.py # produce GEN samples for LO QCD+ADD
submit_herwig_samples_13TeV.py # produce GEN samples for QCD

calculate_crosssections_uzh.py # extract LO QCD, LO QCD+CI and LO QCD+ADD from production Pythia log files, Herwig cross sections have to be taken from LHC.log file by hand.
xsdj_table.py # extract LO DM cross sections from LHC headers

copy-samples.py # copy GEN samples from PSI to CERN
copy-tree.sh # copy data and full simulation QCD from PSI to CERN

-------- Data analysis in CMSSW_7_4_X:

plotSignal_13TeV_uzh2.py # produce dijet angular histograms from GEN samples for QCD, CI and ADD samples

plotSignal_13TeV_lxplus_loop.py # produce dijet angular histograms from GEN samples for DM samples

plot_data_13TeV_uzh2_loop.py # produce dijet angular histograms for data and fullsim QCD samples

plotSignal_jes_13TeV_uzh.py # produce JES uncertainty histograms from CI and QCD GEN samples
plot_chi_jes_plots_13TeV_2016.py # plot JES uncertainty histograms

plot_nonpert_13TeV.py # plot non perturbative correction histograms

add_systematics_13TeV_2016.py # add systematic shift histograms, NLOQCD and data histograms in the datacards for each CI, ADD and DM signal
plot_chi_uncertainties_13TeV_2016.py # plot summary of all systematic uncertainties

add_systematics_qbh.py # add systematic shift histograms, NLOQCD and data histograms in the datacards for a QBH signal
submit_add_systematics_qbh.py # add systematic shift histograms, NLOQCD and data histograms in the datacards for a QBH signal

plot_chi_combined_data_13TeV_v2_2016.py # final result plot

-------- Limit calculation in CMSSW_7_1_X:

calculate_limit_shape_13TeV_2016.py # calculate CLS for each CI, ADD, DM and QBH model
calculate_limit_shape_13TeV_loop.py # calculate CLS for each DM model
plot_limit_shape_13TeV_2016.py # compute CLS limit for each CI, ADD and QBH model
plot_limit_shape_13TeV_dm.py # compute CLS limit for each DM model
plot_limit_summary.py #  summary of limits on various models (still 8 TeV version)

summarize_pvalues_13TeV.py # make table of p-values of the data in each mass bin
calculate_goodness_13TeV.py # calculate goodness of fit measure of the data in each mass bin
summarize_goodness_13TeV.py # make table of goodness of fit measure
calculate_bestfit.py # make table of bestfit JER (still 8 TeV version)
