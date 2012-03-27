scenario=""
#scenario="_loose_massdrop"
#scenario="_tight_massdrop"

f=file("efficiency_table"+scenario+".txt","w")

f.write("sample & mass & acceptance(>890) & acceptance(1sigma) & efficiency(m-only,>890) & efficiency(m-only,1sigma) & efficiency(>890) & efficiency(1sigma) \\\\ \n")

masses=[750,1000,1500,2000,3000]

files=[]

labels=["0.75 TeV","1 TeV","1.5 TeV","2 TeV","3 TeV"]

for mass in masses:
    files+=[("plots/signal4"+scenario+"_q*->qW ("+labels[masses.index(mass)]+")_"+str(mass)+"_1tag_eff.txt",mass)]
for mass in masses:
    files+=[("plots/signal5"+scenario+"_q*->qZ ("+labels[masses.index(mass)]+")_"+str(mass)+"_1tag_eff.txt",mass)]
for mass in masses:
    files+=[("plots/signal1"+scenario+"_G*->WW ("+labels[masses.index(mass)]+")_"+str(mass)+"_2tag_eff.txt",mass)]
for mass in masses:
    files+=[("plots/signal2"+scenario+"_G*->ZZ ("+labels[masses.index(mass)]+")_"+str(mass)+"_2tag_eff.txt",mass)]
for mass in masses:
    files+=[("plots/signal3"+scenario+"_W'->WZ ("+labels[masses.index(mass)]+")_"+str(mass)+"_2tag_eff.txt",mass)]
for mass in masses:
    files+=[("plots/signal11"+scenario+"_G*->WW ("+labels[masses.index(mass)]+")_"+str(mass)+"_2tag_eff.txt",mass)]
for mass in masses:
    files+=[("plots/signal12"+scenario+"_G*->ZZ ("+labels[masses.index(mass)]+")_"+str(mass)+"_2tag_eff.txt",mass)]
for mass in masses:
    files+=[("plots/signal111"+scenario+"_G*->WW ("+labels[masses.index(mass)]+")_"+str(mass)+"_2tag_eff.txt",mass)]
for mass in masses:
    files+=[("plots/signal112"+scenario+"_G*->ZZ ("+labels[masses.index(mass)]+")_"+str(mass)+"_2tag_eff.txt",mass)]

for name,mass in files:
    try:
        fin=file(name,"r")
    except: continue
    lines=fin.readlines()
    if "_" in scenario:
        entry=name.split("_")[3]+" & "
    else:
        entry=name.split("_")[1]+" & "
    entry+=str(mass)+" & "
    entry+="%.3f & " % float(lines[0].split("=")[1].strip("\n"))
    entry+="%.3f & " % float(lines[1].split("=")[1].strip("\n"))
    entry+="%.3f & " % float(lines[2].split("=")[1].strip("\n"))
    entry+="%.3f " % float(lines[3].split("=")[1].strip("\n"))
    if scenario=="":
        entry+=" & "
        entry+="%.3f & " % float(lines[4].split("=")[1].strip("\n"))
        entry+="%.3f " % float(lines[5].split("=")[1].strip("\n"))
    entry+="\\\\ \n"
    print entry.strip("\n")
    f.write(entry)
f.close()
