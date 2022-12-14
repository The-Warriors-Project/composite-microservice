from fastapi import Response, status
import json
import requests
import IP_calls


def delete_user_by_user_name(user_name: str):
    """
    param: user_name: id for query
    return: json with success/ Failure
    """
    deletion = True
    likes_offset = -1

    # Getting books
    user_books = get_user_books(user_name)
    stat_code = user_books.status_code
    user_books = user_books.json()
    if stat_code != 200 or not user_books or not user_books["success"]:
        payload = json.dumps({"success": False, "payload": " users MC failed fetching books"})
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content=payload)

    # Deleting user
    response = update_users(user_name,deletion)
    stat_code = response.status_code
    res_users = response.json()
    if stat_code != 200 or not res_users or not res_users["success"]:
        payload = json.dumps({"success": False, "payload": "users MC failed fetching books"})
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content=payload)


    # Decrementing books' likes count
    book_ids = user_books["payload"][0]["liked_books"]
    if book_ids != None:
        res_books = update_books(book_ids.strip(),likes_offset)

    if book_ids != None and res_books.status_code != 200:

        # Reverting user's deletion
        deletion = False
        response = update_users(user_name, deletion)
        stat_code = response.status_code
        revert_users = response.json()
        if stat_code != 200 or not revert_users or not revert_users["success"]:

            payload = json.dumps({"success": False, "payload": "books MC failed updating and users failed to revert"})
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content=payload)
        payload = json.dumps({"success": False, "payload": "books MC failed fetching books"})
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content=payload)

    # Removing reviews
    res_reviews = update_reviews(user_name).json()
    if not res_reviews or res_reviews["status"] != "Success":
        error_msg = "Reviews MC failed to update"
        failed = []

        # reverting user's deletion
        deletion = False
        revert_users = update_users(user_name, deletion).json()
        if not revert_users or not revert_users["success"]:
            failed.append("Users")

        # reverting Books decrements
        likes_offset = +1
        revert_books = update_books(book_ids, likes_offset).json()
        if res_books.status_code != 200:
            failed.append("Books")

        # updating message about fails
        if failed:
            error_msg += " and " + ' & '.join(failed) + " failed to revert."

        payload = json.dumps({"success": False, "payload": error_msg})
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content=payload)

    payload =  {
        "success": True,
        "payload": user_name + " successfully deleted"
    }

    return Response(status_code=status.HTTP_200_OK,
                    content=json.dumps(payload))

def update_users(user_name: str, deletion: bool):
    """
        param: user_name: id for query
        return: json with from users MC
    """
    users_endpoint = IP_calls.USERS + 'user_name/delete_user/' + str(user_name)
    payload = {"disable" : deletion}
    return requests.put(users_endpoint, data= json.dumps(payload))   # /user_name/delete_user/{user_name}

def get_user_books(user_name:str):
    """
        param: user_name: id for query
        return: json with success and book_ids or Failure
    """

    users_endpoint = IP_calls.USERS + "get_books/" + str(user_name)
    return requests.get(users_endpoint)

def update_books(book_ids: list, likes_offset: int):
    """
        param: user_name: book_ids to be updated.
        param: likes_offset: increment/decrement likes.
        return: json with success and book_ids or Failure
    """
    books_endpoint = IP_calls.BOOKS + "likes_count"

    payload = {
        "offset": likes_offset,
        "book_ids": book_ids
               }
    return requests.put(books_endpoint, data=json.dumps(payload))

def update_reviews(user_name: int, deletion = True):
    """
        param: user_name: id for soft deletion
        return: json with success and user_name or Failure
    """
    reviews_endpoint = IP_calls.REVIEWS + str(user_name)
    payload = {"disabled": deletion}
    return requests.put(reviews_endpoint, data=json.dumps(payload))

def get_book_shelf(user_name: str):
    """
    param: user_name: user from which to obtain book_ids
    return: json with all books info or failure
    """

    user_books = get_user_books(user_name).json()
    if not user_books or not user_books["success"]:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="users MC failed fetching books")
    

    book_ids = user_books["payload"][0]["liked_books"]

    if book_ids != None:
        return get_books_info(book_ids.strip())
    
    return {}

def get_books_info(book_ids: str):
    """
    param: book_ids: list of book ids to fetch data for
    return: json with all books info or failure
    """
    path_params = '+'.join(book_ids.split())
    books_endpoint = IP_calls.BOOKS + "book_ids/" + path_params
    return requests.get(books_endpoint)


def like_book(user_name: str, book_id: str):
    """
    param: user_name: str
    param: book_id: book id to like
    return: Response object
    """
    users_call = IP_calls.USERS + "user_name/add_book/" + user_name + "?books=" + book_id
    users_res = requests.put(users_call, data= {'books': book_id})
    # users need to change
    try:
        users_res = users_res.json()
    except Exception:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content=" users MC failed to like book")
    if not users_res['success']:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content=users_res['payload'])

    res_books = update_books(book_id, +1)
    if res_books.status_code != 200:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content=" books MC failed to like book, users did not revert")

    payload = {
        "success": True,
        "payload": " book id  #" + book_id + " is now in " + user_name + "'s liked books"
    }
    return Response(status_code=status.HTTP_200_OK,
                    content=json.dumps(payload))


def unlike_book(user_name: str, book_id: str):
    """
    param: user_name: str
    param: book_id: book id to like
    return: Response object
    """
    users_call = IP_calls.USERS + "user_name/remove_book/" + user_name + "?books=" + book_id
    users_res = requests.put(users_call, data= {'books': book_id})

    try:
        users_res = users_res.json()
    except Exception:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content=" users MC failed to unlike book")
    if not users_res['success']:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content=users_res['payload'])


    res_books = update_books(book_id, -1)
    if res_books.status_code != 200:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content=" books MC failed to like book, users did not revert")

    payload = {
        "success": True,
        "payload": " book id  #" + book_id + " is out of " + user_name + "'s liked books"
    }
    return Response(status_code=status.HTTP_200_OK,
                    content=json.dumps(payload))