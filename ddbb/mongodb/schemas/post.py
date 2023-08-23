from post import Post

def post_schema(post) -> dict(Post):
    return { 
            "id": str(post["_id"]),
            "creator": post["creator"],
            "url": post["url"],
            "caption": post["caption"],
            "likes": post["likes"],
            "comments": post["comments"]
            }

def posts_schema(posts) -> list:
    return [post_schema(post) for post in posts]