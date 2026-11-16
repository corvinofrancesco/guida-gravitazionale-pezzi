# Procedure di costruzione

Indicazioni di lavoro per cartone da 3 mm. Dove non è dimostrato, il testo dice «da provare».

## Passo 0 — Campione di prova (obbligatorio prima di tagliare le parti vere)

Con un ritaglio di cartone da 3 mm e una stampa di prova (la pagina di una sagoma andrà bene):

1. **Spessore reale**: misura 5 punti del cartone con il calibro e annota media e variazione.
2. **Taglio**: taglia una striscia di 20 mm con righello metallico e lama nuova; conta le passate.
   Misura la larghezza con il calibro in tre punti: annota lo scostamento.
3. **Piega**: incidi a metà spessore una linea *parallela* alle onde e una *perpendicolare*;
   piega entrambe; annota quale regge e quale si rompe.
4. **Fissaggio**: prova nastro di carta, colla vinilica e graffetta su due strisce; annota la tenuta
   e se la graffetta passa senza rovinare il cartone.
5. **Esito**: scrivi i risultati in `dati/prove_guida.csv` (tipo `campione`) e adegua questa
   guida e `requisiti.md` ai risultati reali.

## 1. Stampa

- Stampa su A4 a **scala 100%** (su Mac «Scala 100%», non «Adatta in scala»). Controlla con il
  righello che la barra misuri 100 mm; ricorda i ~13 mm in alto che la DeskJet 2721e non stampa.
- Stampa una pagina alla volta e tieni il codice della parte visibile.

## 2. Trasferimento sul cartone

- Incolla la sagoma (carta) sul cartone con colla stick sottile o colla spray removibile, senza
  grinze: le grinze falsano le quote.
- Alternativa: ritaglia la sagoma in carta e usala come dima, ricalcando il bordo con la matita.
- Orienta le **onde del cartone** nel verso che serve alle pieghe (vedi il campione).

## 3. Taglio

- Righello **metallico**, lama nuova, tappetino sotto.
- Più passate leggere (3–5 per 3 mm), non una sola forzata.
- Tieni la lama inclinata sempre nello stesso verso per bordi coerenti.
- Taglia prima i bordi **interni** (aperture e asole), poi il perimetro.
- Nei canali, dove la quota è critica, controlla con il calibro dopo il taglio.

## 4. Pieghe

- Incisione parziale (circa metà spessore) sul lato esterno della piega, con la costa del
  taglierino o una punta senza filo, senza tagliare del tutto.
- Piega sul bordo di un tavolo, lentamente.
- Se il cartone si spezza, sostituisci la linguetta con un'unione di testa con nastro o graffette.

## 5. Fissaggio

| Unione | Metodo suggerito | Perché |
|---|---|---|
| Parti regolabili (canali, soglia, imbuto) | nastro di carta | si stacca e si riposiziona |
| Parti fisse (gambe B6, base BP1, strati incollati) | colla vinilica, graffette | tenuta |
| Cerniera rampa–base | nastro di carta o di tela | permette di cambiare inclinazione |

Le unioni critiche restano **a nastro**, come previsto nel README principale: servono a regolare.

## 6. Controlli a ogni modulo

| Modulo | Controlli |
|---|---|
| A — imbuto | sta in piedi da solo; la paratia scorre; l'uscita non scende sotto 50 mm |
| B — rampa | piano senza imbarcamenti; canale misurato con il calibro; luce guida curva ↔ corpo ≥ 2 mm |
| C — uscita | canale uguale a quello della rampa; allineato con l'uscita della rampa |
| Insieme | inclinazione impostata a 20°; nessuna parte si sposta toccando il piano |

## 7. Registro

Annota ogni costruzione: data, spessore misurato, quote reali dei canali, problemi di taglio e
di piega. Queste note servono a decidere come adeguare le sagome.
