PLUGIN_PREFIX = '/video/plex-updater'

import updater
updater.init(repo = 'mikew/plex-updater')

def Start():
    pass

def ValidatePrefs():
    pass

@handler(PLUGIN_PREFIX, 'plex-updater')
def MainMenu():
    container = ObjectContainer()
    updater.add_button_to(container)

    return container

@route('%s/reset' % PLUGIN_PREFIX)
def ResetDict():
    Dict.Reset()
    Dict.Save()
