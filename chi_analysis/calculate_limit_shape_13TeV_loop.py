import os
counter=100
for gq in ["0.1","0.15","0.2","0.25","0.5","0.75","1.0","1.25","1.5","1.75","2.0","2.25","2.5","2.75","3.0","3.5","4.0","6.0","8.0", "10.0"]:
   for vector in ["800"]:# ,"801"
     string="python calculate_limit_shape_13TeV.py "+str(counter)
     if counter%5!=4:
       string+=" &"
     print string
     counter+=1
for gq in ["1.0", "1.5", "2.0", "2.5", "3.0", "3.5", "4.0", "4.5", "5.0", "5.5", "6.0", "8.0", "10.0", "12.0", "15.0", "20.0"]:
   for vector in ["800"]:#"801"
     string="python calculate_limit_shape_13TeV.py "+str(counter)
     if counter%5!=4:
       string+=" &"
     print string
     counter+=1
