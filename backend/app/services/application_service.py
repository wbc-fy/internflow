from typing import List, Optional
from app.database import get_connection
from app.models.schemas import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationStatusUpdate,
)
def create_application(data: ApplicationCreate) -> ApplicationResponse:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO applications (company, position, match_score, status, notes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            data.company,
            data.position,
            data.match_score,
            data.status,
            data.notes,
        ),
    )

    conn.commit()
    application_id = cursor.lastrowid

    cursor.execute(
        "SELECT * FROM applications WHERE id = ?",
        (application_id,),
    )

    row = cursor.fetchone()
    conn.close()

    return ApplicationResponse(**dict(row))


def list_applications() -> List[ApplicationResponse]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM applications ORDER BY created_at DESC"
    )

    rows = cursor.fetchall()
    conn.close()

    return [ApplicationResponse(**dict(row)) for row in rows]

def update_application_status(
    application_id: int,
    data: ApplicationStatusUpdate
) -> Optional[ApplicationResponse]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE applications
        SET status = ?, notes = COALESCE(?, notes)
        WHERE id = ?
        """,
        (
            data.status,
            data.notes,
            application_id,
        ),
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return None

    cursor.execute(
        "SELECT * FROM applications WHERE id = ?",
        (application_id,),
    )

    row = cursor.fetchone()
    conn.close()

    return ApplicationResponse(**dict(row))