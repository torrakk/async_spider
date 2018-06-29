## ce module permet de faire correspondre les balises parsés au nom de champ.

def mapp(orig, results):
    assert isinstance(orig, dict) == True
    assert isinstance(results, dict) == True
    try:
        return {v:results[k] for k, v in orig.items()}
    except(KeyError):
        raise KeyError("le mapping est incorrect \n-orig : {0}\n-reuslts : {1}".format(orig, results))


if __name__=='__main__':
    orig = {'href': 'attribut1', 'title': 'attribut2', 'text': 'attribut3'}
    results = {'href': '/veve.ergfergerg/defdd.fr', 'title': 'LEs grandias', 'text': 'Url qui va bien'}
    print(mapp(orig, results))