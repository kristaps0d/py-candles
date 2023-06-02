## Problema <a name = "problem_statement"></a>

-  Izveidot pastāvīgu un uzticamu darbaspēka suplements, ar kuru vidē ar strauji augošiem pieprasījumiem cilvēku darbaspēkā būtu arī rezerves opcijas tā, lai darbs tiku veikts produkti un sasniegtu klientus laikā pat sliktākajos laikos.

#

1. Problēma tiks risināta indirekti, nevis sniedzot gatavu produktu izmantotu produkcijas līnijās, bet izstrādātu koda bāzi ar iespējām un funkcijām tikt pielāgotam plašam vajadzību lokam. 

2. Funkcijas, kas jau tiks dotas līdzi ar koda bāzi būs piemērotas vizuālai datu apstrādei. 	
Galvenā jau iepriekš iebūvētā niša būs teju svecīšu skaitīšana un tipa kategorizēšana pēc vizuālajiem kritējiem. 

#

## Funkcijas <a name = "function_statement"></a>

-	Vides automātiska maskēšana ar “ArUco” zīmju palīdzību.
-	Sveču katagorizēšana pēc krāsām un defektivitāti.
-	Datubāze kopskaitu un atdeves laiku saglabāšanai.
-	Aplikācijas funkcijas pārvaldes lietotāja interfeiss

#

## Izstrādes plāns <a name = "plan_statment"></a>

1.	Izveidot vispārēju sistēmas bāzi ar spēju maskēt un izmainīt vizuālus datus
2.	Sistēmai pievienot spēju atpazīt sveces
3.	Sistēmai pievienot spēju katagorizēt sveces
4.	Sistēmai pievienot spēju sekot atpazītām svecēm
5.	Kopumu apvienot ar datubāzi
6.	Kopējo sistēmu integrēt ar lietotājiem pieejamu UI

#

## Uzturēšanas plāns <a name = "upkeep_statment"></a>

Dotais produkts tiks uzturēts kā atvērtā avota produkts, kā jau to nosaka tā licence- GPLv3. Tas ir atvērts un brīvi pieejams tā github lapā, kur cilvēki spēs veidot pull piedāvājumus, lai veiktu koda uzlabojumus. Taču pats autors negrasās produktu aktīvi uzturēt dēļ tā laikietilpīgās dabas.

#


## Pabeigtā darba mērķis <a name = "upkeep_statment"></a>

- Pabeigtā darba mērķis ir iegūt sistēmu, kura ir spējīga vismaz daļēji aizvietot cilvēku uzmanību produktu kvalitātes kontrolē. Sistēmai vajadzētu būt spējīgai atpazīt un saskaitīt sveces pēc krāsām, un pēc tās defektiem. 

- Un, lai šādus datus varētu apkopot pabeigtajam darbā būs datubāze, kurā tiks uzturēti dati par visām kopējām produkcijām un to informācijām.

- Arī priekš informācijas aizsardzības un rīku drošības nodrošināšanai pabeigtajā darbā būs iespējama lietotāju interfeisa ieslēgt obligātu lietotāju autentifikāciju drošai rīku piekļuvei.

#

## 🏁 Lietotāju ceļvedis <a name = "getting_started"></a>

### Launch

Asinhronā (Lietotāju skarnes) režīma palaišana:

```
python ./app/__init__.py
```
#
Sinhronā (Bez lietotāju skarnes) režīma palaišana:

```
python ./app/__init__.py --nogui
```
#
Asinhronā testēšanas (Bez lietotāju skarnes) režīma palaišana:

```
python ./app/__init__.py --nogui --dev
```
vai
```
python ./app/__init__.py --dev
```

### Lietotāju saskarnes ceļvedis

Aplikācijas palaišana

![./docs/Picture1](https://raw.githubusercontent.com/kristaps0d/py-candles/prod/docs/Picture1.png)

1. Lietotāju authentifikācija
2. Sesijas konfigurēšana
3. Sesijas palaišana

![./docs/Picture2](https://raw.githubusercontent.com/kristaps0d/py-candles/prod/docs/Picture2.png)
#
## Demo <a name = "demo_started"></a>

### Asinhronais režīms

https://raw.githubusercontent.com/kristaps0d/py-candles/prod/docs/demo.mp4

#

### Sinhronais režīms

http://tastur.ddns.net/static/videos/material.mp4