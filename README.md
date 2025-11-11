# Lab 08

#### Argomenti

- Utilizzo Pattern MVC
- Utilizzo dei Package
- Utilizzo di mysql-connector-python (suggerita v8.4.0)
- Utilizzo del Pattern DAO
- Utilizzo dell'Object Relational Mapping (ORM)
- Algoritmi di Ricorsione

---
> **❗ ATTENZIONE:** 
>  Ricordare di effettuare il **fork** del repository principale, quindi clonare su PyCharm il **repository personale** 
> (https://github.com/my-github-username/Lab08) e non quello principale.
> 
> In caso di dubbi consultare la guida caricata nel lab02: 
> https://github.com/Programmazione-Avanzata-2025-26/Lab02/blob/main/Guida.pdf

---

##  Consumi Energetici e Pianificazione Interventi 
Progettare e realizzare un programma che gestisca le informazioni sui consumi energetici giornalieri di due impianti 
industriali (Impianto A e Impianto B) e che consenta di pianificare nel modo più efficiente gli interventi di 
manutenzione, individuando, per un periodo di più giorni la sequenza ottimale di impianti su cui operare, 
in modo da minimizzare il costo complessivo derivante dai prezzi dell’energia e dagli spostamenti tra i due impianti.

Il programma utilizza il database fornito, denominato `gestione_energia.sql`, che contiene due tabelle principali: 
- `impianto`: contiene le informazioni sui due impianti (Impianto A e Impianto B):
  - id
  - nome 
  - indirizzo 

- `consumo`: contiene i dati giornalieri di consumo dei due impianti per tutto l’anno 2026:
  - data 
  - kwh (il consumo in kWh)
  - id_impianto

![relazione_db.png](img/relazione_db.png)

L’applicazione, sviluppata in Python, deve permettere di:
- Interrogare la base dati per ottenere i **consumi energetici medi** nel corso di un **mese specifico** per entrambi 
gli impianti; 
- Calcolare, attraverso un algoritmo di ottimizzazione ricorsiva, la sequenza di giornate più conveniente per 
pianificare gli interventi tecnici di manutenzione sui due impianti **nei primi 7 giorni di un mese selezionato**. 
L’obiettivo del programma è ottimizzare la pianificazione settimanale delle attività, decidendo giorno per giorno su 
quale impianto operare, in modo da ridurre al minimo il costo totale derivante dai consumi energetici e dagli 
spostamenti del tecnico tra i due impianti.

##  Funzionalità Richieste
Nel progetto di base, l'interfaccia grafica (file `view.py` e `controller.py`) è già implementata con il seguente layout:
![layout.png](img/layout.png)
A partire dal layout proposto le funzionalità richieste sono le seguenti:

### (1) **Calcolo dei consumi medi mensili (usando l’ORM)**
L’applicazione deve permettere all’utente di: 
- Selezionare un mese dell’anno (valore intero tra 1 e 12), tramite un Dropdown; 
- Premendo un pulsante (“Consumo Medio”) visualizzare tramite una ListView il valore medio del consumo giornaliero 
di energia elettrica (in kWh) per il mese selezionato dal Dropdown, per ciascuno dei due impianti presenti nel 
database. 

>💡 **Esempio**: L’utente seleziona il mese “1” → il programma mostra il consumo medio giornaliero di elettricità a 
> gennaio per Impianto A e Impianto B. 
![consumo_medio.png](img/consumo_medio.png)

### (2) **Problema di ottimizzazione (algoritmo ricorsivo)** 
Sapendo che nel database sono presenti due impianti (A e B). Si supponga che un tecnico debba effettuare interventi 
sui due impianti per i primi 7 giorni in uno specifico mese selezionato tramite Dropdown. 

Ogni giornata di lavoro comporta un costo operativo, determinato da due componenti: 
- **Un costo fisso di 5€** ogni volta che il tecnico si sposta da un impianto all’altro;
- **Un costo variabile**, pari al consumo energetico medio dell’impianto nel giorno considerato (il valore kWh 
prelevato dal database).

Si desidera visualizzare, premendo un pulsante ("Mostra sequenza"), la sequenza ottimale di interventi, cioè stabilire, 
per ciascuno dei primi 7 giorni di un mese selezionato, su quale dei due impianti operare, in modo da minimizzare il 
costo complessivo derivante sia dal consumo energetico giornaliero sia dai costi di spostamento del tecnico 
tra gli impianti. 

>💡 **Esempio**: L’utente seleziona il mese “1” → il programma mostra la sequenza di impianti (tra A e B) sui quali il 
> tecnico deve effettuare gli interventi per minimizzare il costo totale (anch'esso mostrato) nella prima settimana 
> di gennaio (da Giorno 1 a Giorno 7).
![calcola_sequenza.png](img/calcola_sequenza.png)

##  Nota Bene
Per pensare come impostare la **ricorsione**, è consigliato utilizzare lo schema seguente. 
Può esser utile ragionare su carta per capire come impostare l’algoritmo.

```code
def recursion(..., level):
    # 🟤 E - istruzioni che dovrebbero essere sempre eseguite (raramente necessarie)
    do_always(...)
    
    # 🟢 A
    if terminal_condition:
        do_something(...)
        return ...
    
    for ...: # un loop, se necessario
        # 🔵 B
        compute_partial()
        
        if filter: # 🟡 C - Se necessario filtrare prima di procedere con la ricorsione
            recursion(..., level  +1)
        
        # 🟣 D
        back_tracking()
```
---

## Materiale Fornito
Il repository del lab08 è organizzato con la struttura ad albero mostrata di seguito e contiene tutto il necessario per 
svolgere il laboratorio:

```code
Lab08/
├── database/
│   ├── __init__.py
|   ├── connector.cnf 
|   ├── DB_connect.py 
│   ├── consumo_DAO.py
│   └── impianto_DAO.py
│
├── model/
│   ├── __init__.py
│   ├── model.py (DA MODIFICARE) 
│   ├── consumo_DTO.py 
│   └── impianto_DTO.py (DA MODIFICARE)
│
├── UI/
│   ├── __init__.py
│   ├── alert.py
│   ├── controller.py
│   └── view.py
│
├── gestione_energia.sql (DA IMPORTARE)
└── main.py (DA ESEGUIRE)
 ```
