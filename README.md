# Advanced Calculator

An advanced, test-driven calculator with a REPL, history with undo/redo (Memento), operation factory, observers for logging and auto-save, configuration via `.env`, CSV persistence with pandas, and CI via GitHub Actions. Color-coded CLI output and a decorator-powered dynamic help menu are included as optional enhancements.

## Setup
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration
Copy `.env` (already provided) and adjust values as needed.

## Run
```bash
python -m app
# examples:
# calc> add 2 3
# calc> power 2 8
# calc> history
# calc> undo
# calc> save
```

## Tests & Coverage
```bash
pytest --cov=app --cov-fail-under=90
```

- **How to Run the REPL**
  ```bash
  python -m app
  ```

- **Testing & Coverage**
  ```bash
  pytest --cov=app --cov-fail-under=90
  ```
  Additional observer tests located in `tests/test_observers.py` (uses `unittest.mock`).

- **CI/CD**
  GitHub Actions workflow at `.github/workflows/python-app.yml` enforces coverage gate.

- **Config (.env)**
  See `.env` for directory, precision, autosave, and file paths. Defaults are provided.

- **Coloring**
  added color-coded outputs to improve the readability and user experience of the application.

