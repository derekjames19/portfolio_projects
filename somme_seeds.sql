/*
Somme Seed Data Exploration by Derek Hofland
Written on 2022/02/06; Last updated on 2022/02/07

Somme Woods and Somme Prairie Grove are forest preserves that volunteers have
been working to restore for almost 40 years. Volunteers pick seeds of native
plants and remove invasive brush in an effort to restore the landscape to its
native state. I volunteered with the Somme Preserves regularly from 2017 to
2020 and helped the stewards of the site organize some of their information by
creating spreadsheets of seed-picking data. I recently uploaded some of this
information into SQL Server so that I could practice writing queries and
demonstrate my skills in SQL.
*/

--explore the genetic diversity of species by seeing the size of plant families

SELECT [Scientific Name]
	, Family
	, COUNT(Family) OVER (PARTITION BY Family) AS SizeOfFamily
FROM FloraOfTheChicagoRegion
ORDER BY SizeOfFamily



--compare the conservation values of plants when grouped by their wetness value

SELECT 'Chicago Region' AS Source
	, W AS WetnessValue
	, AVG(C) AS AvgConservationValue
FROM FloraOfTheChicagoRegion
GROUP BY W

UNION

SELECT 'Somme' AS Source
	, W AS WetnessValue
	, AVG(C) AS AvgConservationValue
FROM FloraOfSomme
GROUP BY W



--find species names from seed lists that are not in the master list

SELECT '2019' AS Year
	, [SCIENTIFIC NAME] AS ScientificName
FROM FallSeeds2019
WHERE [SCIENTIFIC NAME] NOT IN
(
	SELECT [Scientific Name]
	FROM FloraOfTheChicagoRegion
)

UNION

SELECT '2020' AS Year
	, [SCIENTIFIC NAME] AS ScientificName
FROM FallSeeds2020
WHERE [SCIENTIFIC NAME] NOT IN
(
	SELECT [Scientific Name]
	FROM FloraOfTheChicagoRegion
)



--list the species in the 2020 mesic open seed mix

SELECT C AS ConservationValue
	, [SCIENTIFIC NAME] AS ScientificName
	, [COMMON NAME] AS CommonName
FROM FallSeeds2020
WHERE MO IS NOT NULL
ORDER BY ScientificName



--compare the amount of each seed picked in 2019 vs 2020

SELECT f19.C AS ConservationValue
	, f19.[SCIENTIFIC NAME] AS ScientificName
	, CONCAT(f19.[AMOUNT FROM SOMME], ' ', f19.UNIT) AS AmountIn2019
	, CONCAT(f20.[AMOUNT FROM SOMME], ' ', f20.UNIT) AS AmountIn2020
FROM FallSeeds2019 f19
JOIN FallSeeds2020 f20
	ON f19.[SCIENTIFIC NAME] = f20.[SCIENTIFIC NAME]
ORDER BY ConservationValue



--explore properties of plants when grouped by plant structure

SELECT (CASE
		WHEN Native = 'Y' THEN 'Native'
		WHEN Native = 'N' THEN 'Non-native'
		ELSE 'Unknown'
	END) AS NativeStatus
	, Physiognomy
	, COUNT(Physiognomy) AS SpeciesCount
	, ROUND(AVG(C), 2) AS AvgConservationValue
FROM FloraOfSomme
WHERE Physiognomy <> 'Crypt'
GROUP BY Physiognomy, Native
ORDER BY AvgConservationValue