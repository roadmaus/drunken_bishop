![Banner](banner.png)

# Zufälliger ASCII-Kunst-Muster-Generator

## Beschreibung

Dieses Python-Skript generiert zufällige ASCII-Kunst-Muster unter Verwendung mehrerer Bischöfe mit verschiedenen Anpassungsoptionen. Es produziert sowohl Text- als auch PDF-Ausgaben mit den ASCII-Mustern. Der Kernalgorithmus dieses Projekts basiert auf dem "betrunkenen-Bischof"-Algorithmus zur Visualisierung von SSH-Schlüsselfingerabdrücken in OpenSSH.

Dieses Projekt wurde inspiriert von und enthält modifizierten Code aus Manfred Tourons Implementierung des "betrunkenen-Bischof"-Algorithmus, das ursprüngliche Konzept des Algorithmus wird jedoch Alexander von Gernler zugeschrieben.

## Funktionen

- Anpassbare Anzahl von Bischöfen
- Optionale Verwendung verschiedener Alphabete für verschiedene Bischöfe
- Ausgabe in `.txt` und `.pdf` Formaten

## Über den Betrunkenen-Bischof-Algorithmus

Der "betrunkenen-Bischof"-Algorithmus, ursprünglich für die Visualisierung von SSH-Schlüsselfingerabdrücken in OpenSSH konzipiert, stellt einen anspruchsvollen Ansatz dar, komplexe Daten in ein zugängliches, visuelles Format zu übertragen. Dieser Algorithmus entstand nicht nur als skurrile Methode, sondern als robustes Mittel zur Darstellung der inhärenten Zufälligkeit und Einzigartigkeit von SSH-Schlüsseln.

In diesem Zusammenhang wird der Zufällige ASCII-Kunst-Muster-Generator den "betrunkenen-Bischof"-Algorithmus zweckentfremdet. Hier ist der Algorithmus nicht mehr ein Werkzeug für die Sicherheitsvisualisierung, sondern ein Instrument zur Erzeugung unverwechselbarer ASCII-Muster. Das Kernprinzip des Algorithmus ist seine stochastische Bewegung, die an die diagonalen Schritte eines Bischofs im Schach erinnert. Diese Bewegung, diktiert durch die Eingabedaten, stellt sicher, dass jede Ausführung ein einzigartiges, nicht repetitives Muster ergibt.

Die Eleganz des Algorithmus liegt in seiner Fusion aus Einfachheit und Komplexität, Ordnung und Chaos. Er demonstriert, wie algorithmische Prozesse ihre ursprünglichen utilitaristischen Zwecke transzendieren können, um kreative Expression zu inspirieren.

## Klonen des Repositories

Bevor Sie die virtuelle Umgebung einrichten, müssen Sie zuerst das Repository auf Ihren lokalen Rechner klonen. So geht's:

1. **Öffnen Sie das Terminal oder die Eingabeaufforderung**: Navigieren Sie zu dem Verzeichnis, in dem Sie das Repository klonen möchten.

2. **Klonen Sie das Repository**: Verwenden Sie den folgenden Befehl, um das Repository zu klonen:

   ```bash
   git clone https://github.com/roadmaus/drunken_bishop.git
   ```

   Dieser Befehl erstellt eine Kopie des `drunken_bishop`-Repositorys in Ihrem aktuellen Verzeichnis.

3. **Navigieren Sie zum Repository-Verzeichnis**: Nach dem Klonen, bewegen Sie sich in das Repository-Verzeichnis:

   ```bash
   cd drunken_bishop
   ```

Mit dem erfolgreich geklonten Repository sind Sie bereit, die virtuelle Umgebung einzurichten, wie im nächsten Abschnitt beschrieben.

## Installation mit Virtueller Umgebung

Um eine saubere und isolierte Umgebung für das Ausführen des Skripts zu gewährleisten, wird empfohlen, eine virtuelle Umgebung zu verwenden. So können Sie sie einrichten:

1. **Erstellen einer Virtuellen Umgebung:**

   Je nach Betriebssystem kann der Befehl zum Erstellen einer virtuellen Umgebung leicht variieren:

   - Auf **macOS und Linux**:

     ```bash
     python3 -m venv venv
     ```

     Dieser Befehl erstellt eine neue virtuelle Umgebung namens `venv` in Ihrem aktuellen Verzeichnis mit Python 3.

   - Auf **Windows**:

     ```bash
     python -m venv venv
     ```

     Wenn Sie sowohl Python 2 als auch Python 3 installiert haben, ersetzen Sie `python` durch `python3`,

 um sicherzustellen, dass Python 3 verwendet wird.


