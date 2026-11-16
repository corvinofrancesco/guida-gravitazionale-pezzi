# Requisiti: dai dati e dal materiale

## 1. Quote che la struttura deve rispettare (dai dati in `dati/`)

Valori **stimati da foto o dichiarati dai rivenditori**, non misurati con strumenti (vedi
`dati/README.md`). Il set dell'utente è stato stimato da foto, con incertezza di ±1,5–3 mm.

| Grandezza | Valore | Stato | Conseguenza per il prototipo |
|---|---|---|---|
| Base del re | 34–45 mm (12 set); stima set utente ~36 | dichiarato/stimato | il passaggio più stretto non scende sotto 50 mm: margine ≥ 5 mm sul re più largo |
| Base del pedone | dichiarata 25,5–33 mm; stima set utente ~27 | dichiarato/stimato | il canale deve essere almeno 1 mm più largo della base per lato |
| Collo del pedone | stima ~9 mm (non 12) | stimato | la luce della guida curva dipende da questo valore |
| Altezza pedone | 46–53 mm; stima set utente 48,5 | dichiarato/stimato | altezze di guida e soglia |
| Peso e baricentro | **non misurati** | — | premessa del meccanismo: senza questi dati non si sa se il pezzo si raddrizza |

**Misure da prendere prima di fissare le quote** (con gli strumenti dell'inventario):
1. base del pedone con la striscia di carta (circonferenza ÷ π, precisione ~±0,3 mm);
2. peso di ogni pezzo con la bilancia da cucina;
3. baricentro: pezzo coricato in equilibrio sul bordo di un righello.

## 2. Canali e gioco

Canale di progetto 30 / 34 / 38 mm. Con il pedone del set dell'utente (base stimata ~27 mm)
il gioco per lato è circa 1,5 / 3,5 / 5,5 mm. **Da verificare con la base misurata**: se la base
reale fosse 28,5 mm, il canale da 30 mm lascerebbe solo 0,75 mm per lato.

## 3. Cartone da 3 mm: effetti sulle quote (aperto)

Il generatore **non tiene conto dello spessore del cartone**. Punti da risolvere con un campione:

- **Larghezza del canale.** Le linee su `B1` indicano 30/34/38 mm tra le linee; le guide (`B3`) si
  fissano con linguette. Con guide da 3 mm la larghezza utile dipende da **quale faccia** si allinea
  alla linea. Regola provvisoria: la faccia **interna** della guida va sulla linea; se la sagoma
  segna il centro o il bordo esterno, il canale risulta più stretto di fino a 6 mm.
- **Pieghe e linguette.** Il cartone da 3 mm si piega male perpendicolarmente alle onde e tende a
  rompersi. Le linguette da 10–12 mm delle sagome potrebbero essere sostituite da **unioni di
  testa con nastro o graffette**. Da decidere con il campione di piegatura.
- **Altezze.** Guide da 16 mm e pareti da 45 mm stanno nelle sagome come altezza *netta*; il
  piano `B1` da 3 mm si somma alle altezze sotto la guida curva.
- **Guida curva `B5`.** Deve restare in **cartoncino sottile**: da 3 mm non si cura ad arco.
- **Precisione di taglio.** Il taglierino su 3 mm dà scostamenti di circa ±0,5–1 mm. I canali da
  30 mm hanno quindi poco margine: tagliare i bordi dei canali con più passate e verificare con
  il calibro.

Queste sono stime da esperienza generale, **non misure**: vanno confermate con il campione
(`procedure.md`, passo 0).

## 4. Requisiti di prova

- Pezzo di prova: **il pedone** del set dell'utente, poi gli altri.
- Una prova ripetibile: stessa altezza di caduta, stessa inclinazione, 10 lanci per condizione.
- Esito registrato in `dati/prove_guida.csv` (vedi `protocollo_prova.md`).
