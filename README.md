# KGBTRBot **HORT** module

![KGBTRBot Logo](https://user-images.githubusercontent.com/29407019/111668072-6b951800-8826-11eb-9f77-7ace7ecd866e.png)

## What is? 🤔

### What is **KGBTRBot**?

To put it simply, KGBTR Bot is a reddit bot developed to meet the needs(moderation or fun) of [r/KGBTR](https://reddit.com/r/KGBTR) subreddit.

### What is **HORT**?

Hort is an expression specific to KGBTR community. This commune uses this term for repost submission or post.

## Requirements ⚓

- Python >= 3.6
- Python 3 knowledge 😀
- PostgreSQL Database ([You can use heroku PostgreSQL add-on](https://elements.heroku.com/addons/heroku-postgresql))

## Installation 🦆

### You can quickly start with `Deploy to Heroku` button right now

[![Deploy on Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/KGBTR/Reddit-Repost-Bot)

### If you want running locally you can follow this steps

1. Clone this repo into local project directory.

2. `pip install -r requirements.txt`

3. On Unix-based systems, you must doing `.env.example` rename as `.env` via `mv .env.example .env`. If you are using Windows-based system, you can use Powershell's `Rename-Item .env.example .env`. You need to do this terminal command to the project root folder.

4. Fill the inside of the `.env` file with the environment variables. Like this: 

```dotenv
  DATABASE_URL=postgresql://localhost:5433/mydb
```

5. Run both command `python src/main.py` and `python src/hoarder.py`

### If you want running locally with `docker-compose` you follow this steps 🐳

1. `docker-compose up`. It's that easy with `docker-compose` 😄
2. `docker-compose` services down below:
   - hoarder
   - main

## Contributing 🎉

We love the open source. We appreciate to any kind of contribution. Let's open a PR (Pull Request acronym) 🎊

## Licence 📋

This project under the [MIT license](LICENSE).
