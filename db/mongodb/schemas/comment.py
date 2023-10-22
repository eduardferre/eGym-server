def comment_schema(comment) -> dict:
    return {
        "id": str(comment["_id"]),
        "postId": str(comment["postId"]),
        "creator": comment["creator"],
        "content": comment["content"],
    }


def comments_schema(comments) -> list:
    return [comment_schema(comment) for comment in comments]
