# RUN

### Normal run

    /usr/bin/python3 ./main.py

### Run when `UNSAFE_LEGACY_RENEGOTIATION_DISABLED`

    OPENSSL_CONF=./openssl.cnf /usr/bin/python3 ./main.py

# CRON

1. Edit `crontab` running `crontab -e` command
2. Add `crontab` line:

    
    0 */8 * * * /usr/bin/python3 ~/uy_exchange/main.py
