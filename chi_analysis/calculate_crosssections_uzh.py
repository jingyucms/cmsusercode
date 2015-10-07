import os

if __name__ == '__main__':

    samples=[("QCD",[("pythia8_ci_m1000_1500_50000_1_0_0_13TeV_Oct1",3.769e-05),
		       ("pythia8_ci_m1500_1900_50000_1_0_0_13TeV_Oct1",3.307e-06),
		       ("pythia8_ci_m1900_2400_50000_1_0_0_13TeV_Oct1",8.836e-07),
		       ("pythia8_ci_m2400_2800_50000_1_0_0_13TeV_Oct1",1.649e-07),
		       ("pythia8_ci_m2800_3300_50000_1_0_0_13TeV_Oct1",6.446e-08),
		       ("pythia8_ci_m3300_3800_50000_1_0_0_13TeV_Oct1",1.863e-08),
		       ("pythia8_ci_m3800_4300_50000_1_0_0_13TeV_Oct1",5.867e-09),
		       ("pythia8_ci_m4300_13000_50000_1_0_0_13TeV_Oct1",3.507e-09),
		       ]),
             ("QCDCIplusLL8000",[("pythia8_ci_m1500_1900_8000_1_0_0_13TeV_Oct1",3.307e-06),
		       ("pythia8_ci_m1900_2400_8000_1_0_0_13TeV_Oct1",8.836e-07),
		       ("pythia8_ci_m2400_2800_8000_1_0_0_13TeV_Oct1",1.649e-07),
		       ("pythia8_ci_m2800_3300_8000_1_0_0_13TeV_Oct1",6.446e-08),
		       ("pythia8_ci_m3300_3800_8000_1_0_0_13TeV_Oct1",1.863e-08),
		       ("pythia8_ci_m3800_4300_8000_1_0_0_13TeV_Oct1",5.867e-09),
		       ("pythia8_ci_m4300_13000_8000_1_0_0_13TeV_Oct1",3.507e-09),
		       ]),
             ("QCDCIplusLL9000",[("pythia8_ci_m1500_1900_9000_1_0_0_13TeV_Oct1",3.307e-06),
		       ("pythia8_ci_m1900_2400_9000_1_0_0_13TeV_Oct1",8.836e-07),
		       ("pythia8_ci_m2400_2800_9000_1_0_0_13TeV_Oct1",1.649e-07),
		       ("pythia8_ci_m2800_3300_9000_1_0_0_13TeV_Oct1",6.446e-08),
		       ("pythia8_ci_m3300_3800_9000_1_0_0_13TeV_Oct1",1.863e-08),
		       ("pythia8_ci_m3800_4300_9000_1_0_0_13TeV_Oct1",5.867e-09),
		       ("pythia8_ci_m4300_13000_9000_1_0_0_13TeV_Oct1",3.507e-09),
		       ]),
             ("QCDCIplusLL10000",[("pythia8_ci_m1500_1900_10000_1_0_0_13TeV_Oct1",3.307e-06),
		       ("pythia8_ci_m1900_2400_10000_1_0_0_13TeV_Oct1",8.836e-07),
		       ("pythia8_ci_m2400_2800_10000_1_0_0_13TeV_Oct1",1.649e-07),
		       ("pythia8_ci_m2800_3300_10000_1_0_0_13TeV_Oct1",6.446e-08),
		       ("pythia8_ci_m3300_3800_10000_1_0_0_13TeV_Oct1",1.863e-08),
		       ("pythia8_ci_m3800_4300_10000_1_0_0_13TeV_Oct1",5.867e-09),
		       ("pythia8_ci_m4300_13000_10000_1_0_0_13TeV_Oct1",3.507e-09),
		       ]),
             ("QCDCIplusLL11000",[("pythia8_ci_m1500_1900_11000_1_0_0_13TeV_Oct1",3.307e-06),
		       ("pythia8_ci_m1900_2400_11000_1_0_0_13TeV_Oct1",8.836e-07),
		       ("pythia8_ci_m2400_2800_11000_1_0_0_13TeV_Oct1",1.649e-07),
		       ("pythia8_ci_m2800_3300_11000_1_0_0_13TeV_Oct1",6.446e-08),
		       ("pythia8_ci_m3300_3800_11000_1_0_0_13TeV_Oct1",1.863e-08),
		       ("pythia8_ci_m3800_4300_11000_1_0_0_13TeV_Oct1",5.867e-09),
		       ("pythia8_ci_m4300_13000_11000_1_0_0_13TeV_Oct1",3.507e-09),
		       ]),
             ("QCDCIplusLL12000",[("pythia8_ci_m1500_1900_12000_1_0_0_13TeV_Oct1",3.307e-06),
		       ("pythia8_ci_m1900_2400_12000_1_0_0_13TeV_Oct1",8.836e-07),
		       ("pythia8_ci_m2400_2800_12000_1_0_0_13TeV_Oct1",1.649e-07),
		       ("pythia8_ci_m2800_3300_12000_1_0_0_13TeV_Oct1",6.446e-08),
		       ("pythia8_ci_m3300_3800_12000_1_0_0_13TeV_Oct1",1.863e-08),
		       ("pythia8_ci_m3800_4300_12000_1_0_0_13TeV_Oct1",5.867e-09),
		       ("pythia8_ci_m4300_13000_12000_1_0_0_13TeV_Oct1",3.507e-09),
		       ]),
             ("QCDCIplusLL13000",[("pythia8_ci_m1500_1900_13000_1_0_0_13TeV_Oct1",3.307e-06),
		       ("pythia8_ci_m1900_2400_13000_1_0_0_13TeV_Oct1",8.836e-07),
		       ("pythia8_ci_m2400_2800_13000_1_0_0_13TeV_Oct1",1.649e-07),
		       ("pythia8_ci_m2800_3300_13000_1_0_0_13TeV_Oct1",6.446e-08),
		       ("pythia8_ci_m3300_3800_13000_1_0_0_13TeV_Oct1",1.863e-08),
		       ("pythia8_ci_m3800_4300_13000_1_0_0_13TeV_Oct1",5.867e-09),
		       ("pythia8_ci_m4300_13000_13000_1_0_0_13TeV_Oct1",3.507e-09),
		       ]),
             ("QCDCIplusLL14000",[("pythia8_ci_m1500_1900_14000_1_0_0_13TeV_Oct1",3.307e-06),
		       ("pythia8_ci_m1900_2400_14000_1_0_0_13TeV_Oct1",8.836e-07),
		       ("pythia8_ci_m2400_2800_14000_1_0_0_13TeV_Oct1",1.649e-07),
		       ("pythia8_ci_m2800_3300_14000_1_0_0_13TeV_Oct1",6.446e-08),
		       ("pythia8_ci_m3300_3800_14000_1_0_0_13TeV_Oct1",1.863e-08),
		       ("pythia8_ci_m3800_4300_14000_1_0_0_13TeV_Oct1",5.867e-09),
		       ("pythia8_ci_m4300_13000_14000_1_0_0_13TeV_Oct1",3.507e-09),
		       ]),
             ("QCDCIplusLL16000",[("pythia8_ci_m1500_1900_16000_1_0_0_13TeV_Oct1",3.307e-06),
		       ("pythia8_ci_m1900_2400_16000_1_0_0_13TeV_Oct1",8.836e-07),
		       ("pythia8_ci_m2400_2800_16000_1_0_0_13TeV_Oct1",1.649e-07),
		       ("pythia8_ci_m2800_3300_16000_1_0_0_13TeV_Oct1",6.446e-08),
		       ("pythia8_ci_m3300_3800_16000_1_0_0_13TeV_Oct1",1.863e-08),
		       ("pythia8_ci_m3800_4300_16000_1_0_0_13TeV_Oct1",5.867e-09),
		       ("pythia8_ci_m4300_13000_16000_1_0_0_13TeV_Oct1",3.507e-09),
		       ]),
             ("QCDCIplusLL18000",[("pythia8_ci_m1500_1900_18000_1_0_0_13TeV_Oct1",3.307e-06),
		       ("pythia8_ci_m1900_2400_18000_1_0_0_13TeV_Oct1",8.836e-07),
		       ("pythia8_ci_m2400_2800_18000_1_0_0_13TeV_Oct1",1.649e-07),
		       ("pythia8_ci_m2800_3300_18000_1_0_0_13TeV_Oct1",6.446e-08),
		       ("pythia8_ci_m3300_3800_18000_1_0_0_13TeV_Oct1",1.863e-08),
		       ("pythia8_ci_m3800_4300_18000_1_0_0_13TeV_Oct1",5.867e-09),
		       ("pythia8_ci_m4300_13000_18000_1_0_0_13TeV_Oct1",3.507e-09),
		       ]),
             ]

    crosssections={}
    for i in range(len(samples)):
      for j in range(len(samples[i][1])):
       crosssections[samples[i][1][j][0]]=samples[i][1][j][1]
       for k in range(200):
         d="jobout_"+samples[i][1][j][0]+"/myout.txt"
	 #try:
	 #  files=os.listdir(d)
	 #except:
	 #  continue
	 #for f in files:
	 # if "LSFJOB" in f:
	 #   d+=f+"/STDOUT"
         print "logfile",d
         break
       try:
         f=file(d)
       except:
         print "no cross section found for ",d
	 continue
       for l in f.readlines():
	    if "| sum" in l:
                crosssections[samples[i][1][j][0]]=l.strip().split(" ")[-4]
		break

print crosssections
fout=file("xsecs_13TeV.txt","w")
fout.write(str(crosssections))
fout.close()
