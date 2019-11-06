import click
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

# Convert the Data received into a new CSV file.
def convertDataToCSV():
    print("Data Saved")
    return

# Create a new instance of the Chrome driver and go to the WITS website
def setupInstance():
    driver = webdriver.Chrome(executable_path=".//chromedriver")
    driver.get("https://wits.worldbank.org/CountryProfile/en/Country/ARG/Year/2017/TradeFlow/Export/Partner/ All/Product/Total")
    return (driver)

# Fill the form present in the page corresponding to the export of the Country selected in 2017
def setupSearch(driver):
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID,'selectedCountryRegion')))
    element = driver.find_element_by_id("selectedCountryRegion").click()
    element = wait.until(EC.element_to_be_clickable((By.ID,'byCountry_country_dropdown')))
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
    instance = setupInstance()
    setupSearch(instance)
    instance.quit()
    return

@imports.command('all')
@click.option('--save', default=None, help="Save Data to a CSV file.", is_flag=True)
def listImportsOfFiveCountry(save):
    "Display major imports of 5 random country."
    if save:
        convertDataToCSV()
    return

if __name__ == '__main__':
    cli()