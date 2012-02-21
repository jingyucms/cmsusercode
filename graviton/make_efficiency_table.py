f=file("efficiency_table.txt","w")

f.write("sample & mass & acceptance & efficiency \\\\ \n")

masses=[750,1000,1500,2000,3000]

files=[]

for mass in masses:
    files+=[("plots/signal4_q*->qW_"+str(mass)+"_1tag_eff.txt",mass)]
for mass in masses:
    files+=[("plots/signal5_q*->qZ_"+str(mass)+"_1tag_eff.txt",mass)]
for mass in masses:
    files+=[("plots/signal1_G*->WW_"+str(mass)+"_2tag_eff.txt",mass)]
for mass in masses:
    files+=[("plots/signal2_G*->ZZ_"+str(mass)+"_2tag_eff.txt",mass)]
for mass in masses:
    files+=[("plots/signal3_W'->WZ_"+str(mass)+"_2tag_eff.txt",mass)]

for name,mass in files:
    try:
        fin=file(name,"r")
    except: continue
    lines=fin.readlines()
    entry=name.split("_")[1]+" & "
    entry+=str(mass)+" & "
    entry+=lines[0].split("=")[1].strip("\n")+" & "
    entry+=lines[1].split("=")[1].strip("\n")+"\\\\ \n"
    print entry.strip("\n")
    f.write(entry)
f.close()
