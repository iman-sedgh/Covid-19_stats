"""Corona Virus (COVID-19) Stats In Iran \n Made by Sam Abbasi and Iman Sedgh"""

from bs4 import BeautifulSoup
import requests


class Data:
    def __init__(self):
        self.url = "https://www.worldometers.info/coronavirus/country/iran/"
        
    def scrape_data(self):
        page = requests.get('https://www.worldometers.info/coronavirus/country/iran/')
        soup = BeautifulSoup(page.content,'html.parser')
        selected = soup.select("#maincounter-wrap span")
        self.number_list = [ item.text for item in selected ]
         
    def get_data(self):
        return self.number_list

if __name__ == "__main__":
    numbers = Data()
    numbers.scrape_data()
    numbers = numbers.get_data()

    print ("Number Of Corona Virus Cases:  " +  numbers[0])
    print("Number Of Corona Virus Deaths: " + numbers[1])
    print("Number Of Corona Virus Recovers: " + numbers[2])
