discord verification bot
========================

https://arc-verification.unswsecurity.com


## Hosting instructions
1. Get a Mailgun API key (required for sending email, note: costs a small amount of money) and a Discord
bot key.
2. Using the exampledotenv file as a template, create a prod.env file with all the required details.
3. Use docker-compose 1.25 or above to run the stack. Command: `docker-compose --env-file app.env up -d`
4. Manually migrate using `./scripts/migrate.sh` because I haven't gotten around to doing that yet.
5. Restart the API service by running `docker-compose --env-file app.env up api -d` otherwise it won't
connect to a non-existent database.

## Notes
- This bot was designed to be able to service multiple clubs on multiple servers, but is currently only
being used by the UNSW Security Society.
- Still working on a more granular security model, but it should be fine for now.

## Discord configuration instructions


## Features
TODO
