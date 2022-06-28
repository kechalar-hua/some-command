import sys


def usage():
    print('Usage: python json.py [sample.json] [sample.json.txt]')


def main():
    lines = open(sys.argv[1], 'r').readlines()
    box = [sys.argv[1]]
    a = 0
    flag = 0
    for line in lines:
        if "after_filtering" in line:
            flag = 1
            a += 1
        if "}," in line:
            flag = 0
        if a == 1:
            if flag == 1:
                if "{" in line or "}" in line:
                    pass
                else:
                    box.append(line.strip().split(":")[1].strip(","))
            else:
                pass
        else:
            pass
    new = open(sys.argv[2], 'w')
    for x in box:
        new.write(x + '\t')
    new.write("\n")
    new.close()
    print(sys.argv[2] + " is finished!")


try:
    main()
except IndexError:
    usage()
