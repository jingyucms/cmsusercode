import os, sys

energies=[6500,7000,7500,8000,8500,9000,9500]
#energies=[8000,9000,8500]
#energies=[7000]

for energy in energies:
    #os.system("./submit_python.sh add_systematics_qbh.py "+str(energy)+" -1 ./"+str(energy)+".log")
    #os.system("./submit_python.sh plot_signal_only.py "+str(energy)+" -1 ./"+str(energy)+"_signalonly.log")
    os.system("python add_systematics_qbh.py "+str(energy)+" -1")
