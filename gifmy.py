from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip
import os


def create_frame(text, width=400, height=200):
    # Создаем изображение
    img = Image.new('RGB', (width, height), color=(73, 109, 137))
    d = ImageDraw.Draw(img)

    # Настраиваем шрифт
    font = ImageFont.load_default()

    # Добавляем текст на изображение
    text_bbox = d.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    position = ((width - text_width) / 2, (height - text_height) / 2)
    d.text(position, text, fill=(255, 255, 255), font=font)

    return img


def generate_countdown_gif(duration=120, step=1, output_path='countdown.gif'):
    frames = []

    # Создаем кадры для каждого шага
    for i in range(duration, -1, -step):
        minutes = i // 60
        seconds = i % 60
        text = f'{minutes:02}:{seconds:02}'
        frame = create_frame(text)
        frames.append(frame)

    # Сохраняем кадры во временные файлы
    temp_dir = 'temp_frames'
    os.makedirs(temp_dir, exist_ok=True)
    frame_paths = []
    for idx, frame in enumerate(frames):
        frame_path = os.path.join(temp_dir, f'frame_{idx:04d}.png')
        frame.save(frame_path)
        frame_paths.append(frame_path)

    # Создаем GIF из кадров с правильным fps
    clip = ImageSequenceClip(frame_paths, fps=1)  # 1 кадр в секунду
    clip.write_gif(output_path)

    # Удаляем временные файлы
    for frame_path in frame_paths:
        os.remove(frame_path)
    os.rmdir(temp_dir)


# Генерируем GIF с обратным отсчетом
generate_countdown_gif()


