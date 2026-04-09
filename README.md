# ChatHouseDiffusion

## Установка

### 1. Системные требования
Перед началом работы убедитесь, что в системе установлен **Microsoft Visual C++ Redistributable**. 

### 2. Клонирование и настройка Python
Выполните команды в терминале:

```bash
# Клонирование репозитория
git clone https://github.com/ChatHouseDiffusion/chathousediffusion.git
cd chathousediffusion

# Установка зависимостей
pip install -r requirements.txt
```

---

## Подготовка данных и весов

### 1. Тестовые данные
1. Скачайте архив с данными по [этой ссылке](https://cloud.tsinghua.edu.cn/f/2844208e0c344d18bd72/).
2. Извлеките папки `image_test`, `mask_test` и `text_test`.
3. Разместите их строго по следующему пути:

```text
chathousediffusion/
└── chat_test_data/
    └── 0614-kimi/
        ├── image_test/
        ├── mask_test/
        └── text_test/
```

### 2. Веса модели
1. Скачайте веса по [этой ссылке](https://cloud.tsinghua.edu.cn/f/a01a8205be55462685fd/).
2. Извлеките содержимое и поместите файлы в две директории (создайте их, если они отсутствуют):
   * `prefict_model/`
   * `results/`

---

## Конфигурация API

Для работы модуля LLM (GPT-4, Kimi, Ollama и др.) создайте файл `api_info.json` в корневой директории проекта и добавьте туда свои данные:

```json
{
  "api_key": "<ваш_api_key>",
  "base_url": "https://api.moonshot.cn/v1",
  "model": "moonshot-v1-8k"
}
```
*Примечание: Поддерживается любой провайдер, использующий формат OpenAI.*

---

## Запуск

### Интерфейс (UI)
Для запуска графического интерфейса используйте:
```bash
python ui.py
```

### Тестирование и визуализация
Для проведения тестов и визуального сравнения результатов выполните:
```bash
# Запуск тестов
python test.py

# Визуальная проверка результатов
python visualize_check.py
```
<img width="1487" height="874" alt="image" src="https://github.com/user-attachments/assets/9556a551-fcd7-4fd6-a10b-a4535832a584" />
