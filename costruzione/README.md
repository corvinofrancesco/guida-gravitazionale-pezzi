# Costruzione del prototipo: materiali, utensili, procedure e prove

Questa cartella contiene **tutto ciò che serve per costruire e provare il prototipo a casa**,
prima di giudicare le sagome. Le sagome (`genera_svg.py`) dicono *cosa tagliare*; qui si
descrive *con che cosa, come e come si controlla il risultato*.

> **Avviso.** Il meccanismo non è validato (vedi [AGENTS.md](../AGENTS.md)). Quello che
> segue è un metodo di lavoro, non una garanzia: le indicazioni sul cartone da 3 mm sono
> **ipotesi da provare su un campione** prima di tagliare le parti vere.

**Obiettivo.** Raddrizzare i pezzi da torneo e farli cadere in posizione verticale, con un
prototipo da provare a casa.

## Percorso (nell'ordine)

| Passo | File | Cosa produce |
|---|---|---|
| 1. Inventario | [inventario.md](inventario.md) | cosa c'è, cosa manca, cosa si può acquistare |
| 2. Requisiti | [requisiti.md](requisiti.md) | quote da rispettare, ricavate dai dati, e effetti del cartone da 3 mm |
| 3. Distinta materiali | [distinta_materiali.md](distinta_materiali.md) | materiale e quantità per ogni parte (A1…C2) |
| 4. Procedure | [procedure.md](procedure.md) | stampa, taglio, piega, fissaggio, con controlli a ogni passo |
| 5. Prove | [protocollo_prova.md](protocollo_prova.md) | come provare e dove registrare i risultati |

Il **feedback sulle sagome** ha senso solo dopo i passi 3–4 e il campione di prova
(procedure.md, passo 0). I risultati delle prove vanno in `dati/prove_guida.csv`.

## Stato

- Inventario: compilato con le informazioni dell'utente (cartone 3 mm, taglierino, pinzatrice).
- Domande aperte: elencate in `inventario.md` e `requisiti.md`.
- Sagome: **non ancora adeguate** allo spessore del cartone (vedi `requisiti.md`, punto 3).
