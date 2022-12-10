from __future__ import absolute_import, division, print_function
import json
import os

from trakt import Trakt

import six


def _authenticate():
    authorization = None
    try:
        with open("authorization.json", "r") as fp:
            authorization = json.load(fp)
    except IOError:
        print("No authorization found, requesting new one")
    if authorization:
        return authorization

    print("Navigate to: %s" % Trakt["oauth"].authorize_url("urn:ietf:wg:oauth:2.0:oob"))

    code = six.moves.input("Authorization code:")
    if not code:
        exit(1)

    authorization = Trakt["oauth"].token(code, "urn:ietf:wg:oauth:2.0:oob")
    if not authorization:
        exit(1)

    print("Authorization: %r" % authorization)
    with open("authorization.json", "w") as fp:
        json.dump(authorization, fp, indent=4)
    return authorization


Trakt.configuration.defaults.client(
    id=os.environ.get("TRAKT_CLIENT_ID", ""),
    secret=os.environ.get("TRAKT_CLIENT_SECRET", ""),
)

# Authenticate
Trakt.configuration.defaults.oauth.from_response(_authenticate())


def get_watched_history():
    # Retrieve all history records
    for item in Trakt["sync/history"].movies(
        pagination=True, per_page=25, extended="full"
    ):
        yield item


def query_item(trakt_id: int):
    return Trakt["search"].lookup(trakt_id, "trakt", extended="full")[0]
