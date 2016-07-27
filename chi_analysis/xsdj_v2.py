#! /usr/bin/env python

import ROOT as r
import argparse,commands,os

aparser = argparse.ArgumentParser(description='Process benchmarks.')
#aparser.add_argument('-sample'  ,'--sample'    ,action='store' ,dest='sample' ,default='Spring15_a25ns_DMJetsVector_Mphi-10000_Mchi-50_gSM-1p0_gDM-1p0',  help='sample')
aparser.add_argument('-proc' ,'--proc'  ,action='store' ,dest='proc',default='800',  help='800,801,805,806 => V,A,S,P')
aparser.add_argument('-med'  ,'--med'   ,action='store' ,dest='med' ,default='500',  help='med mass')
aparser.add_argument('-dm'   ,'--dm'    ,action='store' ,dest='dm'  ,default='1',    help='dm mass')
aparser.add_argument('-gq'   ,'--gq'    ,action='store' ,dest='gq'  ,default='1',    help='gq')
aparser.add_argument('-list' ,'--list'  ,action='store_true',dest='list'  ,  help='list everything')
options = aparser.parse_args()

eos='/afs/cern.ch/project/eos/installation/cms/bin/eos.select'
basedir='eos/cms/store/cmst3/group/monojet/mc/model3_v2/gen'

def computeXS(med,dm,gq,proc):
    global sumweights,sumxs,sumentries
    infile='%s/dijet_%s_%s_%s_%s.root' % (basedir,med,dm,gq,proc) #_zprime
    #print "root://eoscms//%s" % (infile)
    lFile = r.TFile().Open("root://eoscms//%s" % (infile))
    events = lFile.Get("Runs") #"Events"
    for event in events:
     return event.GenRunInfoProduct_generator__GEN.product().crossSection()
     #return event.edmHepMCProduct_generator__GEN.product().getHepMCData().cross_section()
if options.list: 
    command = '%s ls %s | grep dijet | sed "s@_@ @g" | awk \'{print "mMed="$2" mDM="$3}\' | uniq' % (eos,basedir)
    exists = commands.getoutput(command)
    for line in exists.splitlines():
        print line
    quit()

xs=computeXS(options.med,options.dm,options.gq,options.proc)
    
print "DM"+str(options.med)+"_"+str(options.dm)+"_"+str(options.gq)+"_"+str(options.proc),"   ",xs
