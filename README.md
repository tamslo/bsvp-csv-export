# Konfigurator CSV Export

Python-basierter BSVP Export von CSV Dateien.

## Installation

Es wird Python 3 benötigt, das auf der [offiziellen Python Website](https://www.python.org/downloads/) heruntergeladen werden kann. Um Python aus der Kommandozeile ausführen zu können, muss das Installationsverzeichnis von Python zur `PATH` Variable hinzugefügt werden.

## Ausführung

Für die manuelle Ausführung muss zunächst die Kommandozeile gestartet werden, indem man zum Beispiel `WINDOWS + R` drückt, `cmd` eingibt und bestätigt. Dann muss in das Verzeichnis gewechselt werden, in dem die Python Datein liegen, wo das Skript `main.py` ausgeführt werden kann.

```
cd  <Pfad zum Export Ordner>
python main.py
```

Die erstellten CSV Dateien werden im in der `config.json` angegebenen Ordner gespeichert, der angelegt wird, wenn er noch nicht vorhanden ist. Der jeweils letzte Export wird in den angegebenen Archiv-Ordner verschoben.

Wenn eine PROD Datei nicht bearbeitet werden konnte, steht in der Ausgabe, dass sie übersprungen wurde. Gründe dafür sind:

* Der PROD Ornder und die PROD Datei haben unterschiedliche Namen (PROD_UNTERSCHIEDLICH)
* Die PROD Datei enthält keine TECHDATA (KEIN_TECHDATA)
* Die TECHDATA enthält keinen Produkttyp (KEIN_PRODUKTTYP)

_TODO Automatische Ausführung mit Windows Aufgabenplanung_

## Konfiguration

Die Kofigurations-Dateien sind im JSON Format hinterlegt. Beim JSON Format empfiehlt es sich, mit einem Editor zu arbeiten, der auf Syntax-Fehler aufmerksam macht.

In `config.json` werde allgemeine Einstellungen spezifiziert. Bei der Angabe von Verzeichnissen ist darauf zu achten, dass sie mit einem `/` enden.

Die JSON Dateien für die Export-Konfigurationen liegen in `configs`. Der Dateiname der jeweiligen JSON Datei bestimmt den Dateinamen der CSV Datei, die erstellt wird (Bsp. `Kühlschränke.json` wird zu `Kühlschränke.csv`). Als Felder werden der Produkttyp und Attribute angegeben, die exportiert werden sollen.

Der Produkttyp muss so angegeben werden, wie er in den BSVP-Produkt-Dateien steht, allerdings ohne HTML kodierte Zeichen (Bsp. `PUM::Produkttyp::K&uuml;hlregal`, in der Konfiguration steht `"Kühlregal"`).

Die Attribute werden als Key-Value-Paar angegeben, wobei der Key das Attribut so wie es in den BSVP-Produkt-Dateien steht ist (Bsp. `PUM::Anzahl Regalböden`, der Key ist `"Anzahl Regalböden"`). Der Value ist der Name, der als Feld-Bezeichner in der CSV Datei steht (Bsp. `"anzahl_regalboeden"`).

## Fehlerbehebung

_Hier können häufig auftretende Fehler und ihre Lösung beschrieben werden_

## Kontakt

Bei Fragen und Problemen mit dem Export meldet euch gerne bei mir unter tamaraslosarek@gmail.com.
