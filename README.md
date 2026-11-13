# Guida gravitazionale per pezzi degli scacchi — prototipo in cartone

Prototipo **sperimentale** che riceve pezzi degli scacchi mescolati e prova a portarli
in posizione verticale sfruttando solo la gravità. Tre moduli: **A** imbuto di
alimentazione, **B** rampa con guide e raddrizzatore, **C** tratto di uscita verticale.

> **Avviso onesto (obbligatorio).** Questo NON è un meccanismo validato. La gravità
> **non** raddrizza un pezzo da qualunque orientamento. Il raddrizzatore (combi `B4`
> + striscia `B5`) è una **prima ipotesi di forma**, pensata per essere osservata,
> regolata e — se serve — **ritagliata di nuovo** dopo le prime prove. Alcuni
> orientamenti di partenza resteranno probabilmente irrecuperabili: è previsto.

---

## 1. Principio di funzionamento (sperimentale)

I pezzi da torneo sono **zavorrati sul fondo**: il baricentro è basso. Il prototipo
cerca di sfruttare questo fatto.

1. **Imbuto (A):** si versano pochi pezzi; le pareti inclinate li convogliano verso
   un'uscita stretta e **regolabile** (paratia `A5`) che cerca di farli entrare in
   rampa **uno alla volta**. L'uscita non scende mai sotto i 50 mm liberi, così il
   **re** (base ⌀50) non si blocca mai in modo irrimediabile.
2. **Rampa + raddrizzatore (B):** il piano è inclinato (regolabile 15–25°). Due
   **guide inferiori** (`B3`) formano un **canale** che contiene la base del pedone e
   lo tiene allineato. Una **guida curva superiore** (striscia di cartoncino `B5`
   tesa fra due combi `B4`) scende dall'ingresso verso l'uscita: accompagna il corpo
   del pezzo e, insieme a una **soglia/gradino removibile** che fa da perno, cerca di
   far ruotare il pezzo con la **base in basso** (più pesante) e il **corpo in alto**,
   fino alla verticale.
3. **Uscita (C):** un canale rettilineo con guide laterali regolabili mantiene il
   pezzo in piedi e lascia osservare il comportamento, facendolo avanzare in fila.

Le parti più critiche (inclinazione, larghezza del canale, altezza/curva della guida
superiore, posizione della soglia) sono **tutte regolabili senza ricostruire nulla**.

---

## 2. Come stampare le sagome (scala 1:1)

> **Nota (repo GitHub):** la cartella `svg/` **non è versionata** — in un clone pulito
> non esiste finché non esegui `python3 genera_svg.py`. In ogni Pull Request la CI la
> rigenera e pubblica SVG e **anteprime PNG** come *artifact*. Vedi [AGENTS.md](AGENTS.md).

I file (una volta generati) sono in `svg/`:

- **`guida-pezzi-tutto.svg`** — documento unico multi-pagina (compatibile Inkscape:
  le 11 pagine sono affiancate, con i riquadri pagina già definiti).
- **`foglio-01.svg` … `foglio-11.svg`** — un file per ogni foglio A4 (comodi per la
  stampa diretta a 100%).

**Regole di stampa (fondamentali):**

1. Stampa **A4**, **senza adattamento** ("Dimensioni effettive" / "100%" / "Scala
   100", MAI "Adatta alla pagina").
2. Su ogni foglio c'è una **barra "SCALA DI CONTROLLO"**: col righello deve misurare
   **esattamente 100 mm**. Se non è 100 mm, correggi lo zoom di stampa e ristampa.
3. I **crocini tratto-punto** agli angoli servono ad allineare i fogli fra loro.
4. La **cornice grigia** è il margine di stampa: **non si taglia**.

**Legenda linee:**

| Tratto | Significato |
|---|---|
| Continuo | **Taglio** |
| Tratteggiato (blu) | **Piega** |
| Tratto-punto (rosso) | Riferimento di **allineamento / registro** |
| Retino arancio | **Zona da incollare** (linguetta) |

Ogni sagoma riporta **codice**, **nome**, **quantità**, **materiale** e indicazioni
di **verso** (frecce "verso valle / uscita").

**Mappa dei fogli:**

| Foglio | Contenuto |
|---|---|
| 1 | Copertina, legenda, indice delle parti |
| 2 | **Vista d'assieme con i codici** di tutti i componenti (laterale + sezione + dall'alto) |
| 3 | **Montaggio moduli A e B** — esploso + passi affiancati |
| 4 | **Montaggio modulo C e unione** dei moduli — esploso + passi |
| 5 | Tavola quotata (mm) |
| 6 | Sagome: `BP1` |
| 7 | Sagome: `B1`, `C1` |
| 8 | Sagome: `A5`, `A1` |
| 9 | Sagome: `B6`, `A3`, `B4` |
| 10 | Sagome: `B2`, `B5`, `C2`, `B3` |
| 11 | Sagome: `A6` |

