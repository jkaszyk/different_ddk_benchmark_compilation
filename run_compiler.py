import os
import re
import csv
import sys

config_options=[]

f=open('.config')
for f in f.readlines():
	config_options.append(f.strip())

compiler_path=config_options[0]

benchmark_path=sys.argv[1]+'/'
f=open(sys.argv[2],"r")
filename_list=[]
pattern = re.compile("__kernel")

register_pattern = re.compile("uniform registers used")
instr_pattern = re.compile("Instructions Emitted")
short_path_pattern = re.compile("Shortest Path Cycles")
long_path_pattern = re.compile("Longest Path Cycles")

for f in f.readlines():
	 filename_list.append(f.replace('\n','').strip())
			      
compilers=os.listdir(compiler_path)
      

with open("out.csv", "wb") as csvfile:
         writer = csv.writer(csvfile, delimiter=',')
         writer.writerow(["benchmark", "kernel", "compiler", "num_registers", "num_arithmetic_instructions", "num_ls_instructions", "num_tex_instructions", "arithmetic_shortest_cycles", "ls_shortest_cycles", "tex_shortest_cycles", "arithmetic_longest_cycles", "ls_longest_cycles", "tex_longest_cycles"])
         for f in filename_list:
                  os.system('mkdir -p benchmark_results/'+f)

                  cl=open(benchmark_path+f+"/"+f+"_Kernels.cl", 'r')
                  kernels=[]
                  for l in cl.readlines():
                           for match in re.finditer(pattern, l):
                                    l = l.replace('__attribute__((reqd_work_group_size(256,1,1))) ', '').replace('__kernel void ', '')
                                    l = l[:l.find('(')]
                                    l = l.strip()
                                    kernels.append(l)

                  
                  for k in kernels:
                           for c in compilers:
	                            os.system(compiler_path + '/' + c + "/malisc -c Mali-G71 -r r0p0 " + benchmark_path +f+"/"+f+"_Kernels.cl --name " + k + " > benchmark_results/" + f + "/" + k + "_" + f + "_" + c)
                                    print f + ' ' + k + ' ' + c
                                    result=open("benchmark_results/" + f + "/" + k + "_" + f + "_" + c, 'r')

                                    reg_numbers = 0xdeadbeef
                                    instr_numbers = 0xdeadbeef
                                    short_numbers = 0xdeadbeef
                                    long_numbers = 0xdeadbeef

                                    for l in result.readlines():                                    
                                             for match in re.finditer(register_pattern, l):
                                                      reg_numbers = [int(s) for s in l.split() if s.isdigit()][1:]
                                             
                                             for match in re.finditer(instr_pattern, l):
                                                      instr_numbers = [int(s) for s in l.split() if s.isdigit()]
                                                      
                                             for match in re.finditer(short_path_pattern, l):
                                                      short_numbers = [int(s) for s in l.split() if s.isdigit()]

                                             for match in re.finditer(long_path_pattern, l):
                                                      long_numbers = [int(s) for s in l.split() if s.isdigit()]

                                    if (reg_numbers != 0xdeadbeef and instr_numbers != 0xdeadbeef and short_numbers != 0xdeadbeef and long_numbers != 0xdeadbeef):
                                             lst = [f,k,c]
                                             lst.extend(reg_numbers)
                                             lst.extend(instr_numbers)
                                             lst.extend(short_numbers)
                                             lst.extend(long_numbers)
                                             writer.writerow(lst)
                                    
