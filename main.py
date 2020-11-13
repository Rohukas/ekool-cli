# Autor: Robi Rohumaa
# 
# Programmi abil saab vaadata eKooli teateid/hindeid ning näha kodutöid.
# Et programm töötaks tuleb sisestada enda eKooli e-mail ja parool line #47 ja #48'l olevatesse muutujatesse.
# 
# Programm annab kasutajale valiku 
# * Sisestades 'voog' või selle lühend 'v' saab kätte kõik hinded ja teated.
# * Sisestades 'kodutoo' või 'k' saab kätte kõik praeguse nädala kodutööd.
# 
# 
# eKool> voog 
# eKool> v 
# Sisestades selle saab ekraanil näha kõiki hindeid ja teated. Igal hindel/teatel on oma ID, mille järgi saab
# seda lähemalt vaadata.
# 
# eKool> voog [ID]
# eKool> v [ID]
# Et uurida näiteks teate, mille ID'ks on 1 sisu, peame sisestame programmi 'voog 1' või lühendi 'v 1'.
# See näitab meile lisainfot teate kohta. Sama nagu eKoolis teate peale vajutamine.
# 
# eKool> kodutoo
# Sisestades 'kodutoo' saame näha kõiki praeguse nädala kodutöid.
# 
# eKool> kodutoo [esmaspaev, teisipaev, kolmapaev, neljapaev, reede]
# eKool> k [e, t, k, n, r]
# Kui soovime näha näiteks kõiki esmaspäeva kodutöid, peame programmi sisestama kas 'kodutoo esmaspaev' või lühendi
# 'k e', milles k='kodutoo' ja e='esmaspaev'
# See toob meile koik esmaspaeva kodutood.
#
# eKool> kodutoo [esmaspaev, teisipaev, kolmapaev, neljapaev, reede] [ID]
# eKool> k [e, t, k, n, r] [ID]
# Sisestame päeva, mille kodutööd tahame ning selle päeval valitud kodutöö ID.
# Tagasi saame kogu kodutöö sisu koos manustega(kui need on olemas)

import requests
import hashlib
from datetime import datetime, timedelta
import json
from EKoolParser import EKoolParser
from cmd import Cmd
from termcolor import colored
from bs4 import BeautifulSoup
import warnings
import colorama 

# EKOOLI LOGIN
EMAIL = ''
PASSWORD = ''

# Windowsis ei näita muidu värve õigesti, kui ei kasuta colorama.init()
colorama.init()

# Ära näita warningut siis, kui eKooli kodutöö sisu on ainult link.
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

