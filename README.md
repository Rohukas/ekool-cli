# ekool-cli
EKooli CLI Versioon

Autor: Robi Rohumaa

Programmi abil saab vaadata eKooli teateid/hindeid ning näha kodutöid.
Et programm töötaks tuleb sisestada enda eKooli e-mail ja parool line #47 ja #48'l olevatesse muutujatesse.

Programm annab kasutajale valiku 
* Sisestades 'voog' või selle lühend 'v' saab kätte kõik hinded ja teated.
* Sisestades 'kodutoo' või 'k' saab kätte kõik praeguse nädala kodutööd.


eKool> voog 
eKool> v 
Sisestades selle saab ekraanil näha kõiki hindeid ja teated. Igal hindel/teatel on oma ID, mille järgi saab
seda lähemalt vaadata.

eKool> voog [ID]
eKool> v [ID]
Et uurida näiteks teate, mille ID'ks on 1 sisu, peame sisestame programmi 'voog 1' või lühendi 'v 1'.
See näitab meile lisainfot teate kohta. Sama nagu eKoolis teate peale vajutamine.

eKool> kodutoo
Sisestades 'kodutoo' saame näha kõiki praeguse nädala kodutöid.

eKool> kodutoo [esmaspaev, teisipaev, kolmapaev, neljapaev, reede]
eKool> k [e, t, k, n, r]
Kui soovime näha näiteks kõiki esmaspäeva kodutöid, peame programmi sisestama kas 'kodutoo esmaspaev' või lühendi
'k e', milles k='kodutoo' ja e='esmaspaev'
See toob meile koik esmaspaeva kodutood.

eKool> kodutoo [esmaspaev, teisipaev, kolmapaev, neljapaev, reede] [ID]
eKool> k [e, t, k, n, r] [ID]
Sisestame päeva, mille kodutööd tahame ning selle päeval valitud kodutöö ID.
Tagasi saame kogu kodutöö sisu koos manustega(kui need on olemas)
