# Ipotesi della guida confrontate con i dati

Confronto tra le quote usate in `genera_svg.py` / `README.md` e i dati in questa cartella.
Stato dei dati: `dichiarato` = scheda del rivenditore · `stima` = stimato da foto (±1,5–2 mm).
Aggiornato con i dati del 2026-11-16; rigenera i numeri con `python3 dati/verifica_dati.py`.

| Ipotesi nella guida | Dati | Esito |
|---|---|---|
| Re: base ⌀50 come ingombro massimo da non bloccare | dichiarato 34–45 mm (12 set); FIDE: massimo 47,5 mm (50% di 95); stima set utente circa 36 | **Supportata** come tetto prudente |
| Uscita imbuto mai sotto 50 mm; apertura massima ~55 per il re | coerente con la riga precedente: margine di almeno 5 mm sul re più largo trovato (45) | **Supportata** |
| Pedone: altezza 48 | dichiarato 46–53 (FIDE 50); stima set utente 48,5 | **Supportata** |
| Pedone: base ⌀30 | dichiarato 25,5–33 (8 set); stima set utente circa 27 | **Da verificare** (vedi sotto) |
| Pedone: collo ⌀12 | stima set utente circa 9 (tratto più stretto); nessun dato dichiarato | **Non confermata**: il collo misurato è più sottile |
| Pedone: testa ⌀16 | stima set utente circa 15 | **Compatibile** (entro l'incertezza) |
| Canale a 30 / 34 / 38 mm | vedi sotto | **Da rivedere se si vuole servire più set** |
| Luce guida curva ↔ corpo ≥ 2 mm | con collo circa 9 mm la luce disponibile è maggiore di quanto previsto con 12 | **Non contraddetta**; verificare con la striscia di carta |
| Pezzi da torneo zavorrati sul fondo (baricentro basso) | peso e baricentro **non misurati**; un solo rivenditore dichiara pezzi zavorrati con perno di ferro | **Nessun dato**: è la premessa dell'intero meccanismo |

## Canale e base del pedone

Con base del pedone dichiarata tra 25,5 e 33 mm (valori: 25,5 · 28 · 29 · 29 · 30 · 31 · 32 · 33):

- Canale **30 mm**: passano senza gioco solo i pedoni con base inferiore a 30 (4 set su 8); uno è
  esattamente 30 (gioco zero) e tre non passano.
- Canale **34 mm**: passano tutti, ma il più largo (33) ha solo 0,5 mm per lato.
- Canale **38 mm**: passano tutti con almeno 2,5 mm per lato.
- Col pedone del set dell'utente (base stimata circa 27): gioco per lato di circa 1,5 / 3,5 / 5,5 mm.

La guida è pensata per un set preciso: prima di cambiare le quote conviene **misurare la base
del pedone di quel set** con la striscia di carta (precisione circa ±0,3 mm) e poi scegliere il
canale. Nessuna di queste quote va considerata **validata** senza una prova fisica.

## Osservazioni sui dati

- Il cavallo è spesso più alto del nominale FIDE: 6 set dichiarati su 8 superano il +10% (68–77 mm
  contro 60; gli altri due sono 61 e 62). Il cavallo del set dell'utente (circa 59) è entro la tolleranza.
- Il pedone ha spesso un rapporto base/altezza del 53–65%, sopra il 40–50% che la norma indica
  come regola generale: la deviazione è comune e non indica un errore dei dati.
- Torre del set dell'utente: la prima foto ravvicinata dava 47 mm (non attendibile); con la foto a
  inquadratura intera risulta circa 50 mm (±3), appena sopra il pedone (48,5): la differenza è
  entro l'incertezza, quindi l'ordine FIDE torre > pedone non si può né confermare né escludere.
