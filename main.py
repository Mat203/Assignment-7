import argparse

parser = argparse.ArgumentParser()
parser.add_argument('infile', type=argparse.FileType('r'))
parser.add_argument('-medals', dest='medals', nargs=2)
parser.add_argument('-output', '--output', type=argparse.FileType('w', encoding='UTF-8'))
parser.add_argument('-overall', nargs='*')
parser.add_argument('-total', nargs=1)
parser.add_argument('-interactive')

def medals(country, year):
    with args.infile as file:
        next_line = file.readline()

        sport_info = {'amount': 0, 'Gold': 0, 'Silver': 0, 'Bronze': 0, 'Name_disc_medal':''}
        next_line = file.readline()

        while next_line != '':
            olympic_info = next_line.split('\t')
            a = olympic_info[6] == country or olympic_info[7] == country
            b = olympic_info[9] == year
            c = olympic_info[14] != 'NA\n'
            if sport_info['amount'] < 10:
                
                if a and b and c:
                    print(olympic_info[1], olympic_info[12],olympic_info[14])
                    sport_info['Name_disc_medal'] = sport_info['Name_disc_medal']+olympic_info[1]+' '+olympic_info[12] +' '+olympic_info[14]+'; '
                    sport_info['amount'] += 1 
            if olympic_info[14] == 'Gold\n' and a and b: sport_info['Gold'] += 1 
            if olympic_info[14] == 'Silver\n' and a and b: sport_info['Silver'] += 1
            if olympic_info[14] == 'Bronze\n' and a and b: sport_info['Bronze'] += 1
            next_line = file.readline()
        if sport_info['amount'] == 0:
            print('В обраний рік країна не брала участі в олімпіаді')
        else:    
            print(sport_info['Gold'],sport_info['Silver'],sport_info['Bronze'])
    return sport_info

def total(Year):
    totalInfo = dict()
    with args.infile as file:
        line = file.readline()

        while line:
            line = line[:-1]
            parsedLine = line.split('\t')
            country = parsedLine[6]
            year = parsedLine[9]
            medal = parsedLine[14]
            if year == Year:
                if medal != 'NA':
                    if country in totalInfo:
                        if medal in totalInfo[country]:
                            totalInfo[country][medal]+=1
                        else:
                            totalInfo[country][medal]=1
                    else:
                        totalInfo[country]=dict()
                        totalInfo[country][medal] = 1
            line = file.readline()
    
    for countryName, results in totalInfo.items():
        print(f'{countryName}')
        for medal, count in results.items():
            print(f'\t{medal} - {count}')


def overall(overall_dict):
    with args.infile as file:
        next_line = file.readline()
        while next_line != '':
            next_line = file.readline()
            olympic_info = next_line.split('\t')
            for i in overall_dict:
                if next_line != '':
                    if i == olympic_info[6] and olympic_info[14] != 'NA\n':
                        overall_dict[i] = overall_dict[i] + olympic_info[9] + ';'
        for i in overall_dict:
            year_max = 0
            medals_count = 0
            years = overall_dict[i].split(';')
            for j in range(1910,2023):
                if years.count(str(j)) > medals_count: 
                    medals_count = years.count(str(j))
                    year_max = j
            print(i,year_max, medals_count)  
    return overall_dict

def interactive():
    while True:
        print('Введіть назву країни або код(exit для виходу):')
        value =  input('->')
        if value=='exit':
            break
        
        countryTotalInfo=dict()
        with args.infile as file:
            line = file.readline()
            while line:
                line = line[:-1]
                parsedLine = line.split('\t')
                country = parsedLine[6]
                code = parsedLine[7]
                year = parsedLine[9]
                place = parsedLine[11]
                medal = parsedLine[14]
                
                if value == country or value == code:
                    if year not in countryTotalInfo:
                        countryTotalInfo[year]=dict()
                        countryTotalInfo[year]['Gold'] = 0
                        countryTotalInfo[year]['Silver'] = 0
                        countryTotalInfo[year]['Bronze'] = 0
                        countryTotalInfo[year]['total'] = 0
                    countryTotalInfo[year]['place']=place
                    if medal != 'NA':
                        countryTotalInfo[year]['total'] += 1
                        if medal in countryTotalInfo[year]:
                            countryTotalInfo[year][medal]+=1
                        else:
                            countryTotalInfo[year][medal]=1

                line = file.readline()
        
        countryTotalInfo=dict(sorted(countryTotalInfo.items()))

        theFirstYear = 3000
        theFirstYearPlace = ''

        theBest = 0
        theBestYear = 0
        theWorst = 99999
        theWorstYear = 0

        totalMedals={
            'Gold':0,
            'Silver':0,
            'Bronze':0,
            'total':0
        }
        counter = 0
        
        for y, results in countryTotalInfo.items():
            if theFirstYear > int(y):
                theFirstYear = int(y)
                theFirstYearPlace = results['place']
                
            print(f"{y}  - {results['place']}")
            for medal , count in results.items():
                print(f"\t{medal}  - {count}")
                if medal!='place':
                    totalMedals[medal]+=count
            if results['total'] > theBest:
                theBest = results['total']
                theBestYear = y
            if results['total'] < theWorst:
                theWorst = results['total']
                theWorstYear = y

            counter+=1

        print(f'Всередньому на кожній олімпіаді: ')
        print(f'золотих :{totalMedals["Gold"]/counter}')
        print(f'срібних :{totalMedals["Silver"]/counter}')
        print(f'бронзових :{totalMedals["Bronze"]/counter}')
        print(f'загально :{totalMedals["total"]/counter}')

        print(f'найгірший рік {theWorstYear} - {theWorst} медалей')
        print(f'найкращий рік {theBestYear} - {theBest} медалей')

        print(f'перший рік {theFirstYear} - {theFirstYearPlace}')


args = parser.parse_args()

    
if args.interactive is not None:
    a = interactive()
    
if args.total is not None:
    total(args.total[0])

if args.medals is not None:     
    sport_info = medals(args.medals[0], args.medals[1])

if args.output is not None:
    names = sport_info['Name_disc_medal'].split(';')
    for name in names:
        args.output.writelines(name)
    args.output.writelines(str(sport_info['Gold'])+' '+str(sport_info['Silver'])+' '+str(sport_info['Bronze'])) 

if args.overall is not None:
    overall_dict = dict.fromkeys(args.overall,'')
    a = overall(overall_dict)