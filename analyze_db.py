import sqlite3

conn = sqlite3.connect("mali_offline_compiler.db")
cur = conn.cursor()

header = "benchmark, kernel, compiler_1, compiler_2, diff"

cur.execute("create table if not exists ls_cross_product_instr(" + header +")")
cur.execute("create table if not exists ls_cross_product_short(" + header +")")
cur.execute("create table if not exists ls_cross_product_long(" + header +")")

cur.execute("create table if not exists arith_cross_product_instr(" + header +")")
cur.execute("create table if not exists arith_cross_product_short(" + header +")")
cur.execute("create table if not exists arith_cross_product_long(" + header +")")

cur.execute("create table if not exists tex_cross_product_instr(" + header +")")
cur.execute("create table if not exists tex_cross_product_short(" + header +")")
cur.execute("create table if not exists tex_cross_product_long(" + header +")")

cur.execute("create table if not exists reg_cross_product(" + header +")")

# ls difference
ls_instr_query = "select t1.benchmark, t1.kernel, t1.compiler, t2.compiler, (t1.num_ls_instructions-t2.num_ls_instructions+0.0)/t1.num_ls_instructions as diff from benchmarks as t1 cross join benchmarks as t2 where t1.benchmark = t2.benchmark and t1.kernel = t2.kernel order by t1.benchmark, t1.kernel, diff"

ls_short_cycles_query = "select t1.benchmark, t1.kernel, t1.compiler, t2.compiler, (t1.ls_shortest_cycles-t2.ls_shortest_cycles+0.0)/t1.ls_shortest_cycles as diff from benchmarks as t1 cross join benchmarks as t2 where t1.benchmark = t2.benchmark and t1.kernel = t2.kernel order by t1.benchmark, t1.kernel, diff"

ls_long_cycles_query = "select t1.benchmark, t1.kernel, t1.compiler, t2.compiler, (t1.ls_longest_cycles - t2.ls_longest_cycles+0.0)/t1.ls_longest_cycles as diff from benchmarks as t1 cross join benchmarks as t2 where t1.benchmark = t2.benchmark and t1.kernel = t2.kernel order by t1.benchmark, t1.kernel, diff"

# arith difference
arith_instr_query = "select t1.benchmark, t1.kernel, t1.compiler, t2.compiler, (t1.num_arithmetic_instructions-t2.num_arithmetic_instructions+0.0)/t1.num_arithmetic_instructions as diff from benchmarks as t1 cross join benchmarks as t2 where t1.benchmark = t2.benchmark and t1.kernel = t2.kernel order by t1.benchmark, t1.kernel, diff"

arith_short_cycles_query = "select t1.benchmark, t1.kernel, t1.compiler, t2.compiler, (t1.arithmetic_shortest_cycles-t2.arithmetic_shortest_cycles+0.0)/t1.arithmetic_shortest_cycles as diff from benchmarks as t1 cross join benchmarks as t2 where t1.benchmark = t2.benchmark and t1.kernel = t2.kernel order by t1.benchmark, t1.kernel, diff"

arith_long_cycles_query = "select t1.benchmark, t1.kernel, t1.compiler, t2.compiler, (t1.arithmetic_longest_cycles - t2.arithmetic_longest_cycles+0.0)/t1.arithmetic_longest_cycles as diff from benchmarks as t1 cross join benchmarks as t2 where t1.benchmark = t2.benchmark and t1.kernel = t2.kernel order by t1.benchmark, t1.kernel, diff"

# tex difference
tex_instr_query = "select t1.benchmark, t1.kernel, t1.compiler, t2.compiler, (t1.num_tex_instructions-t2.num_tex_instructions+0.0)/t1.num_tex_instructions as diff from benchmarks as t1 cross join benchmarks as t2 where t1.benchmark = t2.benchmark and t1.kernel = t2.kernel order by t1.benchmark, t1.kernel, diff"

tex_short_cycles_query = "select t1.benchmark, t1.kernel, t1.compiler, t2.compiler, (t1.tex_shortest_cycles-t2.tex_shortest_cycles+0.0)/t1.tex_shortest_cycles as diff from benchmarks as t1 cross join benchmarks as t2 where t1.benchmark = t2.benchmark and t1.kernel = t2.kernel order by t1.benchmark, t1.kernel, diff"

