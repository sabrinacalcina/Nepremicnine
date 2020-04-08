import re
import orodja

regije = ['ljubljana-mesto', 'ljubljana-okolica', 'gorenjska', 'juzna-primorska', 'severna-primorska',
            'notranjska', 'savinjska', 'podravska', 'koroska', 'dolenjska', 'posavska', 'zasavska', 'pomurska']

stevilo_oglasov = [3078, 2886, 1390, 2239, 795, 458, 1896, 3022, 299, 1375, 652, 157, 713]

st_datotek = [103, 97, 47, 75, 27, 16, 64, 101, 10, 46, 22, 6, 24]


#funkcija ki se zapelje po vseh straneh in jih shrani
def shrani_strani(regije, stevilo_oglasov):
    for regija, stevilo in zip(regije, stevilo_oglasov):
        print (regija, stevilo)
        st_strani = stevilo // 30 + 1
        print(st_strani)
        for stevilka in range(1, st_strani + 1):
            url = (
                f'https://www.nepremicnine.net/oglasi-prodaja/{regija}/{stevilka}/'             #f dela kot format
            )
            orodja.shrani_spletno_stran(url, f'html_regije/{regija}{stevilka}.html', vsili_prenos=False)


vzorec = re.compile (
    r'<span class="title">(?P<ime>.*?)</span></a></h2>.*?'
    r'<span class="posr">(?P<posred>.*?): <span class="vrsta">(?P<vrsta>.*?)</span>.*?'
    r'<span class="tipi">(?P<tip>.*?)</span>.*?'
    r'<span class="atribut leto">Leto: <strong>(?P<leto>.*?)</strong>'
    r'(</span><span class="invisible">, </span><span class="atribut">Zemljišče: <strong>(?P<zemljisce>.*?) m2</strong>)?.*?'
    r'<span class="velikost" lang="sl">(?P<velikost>.*?) m2</span><br />.*?'
    r'<span class="cena">(?P<cena>.*?) &euro.*?</span>.*?'
    r'<span class="agencija">(?P<agencija>.*?)</span>', 
    flags=re.DOTALL
    )


def razbij_na_oglase(vsebina_strani):
    vzorec_oglasa = re.compile (
        r'<!--<meta itemprop="url" content.*?'
        r'</i><span>O ponudniku</span></a>',
        flags=re.DOTALL    
        )
    oglasi = re.findall(vzorec_oglasa, vsebina_strani)
    return oglasi


def naredi_seznam_nepremicnin(st_datotek, regije, vzorec):
    nepremicnine = []
    for regija, st_htmljev in zip(regije, st_datotek):
        print(regija, st_htmljev)
        for i in range(1, (st_htmljev+1)):
            
            with open(f'html_regije/{regija}{i}.html', encoding='utf-8') as f:
                count = 0
                vsebina = f.read()
                #print(i)
                oglasi = razbij_na_oglase(vsebina)
                for oglas in oglasi:
                    for zadetek in re.finditer(vzorec, oglas):
                        zadetek = zadetek.groupdict()
                        zadetek['regija'] = f'{regija}'
                        nepremicnine.append(zadetek)
                        count += 1
                        #print(zadetek)
                print(count)
    #print(nepremicnine)
    return nepremicnine


def popravi_zapisi(seznam):
    for nepremicnina in seznam:
        nepremicnina['leto'] = int(nepremicnina['leto'])
        nepremicnina['velikost'] = float(nepremicnina['velikost'].replace('.','').replace(',','.'))
        nepremicnina['cena'] = int(nepremicnina['cena'])
        if nepremicnina['zemljisce'] is not None:
            nepremicnina['zemljisce'] = float(nepremicnina['zemljisce'].replace('.','').replace(',','.'))
    imena_polj = ['ime', 'posred', 'vrsta', 'tip', 'leto', 'zemljisce',
                'velikost', 'cena', 'agencija', 'regija']
    orodja.zapisi_csv(seznam, imena_polj, f'podatki/nepremicnine.csv')
    orodja.zapisi_json(seznam, f'podatki/nepremicnine.json')


nepremicnine = naredi_seznam_nepremicnin(st_datotek, regije, vzorec)
popravi_zapisi(nepremicnine)
