# Sync your trakt watched list to Notion database

Use this script to sync your trakt watched list to Notion database.

## Usage

### On Notion
1. Create a Notion database from <https://www.notion.so/rxrw/df31e19f1cd44e7a8398e3c57c87b06d?v=a6ec1df76b5444a690076b96d943a0a0>

### This project
#### Code
1. Clone the repository.
2. Set variables:
  * `TRAKT_CLIENT_ID` and `TRAKT_CLIENT_SECRET` from <https://trakt.tv/oauth/applications>
  * `NOTION_SECRET` from <https://www.notion.so/my-integrations>
  * `NOTION_DATABASE_ID` from the database URL
  * `TMDB_ID` from <https://www.themoviedb.org/settings/api>
3. Run `python3 main.py`

#### Docker
```bash
docker run -e TRAKT_CLIENT_ID=xxx -e TRAKT_CLIENT_SECRET=xxx -e NOTION_SECRET=xxx -e NOTION_DATABASE_ID=xxx -e TMDB_ID=xxx -name notion-trakt reprover/notion-trakt
```

## Note
Default it's for Chinese users(timezone and language), you can change the code.

You can run this when you want to sync.

It's just for my personal use, so welcome any PRs for improving the code quaility.