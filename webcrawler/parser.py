####
# Le parser permet d'aller chercher les éléments qui nous interessent dans la page web

####
from bs4 import BeautifulSoup



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

        args=[]
        #print('kwargs : ', kwargs)
        try:
            selection, resultat = kwargs['selection'].copy(), kwargs['resultat'].copy()
        except:
            raise Exception("les keys arguments sont malformés, ces derniers doivent contenir les clés 'resultat' et 'selection' kwargs : {}".format(kwargs))
        # print("selection, args ", kwargs, selection, args)
        if 'type' in selection:
            args.append(selection.pop('type'))


        ## Recherche de contenu
        recherche = self.soup.find_all(*args, attrs=selection)
        #print(recherche)
        return [{cle:item.get(cle) for cle in resultat.get('attrs') } for item in recherche ]




if __name__=='__main__':
    a = Parse('<html><head><title>test</title></head><body><div class="test" value="ok" roror="tatayoyo" rama="rama yade">'
              'xxx</div><span class="roro" value="ok" roror="tatayoyo" rama="rama yade">'
              'je vis en pyjama</span><div class="ruru" >yyy</div></body></html>').list_parse([{'selection':{'type':'span', 'class':'roro', 'value':'ok'},
                                                                              'resultat':{'text':'', 'attrs':['class', ]}},
                                                                                               {'selection': {
                                                                                                   'type': 'div',
                                                                                                   'class': 'test',
                                                                                                   'value': 'ok'},
                                                                                                'resultat': {'text': '',
                                                                                                             'attrs': [
                                                                                                                 'class', ]}}
                                                                                               ])
    print(a)