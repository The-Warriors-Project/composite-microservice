from fastapi import APIRouter, status
import db_util
composite_router = APIRouter(prefix='/api/v1/composite')

@composite_router.delete(path='/manage_users/{user_id}', status_code=status.HTTP_200_OK, operation_id='delete_user_by_id')
def get_user_info_by_id(user_id: int):
    """
    param user_id: user id
    return: return all user info by id
    """

    return db_util.delete_user_by_id(user_id=user_id)

