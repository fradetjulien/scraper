import click
import pycountry
import csv
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

# Convert the Data received into a new CSV file
def saveResultsToCSV(results):
    with open('results.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for result in results:
            filewriter.writerow(result)
    return

# Create a new instance of the Chrome driver and go to the WITS website, then configure the search
def loadData(driver, isocode):
    try:
        driver.get("https://wits.worldbank.org/CountryProfile/en/Country/" + isocode + "/Year/2017/TradeFlow/Export/Partner/by-country/Product/Total")
    except:
        print("Error while loading data.")
        raise
    return (driver)

# Get the top 4 countries
def getTopCountries(driver, isocode):
    topCountries = []
    i = 0
    while (i < 4):
        path = "//div[@id='row" + str(i) + "jqx-ProductGrid']"
        try:
            all_data = driver.find_elements_by_xpath(path)
            for data in all_data:
                topCountries.append(addToList(data))
            i = i + 1
        except:
            print("Error while getting data.")
            break
    return (topCountries)

# Convert the country name into an ISO Code
def convertToIsoCode(countryName):
    try:
        isoCode = pycountry.countries.get(name=countryName).alpha_3
    except:
        print("Impossible to convert this country name into an ISO Code.")
        return (countryName)
    return (isoCode)

# Round the total value
def roundedValue(number):
    try:
        totalValue = number.split(',')
        roundedValue = totalValue[0]
    except:
        print("Failed while rounding the total value.")
        return (number)
    roundedValue = roundedValue + "B"
    return (roundedValue)

# Add the data into a list
def addToList(data):
    try:
        country = data.text.splitlines()
        country.pop()
    except:
        print("Error while adding data.")
        raise
    country[0] = convertToIsoCode(country[0])
    country[1] = roundedValue(country[1])
    return country

# Display final results
def displayResults(topCountries):
    try:
        for country in topCountries:
            print(country[0], country[1])
    except:
        print("Results no found.")
        raise
    return

@click.group()
def cli():
    """Scrapper Project"""

@cli.group('imports')
def imports():
    """Commands for Imports"""

@imports.command('country')
@click.option('--save', default=None, help="Save Data to a CSV file.", is_flag=True)
@click.argument('isocode')
def displayImportsByCountry(save, isocode):
    "Display major imports of a country"
    driver = webdriver.Chrome(executable_path=".//chromedriver")
    driver = loadData(driver, isocode)
    topCountries = getTopCountries(driver, isocode)
    displayResults(topCountries)
    if save:
        saveResultsToCSV(topCountries)
    return (topCountries)

@imports.command('all')
@click.option('--save', default=None, help="Save Data to a CSV file.", is_flag=True)
def listImportsOfFiveCountry(save):
    "Display major imports of 5 random country."
    driver = webdriver.Chrome(executable_path=".//chromedriver")
    isoCode = []
    for country in pycountry.countries:
        isoCode.append(country.alpha_3)
    i = 0
    allResults = []
    while (i < 5):
        x = random.randint(1,248)
        driver = loadData(driver, isoCode[x])
        allResults.append(getTopCountries(driver, isoCode[x]))
        i = i + 1
    if save:
        saveResultsToCSV(allResults)
    print(allResults)
    return

if __name__ == '__main__':
    cli()