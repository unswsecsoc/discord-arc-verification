discord verification bot
========================

https://arc-verification.unswsecurity.com


i dunno, needs a better readme

## Hosting instructions
1. Get a mailgun key, discord bot key
2. Use the exampledotenv template to populate your secrets.
3. Use docker-compose 1.25 or above to run the stack. Command: `docker-compose --env-file app.env up -d`
4. Manually migrate using `./scripts/migrate.sh` because I haven't gotten
around to doing that yet.
5. Restart the API service by running `docker-compose --env-file app.env up api -d`

## Discord configuration instructions
TODO

## Features
TODO