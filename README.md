# Exam

## Pyinstaller

```commandline
pyinstaller -F .\main.py -n shoes --icon=icon.ico --noconsole

pyinstaller -F .\main.py -n shoes --icon=icon.ico --noconsole --add-data "media;media" --collect-all mysql.connector
```

> Папка media с файлами-картинками должна находится рядом с exe

## Env

```dotenv
DB_PASSWORD="qwerty123"
```

## Venv

```commandline
python -m venv venv
venv\Scripts\activate
deactivate
```

## Repo

```shell
git remote add origin git@github.com:ej-you/dem_dudkov_is_45.git
git branch -M master
git push -u origin master
```
