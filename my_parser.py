from requests_html import HTMLSession

class Parser():


    def __init__(self, place):
        self.events = []
        self.session = HTMLSession()
        processed_place = self.process_query(place)
        if "dintorni" in processed_place:
            processed_place = processed_place.replace("dintorni","").strip()
            if " " in processed_place:
            #Decide between "-" and "" to replace spaces where the place's name has multiple words
                self.request = self.session.get("https://iltaccodibacco.it/{}/".format(processed_place.replace(" ","-")))
                for h in self.request.html.find("h2"):
                    if h.text == "OPS!":
                        self.request = self.session.get("https://iltaccodibacco.it/{}/".format(processed_place.replace(" ","")))
                        break
            else:
                self.request = self.session.get("https://iltaccodibacco.it/{}/".format(processed_place))
        else:
            self.request = self.session.get("https://iltaccodibacco.it/?md=Ricerca&des_ricerca={}&c_all=1"
                .format(processed_place.strip().replace(" ","+")))


    def getEvents(self):
        events = self.request.html.find('div')
        for event in events:
            if 'class' in event.attrs:
                if list(event.attrs['class'])[0]=='evento-normale':
                    event_details = {}
                    divs = event.find('div')
                    for div in divs:
                        if 'class' in div.attrs:
                            class_type = list(div.attrs['class'])[0]
                            if class_type == 'evento-img':
                                a = div.find('a')[0]
                                img = div.find('img')[0]
                                event_details['name'] = img.attrs['alt']
                                event_details['link'] = a.attrs['href']
                                event_details['img'] = img.attrs['src']
                            elif class_type == 'evento-data':
                                event_details['place'] = div.text
                            elif class_type == 'testa':
                                event_details['date'] = self.parse_date(div.text)
                    self.events.append(event_details)
        return self.events


    def process_query(self, place):
        return ' '.join([elem.strip() for elem in place.lower().split(' ') if elem.strip() != ''])

    def parse_date(self, date_str):
        if "al" in date_str:
            words = date_str.replace(",","").replace("-","").replace("ll'", "l ").split("al")
            return "{} - {}".format(words[1].strip(), " ".join(words[2].strip().split(" ")[:3]))
        else:
            return " ".join(date_str.split(" ")[1:])
