# upwork creds
CLIENT_ID = ''
CLIENT_SECRET = ''

# token must be in single line
TOKEN = None

# contract_id
CONTRACT_ID = ''

# Zep creds should be in urlencoded form
USERNAME = ''
PASSWORD = ''

# Regex for extracting client_session_id and request_token
REGEX_CLIENT_SESSION_ID = r"(CLIENTSESSID=)([a-z,0-9]*)"
REGEX_REQUEST_TOKEN = r"(requesttoken = ')([a-z,0-9]*)"

# request urls
LOGIN_URL = 'https://www.zep-online.de/zeppstag/view/login.php'
TIMEZONE_URL = 'https://www.zep-online.de/zeppstag/view/index.php?action=save&timezoneOffset=5.5'
POST_TIME_URL = 'https://www.zep-online.de/zeppstag/view/ajax.php?CLIENTSESSID={}&pageContextId=Project+Times&mgr=ProjektzeitMgr&mgrId=1&action=save&JS_ENV_VAR_isFast=true&JS_ENV_VAR_locale=en_de&ajax=1&json=true'
TICKET_ID_URL = 'https://www.zep-online.de/zeppstag/view/index.php?CLIENTSESSID={client_session_id}&menu=ProjektzeitVerwaltungMgr&ticketId={ticket_id}'

# xpath for extracting identifiers for a ticket_id
XPATH_PROJECT_ID = '//select[@id="projektId"]/option[@selected="selected"]/@value'
XPATH_OCCURRENCE_ID = '//select[@id="vorgangId"]/option[@selected="selected"]/@value'

# zep post-time payload
POST_TIME_PAYLOAD = 'ueberschreiben=0&' \
                  'doppelbuchungTrotzdemFragenObUeberschreiben=1&' \
                  'ueberschreibenTrotzDoppelbuchung=0&' \
                  'preisfaktorantwort=&' \
                  'datum={date}&' \
                  'von={start_time}&' \
                  'bis={end_time}&' \
                  'dauer={duration}&' \
                  'projektId={project_id}&' \
                  'vorgangId={occurrence_id}&' \
                  'taetigkeit=MW&' \
                  'ort=NULL&' \
                  'letzterReiseOrt=&' \
                  'ortProjektrelevant=1&' \
                  'reise=0&' \
                  'startort=&' \
                  'zielort=&' \
                  'fahrzeug=NULL&' \
                  'km=&' \
                  'mitfahrer=&' \
                  'bemerkung={memo}&' \
                  'plusDays=0&' \
                  'plusMinutes=0&' \
                  'pastDays=2&' \
                  'pastDaysBezug=1&' \
                  'montagsErfassungFuerVorwoche=&' \
                  'fakturierbar=0&' \
                  'privat=0'


