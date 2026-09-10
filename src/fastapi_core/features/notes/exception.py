class NoteNotFound(Exception):
    def __init__(self, note_id: int) -> None:
        self.note_id = note_id
        super().__init__(f"No note with {note_id}")
