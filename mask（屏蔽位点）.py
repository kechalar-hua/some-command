#import time
lines = open("21sum_mafft.oneline.fasta", "r").readlines()
a = 0
lenth = 0
judge_box = []
final_box = []
for line in lines:
    if line.startswith(">"):
        a += 1
    else:
        lenth = (len(line))
#print(lenth)  # 141314
#print(a)
b = 0
for i in range(lenth):
    for line in lines:
        if line.startswith(">"):
            b += 1
        else:
            judge_box.append(line[i])
            # print(judge_box)
            if b == a:
                judge = set(judge_box)
                if len(judge) == 1:
                    final_box.append(judge_box[0])
                else:
                    final_box.append("N")
                print(len(final_box))
                judge_box = []
                b = 0
            #time.sleep(0.05)


final_box_end = "".join(final_box)
print(final_box_end)

new = open("out.txt", "w")
for x in final_box_end:
    new.write(x)
new.close()