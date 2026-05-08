import httpx


class StudentClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_student_name(self, user_id: str) -> str:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(f"{self.base_url}/api/v1/students/{user_id}")
            response.raise_for_status()
            return response.json()["full_name"]


class CourseClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_course_title(self, course_id: str) -> str:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(f"{self.base_url}/api/v1/courses/{course_id}")
            response.raise_for_status()
            return response.json()["title"]
