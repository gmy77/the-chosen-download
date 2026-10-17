# The Chosen · Download in italiano

Un piccolo script Python per verificare il catalogo pubblico di **The Chosen** e scaricare gli episodi disponibili in **MP4, Full HD 1920×1080, con audio italiano**.

Questo progetto nasce dall'apprezzamento per una serie che merita di essere conosciuta e sostenuta: un lavoro che dedica spazio alle persone, alle loro fragilità e agli incontri che cambiano una vita. Rendere pubblico questo strumento significa condividere un aiuto pratico per la visione personale, mantenendo il collegamento con le fonti ufficiali.

## A proposito di The Chosen

*The Chosen* è una serie statunitense creata, scritta e diretta da **Dallas Jenkins**. Ambientata nella Giudea e nella Galilea del I secolo, racconta la vita e il ministero di Gesù attraverso le persone che lo incontrano e lo seguono. **Jonathan Roumie** interpreta Gesù; il cast comprende anche Shahar Isaac, Elizabeth Tabish e Paras Patel.

Il racconto dedica attenzione alle vicende dei discepoli e alla loro vita quotidiana. Il crowdfunding ha avuto un ruolo rilevante nello sviluppo della produzione, sostenuta dal coinvolgimento del pubblico.

Questa breve presentazione è una sintesi originale basata sulla [voce italiana di Wikipedia dedicata a The Chosen](https://it.wikipedia.org/wiki/The_Chosen_(serie_televisiva)), consultata il **17 ottobre 2026**. Per guardare la serie e conoscere il progetto: [sito di visione ufficiale](https://watch.thechosen.tv/) e [Come and See Foundation](https://www.comeandseefoundation.org/).

## Cosa fa lo script

- Legge le stagioni e gli episodi dal catalogo pubblico ufficiale.
- Seleziona il video **1080p H.264** e la traccia **italiana** dello stesso gruppo audio.
- Unisce video e audio in MP4 con FFmpeg, senza ricodifica.
- Organizza i file per stagione e salta quelli finali già presenti.
- Produce un resoconto `verifica.csv`, segnalando episodi bloccati o formati mancanti.

Include gli speciali presenti nella raccolta *Episodes*. Esclude le altre raccolte, come trailer, aftershow e tavole rotonde. Se mancano il 1080p o l'italiano, segnala l'episodio senza sostituirli con altre qualità o lingue.

## Requisiti

- [Python](https://www.python.org/downloads/) **3.10 o successivo**.
- [FFmpeg](https://ffmpeg.org/download.html) installato e disponibile nel `PATH`.
- Connessione a Internet e spazio libero per i filmati.

Non servono pacchetti Python aggiuntivi. Il programma usa soltanto la libreria standard e FFmpeg.

## Avvio rapido

Scarica questo repository oppure clonalo:

```powershell
git clone https://github.com/gmy77/the-chosen-download.git
cd the-chosen-download
```

**Verifica soltanto**, senza scaricare i filmati:

```powershell
python scarica_chosen.py
```

**Scarica tutte le stagioni disponibili**:

```powershell
python scarica_chosen.py --scarica
```

Altri esempi:

```powershell
# Prova con un solo episodio della prima stagione
python scarica_chosen.py --scarica --stagioni 1 --limite 1

# Seleziona le stagioni
python scarica_chosen.py --scarica --stagioni 1 2

# Scegli la destinazione
python scarica_chosen.py --scarica --cartella "D:\The Chosen"

# Mostra tutte le opzioni
python scarica_chosen.py --help
```

Su macOS e Linux, se necessario, usa `python3` al posto di `python`.

## File salvati e interruzioni

La destinazione predefinita è la cartella `Filmati` accanto allo script. Ogni stagione ha una sottocartella; i nomi includono stagione, episodio, identificativo, lingua e risoluzione.

Un file finale già presente viene saltato **senza controllarne il contenuto**. Durante il download viene usato il suffisso `.incompleto.mp4`: in caso di interruzione l'episodio verrà riscaricato da capo al successivo avvio. Gli episodi già completati rimangono disponibili.

Il resoconto `verifica.csv` viene riscritto a ogni esecuzione. Se almeno un episodio presenta un errore, o non viene trovato alcun episodio, il programma termina con codice `1`: consulta il resoconto per distinguere gli episodi riusciti da quelli non disponibili.

## Verifica iniziale · 17 ottobre 2026

| Raccolta | Risultato nell'accesso pubblico verificato |
| --- | --- |
| Stagioni 1–4 | 32 episodi con video 1080p e traccia italiana dichiarati nei manifest |
| Speciali natalizi nelle raccolte Episodes | 2 video con video 1080p e traccia italiana |
| Stagione 5 | 8 episodi segnalati come bloccati dall'API pubblica (`isLocked`) |
| Stagioni 6–7 | Nessun episodio disponibile nel catalogo esaminato |

È stata inoltre eseguita una prova di unione su **3 secondi del primo episodio**, verificando un MP4 con video H.264 1920×1080 e audio AAC selezionato dalla traccia italiana. Questa prova non equivale al download o alla verifica integrale di tutti gli episodi.

La disponibilità può cambiare nel tempo o secondo l'area geografica. Gli indirizzi e la struttura del servizio possono cambiare e richiedere un aggiornamento dello script. La modalità di sola verifica controlla catalogo e manifest; non certifica che ogni segmento sia scaricabile.

## Progetto indipendente e fonti ufficiali

Questo è uno strumento indipendente, non affiliato a The Chosen o a Come and See Foundation. Il repository contiene il codice e la documentazione; non distribuisce episodi, immagini o tracce audio della serie. I diritti sui contenuti rimangono ai rispettivi titolari.

Lo script usa le risorse pubbliche del servizio, non effettua accessi ad account e non implementa rimozione di DRM o aggiramento dei blocchi. Utilizzalo nel rispetto dei diritti sui contenuti e delle condizioni del servizio. Per la visione offline tramite l'app consulta la [guida ufficiale al download](https://app-come-and-see-foundation.gorgias.help/en-US/download-episodes-for-offline-viewing-1527265).

Se apprezzi la serie, visita i canali ufficiali e valuta di [sostenere il progetto tramite Come and See](https://www.comeandseefoundation.org/).
