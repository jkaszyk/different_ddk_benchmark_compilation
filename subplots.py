# coding: utf-8
# %load subplots.py
# %load subplots.py
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
c_labels = ['Num Arithmetic Instr.', 'Longest Arith. Path(Cyc.)', 'Shortest Arith. Path(Cyc.)', 'Num LS Instr.', 'Longest LS Path(Cyc.)', 'Shortest LS Path(Cyc.)', 'Num Regs. Used']
colors = ['royalblue', 'red', 'orange', 'green', 'purple', 'deepskyblue', 'deeppink', 'limegreen', 'firebrick']
   
import sqlite3
conn = sqlite3.connect("mali_offline_compiler.db")
cur = conn.cursor()
rows = cur.execute("select * from max_all")

new_rows = []
for r in rows:
    sum = 0.0
    for i in range(2,9):
        if r[i] != None:
            sum += r[i]
    new_rows.append(r + (r[0]+ ':' + r[1], sum,))

df = pd.DataFrame([[ij for ij in i] for i in new_rows])
df.rename(columns={0: 'Benchmark', 1: 'Kernel', 2:'Num Arithmetic Instr.', 3: 'Longest Arithmetic Path(Cycles)', 4:'Shortest Arithmetic Path(Cycles)', 5: 'Num LS Instr.', 6: 'Longest LS Path(Cycles)', 7:'Shortest LS Path(Cycles)', 8:'Num Registers Used', 9:'ID', 10:'sum_diff'}, inplace=True);
df.sort_values(by='sum_diff', ascending=False, inplace=True)

new_rows = df.values

x_labels = []
    
new_rows = new_rows[:12]
for row in new_rows:
    x_labels.append(row[0] + ':\n' + row[1])
    
cut_rows = []
for row in new_rows:
    cut_rows.append(list(row[2:9]))
    
sizes = np.array(cut_rows)

for i in range(sizes.shape[0]):
    for j in range(sizes.shape[1]):
        if sizes[i][j] == None:
            sizes[i][j] = 0
            
fig, axes = plt.subplots(ncols=sizes.shape[0], figsize=(10,5), sharey=True, sharex=True)

handles = []
i = 0

fig.text(0.04, 0.6, "Max Difference Between Compilers(%)", rotation='vertical', va='center', fontsize=20)
fig.text(0.5, 0.04, "Kernel", ha="center", fontsize=20)

for ax, height, title in zip(axes, sizes, x_labels):
    ax.tick_params(axis='both', labelsize=20)
    ax.set_facecolor("lightgrey")
    ax.set_xlabel(title, rotation=40, ha='right', fontsize=20)
    left = np.arange(len(height))+1
    for i in range(len(height)):
        if height[i] > 0:
            b = ax.bar(left[i], height[i]*100, color=colors[i], label=c_labels[i], width=1)
            handles.append(b)
        #b = ax.bar(left, height, color=colors, label=c_labels)
    ax.set_xticks(left)
    #ax.legend(handles, labels)
    #i += 1
    i = i % len(c_labels)

fig.legend(handles, c_labels, prop={'size':20}, ncol=4, bbox_to_anchor=(0.95,1.0))

plt.gcf().subplots_adjust(bottom=0.4)
plt.setp(axes, xticks=[])
plt.show()
