# BSVP CSV Exporter

Python-basierter Exporter für die Umwandlung von BSVP zu CSV Dateien.

Trello: <https://trello.com/b/ug9q2Eif/bsvp>

Diese README sieht komisch aus? Dann öffne sie mit einem Editor mit Markdown-Erweiterung (z.B. Notepad++) oder mit einem Online-Viewer (z.B. [Github](https://jbt.github.io/markdown-editor/)).

Bei Fragen und Problemen mit dem Export meldet euch gerne bei mir unter tamaraslosarek@gmail.com.

1.  [Ausführung](#ausfuehrung)
2.  [Installation](#installation)
3.  [Export-Konfigurationen](#export-konfigurationen)
4.  [Fehlerbehebung](#fehlerbehebung)

<a name="ausfuehrung" />

## Ausführung

Um die Webapp zu starten, muss das `start.bat` Skript ausgeführt werden (über die Kommandozeile oder per Doppelklick), das automatisch auf die aktuellste Version updated. Die App ist dann unter `https://localhost:3000` (bzw. anstatt `localhost` die IP-Adresse des Rechners im Netzwerk) erreicht werden. Zum Neustart oder Stoppen können die `restart.bat` und `stop.bat` Skripte ausgeführt werden (Achtung: Alle laufenden Docker Container werden gestoppt).

<a name="installation" />

## Installation

Um die Exporter ausführen zu können, werden lediglich der Inhalt des `setup` Ordners und Docker benötigt (Windows Installer: <https://docs.docker.com/docker-for-windows/install/>).

Konfigurationsdateien (`config.json`, `paths.txt` und `configs`) werden automatisch mit Standardwerten erstellt. Um diese zu überschreiben, können die Dateien kopiert, umbenannt und angepasst werden:

-   `config.json` aus [`config.example.json`](config.json.example)
-   `paths.txt` aus [`paths.example.txt`](paths.txt.example)
-   `configs` aus [`example_configs`](example_configs) (siehe auch [Export-Konfigurationen](#export-konfigurationen))

Der Ordnername von `configs` kann in der `paths.txt` Datei geändert werden.

<a name="export-konfigurationen" />

## Export-Konfigurationen

Die Kofigurations-Dateien sind im JSON Format hinterlegt. Es empfiehlt sich, mit einem Editor mit JSON-Erweiterung zu arbeiten, der auf Fehler aufmerksam machen kann (z.B. Notepad++) oder die JSON-Dateien mit einem Online-Validierer (z.B. [JSONLint](https://jsonlint.com/)) zu überprüfen. Es gibt muss eine Datei `Shop.json` für den allgemeinen BSVP Daten-Export nach Herstellern geben und einen Ordner `Konfigurator`, der die Konfigurationen für den Konfigurator-Export beinhaltet.

### Komplett

In der `Komplett.json` können verschiedene Einstellungen für den kompletten Export festgelegt werden:

-   `exclude`: Felder angeben, die nicht im kompletten Export enthalten sein sollen. Es können normale Felder mit Namen (z.B. `ARTLISTING`) und TECHDATA Felder mit ID (z.B. `0000009`) angegeben werden.

```json
{
  "exclude": [
    "ARTLISTING",
    "CAT0M",
    "0000009"
  ]
}
```

### Shop

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

-   `wert`: Es wird ein fester Wert eingetragen
-   `prod`: Es wird der Name des Feldes in der `.prod`-Datei angegeben
-   `ilugg`: Es wird der Name des Feldes in der `.ilugg`-Datei angegeben
-   `iterierbar`: Es müssen der Präfix des Feldes in der `.prod`-Datei und der Maximalwert angegeben werden; zusätzlich kann der `start` Index (standardmäßig `0`) angegeben werden

Für Werte, die gesondert zusammengebaut werden müssen, wird ein leeres Objekt (`{}`) bzw. werden zusätzliche Spezifikationen angegeben:

-   `p_desc.de`: leeres Objekt
-   `p_movies.de`: leeres Objekt
-   `products_energy_efficiency_text`: Liste von Feldern, die in die Tabelle geschrieben werden (`{ "fields": [ "0000015", "0000089" ] }`)

### Konfigurator

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
  "reihenfolgen": [{
    "felder": ["0000226", "0000225"],
    "reihenfolge": ["temperatur_numerisch", "temperaturen_gruppieren"]
  }],
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
      },
      {
        "vorher": ["Klimaklasse"],
        "nachher": "Kl.",
        "felder": ["0000142"],
        "option": "startswith"
      },
      {
        "vorher": ["RH"],
        "nachher": "RH (relative Feuchte)",
        "felder": ["0000142"],
        "option": "endswith"
      },
      {
        "id": "temperatur_numerisch",
        "vorher": ["°C"],
        "nachher": "",
        "felder": ["0000226", "0000225"],
        "option": "endswith"
      }
    ],
    "gruppierungen": [
      {
        "grenzwerte": [700, 1000],
        "einheit": "mm",
        "felder": ["0000058"]
      },
      {
        "id": "temperaturen_gruppieren",
        "grenzwerte": [0],
        "einheit": "°C",
        "felder": ["0000226", "0000225"]
      }
    ]
  }
}
```

Der Produkttyp muss so angegeben werden, wie er in den BSVP-Produkt-Dateien steht, allerdings ohne HTML kodierte Zeichen (Bsp. `PUM::Produkttyp::K&uuml;hlschrank`, in der Konfiguration steht `"Kühlschrank"`).

Die Felder werden als Key-Value-Paar angegeben, wobei der Key das Feld so wie es in den BSVP-Produkt-Dateien steht ist (Bsp. `"ARTNR"`) bzw. als numerische ID für das Attribut-Feld (Bsp. `"0000017"` für Anzahl Regalböden). Der Value ist der Name des Feldes wie er in der CSV Datei angegeben werden soll (Bsp. `"artikelnummer"` oder `"anzahl_regalboeden"`).

#### Lieferanten CSVs

Neben der globalen CSV Datei können CSV Dateien pro Lieferant erstellt werden. Dazu kann in dem Feld `"hersteller_export"` eine Liste von Lieferantennamen angegeben werden. Die resultierende CSV Datei heißt dann `KONFIGURATION_HERSTELLER.csv`, also zum Beispiel `Kühlschrank_Nordcap.csv`.

#### Kombinationen von Werten

Kombinationen von Werten können angegeben werden, sie müssen es aber nicht. Der Bezeichner einer Kombination entspricht der Bezeichung der Spalte in der CSV Datei. Als Wert werden ein Separator (Bsp. `"|"`) und Feldnamen bzw. Attribut-IDs in einer Liste (eckige Klammern) angegeben.

#### Formatierung von Werten

Formatierungen können in dem Feld `"formatierungen"` angegeben werden.

Einfache Ersetzungen von Werten (Bsp. die Werte `["CNS 1.4301", "CNS 1.4301 (AISI304)", "CNS 18/10"]` sollen immer zu `"CNS"` geändert werden) können im untergeordneten Feld `"ersetzungen"` angegeben werden.

Wenn die Ersetzung für einen Teil-String am Anfang oder am Ende erfolgen soll, muss als Option `"startswith"` bzw. `"endswith"` angegeben werden.

Für Ersetzungen wird nicht auf Groß- und Kleinschreibung geachtet `"Ja"` würde genau wie `"ja"` zu `"yes"` geändert werden. Das gilt nicht für Teil-Ersetzungen.

Außerdem können Gruppierungen numerischer Werte vorgenommen werden. Wichtig dabei ist, dass die Werte im angegebenen Datenfeld tatsächlich numerisch sind, ansonsten funktioniert die Formatierung nicht. Dabei werden Grenzwerte zwischen den Gruppen und die Einheit der Werte angegeben. Der resultierende Wert ist dann zum Beispiel `"bis 700mm"`, `"bis 1000mm"`, oder `"> 1000mm"`

Für komliziertere Formatierungen gibt es folgende vordefinierte Regeln:

-   `"punkt_zu_komma"`: der Punkt (in einer Kommazahl) wird zu einem Komma geändert
-   `"bereich_von_null"`: zu einem Wert wird "0|" hinzugefügt

Zu einer Ersetzung bzw. Regel kann eine Liste von Attribut-IDs angegeben werden, auf die diese dann angewendet werden.

Zusätzlich können Gruppierungen und Ersetzungen, die voneinander abhängen, geordnet werden.
Dazu muss eine `"id"` angegeben werden (diese muss eindeutig sein, aber was darin steht, ist egal).
Dann kann ein Feld mit `"reihenfolgen"` angelegt werden, für jede Reihenfolge werden betroffene Feld IDs in `"felder"` und die Formatierung IDs in `"reihenfolge"` angegeben.
Beispiel (siehe oben): Für Temperaturen (`"0000225"` and `"0000226"`) soll zuerst das `°C` gelöscht werden, bevor nach Temperaturen über und unter 0°C gruppiert wird.
Für die Gruppierung wird die ID `temperaturen_gruppieren` vergeben, für die Ersetzung `temperatur_numerisch`.
Die Reihenfolge der Bearbeitung für die Felder `["0000225", "0000226"]` ist dann `["temperatur_numerisch", "temperaturen_gruppieren"]`.

<a name="fehlerbehebung" />

### Custom

Der Custom Exporter ist eine schnelle Möglichkeit, nur über das Anpassen der `Custom.json` bestimmte Felder zu exportieren.
Bitte beachten: Die Exporter müssen über das Web-Interface neu geladen werden, wenn die `Custom.json` bei laufendem Server geändert wurde.

Die einfache Konfiguration enthält lediglich den CSV-Header-Namen (z.B. `"artikelnummer"` oder `"kaeltemittel"`) und das Feld im Produkt (z.B. `"ARTNR"` oder `"0000139"`).

Zusätzlich kann geprüft werden, ob bestimmte Werte in einem Feld vorhanden sind.
Nur solche Produkte werden exportiert, die den angegebenen Text enthalten.
Das kann wie folgt definiert werden: `"kaeltemittel": {"field": "0000139", "contains": "404"}`.

Wenn solche Überprüfungen für mehrere Werte angegeben werden, werden nur solche Produkte exportiert, die alle Bedingungen erfüllen. Wenn zum Beispiel zusätzlich zum Kältemittel noch `"artikelnummer": {"field": "ARTNR", "contains": "AHT"}` angegeben wird, werden nur Artikel exportiert deren Artikelnummer sowohl `AHT` UND deren Kältemittel `404` beinhaltet.

## Fehlerbehebung

Hier sind Lösungen zu häufigen Fehlern aufgeführt, geordnet nach den Fehlerarten, die in der Kommandozeile ausgegeben werden.

### PermissionError

    PermissionError: [WinError 32] The process cannot access the file because it is being used by another process

Es könnte sein, dass eine CSV Datei, die überschrieben werden soll noch in einem anderen Programm wie Excel geöffnet ist, bitte schließen und den Exporter erneut starten.

### JSONDecodeError

Beim JSON Format empfiehlt es sich allgemein, mit einem Editor zu arbeiten, der auf Syntax-Fehler aufmerksam macht. Alternativ können JSON Dateien auch online validiert werden (z.B. unter <https://jsonlint.com/>).

    json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 19 column 5 (char 566)

Eine der JSON Konfigurationen enthält ein Komma in der letzten Zeile, das bitte entfernen.
