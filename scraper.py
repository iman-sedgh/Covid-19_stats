"""Corona Virus (COVID-19) Stats In Iran \n Made by Sam Abbasi and Iman Sedgh"""

from bs4 import BeautifulSoup
import requests


class Data:
    def __init__(self,API_KEY,PROJECT_TOKEN):
        self.url = f"http://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/"
        self.api_key = API_KEY
        
    def run(self):
        status = requests.post(self.url+ "run" ,params={"api_key":self.api_key})
        if(status.status_code == 200):
            return True
        return False

    def refresh_data(self):
        newdata = requests.get(self.url + "last_ready_run/data" , params={"api_key":self.api_key} , verify = False)
        if(newdata.status_code == 200):
            self.data = newdata.json()
            self.make_total_data()
            self.make_country_data()
            

    def get_full_data(self):
        return self.data

    def get_total_data(self):
        """ return a dict countain total : 
                Coronavirus Cases
                Deaths
                Revocered
        """
        return self.total_data
    def get_country_data(self,country_name):
        """ receive a country name and return a dict contain :
                Coronavirus Cases
                Deaths
                Revocered
            numbers of that country 
            {"country_name": { 
                "total": INT ,
                "death": INT ,
                "recovered": INT ,
            } }
    """
        try:
            country = self.country_data[country_name.lower()]
            return country
        except :
            pass
        return False
    
    def make_total_data(self):
        """make a Dict that contains:
            Total Cases 
            Total Deaths
            Total Recovered
            {'coronavirus cases:': 'number', 'deaths:': 'number', 'recovered:': 'number'}
        """
        total_data =  {}
        raw_data = self.data['total']
        for item in raw_data : 
            total_data.update( { item['name'].lower() : item['number'] } )
        
        self.total_data = total_data
    
    def make_country_data(self):
        """Makes a Dict that 
        keys are name of country
        values are dict contain :
            Coronavirus Cases
            Deaths
            Revocered  for each country
            {"country_name": { 
                "total": INT ,
                "death": INT ,
                "recovered": INT ,
            } 
                }
        """
        total_country = {}
        raw_data = self.data['country']
        for item in raw_data :
            try:
                tmp_country = { 'total': item['total'] , 'death':item['death'], 'recovered': item['recovered']}
                total_country.update( {item['name'].lower() : tmp_country } )
            except:
                pass
        self.country_data = total_country


        

if __name__ == "__main__":
    PROJECT_TOKEN = "tPwDTyxPRMD6"
    API_KEY = "tT3y7qX1U9zq"
    data = Data(API_KEY,PROJECT_TOKEN)
    data.refresh_data()
    #import pdb; pdb.set_trace()
    numbers = data.get_country_data("Iran")
    numbers = data.get_full_data()
    numbers = data.get_total_data()
    exit()
    print(numbers)
    print ("Number Of Corona Virus Cases:  " +  numbers[0])
    print("Number Of Corona Virus Deaths: " + numbers[1])
    print("Number Of Corona Virus Recovers: " + numbers[2])