> **Niente duplicati:** ogni parte è disegnata **una volta sola**. Dove ne servono
> più copie, l'etichetta della sagoma lo dice: es. «Parete laterale rampa
> **(RITAGLIARNE 2)**». Sono 13 disegni per 21 pezzi fisici.
>
> L'assegnazione parte→foglio è generata automaticamente: se rigeneri lo script può
> cambiare. Fai fede ai **codici** stampati su ogni sagoma, non al numero di foglio.
> Nessuna singola parte è spezzata fra due fogli (stanno tutte in un A4), quindi non
> servono linee di giunzione interne alle parti.

---

## 3. Vista generale dell'assieme e montaggio

Il **foglio 2** è la **vista d'assieme con i codici**: ogni componente (A1, A3, A5,
A6, B1, B2, B3, B4, B5, B6, BP1, C1, C2) è richiamato con una **linea di riferimento**
su tre viste — laterale, sezione A-A del canale, dall'alto. Così i codici delle sagome
si ritrovano nel disegno d'insieme.

I **fogli 3 e 4** sono la **guida di montaggio visiva**: ogni modulo è disegnato in
**esploso** con i codici e, accanto, i **passi numerati** (foglio 3 = moduli A e B;
foglio 4 = modulo C e unione dei tre moduli). Gli stessi passi, per esteso, sono qui
al §7.

In sintesi lo schema di flusso è:

```
   [A imbuto]
       |  (i pezzi cadono)
       v
   =========================  <- B rampa INCLINATA (15-25 gradi)
    ( ( (  B5 guida curva  ) ) )     la base resta nel canale (B3),
   -------------------------         il corpo viene accompagnato su
          ^ soglia/perno            fino alla verticale
       |
       v
   [C uscita verticale] -> pezzi in piedi, in fila
```

Flusso del pezzo: **imbuto → rampa (raddrizzamento) → uscita**.

---

## 4. Tavola quotata (quote principali in mm)

Dettaglio sul **foglio 3** (sezione del canale + profilo laterale). Valori chiave:

| Elemento | Quota |
|---|---|
| Pedone di riferimento | H 48 · base ⌀30 · collo ⌀12 · testa ⌀16 |
| Re (ingombro da non bloccare) | base ⌀50 |
| Imbuto: apertura superiore | 140 × 110 |
| Imbuto: uscita (a paratia aperta) | 60 × 60 · altezza 90 |
| Rampa `B1` | 120 × 180 |
| Pareti rampa `B2` | h 45 |
| Guide base `B3` → **canale** | h 16 · canale regolabile **30 / 34 / 38** |
| Combi guida curva `B4` | altezza ingresso **~60** → uscita **~22** |
| Striscia guida curva `B5` | 150 × 42 (cartoncino, da curvare ad arco) |
| Gambe inclinazione `B6` | gradini **15° / 20° / 25°** |
| Base `BP1` | 140 × 190 |
| Uscita `C1` → canale | 60 × 110 · canale **30 / 34 / 38** |
| Guide uscita `C2` | h 22 |
| **Luce minima guida curva ↔ corpo** | **≥ 2 mm** (il collo è ⌀12: non schiacciarlo) |

---

## 5. Elenco delle parti

| Cod. | Componente | Q.tà | Materiale |
|---|---|---:|---|
| A1 | Imbuto parete fronte/retro | 2 | cartone ondulato |
| A3 | Imbuto parete laterale | 2 | cartone ondulato |
| A5 | Paratia regolabile | 1 | cartone ondulato |
| A6 | Guida paratia | 2 | cartone ondulato |
| B1 | Piano rampa | 1 | cartone ondulato rigido |
| B2 | Parete laterale rampa | 2 | cartone ondulato |
| B3 | Guida inferiore base | 2 | cartone ondulato |
| B4 | Combo guida curva | 2 | cartone ondulato |
| B5 | Striscia guida curva | 1 | cartoncino sottile |
| B6 | Gamba inclinazione | 2 | cartone ondulato spesso (2–3 strati) |
| BP1 | Base d'appoggio | 1 | cartone ondulato rigido |
| C1 | Piano uscita | 1 | cartone ondulato rigido |
| C2 | Guida laterale uscita | 2 | cartone ondulato |

**Totale:** 13 parti distinte, **21 pezzi fisici** da ritagliare.

---

## 6. Materiali e attrezzi