# Command-Line sarnane Class, mis küsib kogu aeg commande ja siis teeb midagi nende põhjal.
class EKoolLoop(Cmd):
    # Prompt, mida näidatakse iga commandi ees. 
    prompt = 'eKool> '

    # Konstruktor
    def __init__(self):
        # Kui tahame oma konstruktorit kasutada, peame ennem callima ka Cmd classi konstruktorit.
        super(EKoolLoop, self).__init__()

        # Loome eKooliga rääkiva classi instance. Selle kaudu saame võtta näiteks tunniplaani jne.
        self.ekool = EKoolParser(EMAIL, PASSWORD)


    # Command -> 'eKool> v'
    # Lühend sõnast 'voog' ning teeb täpselt sama asja, mida 'eKool> voog' command.
    def do_v(self,feedNumber):
        self.feed_handler(feedNumber=feedNumber)
    

    # Command -> 'eKool> k'
    # Lühend sõnast 'kodutoo' ning teeb täpselt sama asja, mida 'eKool> kodutoo' command.
    def do_k(self, line):
        # Kui on olemas argument, siis saada need kaasa kodutoo_handler meetodisse
        # args[0] on päev. On eeldatud, et kasutaja sisestab ühe järgnevast. 'e', 't', 'k', 'n', 'r', 'esmaspaev', 'teisipaev', 'kolmapaev',
        # 'neljapaev', 'reede'
        if line:
            args = line.split(' ')
            # Kui argumente on üle ühe, siis on sisestatud ka ilmselt kodutoo id, mida vaadata soovitakse. Saadame ka selle kaasa.
            if len(args) > 1:
                self.kodutoo_handler(args[0], args[1])
            else:
                # on soovitud kindla paeva kodutoid
                self.kodutoo_handler(day=args[0])
        else:
            # Vaata koiki kodutoid
            self.kodutoo_handler()

    def do_kodutoo(self,line):
        # Kui on olemas argument, siis saada need kaasa kodutoo_handler meetodisse
        # args[0] on päev. On eeldatud, et kasutaja sisestab ühe järgnevast. 'e', 't', 'k', 'n', 'r', 'esmaspaev', 'teisipaev', 'kolmapaev',
        # 'neljapaev', 'reede'
        if line:
            args = line.split(' ')
            # Kui argumente on üle ühe, siis on sisestatud ka ilmselt kodutoo id, mida vaadata soovitakse. Saadame ka selle kaasa.
            if len(args) > 1:
                self.kodutoo_handler(args[0], args[1])
            else:
                # on soovitud kindla paeva kodutoid
                self.kodutoo_handler(day=args[0])
        else:
            self.kodutoo_handler()

    # Meetod toob tagasi päeva järjekorranumbri nädalas, alustades nullist, kui anda sisse päeva sõne
    def get_day_from_str(self,dayStr):
        dayStr = dayStr.lower()
        if dayStr == "e" or dayStr == "esmaspäev" or dayStr == "esmaspaev":
            return 0
        if dayStr == "t" or dayStr == "teisipäev" or dayStr == "teisipaev":
            return 1
        if dayStr == "k" or dayStr == "kolmapäev" or dayStr == "kolmapaev":
            return 2
        if dayStr == "n" or dayStr == "neljapäev" or dayStr == "neljapaev":
            return 3
        if dayStr == "r" or dayStr == "reede":
            return 4
        return -1


    # Meetod prindib ekraanile hetkese päeva, kui anda 0'ist algav päeva id.
    # 0 -> esmaspaev
    # 1 -> teisipaev... jne
    def print_day_from_dayid(self, i):
        if i == 0:
            print(colored('Esmaspäev', "cyan"))
        elif i == 1:
            print(colored('Teisipäev', "cyan"))
        elif i == 2:
            print(colored('Kolmapäev', "cyan"))
        elif i == 3:
            print(colored('Neljapäev', "cyan"))
        elif i == 4:
            print(colored('Reede', "cyan"))

    # Tegeleb kodutööde ekraanile printimisega
    def kodutoo_handler (self, day=None, id=None):
        # Arvutame välja hetkese nädala esmaspäeva ja reede, et saade kodutöid selles vahemikus.
        now = datetime.now()
        monday = now - timedelta(days = now.weekday())
        friday = now - timedelta(days = now.weekday()) + timedelta(days=5)

        # Võtame selle nädala kodutööd.
        kodutood = self.ekool.get_assignments_for_timeframe(monday,friday)

        # Jagame kodutood päevade kaupa ära
        e = [t for t in kodutood.assignments if datetime.strptime(t.deadLine, '%d.%m.%Y').weekday() == 0]
        t = [t for t in kodutood.assignments if datetime.strptime(t.deadLine, '%d.%m.%Y').weekday() == 1]
        k = [t for t in kodutood.assignments if datetime.strptime(t.deadLine, '%d.%m.%Y').weekday() == 2]
        n = [t for t in kodutood.assignments if datetime.strptime(t.deadLine, '%d.%m.%Y').weekday() == 3]
        r = [t for t in kodutood.assignments if datetime.strptime(t.deadLine, '%d.%m.%Y').weekday() == 4]
        
        # days[0] on kõik kodutööd esmaspäeval.
        days = [e,t,k,n,r]
        
        # Kui on antud kindel päev, mille kohta kodutöid võtta, siis anname outputi ainult selle päeva kohta.
        if day:
            # Kui on antud kindel kodutöö ID, mille kaudu soovitakse kodutöö kohta lisainfot saada, siis näita tervet kodutööd
            if id:                    
                self.print_kodutoo_by_id(days,day,id)
            else:
                # Näite terve päeva kodutöid
                self.print_kodutoo_by_day(days, day)
        else:
            # Prindi kõik kodutööd sellel nädalal
            self.print_all_kodutoo(days)


    # Prindib välja kõik kodutööd
    def print_all_kodutoo(self, days):
        for i, kodutood in enumerate(days):
            # Prindi hetkene päev
            self.print_day_from_dayid(i) 
            # Kui kodutööde arv on üle nulli siis prindi need välja
            if (len(kodutood) > 0):
                for i, kodutoo in enumerate(kodutood):
                    print(colored(f"[{i + 1}]",'green') +colored(f" [{kodutoo.subject_name}]",'yellow') +  f": {kodutoo.title} | " + colored(f"{kodutoo.author}", "cyan"))
                print()
            else:
                # Kodutööd puuduvad sel päeval
                print("Ülesandeid ei ole.")


    # Prindi välja kõik kodutööd, mis toimuvad sellel päeval
    def print_kodutoo_by_day(self,days, day):
        # Võta päeva id kasutaja sisestatud päeva lühendist. Näiteks 'e' ehk esmaspäev muutub 0'iks, 't' -> 1
        dayId = self.get_day_from_str(day)
        # Kui kasutaja sisestas õige päeva lühendi
        if dayId != -1:
            # Prindi see päev, mille kohta kodutöid võtame
            self.print_day_from_dayid(dayId)

            # Käi läbi kõik kodutööd ja prindi need välja
            for i, kodutoo in enumerate(days[dayId]):
                if len(days[dayId]) > 1:
                    #print(colored(f"[{i + 1}]",'green') + f": {kodutoo.title}")
                    print(colored(f"[{i + 1}]",'green') +colored(f" [{kodutoo.subject_name}]",'yellow') +  f": {kodutoo.title} | " + colored(f"{kodutoo.author}", "cyan"))
                else:
                    print("Ülesandeid ei ole.")
            pass
        else:
            # Kasutaja sisestatud päev oli vigane
            print(colored('Vigane päev!', 'red'))


    # Prindi välja kindel kodutöö kasutades selle ID'd, mida saab leida lihtsalt 'eKool> kodutoo' commandi jooksutamisest.
    # Kasutaja sisestab näiteks 'eKool k e 1', mis tähendab, et võta KODUTÖÖ, mis on ESMASPÄEVAL ja mille ID on 1
    def print_kodutoo_by_id(self,days, day, id):
        # Päeva id
        dayId = self.get_day_from_str(day)
        # Päris index kodutööle on ühe võrra väiksem
        index = int(id) - 1

        # Kui sisestatud päev ei ole vigane
        if dayId != -1:
            # Kodutöö ID, mida proovime võtta ei tohi olla suurem kui kodutööde arv sellel päeval.
            if index >= len(days[dayId]):
                print(colored("Vigane ID!", "red"))
                return
            # Võta see kodutöö, millel on see ID
            kodutoo = days[dayId][index]
            print(colored(f"{kodutoo.title}", "green"))
            # Kasutame BeautifulSoup libraryt, et võtta ära HTML tagid tekstist.
            soup = BeautifulSoup(kodutoo.content, 'lxml')    
            
            # get_text võtab HTML tagid ära
            content = soup.get_text("\n")
            print(colored(f"{content}", "yellow"))
            print(colored(f"\n- {kodutoo.author}", "cyan"))
            # Manuste printimine
            if kodutoo.teacher_attachments: 
                print(colored("Manused: ", "magenta"))
                for attachment in kodutoo.teacher_attachments:
                    print(colored(attachment['fileName'], "yellow") + ": "+  colored("https://ekool.eu"  + attachment['url'], "blue")) 
        else:
            print(colored('Vigiane päev!', 'red'))


    # Command -> 'eKool> voog'
    # Võtab eKooli voo. See sisaldab hindeid ja teateid.
    def do_voog(self, feedNumber):
        self.feed_handler(feedNumber=feedNumber)


    # Tegeleb voo näitamisega.
    def feed_handler(self, feedNumber = None):
        # Võtame eKoolist voo
        feed = self.ekool.get_feed()

        # Kui ei ole antud kindlalt ID'd voo elemendile, mida soovime lähemalt vaadata, siis näita kõiki teateid ja hindeid.
        if feedNumber == "":
            for i, item in enumerate(feed.feed):
                # Ära näita üle 22 voo elemendi. Muidu on liiga palju teksti ekraanil
                if i > 22:
                    break

                # id 1 tähendab hinde tüüpi 
                if (item.item_type == 1):
                    # Prindime välja hinde
                    print(colored(f"{[i + 1]}", "green") + ": " + colored(f"({item.grade})", "red") + f" - Teade - {item.subject_name} | " + colored(f"{item.author_name}", "cyan") + " | " + colored(item.last_modified, "yellow"))
                else:
                    # prindime välja teate/märkuse
                    if item.title != None:
                        print(colored(f"{[i + 1]}", "green") + f": {item.title} | " + colored(item.author_name, "cyan") + " | " + colored(item.last_modified, 'yellow'))
                    else:
                        print(item.raw_obj)
                        print(f"{[i + 1]} Unknown")
        else:
            # On antud kindel voo element, mida soovime vaadata. Toome selle ekraanile
            try:
                # Võtame elemendi ID, mida soovime vaadata
                index = int(feedNumber) - 1
                # Võtame selle voo elemendi
                item = feed.feed[index]

                # item_type == 1 => HINNE
                # Kõik muu loeme hetkel teate alla
                if item.item_type == 1:
                    # Prindime ekraanile hinde
                    print(colored(f"{item.subject_name}", "green"))

                    # grade_type_id == 18 => Kursuse hinna
                    if item.grade_type_id == 18:
                        print(colored(f"Kursuse hinne: {item.grade}", "yellow"))
                        if (item.text_content): 
                            print(colored(f"{item.text_content}", "yellow"))
                        pass
                    else:
                        print(colored(f"Hinne: {item.grade}", "yellow"))
                        if (item.text_content): 
                            print(colored(f"{item.text_content}", "yellow"))

                else:
                    # Prindime tavalise teate sisu
                    print(colored(f"{item.title}", "green"))
                    print(colored(f"{item.content}", "yellow"))
                    print(colored(f"\n- {item.author_name}", "cyan"))
            except(Exception):
                print("Error")


# Alustame oma programmi
ekoolCmd = EKoolLoop()
ekoolCmd.cmdloop()