"""Initial schema

Revision ID: 97c5a4abb4b3
Revises: 
Create Date: 2026-06-04 10:44:20.747679

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97c5a4abb4b3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. users table
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('full_name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=150), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False, server_default='user'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_users_email'), 'users', ['email'], unique=True)

    # 2. sprints table
    op.create_table(
        'sprints',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('sprint_number', sa.Integer(), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('sprint_number'),
        sa.CheckConstraint('sprint_number BETWEEN 1 AND 5', name='sprint_number_range'),
        sa.CheckConstraint('end_date > start_date', name='valid_dates')
    )

    # 3. task_submissions table
    op.create_table(
        'task_submissions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('sprint_id', sa.UUID(), nullable=False),
        sa.Column('submission_date', sa.Date(), nullable=False),
        sa.Column('task1_done', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('task2_done', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('task3_done', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('points_earned', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['sprint_id'], ['sprints.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'submission_date', name='unique_submission'),
        sa.CheckConstraint(
            "points_earned = ((CASE WHEN task1_done THEN 1 ELSE 0 END) + "
            "(CASE WHEN task2_done THEN 1 ELSE 0 END) + "
            "(CASE WHEN task3_done THEN 1 ELSE 0 END)) * 2",
            name='valid_points'
        )
    )
    op.create_index(op.f('idx_submissions_user_date'), 'task_submissions', ['user_id', 'submission_date'], unique=False)
    op.create_index(op.f('idx_submissions_sprint'), 'task_submissions', ['sprint_id'], unique=False)

    # 4. live_sessions table
    op.create_table(
        'live_sessions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('sprint_id', sa.UUID(), nullable=False),
        sa.Column('session_number', sa.Integer(), nullable=False),
        sa.Column('session_date', sa.Date(), nullable=True),
        sa.Column('title', sa.String(length=200), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['sprint_id'], ['sprints.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('sprint_id', 'session_number', name='unique_session'),
        sa.CheckConstraint('session_number BETWEEN 1 AND 2', name='session_number_range')
    )

    # 5. live_attendance table
    op.create_table(
        'live_attendance',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('live_session_id', sa.UUID(), nullable=False),
        sa.Column('validated_by', sa.UUID(), nullable=False),
        sa.Column('validated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('points_awarded', sa.Integer(), nullable=False, server_default='4'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['live_session_id'], ['live_sessions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['validated_by'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'live_session_id', name='unique_attendance')
    )
    op.create_index(op.f('idx_attendance_user'), 'live_attendance', ['user_id'], unique=False)
    op.create_index(op.f('idx_attendance_session'), 'live_attendance', ['live_session_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('idx_attendance_session'), table_name='live_attendance')
    op.drop_index(op.f('idx_attendance_user'), table_name='live_attendance')
    op.drop_table('live_attendance')
    op.drop_table('live_sessions')
    op.drop_index(op.f('idx_submissions_sprint'), table_name='task_submissions')
    op.drop_index(op.f('idx_submissions_user_date'), table_name='task_submissions')
    op.drop_table('task_submissions')
    op.drop_table('sprints')
    op.drop_index(op.f('idx_users_email'), table_name='users')
    op.drop_table('users')
