import os
counter=100
for gq in ["0.05","0.08","0.09","0.1","0.11","0.12","0.13","0.14","0.15","0.16","0.17","0.18","0.19","0.2","0.21","0.22","0.23","0.24","0.25","0.26","0.27","0.28","0.29","0.5","1.0"]:
   for vector in ["800","801"]:
     string="python calculate_limit_shape_13TeV.py "+str(counter)
     if counter%5!=4:
       string+=" &"
     print string
     counter+=1
     
