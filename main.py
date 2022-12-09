import argparse

parser = argparse.ArgumentParser()
parser.add_argument('infile', type=argparse.FileType('r'))
parser.add_argument('-medals', dest='medals', nargs=2, required=True)
parser.add_argument('-output', '--output', type=argparse.FileType('w', encoding='UTF-8'))

def medals(line, country, year,k):
    olympic_info = line.split('\t')
    if (olympic_info[6] == country or olympic_info[7] == country) and (olympic_info[9] == year) and (olympic_info[14] != 'NA\n'):
        print(olympic_info[1], olympic_info[12],olympic_info[14])
        k['Name'] = k['Name']+olympic_info[1]+' '+olympic_info[12] +' '+olympic_info[14]+'; '
        k['amount'] += 1 
        if olympic_info[14] == 'Gold\n':
            k['Gold'] += 1 
        if olympic_info[14] == 'Silver\n':
            k['Silver'] += 1
        if olympic_info[14] == 'Bronze\n':
            k['Bronze'] += 1
    return k
args = parser.parse_args()

with args.infile as file:
    next_line = file.readline()
    k = {'amount': 0, 'Gold': 0, 'Silver': 0, 'Bronze': 0, 'Name':''}
    while next_line:
        if args.medals is not None:
            next_line = file.readline()
            if next_line != '' and k['amount'] < 10:
                a = medals(next_line,args.medals[0], args.medals[1],k)
    print(k['Gold'], k['Silver'], k['Bronze'])
    if args.output is not None:
        f = open('result.txt','w')
        names = k['Name'].split(';')
        for name in names:
            f.write(name)
        f.write(str(k['Gold'])+' '+str(k['Silver'])+' '+str(k['Bronze']))
        f.close()
    if k['amount'] == 0:
        print('В обраний рік країна не брала участі в олімпіаді')      