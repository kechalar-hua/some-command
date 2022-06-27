# # -*- coding: utf-8 -*-
# STEP1
# step1
import re
# import numpy as np
lines_1 = open('input.txt').readlines()  # 打开文件，读入每一行
cup_for_step1 = []  # 第一步的容器，装载输出表格
flag1 = 0  # 设置第一步的标志变量
for line in lines_1:  # 循环每一行
    if line.startswith("The best scores are:"):  # 如果以"The best scores are:"开头
        flag1 = 1  # 设置标志标量为1
    elif line.startswith(">>>S"):  # 如果以">>>S"开头
        flag1 = 0  # 设置标志变量为0，以上步骤框定表格范围
    if flag1 == 1:  # 当flag1是1时，意味着在表格范围内
        if line.startswith("Sspon.0"):  # 如果以"S"开头
            cup_for_step1.append(line)  # 就用容器装载该行
        elif line == "\n":  # 如果是空行
            cup_for_step1.append(line)  # 也装载进去
        else:  # 其他情况时
            pass  # 跳过
    if flag1 == 0:  # 如果flag1是0，意味着在表格范围外
        pass  # 跳过
# step2  # 根据上一步整理出的表格，开始精炼信息
flag2 = 0  # 设置第二步的标志变量为0
head = ""  # 定义空的head
new_line = ""  # 定义空的new_line
cup_for_step2 = []  # 第二步的容器，装载精炼的信息
for i in cup_for_step1:  # 从第一步的容器中遍历每一行
    if i == "\n":  # 如果是空行
        flag2 = 0  # 设置第二步的标志变量依然是0
        head = ""  # 时刻让head为空
        new_line = ""  # 时刻让new_line为空
    elif i.startswith("Sspon.0"):  # 如果容器中某一行以"Sspon.0"开头
        flag2 = 1  # 设置标志变量为1
    if flag2 == 0:  # 如果第二步标志变量为0时，表示这一行没有信息
        head = ""  # 保持head为空
        new_line = ""  # 保持new_line为空
    if flag2 == 1:  # 如果标志变量为1，表示这行有信息
        a = i.split("	")[1].split(" ")[0]  # 让a等于%_id
        b = i.split("	")[1].split(" ")[1]  # 让b等于%_sim
        if a == "1.000" and b == "1.000":  # 如果a,b都是1，表示是自我比对
            head = i.split("	")[0].split(" ")[0]  # 记录下自我比对的ID，它是这组的query
        else:  # 如果不是自我比对
            new_line = head + "\t" + i
            cup_for_step2.append(new_line)  # 整理完的目标行放入第二步的容器
new = open("1.1.table.txt", "w")  # 第1个输出文件，是删除自身比对的输出表格
for j in cup_for_step2:
    new.write(j)
new.close()
# step3
old_table = open("1.1.table.txt").readlines()
cup_for_final = []
for line in old_table:
    tag_01 = line.split("(")[0].strip()
    tag_2_16 = line.split("\t")[2]
    b = re.split(r" +", tag_2_16)
    new_tag_2_16 = b[0] + "\t" + \
                   b[1] + "\t" + \
                   b[2] + "\t" + \
                   b[3] + "\t" + \
                   b[4] + "\t" + \
                   b[5] + "\t" + \
                   b[6] + "\t" + \
                   b[7] + "\t" + \
                   b[8] + "\t" + \
                   b[9] + "\t" + \
                   b[10] + "\t" + \
                   b[11] + "\t" + \
                   b[12] + "\t" + \
                   b[13] + "\t" + \
                   b[14]
    final_tag = tag_01 + "\t" + new_tag_2_16
    cup_for_final.append(final_tag)
new = open("1.2.table_fix.txt", "w")  # 第2个输出文件，是整理格式后的表格，易于后续提取信息
new.write("Target	Query	%_id	%_sim	gnw	alen	an0	ax0	pn0	px0	an1	ax1	pn1	px1	gapq	gapl	fs\n")
for i in cup_for_final:
    new.write(i)
new.close()
print("***STEP-1-Done***")
# STEP2
table = open("1.2.table_fix.txt", "r").readlines()
identity = ""
flag = 0
cup = []
for line in table:
    if line.startswith("Target"):
        pass
    else:
        target = line.split("\t")[0]
        query = line.split("\t")[1]
        identity = float(line.split("\t")[2])
        new_line = target + "\t" + query + "\t" + str(identity) + "\n"
        cup.append(new_line)
# if flag == 0:
#     print("Corrected")
new = open("2.iden_fix.txt", "w")  # 第3个输出文件，修正四舍五入带来的换算误差，并适应cd-hit-est的全局比对一致性计算公式
for i in cup:
    new.write(i)
new.close()
print("***STEP-2-Done***")
# STEP3
# step1 rmdup
iden_fix = open("2.iden_fix.txt", "r").readlines()
cup_for_step2 = []
for line in iden_fix:
    cup_for_step2.append(line)
