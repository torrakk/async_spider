# Chemin static local pour télécharger les fichiers
STATIC_PATH='/home/paul/'

LOG_PATH='/var/log/async_spider.log'

LOG_LEVEL='debug'
# Adresse du guichet adresse
#GUICHET_ADRESSE = 'https://guichet-adresse.ign.fr/login'
GUICHET_ADRESSE = 'https://www.data.gouv.fr/fr/search/?q=servitude+haute-loire'
#GUICHET_ADRESSE = 'https://www.grosfichiers.com/hNEIS4SBs8spU/'

# Login
LOGIN='******'


# mot de passe
MDP='******'

CODES={'username':LOGIN, 'password':MDP, }

## Timeout de session
TIMEOUT = 3000