# GenCheckAiBot
Продуктовая часть проекта на "Большие вызовы"

[ML часть](https://github.com/dima0409/GenCheckAIBot)

Проект подготовлен с использованием изображений, сгенерированных моделью Yandex Art в приложении Шедеврум.  
Изображения предоставлены исключительно для исследовательских целей данного проекта выпускнику Яндекс Лицея и не предназначены для публичного использования

## Технологии 
- Aiogram
- PyTorch
- SQLAlchemy

## Необходимое ПО
[Python 3.12](https://www.python.org/downloads)

[CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit)

## Установка

1. Склонируйте репозиторий
```bash
git clone https://github.com/dima0409/GenCheckAiModel.git
cd GenCheckAiModel
```

2. Создайте виртуальное окружение и активируйте его
```bash
python3 -m venv venv
```
Активация на windows:
```bash
.\venv\bin\activate
```
Активация на linux:
```bash
source venv/bin/activate
```

3. Установите зависимость
```bash
pip install -r requirements\<версия CUDA/cpu>.txt
```
Например:
```bash
pip install -r requirements\12_6.txt
```
## Запуск бота
Открой файл `template.env`, поменяйте значения переменных среды и выполите следующую команду:

Для windows
```bash
copy template.env .env
```
Для linux
```bash
cp template.env .env
```

Для запуска бота пропишите команду:
```bash
python3 main.py
```