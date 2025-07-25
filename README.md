# 🐍 Змейка

Простая и классическая реализация игры **Змейка** на языке Python с использованием библиотеки **pygame**.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7%2B-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Pygame-%3E=2.0-green" alt="Pygame Version">
  <img src="https://img.shields.io/badge/license-MIT-lightgrey.svg" alt="License">
</p>

## 🎮 Описание

Змейка — это классическая аркадная игра, в которой игрок управляет змейкой, поедающей яблоки. Каждое съеденное яблоко увеличивает длину змейки и прибавляет очки. Игра заканчивается, если змейка сталкивается сама с собой.

---

## 🚀 Как запустить

1. Убедитесь, что у вас установлен Python версии 3.7 или выше.
2. Установите зависимости:

```
pip install -r requirements.txt
```

3. Запустите игру:

```
python snake.py
```

(Файл должен называться `snake.py`, либо переименуйте ваш файл с кодом.)

---

## 🕹️ Управление

| Клавиша     | Действие           |
|-------------|--------------------|
| ↑           | Движение вверх     |
| ↓           | Движение вниз      |
| ←           | Движение влево     |
| →           | Движение вправо    |
| Esc         | Выход из игры      |

---

## 🧠 Особенности реализации

- Используется **объектно-ориентированное программирование (ООП)**: классы `Snake`, `Apple`, `GameObject`.
- Простая и эффективная логика отрисовки и перемещения.
- Змейка может проходить сквозь границы и появляться с противоположной стороны.
- Счетчик очков и скорости выводится в заголовке окна.
- Нет внешних зависимостей кроме `pygame`.

---

Приятной игры! 🐍