2. **Aktivieren der Virtuellen Umgebung:**
   
   - Auf Windows:
     
     ```bash
     .\venv\Scripts\activate
     ```
   
   - Auf macOS und Linux:
     
     ```bash
     source venv/bin/activate
     ```
     
     Dieser Schritt aktiviert die virtuelle Umgebung. Sie werden `(venv)` vor Ihrem Befehlsprompt bemerken, wenn sie aktiv ist.

3. **Installieren von Abhängigkeiten:**
   Während die virtuelle Umgebung aktiv ist, installieren Sie die erforderlichen Pakete:
   
   ```bash
   pip install -r requirements.txt
   ```
   
   Dies stellt sicher, dass alle Abhängigkeiten innerhalb von `venv` und nicht global installiert werden.

4. **Ausführen des Skripts:**
   Sie können nun das Skript ausführen, wie im Abschnitt Nutzung erwähnt.

5. **Deaktivieren der Virtuellen Umgebung:**
   Wenn Sie fertig sind, können Sie die virtuelle Umgebung deaktivieren, indem Sie eingeben:
   
   ```bash
   deactivate
   ```

## Nutzung

### Grundlegende Nutzung

Um das Skript mit den Standardeinstellungen auszuführen:

```bash
python drunken_bishop.py
```

## Beispiel-Ausgabe

#### betrunken:

![Beispiel_betrunken](example.png)

#### nüchtern:

![Beispiel_nüchtern](example_sober.png)

#### Textausgabe:

[Hier klicken, um das Beispiel anzusehen](https://raw.githubusercontent.com/roadmaus/drunken_bishop/main/examples/random_112.txt)


### Erweiterte Nutzung

Um die Anzahl der Bischöfe, verschiedene Alphabete und andere Einstellungen anzupassen:

```bash
python drunken_bishop.py --min-bischöfe 4 --max-bischöfe 20 --verschiedene-alphabete --anzahl-ausgaben 12 --zufällige-farbe --nüchtern --querformat 
```

### Interaktiver Modus und Einstellungen

#### Interaktiver Modus

Um das Programm interaktiv zu verwenden, wodurch eine einfache Anpassung verschiedener Einstellungen wie der Anzahl der Bischöfe, Alphabete und Farbschemata ermöglicht wird, verwenden Sie den `--I`-Flag:

```bash
python drunken_bishop.py --I
```

Dies startet eine interaktive Sitzung mit einer Reihe von Fragen, die es Ihnen ermöglichen, die ASCII-Kunst-Generierung gemäß Ihren Vorlieben anzupassen. Optionen umfassen:

- Minimale und maximale Anzahl von Bischöfen
- Wahl der Verwendung verschiedener Alphabete für verschiedene Bischöfe
- Ästhetik der Ausgabe wie Farbschemata und Format

#### Einstellungsdatei

Das Programm unterstützt das Speichern und Laden von Einstellungen aus einer Datei für eine konsistente Nutzung über Sitzungen hinweg. 

- **Einstellungen Speichern**: Verwenden Sie den `--einstellungen`-Flag, um Ihre aktuellen Einstellungen in einer Datei zu speichern.
  
  ```bash
  python drunken_bishop.py --einstellungen
  ```

- **Einstellungen Laden**: Verwenden Sie den `--s`-Flag, um Einstellungen aus einer bestehenden Datei zu laden.
  
  ```bash
  python drunken_bishop.py --s
  ```

Diese Funktion ist besonders nützlich, um konsistente Präferenzen zu pflegen und Lieblingskonfigurationen schnell zu reproduzieren.

### Hilfemenü

Um alle möglichen Verwendungen und Flags einzusehen:

```bash
python drunken_bishop.py -h
```

## Ausgabe

Das Skript generiert eine Textdatei und eine PDF-Datei im Verzeichnis `random_patterns`.

## Mitwirken

Fühlen Sie sich frei, das Repository zu forken und Pull-Anfragen einzureichen. Für alle Fehler oder Funktionsanfragen öffnen Sie bitte ein Issue.

## Lizenz

Dieses Projekt beinhaltet Elemente von Manfred Tourons "betrunkenen-Bischof"-Algorithmus (https://github.com/moul/drunken-bishop). Dieses Werk ist unter der MIT-Lizenz lizenziert. Weitere Details finden Sie in der Datei LICENSE.
