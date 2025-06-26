<h1>Скрипт для обработки csv-файлов с поддержкой фильтрации и агрегации по одной колонке. Использует ООП, абстрактные классы, dataclass, фабричный паттерн. Для вывода используется tabulate.
</h1>>
<h3>Инструкция по установке</h3>

1. Клонируйте репозиторий
```bash
git clone https://github.com/Dimmentor/workmate2.git
```
2. Установите зависимости:

```bash
pip install -r requirements.txt
```

<h3>Предлагаю следующий гайд по тестированию</h3>

```bash
python main.py --file product.csv
python main.py --file product.csv --where "rating>4.7"
python main.py --file product.csv --where "brand=apple"
python main.py --file product.csv --aggregate "rating=avg"
python main.py --file product.csv --where "brand=xiaomi" --aggregate "rating=min"
```
<h3>Доступные аргументы:</h3> 
- `--file` — путь к CSV-файлу
- `--where` — фильтрация по одной колонке (>, <, =)
- `--aggregate` — агрегация по одной числовой колонке (avg, min, max)

<h3>Можно попробовать поиграть с обработкой ошибок, вводя неверные данные. К примеру: создать пустой .csv файл</h3> 
Запуск тестов:

```bash
pytest
```

<h3>Содержимое файла product.csv:</h3>

```
name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
poco x5 pro,xiaomi,299,4.4
``` 