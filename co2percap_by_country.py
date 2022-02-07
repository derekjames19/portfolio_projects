#import and parse the emissions file from OWID
emissions = open("OWID_cleaned_co2_data.csv")
emissions = emissions.read()
emissions = emissions.split('\n')
emissions = [item.split(',') for item in emissions]

#print the column headers for the emissions file
print("EMISSIONS COLUMN HEADERS")
for i in range(len(emissions[0])):
    print(i, emissions[0][i])
print()

#import and parse the region file from the UN
regions = open("UN_regions_and_continents.csv")
regions = regions.read()
regions = regions.split('\n')
regions = [item.split(',') for item in regions]

#print the column headers for the region file
print("REGION COLUMN HEADERS")
for i in range(len(regions[0])):
    print(i, regions[0][i])
print()

#extract regions from the file and create objects to store the information
isoToRegion = {}
countryDict = {}
for i in range(1, len(regions)):
    isoToRegion[regions[i][0]] = regions[i]
    countryDict[regions[i][0]] = {}
sortedCodes = [code for code in isoToRegion if isoToRegion[code][2] == '1']
sortedCodes.sort()

#eliminate lines with unwanted data and store remaining lines
for i in range(1, len(emissions)):
    iso = emissions[i][0]
    if len(iso) != 3:
        continue
    if isoToRegion[iso][2] == '0':
        continue
    year = int(emissions[i][2])
    if year < 1800:
        continue
    country = isoToRegion[iso][1]
    continent = isoToRegion[iso][4]
    co2 = emissions[i][3]
    population = emissions[i][53]
    if co2 == '' or population == '' or float(co2) == 0:
        continue
    co2 = str(int(float(co2) * 10**6))
    co2percap = emissions[i][8]
    if co2percap == '':
        co2percap = str(round(int(co2) / int(population), 3))
    if float(co2percap) == 0:
        continue
    infoString = country + ',' + continent + ','
    infoString+= co2 + ',' + population + ',' + co2percap
    countryDict[iso][year] = infoString

#export the calculated information
infoOut = open("co2percap_by_country.csv", 'w')
infoOut.write("ISO Code,Year,Country,Continent,CO2,Population,CO2 Per Capita")
for iso in sortedCodes:
    foundFirst = False
    lastValidEntry = ''
    for year in range(1800, 2021):
        if year in countryDict[iso]:
            foundFirst = True
            lastValidEntry = countryDict[iso][year]
        if not foundFirst:
            continue
        nextLine = '\n'
        nextLine+= iso + ','
        nextLine+= str(year) + ','
        nextLine+= lastValidEntry
        infoOut.write(nextLine)
infoOut.close()
