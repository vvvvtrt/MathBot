from bs4 import BeautifulSoup


def parse_math_problems(xml_data):
    soup = BeautifulSoup(xml_data, 'lxml')

    problems = []
    problem_block = soup.find('problem')
    if problem_block:
        for item in problem_block.stripped_strings:
            if item.strip():
                problems.append(item.strip())

    examples = {}
    answer_block = soup.find('answer')
    if answer_block:
        for example in answer_block.find_all('example'):
            ex_id = example.get('id', '')
            formul = example.find('formul').get_text(strip=True) if example.find('formul') else ''
            text = example.find('text').get_text(strip=True) if example.find('text') else ''
            if ex_id:
                examples[ex_id] = {'formul': formul, 'text': text}

    return problems, examples


def print_parsed_data(problems, examples):
    arr_slide = []
    arr_text = []
    arr_problems = []

    print("Задачи:")
    for i, problem in enumerate(problems, 1):
        print(f"{i}. {problem}")
        arr_problems.append(problem)

    print("\nРешения:")
    for ex_id, solution in examples.items():
        print(f"\nПример {ex_id}:")
        print(f"Формула: {solution['formul']}")
        print(f"Текст: {solution['text']}")

        arr_slide.append(solution['formul'])
        arr_text.append(solution['text'])

    return arr_slide, arr_text, arr_problems


if __name__ == "__main__":
    data = """
<problem>
1. \[\int x^2 \, dx = ?\]
2. \[\int e^{2x} \cos x \, dx = ?\]
3. \[\int \frac{x^3 + 2x}{x^2} \, dx = ?\]
4. \[\int (5x - 3)^7 \, dx = ?\]
5. \[\int \frac{x^4 + 1}{x^3 - x} \, dx = ?\]
</problem>

<answer>
<example id="1">
<formul>
1.\[\int x^2 \, dx = \dfrac{x^{3}}{3} + C\]
</formul>
<text>
Этот интеграл решается с помощью простого применения правила интегрирования для等多项номов.
</text>
</example>

<example id="2">
<formul>
2.\[\int e^{2x} \cos x \, dx = \dfrac{e^{2x}}{5}(2\cos x + \sin x) + C\]
</formul>
<text>
Для решения этого интеграла необходимо использовать метод интегрирования по частям дважды.
</text>
</example>

<example id="3">
<formul>
3.\[\int \dfrac{x^3 + 2x}{x^2} \, dx = \dfrac{x^2}{2} + x\ln|x| - 4\sqrt{x} + C\]
</formul>
<text>
Первым шагом упрощаем дробь и интегрируем каждое слагаемое отдельно.
</text>
</example>

<example id="4">
<formul>
4.\[\int (5x - 3)^7 \, dx = \dfrac{(5x - 3)^8}{40} + C\]
</formul>
<text>
Этот интеграл решается методом подстановки, где u = 5x - 3.
</text>
</example>

<example id="5">
<formul>
5.\[\int \dfrac{x^4 + 1}{x^3 - x} \, dx = \dfrac{x^4}{4} - \ln|x| + C\]
</formul>
<text>
Первым шагом выполняем деление многочленов и интегрируем полученные слагаемые.
</text>
</example>
</answer>

Process finished with exit code 0

    """

    problems, examples = parse_math_problems(data)
    print_parsed_data(problems, examples)