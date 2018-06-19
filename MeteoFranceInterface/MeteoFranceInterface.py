import requests
import json
import pprint
import prettytable
import time


def getCityCodeFromName( iCityName):
    #TODO mapping to code from name. Hardcode with Biot code
    oCityCode = "060180"
    return oCityCode


def getDataFromMeteoFranceAPI( iCityCode ):
    #url='http://www.meteo-france.mobi/ws/getDetail/france/060180.json'
    #url = 'http://ws.meteofrance.com/ws/getDetail/france/060180.json'

    url = 'http://ws.meteofrance.com/ws/getDetail/france/' + iCityCode + '.json'

    biotMFResp = requests.get(url)
    biotMFParsed = biotMFResp.json()
    biotMFResp.close()

    print("=============================" + biotMFParsed['result']['ville']['nom'] + "=============================")
    print("======================" + time.strftime("%d %b %Y, %H:%M %a", time.localtime()) + "==================")
    matin = ['7h', '13h']
    midi = ['13h', '19h']
    soir = ['19h', '1h']
    nuit = ['1h', '7h']
    slotCube = {'matin': matin, 'midi': midi, 'soir': soir, 'nuit': nuit}
    #    pp = pprint.PrettyPrinter()
    #    pp.pprint(slotCube)
    listeKeys = ['0_matin', '0_midi', '0_soir', '0_nuit']
    listeKeys.extend(['1_matin', '1_midi', '1_soir', '1_nuit'])
    listeKeys.extend(['2_matin', '2_midi', '2_soir', '2_nuit'])
    listeKeys.extend(['3_matin', '3_midi', '3_soir', '3_nuit'])
    listeKeys.extend(['4_matin', '4_midi', '4_soir', '4_nuit'])
    listeKeys.extend(['5_matin', '5_midi', '5_soir', '5_nuit'])
    listeKeys.extend(['6_matin', '6_midi', '6_soir', '6_nuit'])
    meteoTable = prettytable.PrettyTable(['date', 'moment', 'prevision', 'Temp', 'Vent'])
    firstRaw = True
    for k in listeKeys:
        if k in biotMFParsed['result']['previsions']:
            #            print(k+" "+str(biotMFParsed['result']['previsions'][k]['date'])+" "+biotMFParsed['result']['previsions'][k]['moment']+" "+biotMFParsed['result']['previsions'][k]['description']+" "+biotMFParsed['result']['previsions'][k]['temperatureMin']+" "+biotMFParsed['result']['previsions'][k]['temperatureMax']+" "+biotMFParsed['result']['previsions'][k]['vitesseVent'])
            timeValue1 = time.gmtime(biotMFParsed['result']['previsions'][k]['date'] / 1000)
            timeValue2 = timeValue1
            if biotMFParsed['result']['previsions'][k]['moment'] == 'soir':
                timeValue2 = time.gmtime(biotMFParsed['result']['previsions'][k]['date'] / 1000 + 86400)
            if biotMFParsed['result']['previsions'][k]['moment'] == 'nuit':
                timeValue1 = time.gmtime(biotMFParsed['result']['previsions'][k]['date'] / 1000 + 86400)
                timeValue2 = timeValue1
            timeString1 = time.strftime("%d %b %Y, %a", timeValue1)
            timeString2 = time.strftime("%d %b %Y, %a", timeValue2)
            debutListe = [timeString1, slotCube[biotMFParsed['result']['previsions'][k]['moment']][0], ' ',
                          biotMFParsed['result']['previsions'][k]['temperatureMin'], ' ']
            milieuListe = [timeString1, biotMFParsed['result']['previsions'][k]['moment'],
                           biotMFParsed['result']['previsions'][k]['description'],
                           biotMFParsed['result']['previsions'][k]['temperatureCarte'],
                           biotMFParsed['result']['previsions'][k]['vitesseVent']]
            finListe = [timeString2, slotCube[biotMFParsed['result']['previsions'][k]['moment']][1], ' ',
                        biotMFParsed['result']['previsions'][k]['temperatureMax'], ' ']
            if firstRaw:
                meteoTable.add_row(debutListe)
                firstRaw = False
            meteoTable.add_row(milieuListe)
            meteoTable.add_row(finListe)
    return meteoTable


if __name__ == '__main__':
    aCityCode = getCityCodeFromName("biot")
    table = getDataFromMeteoFranceAPI( aCityCode )
    print(table)