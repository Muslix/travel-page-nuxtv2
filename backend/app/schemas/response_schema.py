from typing import Generic, TypeVar, Optional, Any, Dict, List
from pydantic import BaseModel, Field

T = TypeVar('T')

class GenericResponse(BaseModel, Generic[T]):
    """
    Generic response model that can be used for any API response
    """
    success: bool = True
    message: str = "Operation successful"
    data: Optional[T] = None
    errors: Optional[List[Dict[str, Any]]] = None
