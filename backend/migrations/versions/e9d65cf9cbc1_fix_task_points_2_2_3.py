"""fix_task_points_2_2_3

Revision ID: e9d65cf9cbc1
Revises: ac40c91f1b1a
Create Date: 2026-06-17 02:39:39.624672

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9d65cf9cbc1'
down_revision: Union[str, Sequence[str], None] = 'ac40c91f1b1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Drop old constraint
    op.drop_constraint('valid_points', 'task_submissions', type_='check')

    # 2. Fix existing data FIRST (before adding new constraint)
    op.execute(
        "UPDATE task_submissions SET points_earned = "
        "(CASE WHEN task1_done THEN 2 ELSE 0 END) + "
        "(CASE WHEN task2_done THEN 2 ELSE 0 END) + "
        "(CASE WHEN task3_done THEN 3 ELSE 0 END)"
    )

    # 3. Create new constraint
    op.create_check_constraint(
        'valid_points',
        'task_submissions',
        "(CASE WHEN task1_done THEN 2 ELSE 0 END) + "
        "(CASE WHEN task2_done THEN 2 ELSE 0 END) + "
        "(CASE WHEN task3_done THEN 3 ELSE 0 END) = points_earned"
    )


def downgrade() -> None:
    op.drop_constraint('valid_points', 'task_submissions', type_='check')
    op.execute(
        "UPDATE task_submissions SET points_earned = "
        "((CASE WHEN task1_done THEN 1 ELSE 0 END) + "
        "(CASE WHEN task2_done THEN 1 ELSE 0 END) + "
        "(CASE WHEN task3_done THEN 1 ELSE 0 END)) * 2"
    )
    op.create_check_constraint(
        'valid_points',
        'task_submissions',
        "points_earned = ((CASE WHEN task1_done THEN 1 ELSE 0 END) + "
        "(CASE WHEN task2_done THEN 1 ELSE 0 END) + "
        "(CASE WHEN task3_done THEN 1 ELSE 0 END)) * 2"
    )
