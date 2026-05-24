"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    ...

    print_section_header(
        "Enviando prompt para o LangSmith Hub"
    )

    prompt_config = prompt_data[prompt_name]

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            prompt_config["system_prompt"]
        ),
        (
            "human",
            prompt_config["user_prompt"]
        )
    ])

    prompt_path = f"laisagomes/{prompt_name}"

    print(f"Prompt path: {prompt_path}")

    try:

        result = hub.push(
            prompt_path,
            prompt
        )

        print("Prompt enviado com sucesso!")
        print(f"Hub URL: {result}")

        return True

    except Exception as e:

        print(f"Erro ao enviar prompt:")
        print(e)

        return False

def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """

    errors = []

    if not prompt_data:
        errors.append("Arquivo YAML vazio")
        return False, errors

    prompt_name = list(prompt_data.keys())[0]
    prompt_config = prompt_data[prompt_name]

    required_fields = [
        "system_prompt",
        "user_prompt",
        "input_variables",
        "version"
    ]

    for field in required_fields:
        if field not in prompt_config:
            errors.append(
                f"Campo obrigatório ausente: {field}"
            )

    recommended_fields = [
        "description",
        "techniques_applied",
        "tags"
    ]

    for field in recommended_fields:
        if field not in prompt_config:
            errors.append(
                f"Campo recomendado ausente: {field}"
            )

    system_prompt = (
        prompt_config
        .get("system_prompt", "")
        .strip()
    )

    if not system_prompt:
        errors.append(
            "system_prompt está vazio"
        )

    user_prompt = (
        prompt_config
        .get("user_prompt", "")
        .strip()
    )

    if not user_prompt:
        errors.append(
            "user_prompt está vazio"
        )

    techniques = prompt_config.get(
        "techniques_applied",
        []
    )

    if "few-shot-learning" not in techniques:
        errors.append(
            "few-shot-learning ausente"
        )

    return (
        len(errors) == 0,
        errors
    )


def main():
    """Função principal"""
    ...
    required_vars = [
        "LANGSMITH_API_KEY"
    ]

    if not check_env_vars(required_vars):
        sys.exit("Variáveis de ambiente não configuradas")

    prompt_name = "bug_to_user_story_v2"
    prompt_data = load_yaml(f"prompts/{prompt_name}.yml")

    is_valid, errors = validate_prompt(
        prompt_data
    )

    if not is_valid:

        print_section_header(
            "Falha na validação do prompt"
        )

        for error in errors:
            print(f"Erro ao validar o prompt: {error}")

        sys.exit(
            "Prompt inválido"
        )

    if not push_prompt_to_langsmith(prompt_name, prompt_data):
        sys.exit("Erro ao fazer push do prompt")

    print("Prompt enviado com sucesso!")


if __name__ == "__main__":
    sys.exit(main())
