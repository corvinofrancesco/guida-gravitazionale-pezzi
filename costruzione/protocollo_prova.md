# Protocollo di prova e scheda di feedback

Scopo: raccogliere dati ripetibili sul comportamento dei pezzi nella guida. **Nessun risultato
qui «convalida» il meccanismo**: serve a decidere quali parti ritagliare di nuovo e come.

## Prima di ogni sessione

1. Registra: inclinazione (15/20/25°), larghezza canale (misurata), altezza guida curva
   (ingresso/uscita), apertura paratia, posizione soglia.
2. Fissa il supporto del telefono e filma i lanci con la stessa inquadratura.
3. Cambia **un solo parametro alla volta** rispetto alla sessione precedente.

## Le prove

- **Pezzo**: pedone per primo; poi torre, alfiere, cavallo, regina, re.
- **Orientamenti di partenza**: 1) già verticale · 2) coricato con la base verso valle ·
  3) coricato con la testa verso valle.
- **Lanci**: 10 per ogni combinazione pezzo/orientamento/regolazione.
- **Esito di ogni lancio**: `in_piedi` · `coricato` · `incastrato` · `fuori_guida`.

## Dove registrare

File `dati/prove_guida.csv` con queste colonne (valori senza virgole; usa il punto e virgola):

`data, sessione, pezzo, orientamento, inclinazione_gradi, canale_mm, guida_ingresso_mm,
guida_uscita_mm, apertura_paratia_mm, lanci, in_piedi, coricato, incastrato, fuori_guida, note`

Una riga per ogni combinazione di condizioni. Per le prove su campione (`procedure.md`, passo 0)
usa `pezzo = campione` e descrivi il risultato in `note`.

## Come leggere i risultati (senza esagerare)

- Un orientamento con 10 lanci su 10 `in_piedi` è un indizio, **non una validazione**.
- Se il caso 1 (pedone già verticale) peggiora dopo una modifica, la modifica va scartata.
- Registra anche i fallimenti: servono a capire cosa ritagliare di nuovo.
