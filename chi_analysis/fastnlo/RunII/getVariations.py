from ROOT import *
from array import *
import subprocess,os

class getVariations:  # This class helps extract xsecs from NLOJET++ and CIJET++ program and store the xsecs into root histograms or python lists/dictionaries 
    
    def __init__(self):
        # Use version="i"for 2015 analysis and use version="j" for 2016 analysis
        # Default path for NLOJET++ cross section input (.log) files is ./
        # Defualt path for NLOJET++ cross section output files is ./
        # Default path for CIJET++ cross section input (.xsc) files is ./cixsecDir
        # Default path for CIJET++ cross section output files is ./cixsecDir
        self.version="j"
        self.cixsecDir="csxsec_ct14nlo_0-56_LL"
        self.BaseDir=os.getcwd()
        # other initiation
        self.bins=array('d',[1,2,3,4,5,6,7,8,9,10,12,14,16])
        self.styles=["LL-","LL+"]

    def getqcdallmu(self):     
        fileallmu=self.BaseDir+"/InclusiveNJetEvents_fnl5662"+self.version+"_v23_fix_CT14nlo_allmu.log"
        allmulist=[]
        mu=["start"]
        muxsecs=["start"]
        with open(fileallmu) as f:
            for line in f:
                if "The scale factors xmur, xmuf chosen here are" in line:
                    if mu != ["start"] and muxsecs !=["start"]:
                        allmulist.append([mu,muxsecs])
                    mu=[float(line.split()[9].replace(',','')),float(line.split()[10])]
                    muxsecs=[]
                if "#" in line: continue
                if line.split()==[]: continue
                if line.split()[0]=="LHAPDF": continue
                if line.split()[0]=="CT14nlo": continue
                xsec=[float(line.split()[3]),float(line.split()[4]),float(line.split()[6]),float(line.split()[7]),float(line.split()[10])]
                muxsecs.append(xsec)
            allmulist.append([mu,muxsecs])
        return allmulist

    def getqcdallmem(self):
        fileallmem=self.BaseDir+"/InclusiveNJetEvents_fnl5662"+self.version+"_v23_fix_CT14nlo_allmem.log"
        allmemlist=[]
        mem=["start"]
        memxsecs=["start"]
        with open(fileallmem) as f:
            for line in f:
                if "The PDF member chosen here is" in line:
                    if mem != ["start"] and memxsecs !=["start"]:
                        allmemlist.append([mem,memxsecs])
                    mem=[int(line.split()[7])]
                    memxsecs=[]
                if "#" in line: continue
                if line.split()==[]: continue
                if line.split()[0]=="LHAPDF": continue
                if line.split()[0]=="CT14nlo": continue
                xsec=[float(line.split()[3]),float(line.split()[4]),float(line.split()[6]),float(line.split()[7]),float(line.split()[10])]
                memxsecs.append(xsec)
            allmemlist.append([mem,memxsecs])
        return allmemlist

    def getciallmu(self):
        ls = subprocess.Popen(['ls',self.BaseDir+'/'+self.cixsecDir],stdout=subprocess.PIPE)    
        stdouts=[]
        while True:
            line = ls.stdout.readline()
            stdouts.append(line)
            if line == '' and ls.poll() != None:
                break        
        files=[]
        for stdout in stdouts:
            if stdout=='': continue
            if "_0_" not in stdout: continue
            if ".root" in stdout: continue
            file=stdout.replace("\n","")
            files.append(file)
    
        cimudict={}
        for file in files:
            cimudict[file.replace('.xsc','')]=[]
            with open(self.BaseDir+"/"+self.cixsecDir+"/"+file) as f:
                i=-9999
                for line in f:
                    i+=1
                    if "CT14nlo" in line: continue
                    if "Lambda" in line: continue
                    if "cj/4pi" in line: continue
                    if "Bin" in line:
                        i=0
                    if i==1:
                        mass_low=float(line.split()[2])
                        mass_high=float(line.split()[3])
                        chi_low=float(line.split()[0])
                        chi_high=float(line.split()[1])
                    if i>2:
                        xsec=float(line.split()[3])
                        mur=float(line.split()[1])
                        muf=float(line.split()[0])
                        #print cimudict
                        if len(cimudict[file.replace('.xsc','')])<9:
                            mu=[mur,muf]
                            xsecs=[mass_low,mass_high,chi_low,chi_high,xsec]
                            muxsecs=[mu,xsecs]
                            cimudict[file.replace('.xsc','')].append(muxsecs)    
                        else:
                            xsecs=[mass_low,mass_high,chi_low,chi_high,xsec]
                            cimudict[file.replace('.xsc','')][i-3].append(xsecs)
        return cimudict

    def getciallmem(self):
        cimemdict={}
        for style in self.styles:
            for m in range(5,31):
                cimemdict["CIJET_fnl5662i_cs_ct14nlo_"+str(m*1000)+"_"+style]=[]
                for j in range(0,57):
                    filename="CIJET_fnl5662i_cs_ct14nlo_"+str(j)+"_"+str(m*1000)+"_"+style+".xsc"
                    memxsecs=[]
                    with open(self.BaseDir+"/csxsec_ct14nlo_0-56_LL/"+filename) as f:
                        mem=j
                        memxsecs.append(mem)
                        i=-9999
                        for line in f:
                            i+=1
                            if "CT14nlo" in line: continue
                            if "Lambda" in line: continue
                            if "cj/4pi" in line: continue
                            if "Bin" in line:
                                i=0
                            if i==1:
                                mass_low=float(line.split()[2])
                                mass_high=float(line.split()[3])
                                chi_low=float(line.split()[0])
                                chi_high=float(line.split()[1])
                            if i>2:
                                xsec=float(line.split()[3])
                                mur=float(line.split()[1])
                                muf=float(line.split()[0])
                                if mur==1 and muf==1:
                                    xsecs=[mass_low,mass_high,chi_low,chi_high,xsec]
                                    memxsecs.append(xsecs)
                        cimemdict["CIJET_fnl5662i_cs_ct14nlo_"+str(m*1000)+"_"+style].append(memxsecs)
        return cimemdict
    
    def dictPrint(self,mydict):
        for key in mydict:
            print key
            print mydict[key]

    def listPrint(self,mylist):
        for list in mylist:
            print list
            
    def listFill(self,mylist,uncerttype):
        myfile=TFile(self.BaseDir+"/InclusiveNJetEvents_fnl5662"+self.version+"_v23_fix_CT14nlo_all"+uncerttype+".root","RECREATE")
        for list in mylist:
            if uncerttype=="mu":
                mur=str(list[0][0])
                muf=str(list[0][1])
                i=0
                for point in list[1]:
                    #print point
                    if i==0:
                        hist=TH1F("qcd_chi-"+str(int(point[0]))+"-"+str(int(point[1]))+"scale-"+mur+"-"+muf,"chi-"+str(int(point[0]))+"-"+str(int(point[1]))+"scale-"+mur+"-"+muf,len(self.bins)-1,self.bins)
                        hist.Sumw2()
                    hist.Fill(point[2]+(point[3]-point[2])/2,point[4]*(point[3]-point[2])*(point[1]-point[0]))
                    i+=1
                    if i==12:
                        hist.Write()
                        i=0
            elif uncerttype=="mem":
                member=str(list[0][0])
                i=0
                for point in list[1]:
                    if i==0:
                        hist=TH1F("qcd_chi-"+str(int(point[0]))+"-"+str(int(point[1]))+"PDF-"+member,"chi-"+str(int(point[0]))+"-"+str(int(point[1]))+"PDF-"+member,len(self.bins)-1,self.bins)
                        hist.Sumw2()
                    hist.Fill(point[2]+(point[3]-point[2])/2,point[4]*(point[3]-point[2])*(point[1]-point[0]))
                    i+=1
                    if i==12:
                        hist.Write()
                        i=0
            else:
                print "Please specify tyle: mu or mem."
                    
    
    def dictFill(self,mydict,uncerttype):
        for key in mydict:
            myfile=TFile(self.BaseDir+"/"+self.cixsecDir+"/"+key+"_"+uncerttype+".root","RECREATE")
            for list in mydict[key]:
                if uncerttype=="mu":
                    mur=str(list[0][0])
                    muf=str(list[0][1])
                    i=0
                    for j in range(1,len(list)):
                        if i==0:
                            hist=TH1F(key+"_"+"chi-"+str(int(list[j][0]))+"-"+str(int(list[j][1]))+"scale-"+mur+"-"+muf,"chi-"+str(int(list[j][0]))+"-"+str(int(list[j][1]))+"scale-"+mur+"-"+muf,len(self.bins)-1,self.bins)
                            hist.Sumw2()
                        hist.Fill(list[j][2]+(list[j][3]-list[j][2])/2,list[j][4])
                        i+=1
                        if i==12:
                            hist.Write()
                            i=0
                elif uncerttype=="mem":
                    member=str(list[0])
                    i=0
                    for j in range(1,len(list)):
                        if i==0:
                            hist=TH1F(key+"_"+"chi-"+str(int(list[j][0]))+"-"+str(int(list[j][1]))+"PDF-"+member,"chi-"+str(int(list[j][0]))+"-"+str(int(list[j][1]))+"PDF-"+member,len(self.bins)-1,self.bins)
                            hist.Sumw2()
                        hist.Fill(list[j][2]+(list[j][3]-list[j][2])/2,list[j][4])
                        i+=1
                        if i==12:
                            hist.Write()
                            i=0
                else:
                    print "Please specify tyle: mu or mem."
                
            
if __name__ == "__main__":
    myVariations=getVariations()
    
    qcdallmu=myVariations.getqcdallmu()
    myVariations.listFill(qcdallmu,"mu")
    
    qcdallmem=myVariations.getqcdallmem()
    myVariations.listFill(qcdallmem,"mem")

    ciallmu=myVariations.getciallmu()
    myVariations.dictFill(ciallmu,"mu")

    ciallmem=myVariations.getciallmem()
    myVariations.dictFill(ciallmem,"mem")    
            
        
                    
            
            
                
                
            
                
            
    


    
    







