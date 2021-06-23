# astat
Telegram Bot for agentstats.com written in Python 3. /n
No Databas eneeded./n
copy secrets.example.py to secrets.py and fill your secrets.

create a crontab and run for Testmode:
python astats_bot.py --check LevelUp --Test
python astats_bot.py --check Badges --Test
python astats_bot.py --check DailyStats --Test

run for real
python astats_bot.py --check LevelUp
python astats_bot.py --check Badges
python astats_bot.py --check DailyStats
