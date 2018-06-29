####
# Le parser permet d'aller chercher les éléments qui nous interessent dans la page web

####
from bs4 import BeautifulSoup
from itertools import chain

from webcrawler.utils import reorgPaquetGenerator
from webcrawler.log import parse_log
from webcrawler.mapper import mapp

class Parse():

    def __init__(self, page):
        '''
        Le parser permet de parser une page web en fonction d'une liste de balise et de retourner une selection 
        nous pouvons soit parser une liste de balise, soit une seule.
        voir les méthodes : parse et list_parse
        :param page: 
        '''
        assert type(page)==str, "La page doit être de type string"

        self.page = page
        self.soup = BeautifulSoup(self.page, 'html.parser')


    def list_parse(self, list_baliz):
        '''
        Permet de parser une liste de balise
        
        :param list: parse une liste de kwargs
        :return: 
        List_resultat
        '''
        return [self.parse(**baliz) for baliz in list_baliz] if list_baliz else self.page

    def __mapp(self, orig, results):
        '''
        Méthode permettant de mettre en relation les résultats avec les attributs finaux demandés 
        dans le dictionnaire de données
        :param orig: 
        :param results: 
        :return: 
        '''
        assert isinstance(orig, dict) == True
        assert isinstance(results, dict) == True
        try:
            return {v: results[k] for k, v in orig.items()}
        except(KeyError):
            print("le mapping est incorrect \n-orig : {0}\n-reuslts : {1}".format(orig, results))

    def __getBFmethod(self, resu, cle):
        '''
        Méthode permettant d'accéder aux méthodes de beautifulSoup
        :param resu: 
        :param cle: 
        :return: 
        '''
        if hasattr(resu, cle):
            return getattr(resu, cle)
        return

    def parse(self, **kwargs):

        '''
        
        Permet de faire de recherche de balise et de les retourner sous forme de dictionnaire
        :param objet: recherche un objet contenu dans une balise
               kwargs : {'selection':{'type':None, 'classe':None, 'value':None, 'regex':None}, 
                         'resultat':{'text':'', 'attr':['liste des attributs']}}}
               Le selection permet de fair eune selection des balises et le résultat permet 
               de faire remonter les données attendues
        :return:
    
        '''


        selection, resultat, with_parents = kwargs['selection'].copy(), kwargs['results'].copy(),\
                                  kwargs.get('with_parents', None)

        result = self.soup
        # print("selection ", selection)
        for recherche in selection:
            args = []
            for cle, valeurs in recherche.items():
                # try:
                parse_log.debug('Item recherchés :'+ str(recherche.items()))
                val = valeurs.copy()
                # print(val)
                parse_log.debug('Nous recherchons dans la page : '+ str(valeurs))
                if 'type' in val:
                    args.append(val.pop('type'))
                if isinstance(result, list):
                    ## Nous iterons sur les méthodes de beautiful soup sur lesquelles itérer
                    ## Nous applatissons ensuite la liste pour faire remonter les résultats
                    parse_log.debug("Chainage des Methodes Beautiful Soup "+str([ self.__getBFmethod(resu, cle)(*args, attrs=val) for resu in result]))
                    result = list(chain.from_iterable([ self.__getBFmethod(resu, cle)(*args, attrs=val) for resu in result]))
                else:
                    result = self.__getBFmethod(result, cle)(*args, attrs=val)
        if result:
            parse_log.debug(str(result))
            ## nous utilisons le fonction mapp pour rapprocher les resultat attendus et les resultats réels
            return [self.__mapp(resultat,{cle:item.get(cle) if cle != 'text' else item.getText().strip() \
                                          for cle in resultat.keys()}) for item in result ]
        else:
            return


    def getList(self, list_baliz):
        '''
        Permet d'obtenir une liste des balises demandées
        :param list_baliz: 
        :return: 
        '''
        recherche = self.list_parse(list_baliz)
        resultante = min([len([item.values() for item in  item_recherche if item.values()]) for item_recherche in recherche])
        return list(zip(*[[j  for j in reorgPaquetGenerator(i, resultante) if j ] for i in recherche]))


