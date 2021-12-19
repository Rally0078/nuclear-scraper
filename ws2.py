import sys
import re
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
        for self.all_tag in self.all_tags:
            self.texts = self.all_tag.findAll(text=True)
            self.visible_texts = filter(self._tag_visible, self.texts)
            for t in self.visible_texts:
                self.text = t.strip()
                self.list_text.append(self.text)
        
        for i in self.list_text:
            self.list_text_dict = []
            if i in categories:
                for j in self.list_text[self.list_text.index(i)+1:]:
                    if j in categories:
                        break
                    else:
                        self.list_text_dict.append(j)
                self.cat_dictionary[i]=self.list_text_dict
        
    def _tag_visible(self,element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True
    
    def print_cat(self):
        print(self.date_object);
        self.now = datetime.now(timezone.utc)
        print(self.now-self.date_object);
        for k, v in self.cat_dictionary.items():
            # if k == 'Uploaded:':
                # self.no_of_days = (self.now-self.date_object).days
                # self.no_of_seconds = (self.now-self.date_object).seconds
                # if self.no_of_days >= 365:
                    # self.no_of_years = int(self.no_of_days/365)
                    # self.no_of_days = self.no_of_days % 365
                    # if self.no_of_days >= (365/12):
                        # self.no_of_months = int(self.no_of_days/(365/12))
                        # self.no_of_days = int(self.no_of_days % (365/12))
                        # self.time_string = str(
                            # self.no_of_years)+" years, "+str(self.no_of_months)+" months, "+str(self.no_of_days)+" days ago"
                # elif self.no_of_days < 365:
                    # if self.no_of_days >= (365/12):
                        # self.no_of_months = int(self.no_of_days/(365/12))
                        # self.no_of_days = int(self.no_of_days % (365/12))
                        # self.time_string = str(self.no_of_months)+" months, " + \
                            # str(self.no_of_days)+" days ago"
                    # if self.no_of_days < (365/12):
                        # if self.no_of_seconds >= 86400:
                            # # self.no_of_seconds=int(self.no_of_seconds/86400)
                            # no_of_hours = int(self.no_of_seconds/3600)
                            # self.time_string = str(self.no_of_days)+" days, " + \
                                # str(no_of_hours)+" hours ago"
                        # else:
                            # no_of_hours = int(no_of_seconds/3600)
                            # seconds_elapsed = int(no_of_seconds % 3600)
                            # no_of_minutes = int(seconds_elapsed/60)
                            # self.time_string = str(no_of_hours)+" hours, " + \
                                # str(no_of_minutes)+" minutes ago"
                # print(k+" "+self.time_string)
                # break
            
            self.string_list = []
            self.string = ''
    
            for i in v:
                if k == 'Pages:':
                    self.string_list.append(i)
                elif k == 'Uploaded:':
                    self.string_list.append(str(self.now-self.date_object))
                else:
                    self.exp = re.findall(r"(\d+K|\d+)",i)
                    if not self.exp:
                        self.string_list.append(i)
                           
            for i in self.string_list:
                if self.string_list.index(i) == 0:
                    self.string = self.string+" "+i
                if self.string_list.index(i) != 0:
                    self.string = self.string+", "+i
                    
            self.cat_dictionary[k] = self.string    
            print(f"{k}{self.cat_dictionary[k]}")
        if(self.diag_flag == 'd'):
            print(f"\nDiagnostics:")
            print(self.date_object)
      

#Runs standalone too for debugging purposes        
if __name__ == "__main__":
    n_code = (input('Enter nuclear code:'))
    if(len(sys.argv) == 1):
        sauce = NuclearScraper(n_code)
    else:
        sauce = NuclearScraper(n_code,sys.argv[1])
    sauce.print_cat()
