from fastapi import APIRouter, status
import db_util
composite_router = APIRouter(prefix='/api/v1/composite')

@composite_router.delete(path='/manage_users/{user_name}', status_code=status.HTTP_200_OK, operation_id='delete_user_by_user_name')
def get_user_info_by_id(user_name: str):
    """
    param user_name: user id
    return: json with success and user_name or failure
    """

    return db_util.delete_user_by_user_name(user_name=user_name)

@composite_router.get(path='/{user_name}', status_code=status.HTTP_200_OK, operation_id='get_book_shelf')
def get_user_info_by_id(user_name: str):
    """
    param user_name: user id
    return: return all books' info from the user's book-shelf
    """

    return db_util.get_book_shelf(user_name=user_name).json()
