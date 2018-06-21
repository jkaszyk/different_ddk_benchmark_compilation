import os
import re
import csv
import sys

pattern = re.compile("__kernel")

register_pattern = re.compile("uniform registers used")
instr_pattern = re.compile("Instructions Emitted")
short_path_pattern = re.compile("Shortest Path Cycles")
long_path_pattern = re.compile("Longest Path Cycles")


with open("out.csv", "wb") as csvfile:
         writer = csv.writer(csvfile, delimiter=',')
         writer.writerow(["benchmark", "kernel", "compiler", "num_registers", "num_arithmetic_instructions", "num_ls_instructions", "num_tex_instructions", "arithmetic_shortest_cycles", "ls_shortest_cycles", "tex_shortest_cycles", "arithmetic_longest_cycles", "ls_longest_cycles", "tex_longest_cycles"])
         for dirName, subdirList, fileList in os.walk('benchmark_results'):                  
                  for fname in fileList:
                           result=open(dirName + '/' + fname)
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
                                    f=dirName[dirName.find('/')+1:]
                                    k=fname[:fname[:fname.find('_Mali')].find('_')]
                                    c=fname[fname.find('Mali'):]
                                    lst = [f,k,c]
                                    lst.extend(reg_numbers)
                                    lst.extend(instr_numbers)
                                    lst.extend(short_numbers)
                                    lst.extend(long_numbers)
                                    writer.writerow(lst)
                                    
