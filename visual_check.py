import os
import re
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PIL import Image

# 1. Настройка путей
folders = {'sample': 'results/org_cond_scale-1-98/rgb_sample', 'real': 'results/org_cond_scale-1-98/rgb_real', 'text': 'results/org_cond_scale-1-98/val_text'}

# Сбор индексов
try:
    all_indices = sorted([int(re.findall(r'\d+', f)[0]) for f in os.listdir(folders['sample']) if f.endswith('.png')])
except Exception as e:
    print(f"Ошибка при поиске файлов: {e}")
    all_indices = []

current_idx = 0


def get_legend_data():
    colors = [
        [238, 232, 170], [255, 165, 0], [240, 128, 128], [173, 216, 210],
        [107, 142, 35], [218, 112, 214], [221, 160, 221], [255, 215, 0],
        [0, 0, 0], [255, 225, 25], [128, 128, 128], [255, 255, 255]
    ]
    labels = ["Living Room", "Master Room", "Kitchen", "Bathroom", "Balcony", "Dining Room", "Storage", "Common Room",
              "Exterior Wall", "Front Door", "Interior Wall", "Background"]
    return [(labels[i], np.array(colors[i]) / 255.0) for i in range(len(labels))]


def parse_val_text_plain(n):
    """Парсинг JSON в обычный текст для Matplotlib"""
    path = os.path.join(folders['text'], f"val_text-{n}.txt")
    if not os.path.exists(path): return "Описание не найдено"
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        lines = ["Layout Summary:"]
        for room_type, details in data.items():
            for r in details.get('rooms', []):
                flat_links = []
                for link_group in r.get('link', []):
                    if isinstance(link_group, list):
                        flat_links.extend(link_group)
                    else:
                        flat_links.append(link_group)

                links_str = ", ".join(flat_links) if flat_links else "none"
                lines.append(f"• {r['name']} [{r['size']}]")
                lines.append(f"  Loc: {r['location']}")
                lines.append(f"  Links: {links_str}\n")
        return "\n".join(lines)
    except Exception as e:
        return f"Ошибка текста: {str(e)}"


def update_plot():
    global current_idx
    if not all_indices:
        print("Данные не найдены!")
        return

    n = all_indices[current_idx]
    fig.clear()

    # Создаем сетку: слева текст, справа два изображения
    # Сетка 1 строка, 3 колонки (1-я под текст, 2-я и 3-я под картинки)
    ax_text = fig.add_subplot(1, 3, 1)
    ax_real = fig.add_subplot(1, 3, 2)
    ax_sample = fig.add_subplot(1, 3, 3)

    # 1. Отрисовка текста
    txt_content = parse_val_text_plain(n)
    ax_text.text(0.05, 0.95, txt_content, transform=ax_text.transAxes,
                 fontsize=9, verticalalignment='top', family='monospace')
    ax_text.axis('off')

    # 2. Отрисовка изображений
    mapping = [(ax_real, 'real', 'RGB Real'), (ax_sample, 'sample', 'RGB Sample')]
    for ax, key, title in mapping:
        path = os.path.join(folders[key], f"rgb_{key}-{n}.png")
        if os.path.exists(path):
            ax.imshow(Image.open(path))
            ax.set_title(title, fontsize=12, fontweight='bold')
        ax.axis('off')

    # 3. Легенда
    patches = [mpatches.Patch(color=c, label=l) for l, c in get_legend_data()]
    fig.legend(handles=patches, title="Room Types", loc='lower center',
               ncol=4, fontsize=8, frameon=True, bbox_to_anchor=(0.5, 0.02))

    fig.suptitle(f"Образец N={n} ({current_idx + 1}/{len(all_indices)})\n"
                 f"Используйте ← и → для навигации", fontsize=14)

    plt.draw()


def on_key(event):
    global current_idx
    if event.key == 'right':
        current_idx = (current_idx + 1) % len(all_indices)
        update_plot()
    elif event.key == 'left':
        current_idx = (current_idx - 1) % len(all_indices)
        update_plot()
    elif event.key == 'escape':
        plt.close()


# Инициализация окна
fig = plt.figure(figsize=(12, 7))
fig.canvas.manager.set_window_title('Floorplan Viewer')
fig.canvas.mpl_connect('key_press_event', on_key)

if all_indices:
    update_plot()
    print("Управление: стрелки Влево/Вправо — навигация, ESC — выход.")
    plt.show()
else:
    print("Проверьте пути к папкам. Изображения не найдены.")
