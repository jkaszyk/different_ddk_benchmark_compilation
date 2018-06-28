#to_db = [(i['benchmark'], i['kernel'], i['compiler'], i['num_registers'], i['num_arithmetic_instructions'], i['num_ls_instructions'], i['num_tex_instructions'], i['arithmetic_shortest_cycles'],i['ls_shortest_cycles'], i['tex_shortest_cycles'],i['arithmetic_longest_cycles'],i['ls_longest_cycles'],i['tex_longest_cycles']) for i in dr]

import os
import re
import csv
import sys
import sqlite3

# Connecting to the database file
conn = sqlite3.connect("mali_offline_compiler.db")
cursor = conn.cursor()

# Create table holding data from all compiler runs
benchmark_tables_header_str = 'benchmark, kernel, compiler, num_registers, num_arithmetic_instructions, num_ls_instructions, num_tex_instructions, arithmetic_shortest_cycles, ls_shortest_cycles, tex_shortest_cycles, arithmetic_longest_cycles, ls_longest_cycles, tex_longest_cycles'

create_table_str = 'benchmark text, kernel text, compiler text, num_registers int, num_arithmetic_instructions int, num_ls_instructions int, num_tex_instructions int, arithmetic_shortest_cycles int, ls_shortest_cycles int, tex_shortest_cycles int, arithmetic_longest_cycles int, ls_longest_cycles int, tex_longest_cycles int, primary key(benchmark, kernel, compiler)'

cursor.execute('create table if not exists benchmarks(' + create_table_str + ');')


pattern = re.compile("__kernel")

register_pattern = re.compile("uniform registers used")
instr_pattern = re.compile("Instructions Emitted")
short_path_pattern = re.compile("Shortest Path Cycles")
long_path_pattern = re.compile("Longest Path Cycles")

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
                           strings = fname.split('%')
                           k = strings[0]
                           c = strings[2]
                           lst = [f,k,c]
                           lst.extend(reg_numbers)
                           lst.extend(instr_numbers)
                           lst.extend(short_numbers)
                           lst.extend(long_numbers)

                           string_line = ''
                           for i in range(len(lst)):
                                    if i < 3:
                                             string_line += '"' + str(lst[i]) + '"'
                                    else:
                                             string_line += str(lst[i])
                                             
                                    if  i != (len(lst)-1):
                                             string_line += ','
                           if len(lst) < 13:
                                    diff = 13 - len(lst)
                                    for i in range(diff):
                                             string_line += ', NULL'

#                           print string_line
                           query = 'insert into benchmarks(' + benchmark_tables_header_str + ') values(' + string_line + ');'
                           print query
                           cursor.execute('insert or ignore into benchmarks(' + benchmark_tables_header_str + ') values(' + string_line + ');')

conn.commit()
conn.close()
