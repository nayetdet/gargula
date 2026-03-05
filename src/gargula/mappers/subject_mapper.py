from gargula.models.subject import Subject
from gargula.schemas.requests.subject_request_schema import SubjectRequestSchema
from gargula.schemas.responses.subject_response_schema import SubjectResponseSchema

class SubjectMapper:
    @staticmethod
    def to_model(request: SubjectRequestSchema) -> Subject:
        return Subject(
            name=request.name,
            semester=request.semester,
            professor=request.professor
        )

    @staticmethod
    def to_response_schema(subject: Subject) -> SubjectResponseSchema:
        return SubjectResponseSchema(
            id=subject.id,
            name=subject.name,
            semester=subject.semester,
            professor=subject.professor
        )
