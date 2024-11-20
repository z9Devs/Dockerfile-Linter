from dockerfile_parse import DockerfileParser

def parse_dockerfile(file_path):
    """Legge un Dockerfile e restituisce i dati analizzati."""
    dfp = DockerfileParser(file_path)
    data = {
        "base_image": dfp.baseimage,
        "instructions": [instr for instr in dfp.structure],
    }
    return data

if __name__ == "__main__":
    file_path = "Dockerfile"  # Cambia con il tuo percorso
    result = parse_dockerfile(file_path)
    print("Base Image:", result["base_image"])
    print("Instructions:", result["instructions"])