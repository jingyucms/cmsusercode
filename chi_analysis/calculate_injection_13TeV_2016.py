import os

print "########################################"

for mass in [2000,2250,2500,3000,3500,4000,4500]:
    print "limitsDetCBLHCa1107_DMAxial_Dijet_LO_Mphi_v5/mlfitDMAxial_Dijet_LO_Mphi_"+str(mass)+"_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_0p75.root"
    os.system("python diffNuisances.py -a -p x limitsDetCBLHCa1107_DMAxial_Dijet_LO_Mphi_v5/mlfitDMAxial_Dijet_LO_Mphi_"+str(mass)+"_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_0p75.root -A")
    print "limitsDetCBLHCa1107_DMAxial_Dijet_LO_MphiInjection0p75_v5/mlfitDMAxial_Dijet_LO_Mphi_"+str(mass)+"_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_0p75.root"
    os.system("python diffNuisances.py -a -p x limitsDetCBLHCa1107_DMAxial_Dijet_LO_MphiInjection0p75_v5/mlfitDMAxial_Dijet_LO_Mphi_"+str(mass)+"_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_0p75.root -A")
    print "-------------------------------------------------------------------------------------"

print "########################################"
    
for mass in [2000,2250,2500,3000,3500,4000,4500]:
    print "limitsDetCBLHCa1108_DMAxial_Dijet_LO_Mphi_v5/mlfitDMAxial_Dijet_LO_Mphi_"+str(mass)+"_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_1.root"
    os.system("python diffNuisances.py -a -p x limitsDetCBLHCa1108_DMAxial_Dijet_LO_Mphi_v5/mlfitDMAxial_Dijet_LO_Mphi_"+str(mass)+"_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_1.root -A")
    print "limitsDetCBLHCa1108_DMAxial_Dijet_LO_MphiInjection1p0_v5/mlfitDMAxial_Dijet_LO_Mphi_"+str(mass)+"_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_1.root"
    os.system("python diffNuisances.py -a -p x limitsDetCBLHCa1108_DMAxial_Dijet_LO_MphiInjection1p0_v5/mlfitDMAxial_Dijet_LO_Mphi_"+str(mass)+"_1_1p0_1p0_Mar5_gdmv_0_gdma_1p0_gv_0_ga_1.root -A")
    print "-------------------------------------------------------------------------------------"
