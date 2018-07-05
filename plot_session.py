# coding: utf-8
# %load plot_session
# %load test_plot_session.py
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
    

import pandas as pd
df = pd.DataFrame([[ij for ij in i] for i in new_rows])
df.rename(columns={0: 'Benchmark', 1: 'Kernel', 2:'Num Arithmetic Instr.', 3: 'Longest Arithmetic Path(Cycles)', 4:'Shortest Arithmetic Path(Cycles)', 5: 'Num LS Instr.', 6: 'Longest LS Path(Cycles)', 7:'Shortest LS Path(Cycles)', 8:'Num Registers Used', 9:'ID', 10:'sum_diff'}, inplace=True);
#df.sort_values(by=['ID'])
df.sort_values(by='sum_diff')
import matplotlib.pyplot as plt
pl = df.iloc[0:30][['Benchmark','Kernel','Num Arithmetic Instr.', 'Longest Arithmetic Path(Cycles)', 'Shortest Arithmetic Path(Cycles)', 'Num LS Instr.', 'Longest LS Path(Cycles)', 'Shortest LS Path(Cycles)', 'Num Registers Used', 'ID']].plot.bar(x='ID', width=1)
pl.set_ylabel("Differences in Mali Compilier(%)")
pl.set_xlabel("Benchmark:Kernel")
plt.xticks(rotation=75, ha='right')
plt.gca().set_ylim([0,1.0])
plt.tight_layout()
plt.legend(ncol=4)
#plt.autoscale()
plt.show()
conn.close()
