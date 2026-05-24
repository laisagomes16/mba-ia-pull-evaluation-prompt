"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

PROMPTS_FILE = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path,'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


class TestPrompts:

    @pytest.fixture(scope="class")
    def prompt_data(self):
        """Carrega o prompt principal."""
        prompts = load_prompts(PROMPTS_FILE)

        # pega o primeiro prompt do yaml
        prompt_name = next(iter(prompts))
        return prompts[prompt_name]

    def test_prompt_has_system_prompt(self, prompt_data):
        """
        Verifica se o campo 'system_prompt' existe e não está vazio.
        """
        assert "system_prompt" in prompt_data
        assert prompt_data["system_prompt"] is not None
        assert prompt_data["system_prompt"].strip() != ""

    def test_prompt_has_role_definition(self, prompt_data):
        """
        Verifica se o prompt define uma persona.
        """
        system_prompt = prompt_data["system_prompt"].lower()

        role_keywords = [
            "você é",
            "product owner",
            "product manager",
            "persona",
            "especializado"
        ]

        assert any(keyword in system_prompt for keyword in role_keywords), (
            "O prompt deve definir uma persona "
            "(ex: 'Você é um Product Owner')."
        )

    def test_prompt_mentions_format(self, prompt_data):
        """
        Verifica se o prompt exige formato Markdown ou User Story.
        """
        system_prompt = prompt_data["system_prompt"].lower()

        format_keywords = [
            "user story",
            "markdown",
            "critérios de aceitação",
            "como um",
            "eu quero",
            "para que"
        ]

        assert any(keyword in system_prompt for keyword in format_keywords), (
            "O prompt deve exigir formato "
            "Markdown ou User Story."
        )

    def test_prompt_has_few_shot_examples(self, prompt_data):
        """
        Verifica se o prompt contém exemplos de entrada/saída (Few-shot Learning).
        """
        system_prompt = prompt_data["system_prompt"].lower()

        few_shot_keywords = [
            "exemplo",
            "entrada:",
            "saída:",
            "few-shot"
        ]

        found_keywords = sum(
            keyword in system_prompt
            for keyword in few_shot_keywords
        )

        assert found_keywords >= 2, (
            "O prompt deve conter exemplos "
            "de entrada/saída (Few-shot Learning)."
        )

    def test_prompt_no_todos(self, prompt_data):
        """
        Garante que não exista [TODO] no prompt.
        """
        full_prompt_text = ""

        for key, value in prompt_data.items():
            if isinstance(value, str):
                full_prompt_text += value.lower()

        assert "[todo]" not in full_prompt_text, (
            "Foi encontrado '[TODO]' no prompt."
        )

    def test_minimum_techniques(self, prompt_data):
        """
        Verifica se pelo menos 2 técnicas foram listadas.
        """
        assert "techniques_applied" in prompt_data

        techniques = prompt_data["techniques_applied"]

        assert isinstance(techniques, list), (
            "'techniques_applied' deve ser uma lista."
        )

        assert len(techniques) >= 2, (
            "O prompt deve ter pelo menos "
            "2 técnicas listadas."
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])