####
# Le parser permet d'aller chercher les éléments qui nous interessent dans la page web

####
from bs4 import BeautifulSoup



class Parse():

    def __init__(self, page):
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
        results={}

        try:
            selection = kwargs['selection']
            resultat = kwargs['resultat']
        except KeyError:
            raise("les keys arguments sont malformés, ces derniers doivent contenir les clés 'resultat' et 'selection'")

        if 'type' in selection:
            args.append(selection.pop('type'))

        ## Recherche de contenu
        recherche = self.soup.find_all(*args, attrs=selection)

        ## Tri de la balise text
        results.update({'text':contenu.text for contenu in recherche if 'text' in resultat})

        ## Tri de la balise attrs pour ne garder que les attributs
        results.update({j:item.attrs[j][0] if type(item.attrs[j])==list else item.attrs[j]
                        for item in recherche for j in resultat.get('attrs', [])})

        return results




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