import argparse

parser = argparse.ArgumentParser()
parser.add_argument('infile', type=argparse.FileType('r'))
parser.add_argument('-medals', dest='medals', nargs=2)
parser.add_argument('-output', '--output', type=argparse.FileType('w', encoding='UTF-8'))


def medals(line, country, year,sport_info):
    olympic_info = line.split('\t')
    a = olympic_info[6] == country or olympic_info[7] == country
    b = olympic_info[9] == year
    c = olympic_info[14] != 'NA\n'
    if a and b and c:
        print(olympic_info[1], olympic_info[12],olympic_info[14])
        sport_info['Name_disc_medal'] = sport_info['Name_disc_medal']+olympic_info[1]+' '+olympic_info[12] +' '+olympic_info[14]+'; '
        sport_info['amount'] += 1 
        if olympic_info[14] == 'Gold\n': sport_info['Gold'] += 1 
        if olympic_info[14] == 'Silver\n': sport_info['Silver'] += 1
        if olympic_info[14] == 'Bronze\n': sport_info['Bronze'] += 1
    return sport_info

def overall(line, overall_dict):
    olympic_info = line.split('\t')
    for i in overall_dict:
        if i == olympic_info[6] and olympic_info[14] != 'NA\n':
            overall_dict[i] = overall_dict[i] + olympic_info[9] + ';'
    return overall_dict


args = parser.parse_args()

with args.infile as file:
    next_line = file.readline()
    sport_info = {'amount': 0, 'Gold': 0, 'Silver': 0, 'Bronze': 0, 'Name_disc_medal':''}
    overall_dict = dict.fromkeys(args.overall,'')

    while next_line != '':
        next_line = file.readline()
        if args.medals is not None:
            if sport_info['amount'] < 10:
                a = medals(next_line,args.medals[0], args.medals[1],sport_info)
        if args.overall is not None:
            next_line = file.readline()
            if next_line !='': overall_dict = overall(next_line,overall_dict)
    
    if args.medals is not None: print(sport_info['Gold'], sport_info['Silver'], sport_info['Bronze'])
    if args.output is not None:
        names = sport_info['Name_disc_medal'].split(';')
        for name in names:
            args.output.writelines(name)
        args.output.writelines(str(sport_info['Gold'])+' '+str(sport_info['Silver'])+' '+str(sport_info['Bronze']))
    if sport_info['amount'] == 0 and args.medals is not None:
        print('В обраний рік країна не брала участі в олімпіаді')      