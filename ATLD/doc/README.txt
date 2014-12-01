ATLD 1.0 - Analisi testuale, in parallelo su hosts remoti, per file  di grandi dimensioni.

IMPORTANTE: 
Applicazione sviluppata e testata su MacBookPro 13 Retina - Mac OSX 10.10 Yosemite.

* Breve descrizione dell'applicazione:

	Questo programma consente l'esecuzione di una analisi testuale, su hosts remoti, 
	di file testuali di grandi dimensioni.
	Sono presenti tre finestre, ognuna delle quali consente determinate azioni:
	- Finestra di setting del numero di hosts e del file di configurazione (opzionale).
	- Finestra di inserimento delle credenziali d'autenticazione per gli hosts remoti.
	- Finestra di analisi, in cui è possibile connettere gli hosts remoti, scegliere il 
	  file da analizzare, avviare l'analisi, salvare l'attuale configurazione 
	  dell'applicazione, salvare i risultati, e chiudere la finestra.

* Organizzazione delle cartelle

  All’interno della cartella ATLD sono presenti alcune directories, ognuna con una 
  particolare funzione:

  ../conf/ files di configurazione predefiniti o salvati dall’utente.
  ../doc/  tutti i files relativi alla documentazione del progetto.
  ../log/  files di log del programma.
  ../res/  risultati dell’analisi, costituiti da file testuali e grafici in formato svg.
  ../src/  file sorgenti del programa, scritti in Python3.4
  ../temp/ file temporanei creati durante l’analisi che verranno poi cancellati una volta 
  		   terminata l’analisi del testo.
  ../txt/  cartella con files da analizzare d’esempio. L’utente può scegliere se inserire 
  		   il proprio file da analizzare dentro questa directory o se sceglierlo 
  		   direttamente da un altra a piacimento.

* Requisiti / moduli per il funzionamento dell'applicazione (tutte le librerie
  elencate, sia nel caso in cui si specificato, che non, sono relative a Python 3.* ):
  
  Moduli di sistema:
  
  - sys
  - argparse
  - os
  - threading
  - socket
  - time
  - datetime
  - signal
  - collection
  - unittest
  
  
  Moduli non di sistema:
  
  Nota1: una volta scaricato il pacchetto, è necessario eseguire le seguenti operazioni:
  
  - Aprire il terminale.
  - Entrare nella cartella in cui è stato scaricato il pacchetto, es.: 'cd /Downloads'.
  - Scompattare l'archivio col comando 'tar -xzvf nome_archivio.tar.gz'
  - entrare nella cartella scompattata col comando 'cd /cartella_scompattata/'. 
  - installare la libreria col comando 'sudo python3 setup.py install'
  
  - pip --> https://pypi.python.org/pypi/pip
  - easy_install --> https://pypi.python.org/pypi/setuptools
  - Python3.* --> https://www.python.org/downloads/
  - NLTK --> http://www.nltk.org/install.html
  - Pyro4.* --> https://pypi.python.org/pypi/Pyro4/ - https://github.com/irmen/Pyro4
  - paramiko --> http://www.paramiko.org - https://pypi.python.org/pypi/paramiko/ - https://github.com/paramiko/paramiko
  - PyQt4.* --> http://pyqt.sourceforge.net/Docs/PyQt4/
  - pygal -->  https://pypi.python.org/pypi/pygal/ - https://github.com/Kozea/pygal
  
  Nota2: una volta installati i moduli 'pip' e/o 'easy_install' è possibile scaricare
         ed installare i moduli esterni di Python nei seguenti modi:
         - 'sudo pip install nome_modulo' es.: 'sudo pip install nltk'
         - 'sudo easy_install3 nltk' es.: 'sudo easy_install3 paramiko'
  
 * Esecuzione del programma e setting dei parametri di input.
 
   - 'python3 main.py -h' per visualizzare l'help.
 
   - Entrare nella cartella src/: 'cd src/'
   
   - Se si desidera eseguire il programma senza inserimento di parametri: 
     'python3 main.py' in questo modo il programma partirà senza alcuna impostazione.
     Sarà tuttavia possibile impostarle attraverso le finstre grafiche.
     
   - Se si desidera eseguire il programma con i parametri (2 modalità a disposizione): 
   
   	 	Prima modalità: 'python3 main.py -n [numero_hosts] -a [indirizzo1,indirizzo2,...]'
   	 				    es.: python3 main.py -n 2 - a user1@host1,user2@host2
   	 				    
   	 				    Nota: è possibile specificare anche uno solo dei due parametri 
   	 				          opzionali; il programma provvederà automaticamente al 
   	 				          setting adeguato del parametro mancante.
   	 				    
   	 	Seconda modalità: 'python3 main.py -c percorso_del_file_di_configurazione'
   	 					  es.: python3 -c ../conf/conf_6.conf
   	 					  
   	 					  Ricorda: i file di configurazione di default e quelli salvati
   	 					  		   sono all'interno della cartella /conf/ del programma.
   	 
 * Visualizzazione della documentazione:
   - ../doc/html/index.html
   - ../doc/manuale_di_utilizzo.pdf
   - ../doc/README.txt
  
