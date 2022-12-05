import requests
import endpoints


def delete_user_by_user_name(user_name: str):
    """
    param: user_name: id for query
    return: json with success/ Failure
    """

    deletion = True
    likes_offset = -1

    user_books = get_user_books(user_name)
    if not user_books or not user_books["success"]:
        return {"success": False, "payload": "users MC failed fetching books"}

    res_users = update_users(user_name,deletion)
    if not res_users or not res_users["success"]:
        return {"success": False, "payload": "users MC failed deleting user"}

    book_ids = user_books["payload"]
    res_books = update_books(book_ids,likes_offset)

    if not res_books or not res_books["success"]:
        #reverting user's soft deletion
        deletion = False
        revert_users = update_users(user_name, deletion)
        if not revert_users or not revert_users["success"]:
            return {"success": False, "payload": "books MC failed updating and users failed to revert"}

        return {"success": False, "payload": "books MC failed updating"}

    res_reviews = update_reviews(user_name)
    if not res_reviews or not res_reviews["success"]:
        error_msg = "Reviews MC failed to update"
        failed = []

        # reverting user's soft deletion
        deletion = False
        revert_users = update_users(user_name, deletion)
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
            "user_name": user_name
        }
    }

def update_users(user_name: int, deletion: bool):
    """
        param: user_name: id for query
        return: json with from users MC
    """
    users_endpoint = endpoints.USERS + 'user_name/delete_user/{' + str(user_name) + '}'
    payload = {"disable" : deletion}
    return requests.put(users_endpoint, data= payload)

def get_user_books(user_name:int):
    """
        param: user_name: id for query
        return: json with success and book_ids or Failure
    """

    users_endpoint = endpoints.USERS + "books/{" + str(user_name) + '}'
    return requests.get(users_endpoint)

def update_books(book_ids: list[int], likes_offset: int):
    """
        param: user_name: book_ids to be updated.
        param: likes_offset: increment/decrement likes.
        return: json with success and book_ids or Failure
    """
    books_endpoint = endpoints.BOOKS + "likes_count"
    payload = {
        "offset": likes_offset,
        "book_ids": book_ids
               }
    return requests.put(books_endpoint, data=payload)

def update_reviews(user_name: int, deletion = True):
    """
        param: user_name: id for soft deletion
        return: json with success and user_name or Failure
    """
    reviews_endpoint = endpoints.REVIEWS + '{' + str(user_name) + '}'
    payload = {"disable": deletion}
    return requests.put(reviews_endpoint, data=payload)



def get_book_shelf(user_name: int):
    """
    param: user_name: user from which to obtain book_ids
    return: json with all books info or failure
    """

    user_books = get_user_books(user_name)
    if not user_books or not user_books["success"]:
        return {"success": False, "payload": "users MC failed fetching books"}

    book_ids = user_books["payload"]
    return get_books_info(book_ids)

def get_books_info(book_ids: list[int]):
    """
    param: book_ids: list of book ids to fetch data for
    return: json with all books info or failure
    """

    books_endpoint = endpoints.BOOKS + "book_shelf"
    payload = {"book_ids": book_ids}
    return requests.get(books_endpoint, data = payload)