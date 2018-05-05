# Konfigurator CSV Export

Python-basierter BSVP Export von CSV Dateien.

## Installation

Es wird Python 3 benötigt, das auf der [offiziellen Python Website](https://www.python.org/downloads/) heruntergeladen werden kann. Um Python aus der Kommandozeile ausführen zu können, muss das Installationsverzeichnis von Python zur `PATH` Variable hinzugefügt werden.

Außerdem müssen die beispielhaft gegebenen Konfigurationsdateien angepasst werden. Die `config.json.example` muss in `config.json` umbenannt und der Inhalt den Anforderungen angepasst werden. Für jede Export-Konfiguration muss eine Konfigutation in `configs/` angelegt werden, das Format ist unter [Konfiguration](#konfiguration) gezeigt.

## Ausführung

Für die manuelle Ausführung muss zunächst die Kommandozeile gestartet werden, indem man zum Beispiel `WINDOWS + R` drückt, `cmd` eingibt und bestätigt. Dann muss in das `root` Verzeichnis gewechselt werden, in dem die Python Datein liegen, wo das Skript `main.py` ausgeführt werden kann.

```
cd pfad/zum/root/verzeichnis && python main.py
```

Die erstellten CSV Dateien werden im in der `config.json` angegebenen Ordner gespeichert, der angelegt wird, wenn er noch nicht vorhanden ist. Der jeweils letzte Export wird in den angegebenen Archiv-Ordner verschoben.

Wenn eine `.prod` Datei nicht bearbeitet werden konnte, steht in der konfigurierten Log-Datei, dass sie übersprungen wurde. Gründe dafür sind:

* Der `.prod` Ordner und die `.prod` Datei haben unterschiedliche Namen (`PROD_UNTERSCHIEDLICH`)
* Die `.prod` Datei enthält keine Artikelnummer (`KEINE_ARTNR`)
* Die `.prod` Datei enthält kein `TECHDATA` Feld (`KEIN_TECHDATA`)
* Das `TECHDATA` Feld enthält keinen Produkttyp (`KEIN_PRODUKTTYP`)

_TODO Automatische Ausführung mit Windows Aufgabenplanung_

## Updates

Die neuste Version wird als ZIP-Archiv zur Verfügung gestellt. Zum Updaten den im Archiv enthaltenen Code in das `root` Verzeichnis kopieren. Dabei wird nur der Code überschrieben und keine Konfiguration, Daten oder Dateien, die vom Exporter erstellt werden.

## Konfiguration

Die Kofigurations-Dateien sind im JSON Format hinterlegt. Beim JSON Format empfiehlt es sich, mit einem Editor zu arbeiten, der auf Syntax-Fehler aufmerksam macht.

In `config.json` werde allgemeine Einstellungen spezifiziert. Bei der Angabe von Verzeichnissen ist darauf zu achten, dass sie mit einem `/` enden.

Die JSON Dateien für die Export-Konfigurationen liegen in `configs`. Der Dateiname der jeweiligen JSON Datei bestimmt den Dateinamen der CSV Datei, die erstellt wird (Bsp. `Kühlschränke.json` wird zu `Kühlschränke.csv`). Es werden der Produkttyp und Felder angegeben, die exportiert werden sollen.

Das Format sieht wie folgt aus:

```json
{
  "produkttyp": "Kühlschrank",
  "felder": {
    "ARTNR": "artikelnummer",
    "TECHDATA": {
      "0000226": "temperaturbereich_von_grad_celsius",
      "0000017": "anzahl_regalboeden"
    }
  }
}
```

Der Produkttyp muss so angegeben werden, wie er in den BSVP-Produkt-Dateien steht, allerdings ohne HTML kodierte Zeichen (Bsp. `PUM::Produkttyp::K&uuml;hlschrank`, in der Konfiguration steht `"Kühlschrank"`).

Die Felder werden als Key-Value-Paar angegeben, wobei der Key das Feld so wie es in den BSVP-Produkt-Dateien steht ist (Bsp. `"ARTNR"`). Der Value ist entweder der Name des Feldes wie er in der CSV Datei angegeben werden soll (Bsp. `"artikelnummer"`) oder weitere Key-Value-Paare, die zu exportierende Attribute spezifizieren, die im Feld enthalten sind (Bsp. innerhalb von `TECHDATA`). Hierbei wird als Key die numerische ID für das Attribut-Feld angegeben (Bsp. `"0000017"` für Anzahl Regalböden). Der Value ist der Name, der als Feld-Bezeichner in der CSV Datei steht (Bsp. `"anzahl_regalboeden"`).

## Fehlerbehebung

Hier sind Lösungen zu häufigen Fehlern aufgeführt, geordnet nach den Fehlerarten, die in der Kommandozeile ausgegeben werden.

### PermissionError

```
PermissionError: [WinError 32] The process cannot access the file because it is being used by another process
```

Es könnte sein, dass eine CSV Datei, die überschrieben werden soll noch in einem anderen Programm wie Excel geöffnet ist, bitte schließen und den Exporter erneut starten.

### JSONDecodeError

```
json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 19 column 5 (char 566)
```

Eine der JSON Konfigurationen enthält ein Komma in der letzten Zeile, das bitte entfernen.

## Kontakt

Bei Fragen und Problemen mit dem Export meldet euch gerne bei mir unter tamaraslosarek@gmail.com.
