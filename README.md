# BSVP CSV Exporter

Python-basierter Exporter für die Umwandlung von BSVP zu CSV Dateien.

Trello: https://trello.com/b/ug9q2Eif/bsvp

Diese README sieht komisch aus? Dann öffne sie mit einem Editor mit Markdown-Erweiterung (z.B. Notepad++) oder mit einem Online-Viewer (z.B. [Github](https://jbt.github.io/markdown-editor/)).

Bei Fragen und Problemen mit dem Export meldet euch gerne bei mir unter tamaraslosarek@gmail.com.

1.  [Installation](#installation)
    * [Updates](#updates)
    * [Automatische Ausführung](#automatische-ausführung)
2.  [Ausführung](#ausführung)
3.  [Konfigurationen](#konfigurationen)
    * [Allgemeine Einstellungen](#allgemeine-einstellungen)
    * [Export-Konfigurationen](#export-konfigurationen)
4.  [Fehlerbehebung](#fehlerbehebung)

<a name="installation" />

## Installation

1.  Python 3 installieren
    * Mit [offiziellem Installer](https://www.python.org/downloads/)
    * Installationsverzeichnis zur `PATH` Umgebungsvariable hinzufügen
2.  Aktuelle Version des Exporters aus dem Trello herunterladen
3.  Exporter in gewünschtes Verzeichnis verschieben (von jetzt an `EXPORTER_VERZEICHNIS` genannt)
4.  Verzeichnis für Export-Konfigurationen anlegen
5.  Konfigurationen aus dem Trello herunterladen oder neu anlegen
6.  Die `config.json.example` in `config.json` umbenennen und ggf. anpassen

<a name="automatische-ausführung" />

### Automatische Ausführung

1.  Aufgabe im Windows Aufgabenplaner erstellen
2.  Aktion hinzufügen
    * Programm/Skript: `C:\Windows\SysWOW64\cmd.exe`
    * Argumente hinzufügen: `/c "python main.py"`
    * Starten in: `EXPORTER_VERZEICHNIS` (absoluten Pfad angeben, z.B. `C:\BSVP-Server\CSV Exporter`)

<a name="updates" />

### Updates

1.  Neue Version aus dem Trello herunterladen
2.  Inhalt in EXPORTER_VERZEICHNIS verschieben und vorhandene Dateien ersetzen, es wird nur der Code überschrieben, Konfigurationen und andere Daten bleiben so wie sie sind

<a name="ausführung" />

## Ausführung

1.  Kommandozeile starten (z.B. `WINDOWS + R` drücken, `cmd` eingeben und bestätigen)
2.  In das EXPORTER_VERZEICHNIS wechseln mit `cd EXPORTER_VERZEICHNIS`
3.  Exporter ausführen mit `python main.py`

Die erstellten CSV Dateien werden im in der `config.json` angegebenen Ordner gespeichert, der angelegt wird, wenn er noch nicht vorhanden ist. Der jeweils letzte Export wird in den angegebenen Archiv-Ordner verschoben.

Wenn eine `.prod` Datei nicht bearbeitet werden konnte, steht in der konfigurierten Log-Datei, dass sie übersprungen wurde. Gründe dafür sind:

* Der `.prod` Ordner und die `.prod` Datei haben unterschiedliche Namen (`PROD_UNTERSCHIEDLICH`)
* Die `.prod` Datei enthält keine Artikelnummer (`KEINE_ARTNR`)
* Die `.prod` Datei enthält keinen Lieferstatus (`KEIN_DELSTAT`)
* Die `.prod` Datei enthält kein `TECHDATA` Feld (`KEIN_TECHDATA`)
* Das `TECHDATA` Feld enthält keinen Produkttyp (`KEIN_PRODUKTTYP`)
* Die Attribute in `TECHDATA` konnten nicht extrahiert werden, wahrscheinlich weil die numerischen Attribute fehlen (`TECHDATA_LEER`)

<a name="konfigurationen" />

## Konfigurationen

Die Kofigurations-Dateien sind im JSON Format hinterlegt. Es empfiehlt sich, mit einem Editor mit JSON-Erweiterung zu arbeiten, der auf Fehler aufmerksam machen kann (z.B. Notepad++) oder die JSON-Dateien mit einem Online-Validierer (z.B. [JSONLint](https://jsonlint.com/)) zu überprüfen.

### Allgemeine Einstellungen<a name="allgemeine-einstellungen" />

In `config.json` werde allgemeine Einstellungen spezifiziert. Bei der Angabe von Verzeichnissen darauf achten, dass sie mit einem `/` enden.

<a name="export-konfigurationen" />

### Export-Konfigurationen

Der Speicherort der JSON Dateien für die Export-Konfigurationen wird in `config.json` angegeben. Der Dateiname der jeweiligen JSON Datei bestimmt den Dateinamen der CSV Datei, die erstellt wird (Bsp. `Kühlschränke.json` wird zu `Kühlschränke.csv`). Es werden der Produkttyp und Felder angegeben, die exportiert werden sollen. Das Format sieht wie folgt aus:

```json
{
  "produkttyp": "Kühlschrank",
  "felder": {
    "ARTNR": "artikelnummer",
    "TECHDATA": {
      "0000017": "anzahl_regalboeden",
      "0000089": "energieverbrauch"
    }
  },
  "kombinationen": {
    "temperaturbereich": {
      "separator": "|",
      "felder": ["0000226", "0000225"]
    }
  },
  "formatierungen": {
    "punkt_zu_komma": ["0000089"]
  },
  "ersetzungen": [
    {
      "vorher": "ja",
      "nachher": "yes",
      "felder": ["0000241", "0000261", "0000003", "0000091"]
    },
    {
      "vorher": "nein",
      "nachher": "no",
      "felder": ["0000241", "0000261", "0000003", "0000091"]
    },
    {
      "vorher": "220 - 240 Volt",
      "nachher": "230 Volt",
      "felder": ["0000215"]
    }
  ]
}
```

Der Produkttyp muss so angegeben werden, wie er in den BSVP-Produkt-Dateien steht, allerdings ohne HTML kodierte Zeichen (Bsp. `PUM::Produkttyp::K&uuml;hlschrank`, in der Konfiguration steht `"Kühlschrank"`).

Die Felder werden als Key-Value-Paar angegeben, wobei der Key das Feld so wie es in den BSVP-Produkt-Dateien steht ist (Bsp. `"ARTNR"`). Der Value ist entweder der Name des Feldes wie er in der CSV Datei angegeben werden soll (Bsp. `"artikelnummer"`) oder weitere Key-Value-Paare, die zu exportierende Attribute spezifizieren, die im Feld enthalten sind (Bsp. innerhalb von `TECHDATA`). Hierbei wird als Key die numerische ID für das Attribut-Feld angegeben (Bsp. `"0000017"` für Anzahl Regalböden). Der Value ist der Name, der als Feld-Bezeichner in der CSV Datei steht (Bsp. `"anzahl_regalboeden"`).

#### Kombinationen von Werten

Kombinationen von Werten können angegeben werden, sie müssen es aber nicht. Der Bezeichner einer Kombination entspricht der Bezeichung der Spalte in der CSV-Datei. Als Wert sind ein Separator, das Feld (i.d.R. `TECHDATA`) und Attribut-IDs angegeben. Die Attribut-IDs werden dabei in einer Liste (eckige Klammern) angegeben.

#### Formatierung von Werten

Einfache Ersetzungen von Werten (Bsp. `"230 - 240 Volt"` soll immer zu `"230 Volt"` geändert werden) können im Feld `"ersetzungen"` angegeben werden. Kompliziertere Formatierungen können in dem Feld `"formatierungen"` angegeben werden. Dabei gibt es folgende vordefinierte Regeln:

* `"punkt_zu_komma"`: der Punkt (in einer Kommazahl) wird zu einem Komma geändert
* `"bereich_von_null"`: zu einem Wert wird "0|" hinzugefügt

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
