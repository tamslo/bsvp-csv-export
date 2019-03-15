# BSVP CSV Exporter

Python-basierter Exporter für die Umwandlung von BSVP zu CSV Dateien.

Trello: https://trello.com/b/ug9q2Eif/bsvp

Diese README sieht komisch aus? Dann öffne sie mit einem Editor mit Markdown-Erweiterung (z.B. Notepad++) oder mit einem Online-Viewer (z.B. [Github](https://jbt.github.io/markdown-editor/)).

Bei Fragen und Problemen mit dem Export meldet euch gerne bei mir unter tamaraslosarek@gmail.com.

1.  [Installation](#installation)
2.  [Updates](#updates)
3.  [Ausführung](#ausführung)
4.  [Konfigurationen](#konfigurationen)
    - [Allgemeine Einstellungen](#allgemeine-einstellungen)
    - [Export-Konfigurationen](#export-konfigurationen)
5.  [Fehlerbehebung](#fehlerbehebung)

<a name="installation" />

## Installation

1.  Python 3 installieren
    - Mit [offiziellem Installer](https://www.python.org/downloads/)
    - Installationsverzeichnis zur `PATH` Umgebungsvariable hinzufügen
2.  Aktuelle Version des Exporters aus dem Trello herunterladen
3.  Exporter in gewünschtes Verzeichnis verschieben (von jetzt an `EXPORTER_VERZEICHNIS` genannt)
4.  Verzeichnis für Export-Konfigurationen anlegen
5.  Konfigurationen aus dem Trello herunterladen oder neu anlegen
6.  Die `config.json.example` in `config.json` umbenennen und ggf. anpassen
7.  Eingabeaufforderung in `EXPORTER_VERZEICHNIS` öffnen und Abhängigkeiten mit `pip install -r requirements.txt` installieren

<a name="updates" />

## Updates

1.  Neue Version aus dem Trello herunterladen
2.  Inhalt in `EXPORTER_VERZEICHNIS` verschieben und vorhandene Dateien ersetzen, es wird nur der Code überschrieben, Konfigurationen und andere Daten bleiben so wie sie sind
3.  Ggf. Konfigurationen anpassen

<a name="ausführung" />

## Ausführung

1.  Kommandozeile starten (z.B. `WINDOWS + R` drücken, `cmd` eingeben und bestätigen)
2.  In das EXPORTER_VERZEICHNIS wechseln mit `cd EXPORTER_VERZEICHNIS`
3.  Server starten mit `python server.py`
4.  Browser öffnen und `HOST:PORT` in Adresszeile eingeben
    - `HOST`: auf lokalem PC `localhost`, auf Netzwerkrechner die jeweilige IP des Rechners auf dem der Server läuft
    - `PORT`: 5000 (muss für Zugriff im Netzwerk freigegeben werden)

Die erstellten CSV Dateien werden im in der `config.json` angegebenen Ordner gespeichert, der angelegt wird, wenn er noch nicht vorhanden ist. Der jeweils letzte Export wird in den angegebenen Archiv-Ordner verschoben.

Wenn eine `.prod` Datei nicht bearbeitet werden konnte, steht in `exporter.log`, dass sie übersprungen wurde. Gründe dafür sind:

- Der `.prod` Ordner und die `.prod` Datei haben unterschiedliche Namen (`PROD_UNTERSCHIEDLICH`)
- Die `.prod` Datei enthält keine Artikelnummer (`KEINE_ARTNR`)
- Die `.prod` Datei enthält keinen Lieferstatus (`KEIN_DELSTAT`)
- Die `.prod` Datei enthält kein `TECHDATA` Feld (`KEIN_TECHDATA`)
- Das `TECHDATA` Feld enthält keinen Produkttyp (`KEIN_PRODUKTTYP`)
- Die Attribute in `TECHDATA` konnten nicht extrahiert werden, wahrscheinlich weil die numerischen Attribute fehlen (`TECHDATA_LEER`)
- Die Shop-CSV Datei konnte aufgrund von unbekannten Zeichen nicht geschrieben werden, die Konfigurator Datei ist davon grundsätzlich nicht beeinflusst (`UNBEKANNTES_ZEICHEN [FEHLER]`)

Wenn eine `.ilugg` Datei nicht vorhanden ist oder nicht bearbeitet werden konnte, steht das ebenfalls in der Log-Datei.

<a name="konfigurationen" />

## Konfigurationen

Die Kofigurations-Dateien sind im JSON Format hinterlegt. Es empfiehlt sich, mit einem Editor mit JSON-Erweiterung zu arbeiten, der auf Fehler aufmerksam machen kann (z.B. Notepad++) oder die JSON-Dateien mit einem Online-Validierer (z.B. [JSONLint](https://jsonlint.com/)) zu überprüfen.

### Allgemeine Einstellungen<a name="allgemeine-einstellungen" />

In `config.json` werde allgemeine Einstellungen spezifiziert. Bei der Angabe von Verzeichnissen darauf achten, dass sie mit einem `/` enden.

<a name="export-konfigurationen" />

### Export-Konfigurationen

Der Speicherort der JSON Dateien für die Export-Konfigurationen wird in `config.json` angegeben. Es gibt muss eine Datei `Shop.json` für den allgemeinen BSVP Daten-Export nach Herstellern geben und einen Ordner `Konfigurator`, der die Konfigurationen für den Konfigurator-Export beinhaltet.

#### Shop

Durch die `Shop.json` werden Felder angegeben, die in die CSV Datei pro Hersteller geschrieben werden. Als Bezeichner eines Feldes wird der Name angegeben, wie er in der CSV erscheint, als Wert ein Objekt, das den Wert beschreibt:

```json
{
  "XTSOL": { "wert": "XTSOL" },
  "action": { "prod": "ACTION" },
  "p_dics": { "ilugg": "DICOUNT" },
  "p_cat.": { "iterierbar": { "praefix": "CAT", "max": { "wert": "5" } } },
  "p_image.": {
    "iterierbar": {
      "praefix": "PIC.",
      "max": { "ilugg": "PicCount" },
      "start": "1"
    }
  },
  "p_desc.de": {}
}
```

Für den Wert wird der Typ angegeben und der dazugehörige Wert:

- `wert`: Es wird ein fester Wert eingetragen
- `prod`: Es wird der Name des Feldes in der `.prod`-Datei angegeben
- `ilugg`: Es wird der Name des Feldes in der `.ilugg`-Datei angegeben
- `iterierbar`: Es müssen der Präfix des Feldes in der `.prod`-Datei und der Maximalwert angegeben werden; zusätzlich kann der `start` Index (standardmäßig `0`) angegeben werden

Für Werte, die gesondert zusammengebaut werden müssen, wird ein leeres Objekt (`{}`) bzw. werden zusätzliche Spezifikationen angegeben:

- `p_desc.de`: leeres Objekt
- `p_movies.de`: leeres Objekt
- `products_energy_efficiency_text`: Liste von Feldern, die in die Tabelle geschrieben werden (`{ "fields": [ "0000015", "0000089" ] }`)

#### Konfigurator

Der Dateiname der jeweiligen JSON Datei bestimmt den Dateinamen der CSV Datei, die erstellt wird (Bsp. `Kühlschränke.json` wird zu `Kühlschränke.csv`). Es werden der Produkttyp und Felder angegeben, die exportiert werden sollen. Das Format sieht wie folgt aus:

```json
{
  "produkttyp": "Kühlschrank",
  "hersteller_export": ["Nordcap", "KBS"],
  "felder": {
    "ARTNR": "artikelnummer",
    "0000017": "anzahl_regalboeden",
    "0000089": "energieverbrauch"
  },
  "kombinationen": {
    "temperaturbereich": {
      "separator": "|",
      "felder": ["0000226", "0000225"]
    }
  },
  "formatierungen": {
    "punkt_zu_komma": ["0000089"],
    "ersetzungen": [
      {
        "vorher": ["ja"],
        "nachher": "yes",
        "felder": ["0000241", "0000261", "0000003", "0000091"]
      },
      {
        "vorher": ["nein"],
        "nachher": "no",
        "felder": ["0000241", "0000261", "0000003", "0000091"]
      },
      {
        "vorher": ["CNS 1.4301", "CNS 1.4301 (AISI304)", "CNS 18/10"],
        "nachher": "CNS",
        "felder": ["0000158"]
      }
    ]
  }
}
```

Der Produkttyp muss so angegeben werden, wie er in den BSVP-Produkt-Dateien steht, allerdings ohne HTML kodierte Zeichen (Bsp. `PUM::Produkttyp::K&uuml;hlschrank`, in der Konfiguration steht `"Kühlschrank"`).

Die Felder werden als Key-Value-Paar angegeben, wobei der Key das Feld so wie es in den BSVP-Produkt-Dateien steht ist (Bsp. `"ARTNR"`) bzw. als numerische ID für das Attribut-Feld (Bsp. `"0000017"` für Anzahl Regalböden). Der Value ist der Name des Feldes wie er in der CSV Datei angegeben werden soll (Bsp. `"artikelnummer"` oder `"anzahl_regalboeden"`).

##### Lieferanten CSVs

Neben der globalen CSV Datei können CSV Dateien pro Lieferant erstellt werden. Dazu kann in dem Feld `"hersteller_export"` eine Liste von Lieferantennamen angegeben werden. Die resultierende CSV Datei heißt dann `KONFIGURATION_HERSTELLER.csv`, also zum Beispiel `Kühlschrank_Nordcap.csv`.

##### Kombinationen von Werten

Kombinationen von Werten können angegeben werden, sie müssen es aber nicht. Der Bezeichner einer Kombination entspricht der Bezeichung der Spalte in der CSV Datei. Als Wert werden ein Separator (Bsp. `"|"`) und Feldnamen bzw. Attribut-IDs in einer Liste (eckige Klammern) angegeben.

##### Formatierung von Werten

Formatierungen können in dem Feld `"formatierungen"` angegeben werden. Einfache Ersetzungen von Werten (Bsp. die Werte `["CNS 1.4301", "CNS 1.4301 (AISI304)", "CNS 18/10"]` sollen immer zu `"CNS"` geändert werden) können im untergeordneten Feld `"ersetzungen"` angegeben werden. Für komliziertere Formatierungen gibt es folgende vordefinierte Regeln:

- `"punkt_zu_komma"`: der Punkt (in einer Kommazahl) wird zu einem Komma geändert
- `"bereich_von_null"`: zu einem Wert wird "0|" hinzugefügt

Zu einer Ersetzung bzw. Regel kann eine Liste von Attribut-IDs angegeben werden, auf die diese dann angewendet werden.

<a name="fehlerbehebung" />

## Fehlerbehebung

Hier sind Lösungen zu häufigen Fehlern aufgeführt, geordnet nach den Fehlerarten, die in der Kommandozeile ausgegeben werden.

### PermissionError

```
PermissionError: [WinError 32] The process cannot access the file because it is being used by another process
```

Es könnte sein, dass eine CSV Datei, die überschrieben werden soll noch in einem anderen Programm wie Excel geöffnet ist, bitte schließen und den Exporter erneut starten.

### JSONDecodeError

Beim JSON Format empfiehlt es sich allgemein, mit einem Editor zu arbeiten, der auf Syntax-Fehler aufmerksam macht. Alternativ können JSON Dateien auch online validiert werden (z.B. unter https://jsonlint.com/).

```
json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 19 column 5 (char 566)
```

Eine der JSON Konfigurationen enthält ein Komma in der letzten Zeile, das bitte entfernen.
