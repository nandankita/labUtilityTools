'''
Created on Dec 5, 2017
python ~/aTools/utilities/catSelectedOrder.py
@author: nanda
'''

import os
with open("afterlinecorrectclusterselectedOrder.txt","w") as Comb:
    for i in range(0,88):
        n=str(i)
        PATH="/nl/umw_job_dekker/users/an27w/dinoflagellets/analysis/lines-manualAssembly-4/assembly-3/"
#         a = [0, 1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 
#              28, 31, 32, 33, 34, 35, 36, 37, 38, 39, 44, 45, 46, 48, 50, 52, 53, 54, 55, 56, 57, 
#              58, 59, 60, 61, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 79, 80, 81, 82, 83, 84, 85, 86, 87]
#         b = [4, 16, 41, 43, 62]
#         if i in a:
#             PATH="/nl/umw_job_dekker/users/an27w/dinoflagellets/analysis/lines-manualAssembly-4/assembly/"
#         elif i in b:
#             PATH="/nl/umw_job_dekker/users/an27w/dinoflagellets/analysis/manualAssembly-3/"
#         else:
#             PATH="/nl/umw_job_dekker/users/an27w/dinoflagellets/analysis/manualAssembly-2/"
        FileName="cluster"+n+"/selectedOrder"+n
        input_file = PATH+FileName
        print(str(i)+"\n"+input_file)
        with open(input_file) as Sc:
            for line in Sc:
                line=line.rstrip("\n")
                Comb.write(line+"\t"+n+"\n")
        print("cluster"+n+"done")
    for x in ["lnCluster31", "lnCluster53", "lnCluster64"]:
        fileN="/nl/umw_job_dekker/users/an27w/dinoflagellets/analysis/lines-manualAssembly-4/assembly-3/cluster"+x+"/selectedOrder"+x
        print(fileN)
        with open(fileN) as Sc:
            for line in Sc:
                line=line.rstrip("\n")
                Comb.write(line+"\t"+x+"\n")
        print(x+"done")
