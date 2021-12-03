import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
from datetime import datetime, timezone


def _tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def print_cat(dictionary,date_object):
    now = datetime.now(timezone.utc)
    for k, v in dictionary.items():
        if k == 'Uploaded:':
            no_of_days = (now-date_object).days
            no_of_seconds = (now-date_object).seconds
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
        # ((?:(?!k)(?!K)[a-zA-Z]))
        for i in range(0, len(v)):
            if(i % 2) == 1:
                continue
            if i == 0:
                string = string+" "+v[i]
            if i != 0:
                string = string+", "+v[i]
        print(k+string)

def get_tag(n_code):
    categories = ['Title:','Parodies:', 'Characters:', 'Tags:', 'Artists:',
                  'Groups:', 'Languages:', 'Categories:', 'Pages:', 'Uploaded:']
    cat_dictionary = {}
    for category in categories:
        cat_dictionary[category] = []

    n_url = 'https://nhentai.net/g/'+str(n_code)
    html_text = requests.get(n_url).text
    soup = BeautifulSoup(html_text, 'html.parser')


    all_tags = soup.find_all('div', attrs={'class': 'tag-container field-name'})
    name_tags = soup.find_all('meta', attrs={'property': 'og:title'})
    time_tag = soup.find_all('time')
    cat_dictionary['Title:']=[name_tags[0].get('content')]

    for tim in time_tag:
        date_time = tim.get('datetime')  # gets date and time of upload
                                        # 2014-06-28T22:37:00.682160+00:00 (sample date)
        date_object = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S.%f%z")
        #now = datetime.now(timezone.utc) #not needed here
                            # delta_time=now-date_object
        #print(name_tags[0].get('content'))  # gets title, not needed anymore


    list_text = []
    for all_tag in all_tags:
        texts = all_tag.findAll(text=True)
        visible_texts = filter(_tag_visible, texts)
        for t in visible_texts:
            text = t.strip()
            list_text.append(text)
    
    for i in range(0, len(list_text)):
        if list_text[i] in categories:
            cat = list_text[i]
            flag_end_reached = False
            i = i+1
            list_text_dict = []
            while flag_end_reached is not True:
                if i == len(list_text):
                    break
                if list_text[i] in categories:
                    flag_end_reached = True
                    break
                list_text_dict.append(list_text[i])
                i = i+1
            cat_dictionary[cat] = list_text_dict
    return cat_dictionary,date_object
    #_print_cat(cat_dictionary,now,date_object)

if __name__ == "__main__":
    n_code = (input('Enter nuclear code:'))
    raw_dict,date = get_tag(n_code)
    print(date)
    print_cat(raw_dict,date)
