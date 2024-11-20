import sys
import os

# Aggiunge la directory principale al percorso
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa i moduli dal progetto
from dockerfile_linter.core import parse_dockerfile
from dockerfile_linter.checks import check_base_image, check_non_root_user, check_optimized_run
from dockerfile_linter.report import generate_report

def test_parse_dockerfile():
    """Testa il parsing del Dockerfile."""
    dockerfile_content = """
    FROM python:3.9-slim
    WORKDIR /app
    COPY . .
    CMD ["python", "app.py"]
    """
    temp_file = "Dockerfile"
    with open(temp_file, "w") as f:
        f.write(dockerfile_content)
    
    # Parsing del Dockerfile
    result = parse_dockerfile(temp_file)  # Usa il nome corretto del file senza directory
    
    # Verifica del risultato
    assert result["base_image"] == "python:3.9-slim"
    assert len(result["instructions"]) == 4  # FROM, WORKDIR, COPY, CMD
    
    # Cleanup
    os.remove(temp_file)

def test_check_base_image():
    """Testa il controllo sull'immagine di base."""
    # Caso: immagine corretta
    issues = check_base_image("python:3.9-slim")
    assert issues == []

    # Caso: immagine con "latest"
    issues = check_base_image("python:latest")
    assert len(issues) == 1
    assert issues[0][0] == "Avoid using 'latest' tag for base images."
    assert issues[0][1] == "WARN"
    assert issues[0][2] == "Specify a version like 'python:3.9-slim'."

    # Caso: immagine non ottimizzata
    issues = check_base_image("python:3.9")
    assert len(issues) == 1
    assert issues[0][0] == "Consider using a smaller base image instead of python:3.9."
    assert issues[0][1] == "INFO"
    assert issues[0][2] == "Use 'python:3.9-slim' or 'python:3.9-alpine'."

def test_check_non_root_user():
    """Testa il controllo sull'utente non root."""
    # Caso: utente non root
    instructions = [{"instruction": "USER", "value": "appuser"}]
    issues = check_non_root_user(instructions)
    assert issues == []

    # Caso: utente root
    instructions = [{"instruction": "USER", "value": "root"}]
    issues = check_non_root_user(instructions)
    assert len(issues) == 1
    assert issues[0][0] == "No non-root user specified."
    assert issues[0][1] == "FAIL"
    assert issues[0][2] == "Consider adding a non-root USER instruction."

    # Caso: nessun utente specificato
    instructions = []
    issues = check_non_root_user(instructions)
    assert len(issues) == 1
    assert issues[0][0] == "No non-root user specified."
    assert issues[0][1] == "FAIL"
    assert issues[0][2] == "Consider adding a non-root USER instruction."

def test_check_optimized_run():
    """Testa il controllo sull'ottimizzazione dei comandi RUN."""
    # Caso: comandi RUN ottimizzati
    instructions = [{"instruction": "RUN", "value": "apt-get update && apt-get install -y curl"}]
    issues = check_optimized_run(instructions)
    assert issues == []

    # Caso: comandi RUN non ottimizzati
    instructions = [{"instruction": "RUN", "value": "apt-get update"}]
    issues = check_optimized_run(instructions)
    assert len(issues) == 1
    assert issues[0][0] == "Combine RUN commands to reduce image layers."
    assert issues[0][1] == "WARN"
    assert issues[0][2] == "Use '&&' to chain commands in a single RUN."

def test_generate_report():
    """Testa la generazione del report."""
    issues = [
        ("Avoid using 'latest' tag for base images.", "WARN", "Specify a version like 'python:3.9-slim'."),
        ("No non-root user specified.", "FAIL", "Consider adding a non-root USER instruction."),
    ]
    
    # Non possiamo verificare l'output di `rich` direttamente, ma possiamo assicurare che non fallisca
    try:
        generate_report(issues)
        assert True  # Se arriva qui, il test è passato
    except Exception as e:
        assert False, f"generate_report ha lanciato un'eccezione: {e}"

    # Caso: nessun problema
    try:
        generate_report([])
        assert True  # Se arriva qui, il test è passato
    except Exception as e:
        assert False, f"generate_report ha lanciato un'eccezione: {e}"
