# Калькулятор мешков поддонов (Sacs Calculator)

## О проекте
Telegram бот для расчёта количества мешков поддонов на основе количества линий и дополнительных мешков.

## Логика работы
- **Нечётные линии (1,3,5,...,17)**: 10 мешков каждая
- **Чётные линии (2,4,6,...,16)**: 9 мешков каждая
- **Дополнительные мешки**: прибавляются к итогу

### Пример расчёта:
```
11 линий + 8 мешков
= (6 нечётных × 10) + (5 чётных × 9) + 8
= 60 + 45 + 8
= 113 мешков
```

## Требования
- Python 3.11+
- python-telegram-bot v20+
- Ubuntu 24.04 (для хостинга)

## Локальная установка

### 1. Клонируем репозиторий
```bash
git clone https://github.com/yourusername/calc_sacs.git
cd calc_sacs
```

### 2. Создаём виртуальное окружение
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

### 3. Устанавливаем зависимости
```bash
pip install -r requirements.txt
```

### 4. Настраиваем переменные окружения
```bash
cp .env.example .env
# Открываем .env и вставляем свой токен Telegram
nano .env
```

### 5. Получаем токен Telegram
1. Напиши @BotFather в Telegram
2. Введи `/newbot`
3. Следуй инструкциям и получи токен
4. Вставь токен в файл `.env`: `TELEGRAM_BOT_TOKEN=your_token_here`

### 6. Запускаем бота локально
```bash
python bot.py
```

## Команды бота
- `/start` - Начать новый расчёт
- `/calc` - Расчитать количество мешков
- `/help` - Справка по использованию

## Развёртывание на хостинге IONOS

### Шаг 1: Подготовка сервера
```bash
ssh root@87.106.25.155
```

### Шаг 2: Обновляем систему
```bash
apt update && apt upgrade -y
apt install -y python3.11 python3-pip git
```

### Шаг 3: Клонируем репозиторий
```bash
cd /opt
git clone https://github.com/yourusername/calc_sacs.git
cd calc_sacs
```

### Шаг 4: Создаём виртуальное окружение
```bash
python3 -m venv venv
source venv/bin/activate
```

### Шаг 5: Устанавливаем зависимости
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Шаг 6: Создаём файл .env на сервере
```bash
nano .env
```
Вставь:
```
TELEGRAM_BOT_TOKEN=your_token_here
```

### Шаг 7: Создаём systemd сервис
```bash
nano /etc/systemd/system/calc-sacs-bot.service
```

Содержимое:
```ini
[Unit]
Description=Telegram Sacs Calculator Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/calc_sacs
ExecStart=/opt/calc_sacs/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Шаг 8: Запускаем сервис
```bash
systemctl daemon-reload
systemctl enable calc-sacs-bot
systemctl start calc-sacs-bot
```

### Шаг 9: Проверяем статус
```bash
systemctl status calc-sacs-bot
journalctl -u calc-sacs-bot -f
```

## Остановка/Перезагрузка бота
```bash
# Остановка
systemctl stop calc-sacs-bot

# Перезагрузка
systemctl restart calc-sacs-bot

# Логи в реальном времени
journalctl -u calc-sacs-bot -f
```

## Обновление бота на хостинге
```bash
cd /opt/calc_sacs
git pull origin main
systemctl restart calc-sacs-bot
```

## Структура проекта
```
calc_sacs/
├── bot.py              # Основной код бота
├── requirements.txt    # Зависимости Python
├── .env.example        # Пример переменных окружения
├── .env                # Переменные окружения (не в git)
├── .gitignore          # Игнорируемые файлы
└── README.md           # Этот файл
```

## Решение проблем

### Бот не запускается
```bash
# Проверьте логи
journalctl -u calc-sacs-bot -f

# Проверьте, что токен в .env
cat .env
```

### "ModuleNotFoundError: No module named 'telegram'"
```bash
pip install -r requirements.txt
```

### Бот не отвечает
1. Убедитесь, что сервис запущен: `systemctl status calc-sacs-bot`
2. Проверьте логи: `journalctl -u calc-sacs-bot -f`
3. Перезагрузите: `systemctl restart calc-sacs-bot`

## Лицензия
MIT

## Автор
Created with ❤️
