from typing import Optional
from gargula.schemas.queries.base_query_schema import BaseQuerySchema

class SubjectQuerySchema(BaseQuerySchema):
    name: Optional[str] = None
    semester: Optional[str] = None
    professor: Optional[str] = None
