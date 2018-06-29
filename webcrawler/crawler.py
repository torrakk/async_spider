import asyncio
import re
import time


from webcrawler.scenari import scenari
from webcrawler.scenar_list.guichet_adresse import dicto
#from webcrawler.scenar_list.betclick import dicto
#from webcrawler.scenar_list.open_data_servitudes_hautes_loire import dicto

class crawlTime():
    def time(self):
        duree = time.time() - Crawler.heure_debut
        return ("durée webcrawl: {:08.2f} s".format(duree))


class Crawler():
    heure_debut = time.time()
    def __init__(self, scenario, loop):

        self.loop = loop
        self.scenario = scenario

    def do_scenari(self):

        [asyncio.ensure_future(scenari(loop=self.loop, **kwargs).run()) for kwargs in self.scenario]

        try:
            self.loop.run_forever()
        finally:
            print(crawlTime().time())
            self.loop.close()

                # self.loop.run_until_complete(asyncio.gather(*tasks))


if __name__=="__main__":
    loop = asyncio.get_event_loop()



    links = {
             'parse':None,
             'links': [],
             'scenari': False,
             'session': None,
             'inject': {},
             'follow': False
            }

    robot = Crawler(scenario=dicto, loop=loop)
    robot.do_scenari()
