import os
import yaml
from dotenv import load_dotenv

load_dotenv()


def load_and_create_config(
    input_path="config.yaml", output_path="fastagent.config.yaml"
):
    with open(input_path, "r") as f:
        raw_yaml = f.read()

    expanded_yaml = os.path.expandvars(raw_yaml)

    with open(output_path, "w") as f:
        f.write(expanded_yaml)

    return output_path
