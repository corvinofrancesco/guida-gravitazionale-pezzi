# Dati di misura dei pezzi degli scacchi

Cartella di **dati**, separata dalle sagome: raccoglie le misure dei pezzi da torneo (e, per
conoscenza, dei set giganti) per **confermare o confutare** le quote assunte nel generatore
`genera_svg.py` e in altri progetti (strutture di trasporto, organizzazione dei tornei).

> **Avviso.** Quasi tutti i valori sono **dichiarati dai rivenditori** o **stimati da foto**.
> Solo ciò che ha stato `misurato` è stato rilevato con uno strumento (calibro, bilancia).
> Non trattare una stima da foto come una misura.

## File

| File | Contenuto |
|---|---|
| `misure_pezzi_torneo.csv` | un pezzo per riga: norma FIDE, set dell'utente (stime da foto), set commerciali (dichiarati) |
| `misure_pezzi_giganti.csv` | pezzi dei set giganti (altezza, base, casa consigliata) |
| `imballi_giganti.csv` | colli, dimensioni e pesi per il trasporto dei set giganti |
| `ipotesi_guida.md` | confronto tra le quote assunte dalla guida e i dati: cosa è supportato, cosa no |
| `verifica_dati.py` | controllo strutturale dei CSV e riassunto (solo libreria standard) |
| `strumenti/supporto_foto_pezzi_A4_v4.pdf` | foglio A4 da incollare su cartoncino per fotografare i pezzi con scala |

Controllo: `python3 dati/verifica_dati.py` (con `-v` elenca anche i rapporti base/altezza).
Fallisce solo per errori di struttura; le deviazioni dalla norma FIDE sono solo segnalate.

## Colonne di `misure_pezzi_torneo.csv`

`modello, pezzo, colore, altezza_mm, base_mm, collo_mm, collare_mm, testa_mm, peso_g,
baricentro_mm, stato, incertezza_mm, fonte, data, note`

- `pezzo`: re, regina, alfiere, cavallo, torre, pedone.
- `collo_mm`: tratto più stretto del gambo. `collare_mm`: disco sotto la testa (pedone).
- `baricentro_mm`: altezza del baricentro dalla base (da misurare, vedi sotto). Oggi vuota.
- `stato`: `norma` · `dichiarato` · `stimato_foto` · `misurato`.
- `incertezza_mm`: incertezza stimata per i valori `stimato_foto`.
- `fonte` e `data`: URL (o descrizione) e giorno di consultazione/misura (AAAA-MM-GG).
- Nei campi di testo non usare la virgola (usa il punto e virgola): i CSV non sono quotati.

## Come si ricavano le misure dalle foto

1. **Stampa** il PDF in `strumenti/` su A4 a **scala 100%** (su Mac: «Scala 100%», non «Adatta
   in scala»). Controlla con un righello che la barra in basso misuri 100 mm. Il file è tarato
   per una HP DeskJet 2721e, che non stampa i primi ~13 mm dall'alto.
2. Incolla su cartoncino, taglia e piega come da istruzioni sul foglio.
3. Scatta con il telefono fermo nel supporto, **inquadrando tutto il pezzo e i due pannelli**.
   Evita foto ravvicinate o a mano libera: la parallasse falsa le altezze (è il caso della
   torre, lettura non attendibile).
4. Leggi l'altezza sulla scala dei pannelli **all'altezza dell'immagine del dettaglio** e fai la
   media dei due lati. Le larghezze si ricavano dalla distanza di 80,0 mm tra i bordi interni dei
   pannelli. Incertezza tipica: circa ±2 mm sulle altezze, circa ±1,5 mm sulle larghezze.
5. Per le **basi** (serve circa ±1 mm perché il canale ha scatti di 4 mm) è più preciso
   avvolgere una striscia di carta attorno alla base, misurarla e dividere per π.
6. Per il **peso** usa una bilancia da cucina; per il **baricentro** appoggia il pezzo coricato
   sul bordo di un righello fino a trovare l'equilibrio e misura la distanza dalla base.
   Queste due misure servono a verificare la premessa della guida: pezzi zavorrati sul fondo.

## Regole per chi aggiunge dati

- Ogni riga ha `stato`, `fonte` e `data`. Un dato incerto resta `stimato_foto` con `incertezza_mm`.
- Un valore non attendibile si lascia **vuoto** e si spiega in `note`, non si inserisce lo stesso.
- Un dato che contraddice la norma o un altro dato non si corregge: si registra e si annota.
- Dopo ogni modifica esegui `python3 dati/verifica_dati.py`.
