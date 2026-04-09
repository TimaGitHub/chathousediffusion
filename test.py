from denoising_diffusion_pytorch import Unet, GaussianDiffusion, Trainer, seed_torch
import os
import pickle
from PIL import Image
import pandas as pd

def organize_files_by_copying():
    # Названия папок
    source_dir = Path('results/cond_scale-1-98')
    output_dir = Path('results/org_cond_scale-1-98')

    # 1. Проверка существования исходной папки
    if not source_dir.exists():
        return

    # 2. Создание целевой папки
    output_dir.mkdir(exist_ok=True)

    counter = 0

    # 3. Проход по всем файлам в CHDResults
    for file_path in source_dir.iterdir():
        if file_path.is_file():
            # Извлекаем тип (все что до последнего дефиса)
            # Например: 'rgb_real-10.png' -> folder_name = 'rgb_real'
            filename = file_path.name
            if '-' in filename:
                folder_name = filename.rsplit('-', 1)[0]

                # Путь к подпапке (например, Sorted_Files/rgb_real)
                target_folder = output_dir / folder_name
                target_folder.mkdir(exist_ok=True)

                # Копируем файл (copy2 сохраняет метаданные и НЕ удаляет оригинал)
                try:
                    shutil.copy2(file_path, target_folder / filename)
                    counter += 1
                except Exception as e:
                    print(f"Не удалось скопировать {filename}: {e}")
                    

if __name__ == "__main__":

    os.environ["CUDA_VISIBLE_DEVICES"] = "2"
    results_folder = "./results"
    train_num_workers = 0
    with open(os.path.join(results_folder, "params.pkl"), "rb") as f:
        params = pickle.load(f)

    model = Unet(**params["unet_dict"])

    params["diffusion_dict"]["sampling_timesteps"] = 2

    diffusion = GaussianDiffusion(model, **params["diffusion_dict"])

    trainer = Trainer(
        diffusion,
        "./chat_test_data/0614-kimi/image",
        "./chat_test_data/0614-kimi/mask",
        "./chat_test_data/0614-kimi/text",
        **params["trainer_dict"],
        results_folder=results_folder,
        train_num_workers=train_num_workers,
        mode="val",
    )

    seed_torch()
    trainer.val(load_model=98)
    organize_files_by_copying()
    
