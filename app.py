print ("Corona Virus (COVID-19) Stats In Iran \n Made by Sam Abbasi and Iman Sedgh")
from bs4 import BeautifulSoup
import requests
page = requests.get('https://www.worldometers.info/coronavirus/country/iran/')
soup = BeautifulSoup(page.content,'html.parser')
lst = soup.find_all(id='maincounter-wrap')
div_cases= lst[0]
span_cases= div_cases.find('span')
number_cases = span_cases.get_text()


div_death = lst[1]
span_death = div_death.find('span')
number_death = span_death.get_text()



div_recover = lst[2]
span_recover = div_recover.find('span')
number_recover = span_recover.get_text()



print ("Number Of Corona Virus Cases:  " +  number_recover)
print("Number Of Corona Virus Deaths: " + number_cases)
print("Number Of Corona Virus Recovers: " + number_death)
