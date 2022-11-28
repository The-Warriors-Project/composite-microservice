import requests


def delete_user_by_id(user_id: int):
    """
    param: user_id: id for query
    return: json with success/ Failure
    """
    users_endpoint = "http://52.87.245.235:5011/api/v1/users/delete/user_id/"
    reviews_endpoint = "http://44.211.188.169:5011/api/v1/reviews/delete/user_id/"
    users_endpoint += str(user_id)
    reviews_endpoint += str(user_id)

    res_users = requests.delete(users_endpoint)
    if not res_users:
        return {"success": False, "payload": "No response from users MC"}

    # TODO: add functionality for books MC (if we want).

    res_reviews = requests.delete(reviews_endpoint)
    if not res_users:
        return {"success": False, "payload": "No response from reviews MC"}

    return {
        "success": True,
        "payload": {
            "users_payload": res_users,
            "reviews_payload": res_reviews
        }
    }

