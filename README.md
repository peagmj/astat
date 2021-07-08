# astat
Telegram Bot for agentstats.com written in Python 3. </br>
No Databas eneeded. </br>
copy secrets.example.py to secrets.py and fill your secrets. </br>

run for Testmode: </br>
python astats_bot.py --check LevelUp --group XFTeltow --language EN --Test </br>
python astats_bot.py --check Badges --group XFTeltow --language EN --Test </br>
python astats_bot.py --check DailyStats --group XFTeltow --MaxAgentsShown 8 --interval week --language EN --Test </br>

create a crontab and run for real </br>
python astats_bot.py --check LevelUp --group XFTeltow --language DE </br>
python astats_bot.py --check Badges --group XFTeltow --language EN </br>
python astats_bot.py --check DailyStats --group XFTeltow --MaxAgentsShown 8 --interval week --language DE </br>
