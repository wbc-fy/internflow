from typing import List, Optional
from app.database import get_connection
from app.models.schemas import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationStatusUpdate,
    ApplicationStatsResponse,
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
def delete_application_by_id(application_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM applications WHERE id = ?",
        (application_id,),
    )

    conn.commit()
    deleted_count = cursor.rowcount
    conn.close()

    return deleted_count > 0
def get_application_stats() -> ApplicationStatsResponse:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS total FROM applications")
    total_row = cursor.fetchone()
    total = total_row["total"]

    cursor.execute("SELECT AVG(match_score) AS average_score FROM applications")
    avg_row = cursor.fetchone()
    average_score = avg_row["average_score"] or 0

    cursor.execute(
        """
        SELECT status, COUNT(*) AS count
        FROM applications
        GROUP BY status
        """
    )

    rows = cursor.fetchall()
    conn.close()

    status_counts = {
        row["status"]: row["count"]
        for row in rows
    }

    return ApplicationStatsResponse(
        total=total,
        average_match_score=round(float(average_score), 1),
        status_counts=status_counts,
    )