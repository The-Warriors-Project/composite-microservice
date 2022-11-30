from fastapi import APIRouter, status
import db_util
composite_router = APIRouter(prefix='/api/v1/composite')

@composite_router.delete(path='/manage_users/{user_id}', status_code=status.HTTP_200_OK, operation_id='delete_user_by_id')
def get_user_info_by_id(user_id: int):
    """
    param user_id: user id
    return: json with success and user_id or failure
    """

    return db_util.delete_user_by_id(user_id=user_id)

@composite_router.get(path='/{user_id}', status_code=status.HTTP_200_OK, operation_id='get_book_shelf')
def get_user_info_by_id(user_id: int):
    """
    param user_id: user id
    return: return all books' info from the user's book-shelf
    """

    return db_util.get_book_shelf(user_id=user_id)
