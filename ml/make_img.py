import matplotlib.pyplot as plt
from pdf2image import convert_from_path


def latex_to_png(latex_str, file_name):
    fig = plt.figure()
    plt.axis("off")
    plt.text(0.5, 0.5, f"${latex_str}$", size=50, ha="center", va="center")

    pdf_path = f"{file_name}.pdf"
    png_path = f"{file_name}.png"

    plt.savefig(pdf_path, format="pdf", bbox_inches="tight", pad_inches=0.4)
    plt.close(fig)

    images = convert_from_path(pdf_path)
    images[0].save(png_path, "PNG")

    return png_path


def latex_to_png_all(latex_str_list, output_path="result.png"):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis("off")

    y_positions = [0.8 - i * 0.2 for i in range(len(latex_str_list))]

    for latex_str, y in zip(latex_str_list, y_positions):
        ax.text(0.5, y, f"${latex_str}$",
                size=30,
                ha="center",
                va="center",
                usetex=False)

    pdf_path = "temp.pdf"
    plt.savefig(pdf_path, format="pdf", bbox_inches="tight", pad_inches=0.5)
    plt.close(fig)

    images = convert_from_path(pdf_path)
    images[0].save(output_path, "PNG")

    return output_path


if __name__ == "__main__":
    latex_formula = r"\theta^2 = x_1 + y_2"
    result_path = latex_to_png(latex_formula, "result")
    print(f"Изображение сохранено как: {result_path}")

    formulas = [
        r"\theta^2 = x_1 + y_2",
        r"\sum_{i=1}^n i = \frac{n(n+1)}{2}",
        r"e^{i\pi} + 1 = 0",
        r"\nabla \cdot \mathbf{E} = \frac{\rho}{\epsilon_0}"
    ]

    result_path = latex_to_png_all(formulas)
    print(f"Изображение с формулами сохранено как: {result_path}")