- Cartone ondulato rigido (base, piani, pareti) — da scatole da imballo.
- Cartoncino sottile (la sola striscia curva `B5`) — es. una cartelletta.
- Forbici o taglierino + base da taglio, righello metallico.
- Nastro di carta (preferito: si stacca e riposiziona) e/o colla.
- Scarti di cartone per **distanziatori e rinforzi**.
- **Niente** motori, elettronica o stampa 3D.

Suggerimento: per le gambe `B6` e la base `BP1`, incolla **2–3 strati** di cartone
per avere rigidità.

---

## 7. Assemblaggio passo-passo

**Preparazione**
1. Stampa e verifica la barra 100 mm. Ritaglia tutte le sagome lungo le **linee
   continue**; incidi leggermente (senza tagliare) le **linee tratteggiate** e piega.

**Modulo A — imbuto**
2. Prendi `A1`×2 (fronte/retro) e `A3`×2 (laterali). Accostali a formare una piramide
   tronca rovesciata: lato largo in alto, uscita 60×60 in basso.
3. Unisci i quattro spigoli con **nastro** sui lati obliqui (usa le tacche tratto-punto
   di mezzeria per tenerli dritti). L'imbuto deve stare in piedi da solo.
4. Incolla `A6`×2 ai bordi dell'uscita in modo da creare **due asole**: la paratia
   `A5` ci scorre dentro e, alzandola/abbassandola, **regola l'apertura**.

**Modulo B — rampa**
5. Sul piano `B1` individua le linee tratto-punto: pareti (`B2`), canale (`B3` a
   30/34/38), combi (`B4`), soglia.
6. Piega la linguetta di `B2`×2 e **fissale** lungo le due linee delle pareti (prima
   con nastro: così resta regolabile).
7. Piega la linguetta di `B3`×2 e fissale lungo la coppia di linee del canale che
   preferisci. **Parti da 38 mm** (più largo) e stringerai dopo.
