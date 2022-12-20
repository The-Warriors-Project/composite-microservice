from fastapi import APIRouter, status, Response
import db_util
composite_router = APIRouter(prefix='/api/v1/composite')

@composite_router.delete(path='/manage_users/{user_name}', status_code=status.HTTP_200_OK, operation_id='delete_user_by_user_name')
def get_user_info_by_id(user_name: str):
    """
    param user_name: user id
    return: json with success and user_name or failure
    """

    res = db_util.delete_user_by_user_name(user_name=user_name)
    try:
        return res.json()
    except:
        return res

@composite_router.get(path='/{user_name}', status_code=status.HTTP_200_OK, operation_id='get_book_shelf')
def get_user_info_by_id(user_name: str):
    """
    param user_name: user id
    return: return all books' info from the user's book-shelf
    """
    res = db_util.get_book_shelf(user_name=user_name)
    try:
        return res.json()
    except:
        return res

@composite_router.put(path='/like_book/{user_name}', status_code=status.HTTP_200_OK, operation_id='like_book')
def like_book(user_name: str, book: str):
    """
    param user_name: user id
    return: json with success and user_name or failure
    """
    res = db_util.like_book(user_name=user_name, book_id= book)
    try:
        return res.json()
    except:
        return res

@composite_router.put(path='/unlike_book/{user_name}', status_code=status.HTTP_200_OK, operation_id='unlike_book')
def like_book(user_name: str, book: str):
    """
    param user_name: user id
    return: json with success and user_name or failure
    """
    res = db_util.unlike_book(user_name=user_name, book_id= book)
    try:
        return res.json()
    except:
        return res