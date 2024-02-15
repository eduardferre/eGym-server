def post_schema(post) -> dict:
    return {
        "id": str(post["_id"]),
        "creator": post["creator"],
        "url": post["url"],
        "caption": post["caption"],
        "likes": post["likes"],
        "comments": post["comments"],
        "creationDate": str(post["creationDate"]),
    }


def posts_schema(posts) -> list:
    return [post_schema(post) for post in posts]
