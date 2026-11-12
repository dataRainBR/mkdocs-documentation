import tempfile
import unittest
from pathlib import Path

from docs_preview import generate_references_markdown


class GenerateReferencesMarkdownTests(unittest.TestCase):
    def test_reads_project_dependencies_and_uv_git_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            project_root = Path(temporary_directory)
            (project_root / "pyproject.toml").write_text(
                """
[project]
dependencies = ["mkdocs>=1.6", "my-package[extra]>=2.0"]

[tool.uv.sources]
my-package = { git = "https://github.com/example/my-package.git", rev = "abc123" }
""".strip(),
                encoding="utf-8",
            )

            generated_file = generate_references_markdown(project_root)
            generated = generated_file.read_text(encoding="utf-8")

        self.assertIn("https://pypi.org/project/mkdocs/", generated)
        self.assertIn("my-package[extra]", generated)
        self.assertIn("https://github.com/example/my-package/commit/abc123", generated)
        self.assertIn("::: docs_preview.generate_references_markdown", generated)
        self.assertIn("uv sync", generated)

    def test_falls_back_to_requirements_file_and_keeps_direct_urls(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            project_root = Path(temporary_directory)
            (project_root / "requirements.txt").write_text(
                "mkdocs-material>=9.8\n"
                "custom-package @ https://example.org/custom-package.whl\n",
                encoding="utf-8",
            )

            generated_file = generate_references_markdown(project_root)
            generated = generated_file.read_text(encoding="utf-8")

        self.assertIn("https://pypi.org/project/mkdocs-material/", generated)
        self.assertIn(
            "[Abrir referência](https://example.org/custom-package.whl)", generated
        )


if __name__ == "__main__":
    unittest.main()
