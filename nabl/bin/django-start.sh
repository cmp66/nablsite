export DJANGO_SETTINGS_MODULE=nabl.settings.prod_settings
#source ~/Projects/nabl/venv/bin/activate
export PYTHONPATH=$PYTHONPATH:~/projects/NABL
python -B manage.py runfcgi host=127.0.0.1 port=8001 --settings=nabl.settings.dev_settings
