import os
for i in range(1,2000):
  os.system("qsub -q all.q -o /mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_4_7_patch2/src/cmsusercode/chi_analysis/out.txt -e /mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_4_7_patch2/src/cmsusercode/chi_analysis/err.txt submitPythonOnT3batch.sh datacard_shapelimit13TeV_25nsData11_chi"+str(i)+" dijet_angular /mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_4_7_patch2 cmsusercode/chi_analysis/plot_data_13TeV_uzh2_loop.py "+str(i)+" jobtmp_data /mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_4_7_patch2/src/cmsusercode/chi_analysis/jobout")
