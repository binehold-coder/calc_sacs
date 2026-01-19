# ===================================================
# РАЗВЁРТЫВАНИЕ БОТА НА СЕРВЕРЕ IONOS (Ubuntu 24.04)
# IP: 87.106.25.155
# ===================================================

# ШАГ 1: Подключение к серверу
ssh root@87.106.25.155

# ШАГ 2: Обновление системы
apt update && apt upgrade -y

# ШАГ 3: Установка необходимых пакетов
apt install -y python3 python3-pip python3-venv git

# ШАГ 4: Переход в папку /opt
cd /opt

# ШАГ 5: Клонирование репозитория
git clone https://github.com/binehold-coder/calc_sacs.git

# ШАГ 6: Переход в папку проекта
cd calc_sacs

# ШАГ 7: Создание виртуального окружения Python
python3 -m venv venv

# ШАГ 8: Активация виртуального окружения
source venv/bin/activate

# ШАГ 9: Установка зависимостей
pip install --upgrade pip
pip install -r requirements.txt

# ШАГ 10: Создание файла .env с токеном
nano .env

# В nano вставь:
# TELEGRAM_BOT_TOKEN=ваш_токен_от_BotFather
# Сохрани: Ctrl+O, Enter, Ctrl+X

# ШАГ 11: Тестовый запуск (Ctrl+C для остановки)
python bot.py

# Если всё работает, переходи к созданию systemd сервиса:

# ШАГ 12: Создание systemd сервиса
nano /etc/systemd/system/calc-sacs-bot.service

# Вставь следующее содержимое:
# [Unit]
# Description=Telegram Sacs Calculator Bot
# After=network.target
#
# [Service]
# Type=simple
# User=root
# WorkingDirectory=/opt/calc_sacs
# ExecStart=/opt/calc_sacs/venv/bin/python bot.py
# Restart=always
# RestartSec=10
#
# [Install]
# WantedBy=multi-user.target

# Сохрани: Ctrl+O, Enter, Ctrl+X

# ШАГ 13: Активация и запуск сервиса
systemctl daemon-reload
systemctl enable calc-sacs-bot
systemctl start calc-sacs-bot

# ШАГ 14: Проверка статуса
systemctl status calc-sacs-bot

# ШАГ 15: Просмотр логов в реальном времени
journalctl -u calc-sacs-bot -f

# ===================================================
# ПОЛЕЗНЫЕ КОМАНДЫ ДЛЯ УПРАВЛЕНИЯ
# ===================================================

# Остановить бота:
# systemctl stop calc-sacs-bot

# Перезапустить бота:
# systemctl restart calc-sacs-bot

# Посмотреть логи:
# journalctl -u calc-sacs-bot -n 50

# Обновить код из GitHub:
# cd /opt/calc_sacs
# git pull origin main
# systemctl restart calc-sacs-bot

# Проверить, что бот работает:
# systemctl is-active calc-sacs-bot

# ===================================================
# ГОТОВО! Бот работает 24/7
# ===================================================
