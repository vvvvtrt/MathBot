import subprocess
from pathlib import Path
import shutil


def render_latex_to_png(latex: str, file_name: str, dpi: int = 600) -> bool:
    output_path = f"output/formulas/{file_name}.png"
    temp_dir = Path("latex_tmp")
    temp_dir.mkdir(exist_ok=True)

    tex_file = temp_dir / "formula.tex"
    pdf_file = temp_dir / "formula.pdf"
    # log_file = temp_dir / "formula.log"
    png_file = Path(output_path).resolve()

    png_file.parent.mkdir(parents=True, exist_ok=True)

    tex_code = rf"""
\documentclass[preview]{{standalone}}
\usepackage{{amsmath,amssymb}}
\begin{{document}}
\[
{latex}
\]
\end{{document}}
"""

    try:
        tex_file.write_text(tex_code, encoding="utf-8")

        pdflatex_result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", str(tex_file.name)],
            cwd=temp_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if not pdf_file.exists():
            return False

        subprocess.run(
            ["convert", "-density", str(dpi), str(pdf_file), "-quality", "200", "-trim", str(png_file)],
            check=True
        )

        return True

    except Exception as e:
        return False

    # finally:
    #     if log_file.exists():
    #         with log_file.open("r", encoding="utf-8", errors="ignore") as f:
    #             print("".join(f.readlines()[-15:]))
    #
    #     shutil.rmtree(temp_dir, ignore_errors=True) # это для дебага



# Пример:
formula = r"""
\[
\int x^2 \, dx = \frac{x^{3}}{3} + C
\]
"""
render_latex_to_png(formula, "ee")
# int x^2 \, dx = \frac{x^{3}}{3} + C