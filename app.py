"""Corona Virus (COVID-19) Stats In Iran \n Made by Sam Abbasi and Iman Sedgh"""

from bs4 import BeautifulSoup
import requests


class Data:
    def __init__(self):
        self.url = "https://www.worldometers.info/coronavirus/country/iran/"

    def get_data(self):
        page = requests.get('https://www.worldometers.info/coronavirus/country/iran/')
        soup = BeautifulSoup(page.content,'html.parser')
        selected = soup.select("#maincounter-wrap span")
        number_list = [ item.text for item in selected ]
        return number_list 

numbers = Data().get_data()

print ("Number Of Corona Virus Cases:  " +  numbers[0])
print("Number Of Corona Virus Deaths: " + numbers[1])
print("Number Of Corona Virus Recovers: " + numbers[2])