temp_cup = []  # 临时容器用于装载没有多克隆、旁源基因ID的行
tag1 = ""  # 储存query的最后一个字符
tag2 = ""  # 储存target的最后一个字符
for i3 in cup_for_step2:  # 循环第二步容器中的对象
    if i3.split("\t")[0].split("-")[0] != i3.split("\t")[1].split("-")[0]:  # 如果不是互为等位基因的比对
        pass  # 跳过
    else:  # 否则
        tag1 = i3.split("	")[0][-1]  # query的最后一个字符
        tag2 = i3.split("	")[1][-1]  # target的最后一个字符
        A_B_C_D = ["A", "B", "C", "D"]  # 代表等位基因的字符
        if tag1 in A_B_C_D and tag2 in A_B_C_D:  # 如果最后一个字符都是标记了等位基因而不是旁源基因
            temp_cup.append(i3)  # 那么这一个对象就加入到临时容器中
# print(temp_cup)
new = open('3.1.allele_group.txt', 'w')  # 第4个输出文件，剔除旁源非等位参与的比对
for i in temp_cup:
    new.write(i)
new.close()
# step2 average
lines_2 = open('3.1.allele_group.txt').readlines()  # 步骤二打开第一步完成的文件
cup_for_merge = []  # 装载第二步的输出结果
temp_dict = {}  # 用于装载第一次出现的前两列字符串:后两列数据
temp_key = []  # 用于装载字典的key，直接去字典里找key找不到时会报错，故用之
temp_cup = []  # 用于装载第一步结果文件的每一行，一行为一个元素
for line in lines_2:
    temp_cup.append(line.strip())  # 输入文件装入列表
for item in temp_cup:
    str_1 = item.split("\t")[0]
    str_2 = item.split("\t")[1]
    str_3 = item.split("\t")[2]
    if str_2+"\t"+str_1 in temp_key:  # 如果反向比对出现了，就记录均值，并从temp_key里删除key，目的是得到剩下只出现一次的比对
        ave_iden = round((float(temp_dict[str_2 + "\t" + str_1].split("\t")[0]) + float(str_3)) / 2, 3)
        cup_for_merge.append(str_2 + "\t" + str_1 + "\t" + str(ave_iden))
        temp_key.remove(str_2+"\t"+str_1)
    else:  # 如果反向比对没有，就在字典里加入目前的键值对，temp_key里加入key
        temp_dict.update({str_1+"\t"+str_2: str_3})
        temp_key.append(str_1+"\t"+str_2)
lonely_line = []  # 处理只出现一次的比对
for x in temp_key:  # 此时temp_key里只有一次比对的key，装入列表
    str_lonely = x + "\t" + temp_dict[x]
    lonely_line.append(str_lonely)
new = open('3.2.average_both.txt', 'w')  # 第5个输出文件，存在反向比对则求平均，不存在反向比对则保留
for i in cup_for_merge:  # 双向比对求平均为一行，写入第二步结果文件
    new.write(i + "\n")
for j in lonely_line:  # 单向比对为一行，写入第二步结果文件
    new.write(j + "\n")
new.close()
print("***STEP-3-Done***")
# STEP4
lines_3 = open('3.2.average_both.txt').readlines()  # 打开步骤二的结果文件
temp_cup = []
for line in lines_3:  # 步骤二的每一行装载进列表
    temp_cup.append(line.strip())
temp_key = []
for i in temp_cup:   # 装载每一行的基因编号
    key = i.split("\t")[0].split("-")[0]
    if key not in temp_key:  # 如果基因编号不在列表，就添加进去
        temp_key.append(key)
new = open('4.sort.txt', 'w')  # 第6个输出文件，根据基因编号排序，易于后续按基因分组计算
for x in temp_key:  # 循环基因编号
    for y in temp_cup:  # 循环每一行，如果基因编号对应到了，就写入结果文件，这样可以把等位比对排序在一起
        key_2 = y.split("\t")[0].split("-")[0]
        if x == key_2:
            new.write(y + "\n")
new.close()
print("***STEP-4-Done***")
# STEP5
lines_4 = open('4.sort.txt').readlines()
temp_cup = []
temp_dark = []
for line in lines_4:
    if line.strip() in temp_dark:
        pass
    else:
        temp_cup.append(line.strip())
    temp_dark.append(line.strip())
list0 = []
for key in temp_cup:  # 提取第1列的基因编号和第3列，整合为一个字符串
    str_02 = key.split("\t")[0].split("-")[0] + "\t" + key.split("\t")[2]
    list0.append(str_02)
list1 = []
for i in list0:
    if i.split("\t")[0] not in list1:
        list1.append(i.split("\t")[0])
txt = []
gene = ""
for j in list1:
    cup_iden = []
    for jj in list0:
        if jj.split("\t")[0] == j:
            cup_iden.append(float(jj.split("\t")[1]))
            # average = round(float(np.mean(cup_iden)), 3)  # 每组基因求取平均值
            # gene = j + "\t" + str(average)
            cup_iden.sort()
            max_iden = round(cup_iden[-1], 3)  # 每组基因求取最大值
            gene = j + "\t" + str(max_iden)
        else:
            cup_iden = []
    txt.append(gene)
new = open('5.max.txt', 'w')  # 第7个输出文件，每组基因求取平均值，最后保留基因编号和对应的平均值
for x in txt:
    new.write(x + "\n")
new.close()
print("***STEP-5-Done***")
print("***Stage-1-Done***")
