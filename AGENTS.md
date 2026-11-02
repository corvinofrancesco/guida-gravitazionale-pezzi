# AGENTS.md — istruzioni per gli agenti AI

Questo file vale per **qualsiasi agente** (Claude Code, GitHub Copilot, Codex, Cursor…).
Leggilo prima di qualsiasi modifica. Le istruzioni qui **prevalgono** sui comportamenti
di default.

## Cos'è questo progetto

Prototipo **sperimentale** di una *guida gravitazionale per pezzi degli scacchi*
realizzabile in **cartone**: riceve pezzi disordinati e prova a portarli in verticale
sfruttando la gravità (tre moduli — imbuto, rampa con raddrizzatore, uscita).
Il deliverable sono **sagome di taglio in SVG, scala 1:1, su fogli A4**, prodotte da un
**unico generatore Python**. Dettagli completi nel [README.md](README.md).

## Regola numero uno (non negoziabile)

> **Il meccanismo NON è validato.** La gravità non raddrizza un pezzo da qualunque
> orientamento. Nessun agente può dichiarare "funzionante/validato" una geometria:
> solo una **prova fisica fatta da un umano** può farlo. Proponi modifiche come
> *ipotesi sperimentali* e lascia regolabili/ri-tagliabili le parti critiche.

## Architettura: il generatore è l'unica fonte di verità

- **Si modifica solo [`genera_svg.py`](genera_svg.py)** (misure in cima al file e nei
  singoli *builder* di parte: `ramp_floor`, `comb_part`, `prop_part`, `trapezoid_wall`,
  le pagine `assembly_page` / `montaggio_*` / `quote_page`, ecc.).
- **Gli SVG in `svg/` sono OUTPUT generati** e **non sono versionati** (`.gitignore`).
  **Non editarli mai a mano.** Si rigenerano con un comando.
- Nessuna dipendenza esterna: **solo libreria standard Python** (3.9+). Non aggiungere
  dipendenze senza motivo forte e senza dichiararlo nella PR.

## Come lavorare (ciclo minimo)

```bash
python3 genera_svg.py        # rigenera svg/ e stampa un report di auto-verifica
```

Il generatore **si auto-verifica** e fallisce (exit ≠ 0) se qualcosa non va:
- tutti i tracciati chiusi per costruzione;
- ogni file SVG è XML ben formato;
- ogni parte rientra nell'area utile A4;
- nessuna sovrapposizione tra parti sullo stesso foglio.
Se tocchi una misura, **rilancia il generatore** e controlla che il report sia pulito.

## Regole d'oro

1. **Lingua italiana** in codice, commenti, testi delle sagome e messaggi.
2. Rispetta la **legenda delle linee**: continuo = taglio · tratteggiato = piega ·
   tratto-punto = allineamento/registro · retino = incollaggio.
3. **Un disegno per parte**: la quantità si indica sull'etichetta ("RITAGLIARNE N"),
   non duplicando la sagoma.
4. Ogni componente citato nei **disegni d'assieme** deve avere il suo **codice
   richiamato** (A1, B3, …). La nomenclatura è inutile se non compare nei disegni.
5. Niente motori, elettronica o pezzi stampati in 3D: solo cartone, forbici, nastro.
6. Evita parti troppo sottili/fragili per il cartone.
7. Non introdurre una **vista prospettica come sostituto** delle sagome di taglio.

## Flusso di lavoro con verifica umana

- **Mai push diretto su `main`.** Lavora su un **branch** e apri una **Pull Request**.
- La CI (`.github/workflows/verify.yml`) a ogni PR: esegue il generatore, **rasterizza
  gli SVG in PNG** e li pubblica come *artifact* (`anteprime-png`, `sagome-svg`).
- Il **revisore umano** (CODEOWNERS) scarica le anteprime, le guarda, eventualmente
  stampa e prova fisicamente, poi **approva e mergia**. L'agente non mergia da solo.
- Compila la **checklist** del template di PR.

## Convenzioni PR/commit

- Messaggi in italiano, imperativi e sintetici (es. "rampa: riduci il canale a 32 mm").
- Una PR = una modifica coerente. Spiega **cosa** cambia e **cosa deve osservare/provare
  l'umano** (le modifiche al raddrizzatore vanno sempre provate fisicamente).
- Non committare file in `svg/` o `anteprime/` (sono ignorati apposta).
