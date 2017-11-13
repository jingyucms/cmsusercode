import os

ls=os.listdir("./qbh")

for l in ls:
    l1=l.split("_")
    print l1
    out="../datacard_shapelimit13TeV_QBH_"+l1[1]+"_"+l1[2]+"_chi2016.root"
    print out
    command="cp "+l+" "+out
    print command
    os.system(command)
