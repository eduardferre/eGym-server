from comment import Comment

def comment_schema(comment) -> dict(Comment):
    return { 
            "id": str(comment["_id"]),
            "creator": comment["creator"],
            "content": comment["content"]
            }

def comments_schema(comments) -> list:
    return [comment_schema(comment) for comment in comments]