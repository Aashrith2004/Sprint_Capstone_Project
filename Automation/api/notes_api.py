from api.api_client import APIClient


class NotesAPI(APIClient):

    def get_notes(
        self,
        token,
    ):

        headers = {
            "x-auth-token": token
        }

        return self.get(
            "/notes",
            headers=headers,
        )

    def create_note(
        self,
        token,
        title,
        description,
        category="Home",
    ):

        headers = {
            "x-auth-token": token
        }

        payload = {
            "title": title,
            "description": description,
            "category": category,
        }

        return self.post(
            "/notes",
            payload=payload,
            headers=headers,
        )
    def delete_note(
    self,
    token,
    note_id,
):

        headers = {
            "x-auth-token": token
        }

        return self.delete(
            f"/notes/{note_id}",
            headers=headers,
        )
    def get_note_by_id(
    self,
    token,
    note_id,
):

        headers = {
            "x-auth-token": token
        }

        return self.get(
            f"/notes/{note_id}",
            headers=headers,
    )