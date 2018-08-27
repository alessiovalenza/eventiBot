from requests_html import HTMLSession


class Parser:

    def __init__(self, place):
        self.events = []
        self.session = HTMLSession()
        processed_place = self.process_query(place)
        # Decide between "-" and "" to replace spaces where the place's name has multiple words
        if "dintorni" in processed_place:
            processed_place = processed_place.replace("dintorni", "").strip()
            if " " in processed_place:
                self.request = self.session.get("https://iltaccodibacco.it/{}/"
                                                .format(processed_place.replace(" ", "-")))
                for h in self.request.html.find("h2"):
                    if h.text == "OPS!":
                        self.request = self.session.get("https://iltaccodibacco.it/{}/"
                                                        .format(processed_place.replace(" ", "")))
                        break
            else:
                self.request = self.session.get("https://iltaccodibacco.it/{}/".format(processed_place))
        else:
            self.request = self.session.get("https://iltaccodibacco.it/?md=Ricerca&des_ricerca={}&c_all=1"
                                            .format(processed_place.strip().replace(" ", "+")))

    def getEvents(self):
        links = self.request.html.find('a')
        already_found = []
        for link in links:
            if 'name' in link.attrs and link.attrs['name'].isnumeric() and len(link.text)>0:
                if link.attrs['href'] not in already_found:
                    already_found.append(link.attrs['href'])
                    self.events.append({'name':link.text, 'link':link.attrs['href']})
        return self.events

    def process_query(self, place):
        return ' '.join([elem.strip() for elem in place.lower().split(' ') if elem.strip() != ''])
