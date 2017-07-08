DATABASE_URL=$(heroku config:get DATABASE_URL -a tgrinstead-calculator)
echo $DATABASE_URL
web gunicorn Calculator:app