tex_long_cycles_query = "select t1.benchmark, t1.kernel, t1.compiler, t2.compiler, (t1.tex_longest_cycles - t2.tex_longest_cycles+0.0)/t1.tex_longest_cycles as diff from benchmarks as t1 cross join benchmarks as t2 where t1.benchmark = t2.benchmark and t1.kernel = t2.kernel order by t1.benchmark, t1.kernel, diff"

# reg difference
reg_query = "select t1.benchmark, t1.kernel, t1.compiler, t2.compiler, (t1.num_registers-t2.num_registers+0.0)/t1.num_registers as diff from benchmarks as t1 cross join benchmarks as t2 where t1.benchmark = t2.benchmark and t1.kernel = t2.kernel order by t1.benchmark, t1.kernel, diff"

cur.execute('insert or ignore into ls_cross_product_instr(' + header + ')' + ls_instr_query + ';')
cur.execute('insert or ignore into ls_cross_product_short(' + header + ')' + ls_short_cycles_query + ';')
cur.execute('insert or ignore into ls_cross_product_long(' + header + ')' + ls_long_cycles_query + ';')

cur.execute('insert or ignore into arith_cross_product_instr(' + header + ')' + arith_instr_query + ';')
cur.execute('insert or ignore into arith_cross_product_short(' + header + ')' + arith_short_cycles_query + ';')
cur.execute('insert or ignore into arith_cross_product_long(' + header + ')' + arith_long_cycles_query + ';')

cur.execute('insert or ignore into tex_cross_product_instr(' + header + ')' + tex_instr_query + ';')
cur.execute('insert or ignore into tex_cross_product_short(' + header + ')' + tex_short_cycles_query + ';')
cur.execute('insert or ignore into tex_cross_product_long(' + header + ')' + tex_long_cycles_query + ';')

cur.execute('insert or ignore into reg_cross_product(' + header + ')' + reg_query + ';')

# find max for each benchmark

#ls
cur.execute("create table if not exists max_ls_instr_diff as select benchmark, kernel, compiler_1, compiler_2, max(abs(diff)) from ls_cross_product_instr group by benchmark,kernel order by diff")

cur.execute("create table if not exists max_ls_short_diff as select benchmark, kernel, compiler_1, compiler_2, max(abs(diff)) from ls_cross_product_short group by benchmark,kernel order by diff")

cur.execute("create table if not exists max_ls_long_diff as select benchmark, kernel, compiler_1, compiler_2, max(abs(diff)) from ls_cross_product_long group by benchmark,kernel order by diff")

# arith
cur.execute("create table if not exists max_arith_instr_diff as select benchmark, kernel, compiler_1, compiler_2, max(abs(diff)) from arith_cross_product_instr group by benchmark,kernel order by diff")

cur.execute("create table if not exists max_arith_short_diff as select benchmark, kernel, compiler_1, compiler_2, max(abs(diff)) from arith_cross_product_short group by benchmark,kernel order by diff")

cur.execute("create table if not exists max_arith_long_diff as select benchmark, kernel, compiler_1, compiler_2, max(abs(diff)) from arith_cross_product_long group by benchmark,kernel order by diff")

# tex
cur.execute("create table if not exists max_tex_instr_diff as select benchmark, kernel, compiler_1, compiler_2, max(abs(diff)) from tex_cross_product_instr group by benchmark,kernel order by diff")

cur.execute("create table if not exists max_tex_short_diff as select benchmark, kernel, compiler_1, compiler_2, max(abs(diff)) from tex_cross_product_short group by benchmark,kernel order by diff")

cur.execute("create table if not exists max_tex_long_diff as select benchmark, kernel, compiler_1, compiler_2, max(abs(diff)) from tex_cross_product_long group by benchmark,kernel order by diff")

# regs
cur.execute("create table if not exists max_reg_diff as select benchmark, kernel, compiler_1, compiler_2, max(abs(diff)) from reg_cross_product group by benchmark,kernel order by diff")

conn.commit()
conn.close()
