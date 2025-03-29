import os
from gtts import gTTS
from pydub import AudioSegment
import cv2
import subprocess
import parsing as mlpars
import make_img as imgpars
import requests


def make_video(image_files, texts):
    # image_files = ["slide1.jpg", "slide2.jpg", "slide3.jpg"]
    # texts = ["Привет! Это первый слайд.", "Теперь второй слайд.", "И наконец третий!"]
    output_dir = "output"
    final_output = "final_combined_video.mp4"
    fps = 25

    os.makedirs(output_dir, exist_ok=True)

    video_files = []

    # Генерация аудио и видео для каждого слайда
    for i, (img_path, text) in enumerate(zip(image_files, texts)):
        # Генерация аудио
        tts = gTTS(text=text, lang='ru')
        audio_file = os.path.join(output_dir, f"slide_{i + 1}_audio.mp3")
        tts.save(audio_file)

        # Загрузка аудио для расчета длительности
        audio = AudioSegment.from_mp3(audio_file)
        duration = len(audio) / 1000  # Длительность в секундах

        # Создание видео
        img = cv2.imread(img_path)
        height, width, _ = img.shape
        video_file = os.path.join(output_dir, f"slide_{i + 1}_video.avi")

        video_writer = cv2.VideoWriter(
            video_file,
            cv2.VideoWriter_fourcc(*'DIVX'),
            fps,
            (width, height)
        )

        # Рассчет количества кадров
        frame_count = int(duration * fps)

        # Запись кадров
        for _ in range(frame_count):
            video_writer.write(img)

        video_writer.release()

        # Конвертация в MP4 с аудио
        final_clip = os.path.join(output_dir, f"slide_{i + 1}_final.mp4")
        subprocess.call([
            'ffmpeg',
            '-y',
            '-i', video_file,
            '-i', audio_file,
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-strict', 'experimental',
            '-shortest',
            final_clip
        ])

        video_files.append(final_clip)
        # Удаление промежуточных файлов
        os.remove(video_file)
        os.remove(audio_file)

    # Создаем список файлов для склейки
    list_file = os.path.join(output_dir, "list.txt")
    with open(list_file, 'w') as f:
        for vf in video_files:
            f.write(f"file '{os.path.abspath(vf)}'\n")

    # Склеиваем видео
    subprocess.call([
        'ffmpeg',
        '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', list_file,
        '-c', 'copy',
        final_output
    ])

    # Удаляем временные файлы
    os.remove(list_file)
    for vf in video_files:
        os.remove(vf)

    print(f"Все слайды успешно склеены в финальное видео: {final_output}")


def main(data):
    problems, examples = mlpars.parse_math_problems(data)
    arr_formul, arr_text, arr_problems = mlpars.print_parsed_data(problems, examples)
    arr_slide = []

    for i in range(len(arr_formul)):
        imgpars.latex_to_png(arr_formul[i], f"slide_{i}")
        arr_slide.append(f"slide_{i}.png")

    imgpars.latex_to_png_all(arr_problems, "problem.png")
    make_video(arr_slide, arr_text)


def request_to_ml(patterns, count):
    prompt = """Сделай только примеры без комментариев в фомате и потом через раделитель <answer> решение, сделай в таком формате как ниже используя только теги которые есть ниже, в теге <text> обьясни решение обязательно, фомулы в стиле latex но не засовывай их в какие то скобки для выделения latex, соблюдай формат и стиль latex:
<problem>
1. \int x^2 \, dx = ?\
2. d * e = ?
</problem>
<answer>
<example id="1">
<formul>
1.\int x^2 \, dx = \frac{x^{3}}{3} + C\
</formul>
<text>
Этот интеграл решается вот так легко.
<text>
</example>
<example id="2">
<formul>
2. d * e = f
</formul>
<text>
Этот пример решается вот так легко.
<text>
</example>
</answer>
Тема на которую надо сделать примеры: """

    url = "http://54.158.41.142:11434/api/generate"
    data = {
        "model": "deepseek-r1",
        "prompt": prompt + f"Придумай {count} сложных примеров, используя темы {patterns}",
        "stream": False
    }

    response = requests.post(url, json=data).json()
    answer = response["response"]
    data = answer[answer.index("</think>") + 8:]
    #===
    problems, examples = mlpars.parse_math_problems(data)
    arr_formul, arr_text, arr_problems = mlpars.print_parsed_data(problems, examples)
    arr_slide = []

    for i in range(len(arr_formul)):
        imgpars.latex_to_png(arr_formul[i], f"slide_{i}")
        arr_slide.append(f"slide_{i}.png")

    imgpars.latex_to_png_all(arr_problems, "problem.png")

    return "problem.png"