8. Piega la linguetta dei combi `B4`×2 e incollali **in piedi**, uno per lato, lungo
   le linee "combo B4" (lato alto verso l'ingresso).
9. Curva la striscia `B5` ad arco (concavità in basso) e **appoggiala/fissala** sul
   bordo superiore dei due combi: è la guida curva superiore.
10. Ritaglia una strisciolina di scarto per la **soglia/gradino removibile** e
    appoggiala (solo nastro) sulla linea "soglia" vicino all'uscita.

**Modulo C — uscita**
11. Su `C1` fissa le guide `C2`×2 lungo le linee del canale (stessa larghezza del
    canale della rampa).

**Unione dei moduli (base BP1)**
12. Fissa la rampa `B1` alla base `BP1` lungo la linea "cerniera" con una striscia di
    nastro: fa da **cerniera**, così puoi cambiare inclinazione.
13. Metti le gambe `B6`×2 sotto il lato alto della rampa, appoggiate sul gradino
    dell'angolo scelto (parti da **20°**).
14. Posiziona il modulo `C` nell'impronta tratteggiata, **a filo** sotto l'uscita
    della rampa, e fissalo con nastro.
15. Metti l'imbuto `A` sopra l'ingresso della rampa, sostenuto da due montanti di
    scarto, in modo che l'uscita cada **dentro** il canale.

Tutte le unioni "critiche" sono **a nastro**: servono a spostare e regolare.

---

## 8. Regolazioni iniziali suggerite

| Parametro | Dove | Valore di partenza | Campo di prova |
|---|---|---|---|
| Inclinazione rampa | gambe `B6` | **20°** | 15° → 25° |
| Larghezza canale base | guide `B3` | **34 mm** | 30 / 34 / 38 |
| Altezza guida curva all'ingresso | combi `B4` | **~60 mm** | 50 → 65 |
| Altezza guida curva all'uscita | combi `B4` | **~22 mm** | 18 → 26 |
| Luce guida curva ↔ corpo | `B5` vs piano | **≥ 2 mm** | mai < 2 mm |
| Apertura imbuto | paratia `A5` | **~35 mm** | 30 → 55 (55 per il re) |
| Larghezza canale uscita | guide `C2` | **34 mm** | 30 / 34 / 38 |

Regola **un parametro alla volta** e annota cosa cambia.

---

## 9. Sequenza di prove

Prova il pedone nei tre orientamenti d'ingresso richiesti, **uno per volta**, a mano
(prima di usare l'imbuto):

1. **Pedone già verticale.** Deve attraversare rampa e uscita **restando in piedi**.
   *Se cade:* canale troppo largo o guida curva troppo bassa (lo urta). Allarga la
   luce o stringi il canale.
2. **Pedone coricato, base rivolta verso valle (uscita).** È il caso favorevole: la
   base pesante arriva per prima, la soglia dovrebbe farlo **impennare in verticale**.
   *Se non si alza:* abbassa l'uscita della guida curva, oppure alza la soglia, oppure
   aumenta l'inclinazione.
3. **Pedone coricato, base verso monte (ingresso).** È il caso **difficile**: la testa
   arriva per prima. Osserva se la guida curva + soglia riescono a ribaltarlo
   base-in-basso. *Spesso non basta:* annota la percentuale di successo; valuta una
   soglia più marcata o un profilo di `B4` più curvo (vedi §10).

Poi ripeti versando **3–5 pezzi mescolati** dall'imbuto e conta quanti escono in
piedi. Infine prova con un **pezzo grande** (es. torre/re) solo per verificare che
**non si incastri** (non si pretende che li raddrizzi).

---

## 10. Inceppamenti e modifiche

| Sintomo | Causa probabile | Modifica |
|---|---|---|
| Il pezzo **non scivola** / si ferma | inclinazione bassa, attrito | alza a 25°; liscia il canale; riduci i contatti |
| Il corpo **si incastra** fra guida curva e piano | luce troppo piccola | **alza `B5`** (luce ≥ 2–3 mm); mai sotto 2 mm |
| Il pezzo **cade di lato** | canale troppo largo | stringi `B3` (34 → 30) |
| Entrano **due pezzi insieme** | apertura imbuto larga | abbassa la paratia `A5`; aggiungi un dentino che fa passare uno per volta |
| Il pedone **non si raddrizza mai** | curva/soglia inefficaci | ritaglia `B4` sul **profilo alternativo** (più curvo) stampato sulla sagoma; alza la soglia; sposta la soglia verso valle |
| Il **re/pezzi grandi si bloccano** | uscita imbuto troppo stretta | apri la paratia a ~55 mm |
| Il pezzo **rimbalza fuori** dalla rampa | pareti basse | usa `B2` più alte (ritaglia una striscia e incolla sopra) |

Filosofia: la soglia e i combi `B4` sono **sacrificabili**. È normale rifarli 2–3
volte: costano pochi minuti e un ritaglio di cartone.

---

## 11. Verifica tecnica (cosa è stato controllato, e cosa NO)

**Controllato automaticamente dallo script** (`genera_svg.py`):
- Tutti i tracciati sono **chiusi per costruzione** (rettangoli/poligoni/path).
- Ogni file SVG è **XML ben formato** (validazione in fase di scrittura).
- Ogni parte **rientra nell'area utile A4** (controllo degli ingombri).
- **Nessuna sovrapposizione** fra parti sullo stesso foglio.
- Le quote mostrate derivano dagli **stessi valori** usati per disegnare (coerenza).
- Spessori minimi: la parte più sottile è la guida `B3` (16 mm) + piede piegato →
  adatta al cartone; la striscia `B5` è **volutamente** sottile (deve curvarsi).

**NON verificato (richiede prove fisiche — vedi §9):**
- Che la guida curva raddrizzi effettivamente il pedone. **È sperimentale.**
- Le percentuali di successo nei tre orientamenti.
- Le tolleranze reali del tuo cartone (spessore, attrito).

> Coerente con il vincolo del brief: **il meccanismo non è dichiarato validato.**

---

## 12. Rigenerare o modificare le sagome

```bash
cd guida-gravitazionale-pezzi
python3 genera_svg.py      # riscrive svg/foglio-*.svg e svg/guida-pezzi-tutto.svg
```

Le misure chiave sono tutte nel blocco **`CONFIG`** in cima a `genera_svg.py`
(valori in mm, con commenti): imbuto, paratia, rampa, combi `B4`, striscia `B5`,
gambe `B6`, base, uscita. I builder di parte (`ramp_floor`, `comb_part`,
`prop_part`, …) leggono da lì. Per cambiare, ad esempio, la larghezza del canale
o i gradini delle gambe, modifica `CONFIG` e rigenera: lo script
rifà impaginazione, quote, indice e barra di scala, e **ri-verifica** ingombri e
sovrapposizioni.

---

## 13. Contribuire (agenti AI + revisione umana)

Il progetto è pensato per essere portato avanti da **agenti AI con verifica umana**.
Regole operative complete in [AGENTS.md](AGENTS.md). In breve:

- Si modifica **solo** `genera_svg.py`; gli SVG sono **output generati** (non versionati).
- Si lavora su **branch → Pull Request**, mai push diretto su `main`.
- La CI [`verify`](.github/workflows/verify.yml) rigenera le sagome, le auto-verifica e
  carica **anteprime PNG** come *artifact* per la revisione.
- Un **revisore umano** (CODEOWNERS) guarda le anteprime — ed eventualmente stampa e
  prova fisicamente — poi approva e mergia.
- **Nessuna modifica al meccanismo è "validata" senza una prova fisica umana.**

