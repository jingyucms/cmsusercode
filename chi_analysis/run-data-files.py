import os
#for samplenum in [1,2,3,4,5,6,7,8]:
# for i in range(1,2000):
#  os.system("qsub -q all.q -o /mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_4_7_patch2/src/cmsusercode/chi_analysis/out.txt -e /mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_4_7_patch2/src/cmsusercode/chi_analysis/err.txt submitPythonOnT3batch.sh datacard_shapelimit13TeV_25ns_chi"+str(i)+" dijet_angular /mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_4_7_patch2 /mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_4_7_patch2/src/cmsusercode/chi_analysis/plot_data_13TeV_uzh2_loop.py "+str(samplenum*100000+i)+" jobtmp_data"+str(samplenum)+" /mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_4_7_patch2/src/cmsusercode/chi_analysis/jobout")
for samplenum in [0]:
 for i in range(1,11610):
  os.system("qsub -q all.q -o /mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_4_7_patch2/src/cmsusercode/chi_analysis/out.txt -e /mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_4_7_patch2/src/cmsusercode/chi_analysis/err.txt submitPythonOnT3batch.sh datacard_shapelimit13TeV_25ns_chi"+str(i)+" dijet_angular /mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_4_7_patch2 /mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_4_7_patch2/src/cmsusercode/chi_analysis/plot_data_13TeV_uzh2_loop.py "+str(samplenum*100000+i)+" jobtmpFeb5_data"+str(samplenum)+" /mnt/t3nfs01/data01/shome/hinzmann/CMSSW_7_4_7_patch2/src/cmsusercode/chi_analysis/jobout")
