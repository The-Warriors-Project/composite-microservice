import requests
import endpoints


def delete_user_by_id(user_id: int):
    """
    param: user_id: id for query
    return: json with success/ Failure
    """

    deletion = True
    likes_offset = -1

    user_books = get_user_books(user_id)
    if not user_books or not user_books["success"]:
        return {"success": False, "payload": "users MC failed fetching books"}

    res_users = update_users(user_id,deletion)
    if not res_users or not res_users["success"]:
        return {"success": False, "payload": "users MC failed deleting user"}

    book_ids = user_books["payload"]
    res_books = update_books(book_ids,likes_offset)

    if not res_books or not res_books["success"]:
        #reverting user's soft deletion
        deletion = False
        revert_users = update_users(user_id, deletion)
        if not revert_users or not revert_users["success"]:
            return {"success": False, "payload": "books MC failed updating and users failed to revert"}

        return {"success": False, "payload": "books MC failed updating"}

    res_reviews = update_reviews(user_id)
    if not res_reviews or not res_reviews["success"]:
        error_msg = "Reviews MC failed to update"
        failed = []

        # reverting user's soft deletion
        deletion = False
        revert_users = update_users(user_id, deletion)
        if not revert_users or not revert_users["success"]:
            failed.append("Users")

        # reverting Books decrements
        likes_offset = +1
        revert_books = update_books(book_ids, likes_offset)
        if not revert_books or not revert_books["success"]:
            failed.append("Books")

        if failed:
            error_msg += " and " + ' & '.join(failed) + " failed to revert."

        return {"success": False, "payload": error_msg}

    return {
        "success": True,
        "payload": {
            "user_id": user_id
        }
    }

def update_users(user_id: int, deletion: bool):
    """
        param: user_id: id for query
        return: json with from users MC
    """
    users_endpoint = endpoints.USERS + str(user_id)
    payload = {"disable" : deletion}
    return requests.put(users_endpoint, data= payload)

def get_user_books(user_id:int):
    """
        param: user_id: id for query
        return: json with success and book_ids or Failure
    """

    users_endpoint = "http://52.87.245.235:5011/api/v1/users/book_shelf/"
    users_endpoint += str(user_id)
    return requests.get(users_endpoint)

def update_books(book_ids: list[int], likes_offset: int):
    """
        param: user_id: book_ids to be updated.
        param: likes_offset: increment/decrement likes.
        return: json with success and book_ids or Failure
    """
    books_endpoint = endpoints.BOOKS
    payload = {
        "offset": likes_offset,
        "book_ids": book_ids
               }
    return requests.put(books_endpoint, data=payload)

def update_reviews(user_id: int, deletion = True):
    """
        param: user_id: id for soft deletion
        return: json with success and user_id or Failure
    """
    reviews_endpoint = endpoints.REVIEWS + str(user_id)
    payload = {"disable": deletion}
    return requests.put(reviews_endpoint, data=payload)

