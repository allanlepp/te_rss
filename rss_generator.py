#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    RSS voo genereerimiste käivitaja
"""

import makereq
import rssmaker
import sys

import parser_avalikteenistus  # noqa F401
import parser_bns  # noqa F401
import parser_geopeitus  # noqa F401
import parser_jt  # noqa F401
import parser_kuma  # noqa F401
import parser_lounaeestlane  # noqa F401
import parser_nommeraadio  # noqa F401
import parser_pohjarannik  # noqa F401
import parser_stokker  # noqa F401
import parser_tartuekspress  # noqa F401
import parser_teabeleht  # noqa F401
import parser_tootukassa  # noqa F401

RSSdefinitions = []
RSStoGenerate = []
maxArticleURLstoVisit = 10

#                       name,               title,              description                             domain                                  domain_rss (optional)
RSSdefinitions.append(['avalikteenistus',   'Avalik teenistus', 'Avaliku teenistuse "Tartu" töökohad',  'http://www.rahandusministeerium.ee',   'http://www.rahandusministeerium.ee/et/avalikud-konkursid?page=1'])  # noqa E241
RSSdefinitions.append(['bns',               'BNS',              'BNS - uudised Eestist, Lätist, Leedust ja maailmast', 'http://bns.ee',         ''])  # noqa E241
RSSdefinitions.append(['geopeitus',         'Geopeitus',        'Geopeituse "Tartu" aarded',            'http://www.geopeitus.ee',              ''])  # noqa E241
RSSdefinitions.append(['jt',                'Järva Teataja',    'Järva Teataja',                        'http://jarvateataja.postimees.ee',     'http://jarvateataja.postimees.ee/search'])  # noqa E241
RSSdefinitions.append(['kuma',              'Kuma',             'Kuma - Kesk-Eesti uudised',            'http://kuma.fm',                       ''])  # noqa E241
RSSdefinitions.append(['lounaeestlane',     'Lõunaeestlane',    'Lõunaeestlane',                        'http://www.lounaeestlane.ee',          ''])  # noqa E241
RSSdefinitions.append(['nommeraadio',       'Nõmme Raadio',     'Nõmme Raadio - radikaalseim raadio Eestis!', 'http://www.nommeraadio.ee',      ''])  # noqa E241
RSSdefinitions.append(['pohjarannik',       'Põhjarannik',      'Põhjarannik',                          'http://pr.pohjarannik.ee',             ''])  # noqa E241
RSSdefinitions.append(['stokker',           'Stokker - Outlet', 'Stokker - Outlet',                     'http://www.stokker.ee',                'http://www.stokker.ee/kampaaniad/tooriistade-outlet?instorage=1&limit=100'])  # noqa E241
RSSdefinitions.append(['tartuekspress',     'Tartu Ekspress',   'Tartu Ekspress - Kõik uudised',        'http://tartuekspress.ee',              'http://tartuekspress.ee/index.php?page=20&type=3'])  # noqa E241
RSSdefinitions.append(['teabeleht',         'Teabeleht',        'Teabeleht',                            'http://www.teabeleht.com',             ''])  # noqa E241
RSSdefinitions.append(['tootukassa',        'Töötukassa',       'Töötukassa tööpakkumised',             'http://www.tootukassa.ee',             'http://www.tootukassa.ee/toopakkumised?location_id=0051,0795&education_id=KUTSEKORGHARIDUS,BAKALAUREUSEOPE,MAGISTRIOPE'])  # noqa E241


# user input
try:
    sys.argv[1]
except Exception:
    print('rss_generaator: Sisend määramata, genereeritakse kõik vood.')
    RSStoGenerate = range(0, len(RSSdefinitions))
else:
    sisend = sys.argv[1]
    try:
        RSStoGenerate.append(int(sisend))
    except Exception:
        for i in range(0, len(RSSdefinitions)):
            if (sisend == RSSdefinitions[i][0]):
                RSStoGenerate.append(i)
                break
if len(RSStoGenerate) < 1:
    print('rss_generaator: Ei suutnud tuvastada sisendist sobivat nime ega numbrit, genereeritakse kõik vood.')
    RSStoGenerate = range(0, len(RSSdefinitions))

# generate all feeds
for curRSS in RSStoGenerate:

    curName = RSSdefinitions[curRSS][0]
    curTitle = RSSdefinitions[curRSS][1]
    curDescription = RSSdefinitions[curRSS][2]
    curDomain = curDomainRSS = RSSdefinitions[curRSS][3].rstrip('/') + '/'
    if len(RSSdefinitions[curRSS]) > 3 and len(RSSdefinitions[curRSS][4]) > 0:
        curDomainRSS = RSSdefinitions[curRSS][4]
    curParser = sys.modules['parser_' + curName]
    curFilename = curName + '.rss'

    try:
        # load page into tree
        pageTree = makereq.getArticleData(curDomainRSS)
    except Exception:
        print('rss_generaator: Viga! Ei suutnud andmeid pärida leheküljelt: ' + curDomainRSS)
        continue

    dataset = curParser.getArticleListsFromHtml(pageTree, curDomain, maxArticleURLstoVisit)
    rss = rssmaker.rssmaker(dataset, curTitle, curDomain, curDomainRSS, curDescription)

    try:
        rss.write(open(curFilename, 'wb'),
                  encoding='UTF-8', pretty_print=True)
        print('rss_generaator: Fail ' + curFilename + ' salvestatud.')
    except Exception:
        print('rss_generaator: Viga! Ei õnnestunud faili ' + curFilename + ' salvestada.')
