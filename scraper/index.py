'''
Scraper project
'''
import csv
import random
import click
import pycountry
from selenium import webdriver

def save_results_to_csv(results):
    '''
    Convert the Data received into a new CSV file
    '''
    try:
        with open('results.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|',
                                    quoting=csv.QUOTE_MINIMAL)
            for result in results:
                filewriter.writerow(result)
    except IndexError:
        print("Sorry, we were unable to create the file results.")
    except csv.Error:
        print("Sorry, we were unable to create the file results.")

def generate_iso_code():
    '''
    Generate a list of valid iso codes
    '''
    iso_code = []
    try:
        for country in pycountry.countries:
            iso_code.append(country.alpha_3)
    except:
        print("Failure during iso codes generation.")
        raise
    return iso_code

def display_all_results(top_countries, iso_code):
    '''
    Display all 5 final results
    '''
    print(iso_code)
    if top_countries:
        display_results(top_countries)
    print('\n')

def display_results(top_countries):
    '''
    Display final results
    '''
    try:
        for country in top_countries:
            print(country[0], country[1])
    except IndexError:
        print("Results not found.")

def round_up_value(number):
    '''
    Round up the total value
    '''
    try:
        total_value = number.split(',')
        rounded_value = total_value[0]
    except ValueError:
        print("Failed while rounding the total value.")
        return number
    rounded_value = rounded_value + "B"
    return rounded_value

def convert_to_iso_code(country_name):
    '''
    Convert the country name into an ISO Code
    '''
    try:
        iso_code = pycountry.countries.get(name=country_name).alpha_3
    except:
        return country_name
    return iso_code

def add_to_list(data):
    '''
    Add the data into a list
    '''
    try:
        country = data.text.splitlines()
        country.pop()
    except:
        print("Error while adding data.")
        raise
    country[0] = convert_to_iso_code(country[0])
    country[1] = round_up_value(country[1])
    return country

def get_top_countries(driver):
    '''
    Get the top 4 countries
    '''
    top_countries = []
    i = 0
    while i < 4:
        path = "//div[@id='row" + str(i) + "jqx-ProductGrid']"
        try:
            all_data = driver.find_elements_by_xpath(path)
            for data in all_data:
                top_countries.append(add_to_list(data))
            i = i + 1
        except IndexError:
            print("Error while getting data.")
            break
    return top_countries

def load_data(driver, iso_code):
    """
    Create a new instance of the Chrome driver and go to the WITS website, then configure the search
    """
    try:
        driver.get("https://wits.worldbank.org/CountryProfile/en/Country/"
                   + iso_code + "/Year/2017/TradeFlow/Export/Partner/by-country/Product/Total")
    except:
        print("Error while loading data.")
        raise
    return driver

@click.group()
def cli():
    '''
    Scrapper Project
    '''

@cli.group('imports')
def imports():
    '''
    Commands for Imports
    '''

@imports.command('country')
@click.option('--save', default=None, help="Save Data into a CSV file.", is_flag=True)
@click.argument('isocode')
def display_imports_by_country(save, isocode):
    '''
    Display major imports of a country
    '''
    driver = webdriver.Chrome(executable_path=".//chromedriver")
    driver = load_data(driver, isocode)
    top_countries = get_top_countries(driver)
    display_results(top_countries)
    if save:
        save_results_to_csv(top_countries)

@imports.command('all')
@click.option('--save', default=None, help="Save Data to a CSV file.", is_flag=True)
def list_imports_of_five_country(save):
    '''
    Display major imports of 5 random country.
    '''
    driver = webdriver.Chrome(executable_path=".//chromedriver")
    iso_code = generate_iso_code()
    i = 0
    all_results = []
    while i < 5:
        random_value = random.randint(1, 248)
        driver = load_data(driver, iso_code[random_value])
        top_countries = get_top_countries(driver)
        all_results.append(top_countries)
        display_all_results(top_countries, iso_code[random_value])
        top_countries = top_countries.clear()
        i = i + 1
    if save:
        save_results_to_csv(all_results)

if __name__ == '__main__':
    cli()
    print("test4")
