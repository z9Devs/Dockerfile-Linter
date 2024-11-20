
# Dockerfile Linter

**Dockerfile Linter** è uno strumento open-source scritto in Python che analizza i tuoi Dockerfile e fornisce un report con suggerimenti basati sulle best practice. Aiuta a ottimizzare e rendere più sicuri i tuoi container.

## Caratteristiche

- Analisi di immagini base (ad esempio, evitare l'uso di `latest` o raccomandare immagini più leggere).
- Verifica dell'uso di un utente non root.
- Suggerimenti per combinare comandi `RUN` per ridurre i layer.
- Supporto per Dockerfile con nomi personalizzati.

---

## Requisiti

- Python 3.9 o superiore
- Librerie Python:
  - `dockerfile-parse`
  - `pytest`
  - `rich`

Puoi installare i requisiti con:
```bash
pip install -r requirements.txt
```

---

## Installazione

Clona il repository e configura l'ambiente virtuale:
```bash
git clone https://github.com/tuo-repository/dockerfile-linter.git
cd dockerfile-linter
python -m venv venv
source venv/bin/activate  # Su Windows usa: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Utilizzo

### Analisi di un Dockerfile
Per analizzare un Dockerfile, esegui il comando:
```bash
python main.py /path/to/Dockerfile
```

### Specificare un Nome Personalizzato per il Dockerfile
Il linter supporta file con nomi personalizzati:
```bash
python main.py /path/to/custom_dockerfile
```

### Opzioni
- Puoi scegliere il formato dell'output (testuale o JSON):
  ```bash
  python main.py /path/to/Dockerfile --output json
  ```
- Ignora specifici controlli:
  ```bash
  python main.py /path/to/Dockerfile --ignore "Base Image Check"
  ```

---

## Esempio di Output

**Output Testuale**:
```
+----------------------------+----------+-----------------------------------------------+
| Check                      | Severity | Suggestion                                    |
+----------------------------+----------+-----------------------------------------------+
| Avoid using 'latest' tag   | WARN     | Specify a version like 'python:3.9-slim'.    |
| No non-root user specified | FAIL     | Consider adding a non-root USER instruction. |
+----------------------------+----------+-----------------------------------------------+
```

**Output JSON**:
```json
{
  "issues": [
    {
      "check": "Avoid using 'latest' tag for base images.",
      "severity": "WARN",
      "suggestion": "Specify a version like 'python:3.9-slim'."
    },
    {
      "check": "No non-root user specified.",
      "severity": "FAIL",
      "suggestion": "Consider adding a non-root USER instruction."
    }
  ]
}
```

---

## Test

Esegui i test per verificare il corretto funzionamento del progetto:
```bash
pytest
```

Il framework `pytest` testerà automaticamente le funzioni principali del progetto.

---

## Struttura del Progetto

```
dockerfile-linter/
├── dockerfile_linter/
│   ├── __init__.py       # File per il modulo principale
│   ├── checks.py         # Controlli delle best practice
│   ├── core.py           # Parsing dei Dockerfile
│   ├── report.py         # Generazione del report
├── tests/
│   └── test_core.py      # Test delle funzionalità principali
├── main.py               # Entry point del programma
├── Dockerfile            # Esempio di Dockerfile
├── Dockerfile.bad        # Dockerfile con errori per test
├── README.md             # Documentazione
```

---

## Contributi

Se hai idee per migliorare il progetto o hai trovato un bug, apri una issue o invia una pull request su GitHub.

---

## Licenza

Questo progetto è distribuito sotto la licenza MIT. Consulta il file `LICENSE` per i dettagli.

---

### Contattaci

Per domande o suggerimenti, invia una mail a: **tuo.email@example.com**.