if __name__=='__main__':
    heure_debut_rencontre = {'selection':{'type':'span', 'class':'KambiBC-event-item__start-time--time'},
                     'resultat':{'attrs':['class', 'text']}}
    sport = {'selection':{'type':'span', 'class':'KambiBC - modularized - event - path__fragment'},
                     'resultat':{'attrs':['class', 'text']}
             }
    competition = {'selection':{'type':'span', 'class':'KambiBC-modularized-event-path__fragment'},
                     'resultat':{'attrs':['class', 'text']}
             }
    participants = {'selection': {'type': 'div', 'class':'KambiBC-event-participants__name'},
                     'resultat': {'text': '','attrs': ['text']}}
    paris = {'selection': {'type': 'span', 'class': 'KambiBC-mod-outcome__odds'},
                   'resultat': {'attrs': ['class', 'text']}}
    nb_offre_de_paris = {'selection': {'type': 'span', 'class': 'KambiBC-event-item__bet-offer-count'},
             'resultat': {'attrs': ['class', 'text']}}

    a = Parse('''<div class="KambiBC-event-item__event-info"><div class="KambiBC-event-item__score-container">
    <div class="KambiBC-event-item__match-clock-container"><span class="KambiBC-event-item__start-time--time">20:45</span></div></div>
    <div class="KambiBC-event-item__details"><div class="KambiBC-event-item__participants-container">
    <div class="KambiBC-event-participants"><div class="KambiBC-event-participants__name">
    <!-- react-text: 50 -->Republic of Ireland<!-- /react-text --><div class="KambiBC-event-participants__info"></div></div>
    <div class="KambiBC-event-participants__name"><!-- react-text: 53 -->Denmark<!-- /react-text -->
    <div class="KambiBC-event-participants__info"></div></div></div></div><div class="KambiBC-event-item__streaming-path-container">
    <div class="KambiBC-event-item__live-text-container">Live</div><div class="KambiBC-event-item__path-container">
    <div class="KambiBC-modularized-event-path"><span class="KambiBC-modularized-event-path__fragmentcontainer">
    <span class="KambiBC-modularized-event-path__fragment">Football</span></span>
    <span class="KambiBC-modularized-event-path__fragmentcontainer">
    <span class="KambiBC-modularized-event-path__fragment">World Cup Qualifying - Europe</span></span></div></div></div>
    <div class="KambiBC-event-item__each-way-terms-container"><!-- react-empty: 43 --></div></div>
    <span class="KambiBC-event-item__bet-offer-count">+360</span></div>
    <button class="KambiBC-event-item__link--event-statistics" data-touch-feedback="true" title="Statistics" type="button"></button>
    <div class="KambiBC-event-item__bet-offers-container">
    <div class="KambiBC-list-view KambiBC-bet-offers-list KambiBC-bet-offers-list--col2">
    <div class="KambiBC-list-view__column KambiBC-bet-offers-list__column">
    <div class="KambiBC-bet-offer KambiBC-bet-offer--onecrosstwo KambiBC-bet-offer--inline KambiBC-bet-offer--outcomes-3">
    <div class="KambiBC-bet-offer__outcomes"><button class="KambiBC-mod-outcome" data-touch-feedback="true" role="button" type="button">
    <div class="KambiBC-mod-outcome__flexwrap"><div class="KambiBC-mod-outcome__label-wrapper">
    <span class="KambiBC-mod-outcome__label">Republic of Ireland</span></div><div class="KambiBC-mod-outcome__odds-wrapper">
    <span class="KambiBC-mod-outcome__odds">3.25</span></div></div></button>
    <button class="KambiBC-mod-outcome" data-touch-feedback="true" role="button" type="button">
    <div class="KambiBC-mod-outcome__flexwrap"><div class="KambiBC-mod-outcome__label-wrapper">
    <span class="KambiBC-mod-outcome__label">Draw</span></div><div class="KambiBC-mod-outcome__odds-wrapper">
    <span class="KambiBC-mod-outcome__odds">2.80</span></div></div>
    </button><button class="KambiBC-mod-outcome" data-touch-feedback="true" role="button" type="button">
    <div class="KambiBC-mod-outcome__flexwrap"><div class="KambiBC-mod-outcome__label-wrapper">
    <span class="KambiBC-mod-outcome__label">Denmark</span></div>
    <div class="KambiBC-mod-outcome__odds-wrapper"><span class="KambiBC-mod-outcome__odds">2.80</span></div></div><
    /button></div></div></div>
    <div class="KambiBC-list-view__column KambiBC-bet-offers-list__column">
    <div class="KambiBC-bet-offer KambiBC-bet-offer--overunder KambiBC-bet-offer--inline KambiBC-bet-offer--outcomes-2">
    <div class="KambiBC-bet-offer__outcomes">
    <button class="KambiBC-mod-outcome" data-touch-feedback="true" role="button" type="button">
    <div class="KambiBC-mod-outcome__flexwrap"><div class="KambiBC-mod-outcome__label-wrapper">
    <span class="KambiBC-mod-outcome__label">Over</span><span class="KambiBC-mod-outcome__line">1.5</span></div>
    <div class="KambiBC-mod-outcome__odds-wrapper"><span class="KambiBC-mod-outcome__odds">1.72</span></div></div></button>
    <button class="KambiBC-mod-outcome" data-touch-feedback="true" role="button" type="button">
    <div class="KambiBC-mod-outcome__flexwrap"><div class="KambiBC-mod-outcome__label-wrapper">
    <span class="KambiBC-mod-outcome__label">Under</span><span class="KambiBC-mod-outcome__line">1.5</span></div>
    <div class="KambiBC-mod-outcome__odds-wrapper"><span class="KambiBC-mod-outcome__odds">2.14</span>
    </div></div></button></div></div></div></div></div>


<div class="KambiBC-event-item__event-info"><div class="KambiBC-event-item__score-container"><div class="KambiBC-event-item__match-clock-container"><span><span class="KambiBC-event-item__start-time--date">17/11</span><span class="KambiBC-event-item__start-time--time">19:00</span></span></div></div><div class="KambiBC-event-item__details"><div class="KambiBC-event-item__participants-container"><div class="KambiBC-event-participants"><div class="KambiBC-event-participants__name"><!-- react-text: 143 -->Lille<!-- /react-text --><div class="KambiBC-event-participants__info"></div></div><div class="KambiBC-event-participants__name"><!-- react-text: 146 -->Saint-Étienne<!-- /react-text --><div class="KambiBC-event-participants__info"></div></div></div></div><div class="KambiBC-event-item__streaming-path-container"><div class="KambiBC-event-item__live-text-container">Live</div><div class="KambiBC-event-item__path-container"><div class="KambiBC-modularized-event-path"><span class="KambiBC-modularized-event-path__fragmentcontainer"><span class="KambiBC-modularized-event-path__fragment">Football</span></span><span class="KambiBC-modularized-event-path__fragmentcontainer"><span class="KambiBC-modularized-event-path__fragment">France</span></span><span class="KambiBC-modularized-event-path__fragmentcontainer"><span class="KambiBC-modularized-event-path__fragment">Ligue 1</span></span></div></div></div><div class="KambiBC-event-item__each-way-terms-container"><!-- react-empty: 92 --></div></div><span class="KambiBC-event-item__bet-offer-count">+118</span></div><button class="KambiBC-event-item__link--event-statistics" data-touch-feedback="true" title="Statistics" type="button"></button><div class="KambiBC-event-item__bet-offers-container"><div class="KambiBC-list-view KambiBC-bet-offers-list KambiBC-bet-offers-list--col2"><div class="KambiBC-list-view__column KambiBC-bet-offers-list__column"><div class="KambiBC-bet-offer KambiBC-bet-offer--onecrosstwo KambiBC-bet-offer--inline KambiBC-bet-offer--outcomes-3"><div class="KambiBC-bet-offer__outcomes"><button class="KambiBC-mod-outcome" data-touch-feedback="true" role="button" type="button"><div class="KambiBC-mod-outcome__flexwrap"><div class="KambiBC-mod-outcome__label-wrapper"><span class="KambiBC-mod-outcome__label">Lille</span></div><div class="KambiBC-mod-outcome__odds-wrapper"><span class="KambiBC-mod-outcome__odds">2.25</span></div></div></button><button class="KambiBC-mod-outcome" data-touch-feedback="true" role="button" type="button"><div class="KambiBC-mod-outcome__flexwrap"><div class="KambiBC-mod-outcome__label-wrapper"><span class="KambiBC-mod-outcome__label">Draw</span></div><div class="KambiBC-mod-outcome__odds-wrapper"><span class="KambiBC-mod-outcome__odds">3.20</span></div></div></button><button class="KambiBC-mod-outcome" data-touch-feedback="true" role="button" type="button"><div class="KambiBC-mod-outcome__flexwrap"><div class="KambiBC-mod-outcome__label-wrapper"><span class="KambiBC-mod-outcome__label">Saint-Étienne</span></div><div class="KambiBC-mod-outcome__odds-wrapper"><span class="KambiBC-mod-outcome__odds">3.35</span></div></div></button></div></div></div><div class="KambiBC-list-view__column KambiBC-bet-offers-list__column"><div class="KambiBC-bet-offer KambiBC-bet-offer--overunder KambiBC-bet-offer--inline KambiBC-bet-offer--outcomes-2"><div class="KambiBC-bet-offer__outcomes"><button class="KambiBC-mod-outcome" data-touch-feedback="true" role="button" type="button"><div class="KambiBC-mod-outcome__flexwrap"><div class="KambiBC-mod-outcome__label-wrapper"><span class="KambiBC-mod-outcome__label">Over</span><span class="KambiBC-mod-outcome__line">2.5</span></div><div class="KambiBC-mod-outcome__odds-wrapper"><span class="KambiBC-mod-outcome__odds">2.38</span></div></div></button><button class="KambiBC-mod-outcome" data-touch-feedback="true" role="button" type="button"><div class="KambiBC-mod-outcome__flexwrap"><div class="KambiBC-mod-outcome__label-wrapper"><span class="KambiBC-mod-outcome__label">Under</span><span class="KambiBC-mod-outcome__line">2.5</span></div><div class="KambiBC-mod-outcome__odds-wrapper"><span class="KambiBC-mod-outcome__odds">1.58</span></div></div></button></div></div></div></div></div>''')\
        .getList([ participants, heure_debut_rencontre, paris, nb_offre_de_paris ])
    print(a)