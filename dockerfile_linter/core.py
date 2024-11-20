from dockerfile_parse import DockerfileParser

def parse_dockerfile(file_path):
    """Reads a Dockerfile and returns the parsed data."""
    dfp = DockerfileParser(file_path)
    data = {
        "base_image": dfp.baseimage,
        "instructions": [instr for instr in dfp.structure],
    }
    return data