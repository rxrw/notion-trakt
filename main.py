from datetime import datetime
import json
import os
from time import sleep
from notionapi.reader import insert_item, query_items, query_latest_item_watched_at, update_item
import pytz

from traktor import helpers, tmdb


def sync_from_trakt_to_notion():
    database_id = os.environ.get("NOTION_DATABASE_ID", "")
    start_at = query_latest_item_watched_at(database_id)
    for item in helpers.get_watched_history():
        detail = item.to_dict()

        if start_at is not False and start_at >= item.watched_at:
            return

        notion_item = query_items(database_id, int(detail["ids"]["trakt"]))

        exists = "results" in notion_item and len(notion_item["results"]) > 0

        item_watched_at = item.watched_at
        if (
                exists
                and item_watched_at
                <= datetime.fromisoformat(notion_item["results"][0]["properties"]["Last Viewed At"]["date"]["start"])
        ):
            continue
        print("Querying", detail["title"])

        if exists:
            print("Updating", detail["title"])
            update_item(notion_item["results"][0]["id"], last_viewed_at=item.watched_at, rating=detail["rating"])
        else:
            print("Inserting", detail['title'])
            movie = tmdb.get_movie_detail(int(detail["ids"]["tmdb"]))
            tags = []
            for tag in movie["genres"]:
                tags.append(tag["name"].replace(",", ""))
            production_companies = []
            for company in movie["production_companies"]:
                production_companies.append(company["name"].replace(",", ""))
            production_countries = []
            for country in movie["production_countries"]:
                production_countries.append(country["name"].replace(",", ""))
            if "tagline" in movie and movie["tagline"] != "":
                detail["tagline"] = movie["tagline"]
            insert_item(database_id,
                        name=movie["title"],
                        tags=tags,
                        trakt_id=detail["ids"]["trakt"],
                        imdb_id=detail["ids"]["imdb"] if "imdb" in detail["ids"] else "",
                        tmdb_id=detail["ids"]["tmdb"],
                        last_viewed_at=item.watched_at,
                        rating=detail["rating"],
                        release_date=detail["released"],
                        overview=movie["overview"],
                        year=detail["year"],
                        countries=production_countries,
                        original_name=movie["original_title"],
                        tagline=detail["tagline"] if "tagline" in detail else "",
                        english_name=detail["title"],
                        production_companies=production_companies,
                        poster_url="https://image.tmdb.org/t/p/w500" + movie["poster_path"]
                        )


if __name__ == "__main__":
    while True:
        sync_from_trakt_to_notion()
        sleep(60)
