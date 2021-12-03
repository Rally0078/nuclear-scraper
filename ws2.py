import sys
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
from datetime import datetime, timezone


class NuclearScraper:
    def __init__(self,number,diag_flag=None):
        self.number = number
        self.diag_flag = diag_flag
        categories = ['Title:','Parodies:', 'Characters:', 'Tags:', 'Artists:',
                  'Groups:', 'Languages:', 'Categories:', 'Pages:', 'Uploaded:']
        self.cat_dictionary = {}
        for category in categories:
            self.cat_dictionary[category] = []

        self.n_url = 'https://nhentai.net/g/'+str(self.number)
        self.html_text = requests.get(self.n_url).text
        self.soup = BeautifulSoup(self.html_text, 'html.parser')


        self.all_tags = self.soup.find_all('div', attrs={'class': 'tag-container field-name'})
        self.name_tags = self.soup.find_all('meta', attrs={'property': 'og:title'})
        self.time_tag = self.soup.find_all('time')
        self.cat_dictionary['Title:']=[self.name_tags[0].get('content')]

        for tim in self.time_tag:
            self.date_time = tim.get('datetime')  # gets date and time of upload
                                            # 2014-06-28T22:37:00.682160+00:00 (sample date)
            self.date_object = datetime.strptime(self.date_time, "%Y-%m-%dT%H:%M:%S.%f%z")
           
        self.list_text = []
        for all_tag in self.all_tags:
            self.texts = all_tag.findAll(text=True)
            self.visible_texts = filter(self._tag_visible, self.texts)
            for t in self.visible_texts:
                self.text = t.strip()
                self.list_text.append(self.text)
        
        for i in range(0, len(self.list_text)):
            if self.list_text[i] in categories:
                self.cat = self.list_text[i]
                self.flag_end_reached = False
                i = i+1
                self.list_text_dict = []
                while self.flag_end_reached is not True:
                    if i == len(self.list_text):
                        break
                    if self.list_text[i] in categories:
                        self.flag_end_reached = True
                        break
                    self.list_text_dict.append(self.list_text[i])
                    i = i+1
                self.cat_dictionary[self.cat] = self.list_text_dict
        #return cat_dictionary,date_object   no need to return
    def _tag_visible(self,element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True
    
    def print_cat(self):
        now = datetime.now(timezone.utc)
        for k, v in self.cat_dictionary.items():
            if k == 'Uploaded:':
                no_of_days = (now-self.date_object).days
                no_of_seconds = (now-self.date_object).seconds
                if no_of_days >= 365:
                    no_of_years = int(no_of_days/365)
                    no_of_days = no_of_days % 365
                    if no_of_days >= (365/12):
                        no_of_months = int(no_of_days/(365/12))
                        no_of_days = int(no_of_days % (365/12))
                        time_string = str(
                            no_of_years)+" years, "+str(no_of_months)+" months, "+str(no_of_days)+" days ago"
                elif no_of_days < 365:
                    if no_of_days >= (365/12):
                        no_of_months = int(no_of_days/(365/12))
                        no_of_days = int(no_of_days % (365/12))
                        time_string = str(no_of_months)+" months, " + \
                            str(no_of_days)+" days ago"
                    if no_of_days < (365/12):
                        if no_of_seconds >= 86400:
                            # no_of_seconds=int(no_of_seconds/86400)
                            no_of_hours = int(no_of_seconds/3600)
                            time_string = str(no_of_days)+" days, " + \
                                str(no_of_hours)+" hours ago"
                        else:
                            no_of_hours = int(no_of_seconds/3600)
                            seconds_elapsed = int(no_of_seconds % 3600)
                            no_of_minutes = int(seconds_elapsed/60)
                            time_string = str(no_of_hours)+" hours, " + \
                                str(no_of_minutes)+" minutes ago"
                print(k+" "+time_string)
                break
            string = ''
            for i in range(0, len(v)):
                if(i % 2) == 1:
                    continue
                if i == 0:
                    string = string+" "+v[i]
                if i != 0:
                    string = string+", "+v[i]
            print(k+string)
        if(self.diag_flag == 'd'):
            print(self.date_object)
      

#Runs standalone too for debugging purposes        
if __name__ == "__main__":
    n_code = (input('Enter nuclear code:'))
    if(len(sys.argv) == 1):
        sauce = NuclearScraper(n_code)
    else:
        sauce = NuclearScraper(n_code,sys.argv[1])
    sauce.print_cat()
