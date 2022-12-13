import datetime as dt
from datetime import datetime
import os
from notion_client import Client

notion = Client(auth=os.environ.get("NOTION_SECRET", ""))


def get_database(database_id):
    return notion.databases.retrieve(database_id)


def query_items(database_id, trakt_id):
    return notion.databases.query(
        database_id, filter={"property": "Trakt ID", "number": {"equals": trakt_id}}
    )


def query_latest_item_watched_at(database_id):
    item = notion.databases.query(
        database_id, sorts=[{"property": "Last Viewed At", "direction": "descending"}], page_size=1
    )
    if len(item["results"]) > 0:
        return datetime.fromisoformat(item["results"][0]["properties"]["Last Viewed At"]["date"]["start"])
    return False


def insert_item(
        database_id: str,
        name: str,
        tags: list,
        trakt_id: int,
        last_viewed_at: datetime,
        # collected_at: str,
        poster_url: str,
        year: int,
        english_name: str,
        original_name: str,
        tmdb_id: int,
        imdb_id: str,
        overview: str,
        rating: float,
        countries: list,
        # play_times: int,
        release_date: str,
        production_companies: list,
        tagline: str
):
    # convert last_viewed_at like "2021-01-01T00:00:00.000Z"
    str_last_viewed_at = (last_viewed_at + dt.timedelta(hours=8)).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    return notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "Name": {"title": [{"text": {"content": name}}]},
            "Tags": {"multi_select": [{"name": tag} for tag in tags]},
            "Trakt ID": {"number": int(trakt_id)},
            "Last Viewed At": {"date": {"start": str_last_viewed_at, "time_zone": "Asia/Shanghai"}},
            "Countries": {"multi_select": [{"name": country} for country in countries]},
            "Year": {"number": int(year)},
            "Release Date": {"date": {"start": release_date}},
            "English Name": {"rich_text": [{"text": {"content": english_name}}]},
            "Original Name": {"rich_text": [{"text": {"content": original_name}}]},
            "TMDB ID": {"number": int(tmdb_id)},
            "IMDB ID": {"rich_text": [{"text": {"content": imdb_id}}]},
            "Overview": {"rich_text": [{"text": {"content": overview}}]},
            "Rating": {"number": float(rating)},
            # "Plays": {"number": play_times},
            "Production Companies": {"multi_select": [{"name": company} for company in production_companies]},
            "Tagline": {"rich_text": [{"text": {"content": tagline}}]},
        },
        cover={"type": "external", "external": {"url": poster_url}},
    )


def update_item(
        page_id,
        last_viewed_at: datetime,
        rating: float,
):
    str_last_viewed_at = (last_viewed_at + dt.timedelta(hours=8)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return notion.pages.update(
        page_id,
        properties={
            "Last Viewed At": {"date": {"start": str_last_viewed_at, "time_zone": "Asia/Shanghai"}},
            "Rating": {"number": rating},
        },
    )
