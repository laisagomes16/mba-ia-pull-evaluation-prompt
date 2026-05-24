"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub

from utils import (
    save_yaml,
    check_env_vars,
    print_section_header
)

load_dotenv()


def pull_prompts_from_langsmith():

    print_section_header("Baixando prompt do LangSmith Hub")

    prompt_path = "leonanluppi/bug_to_user_story_v1"

    prompt = hub.pull(prompt_path)

    prompt_name = prompt_path.split("/")[-1]

    messages = prompt.messages

    system_prompt = messages[0].prompt.template
    user_prompt = messages[1].prompt.template

    prompt_yaml = {
        prompt_name: {
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "input_variables": prompt.input_variables,
            "version": "v1"
        }
    }

    save_yaml(
        prompt_yaml,
        f"prompts/{prompt_name}.yml"
    )

    print_section_header("Prompt baixado com sucesso!")

    print("✅ Prompt salvo com sucesso!")


def main():

    required_vars = [
        "LANGSMITH_API_KEY"
    ]

    if not check_env_vars(required_vars):
        sys.exit("Variáveis de ambiente não configuradas")

    pull_prompts_from_langsmith()


if __name__ == "__main__":
    sys.exit(main())