import os, sys

## for add qbh
#energies=[6500,7000,7500,8000,8500,9000]

## for RS1 qbh
energies=[4000,4500,5000,5500,6000,6500]

for energy in energies:

    ## skim qbh sample
    #os.system("./submit_python.sh get_qbh_chi_hist.py "+str(energy)+" -1 ./"+str(energy)+"_add6_getQBHChi.log")
    
    ## add systematics
    os.system("python add_systematics_qbh.py "+str(energy)+" -1")
