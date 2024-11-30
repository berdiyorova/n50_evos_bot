from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = "7756798068:AAH4y-6ASp2fXif1C-Xd7qur6i0FALiRb7c"
ADMINS = env.list("ADMINS")
DEVS = env.list("DEVS")

DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_HOST = env.str("DB_HOST")
DB_PORT = env.str("DB_PORT")
DB_NAME = env.str("DB_NAME")

# BOT_TOKEN = "7756798068:AAH4y-6ASp2fXif1C-Xd7qur6i0FALiRb7c"
# ADMINS = "986930502"
# DEVS = "986930502"
#
# DB_NAME = "n50_evos"
# DB_HOST = "localhost"
# DB_PORT = "5432"
# DB_USER = "postgres"
# DB_PASS = "Rrshv1719"

I18N_DOMAIN = 'lang'
LOCALES_DIR = 'locale'
