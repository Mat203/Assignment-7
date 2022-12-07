import sys

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

n = sys.argv
print(n)
with open('data.tsv','r') as file:
    next_line = file.readline()
    k = {'amount': 0, 'Gold': 0, 'Silver': 0, 'Bronze': 0, 'Name':''}
    while next_line:
        if n[2] == '-medals':
            next_line = file.readline()
            if next_line != '' and k['amount'] < 10:
                a = medals(next_line, n[3],n[4],k)
    print(k['Gold'], k['Silver'], k['Bronze'])
    if n[5] == '-output':
        f = open('result.txt','w')
        names = k['Name'].split(';')
        for name in names:
            f.write(name)
        f.write(str(k['Gold'])+' '+str(k['Silver'])+' '+str(k['Bronze']))
        f.close()
    if k['amount'] == 0:
        print('В обраний рік країна не брала участі в олімпіаді')      