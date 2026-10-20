"""Создать users, games и moves.

Revision ID: 0001
Revises: None
"""

import sqlalchemy as sa

from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("password_digest", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "games",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("player_x_id", sa.Uuid(), nullable=False),
        sa.Column("player_o_id", sa.Uuid(), nullable=True),
        sa.Column("next_player", sa.String(length=1), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(["player_o_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["player_x_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_games_status", "games", ["status"], unique=False)

    op.create_table(
        "moves",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("game_id", sa.Uuid(), nullable=False),
        sa.Column("player_id", sa.Uuid(), nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("row", sa.Integer(), nullable=False),
        sa.Column("column", sa.Integer(), nullable=False),
        sa.Column("symbol", sa.String(length=1), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.CheckConstraint("column BETWEEN 0 AND 2", name="ck_move_column"),
        sa.CheckConstraint("row BETWEEN 0 AND 2", name="ck_move_row"),
        sa.ForeignKeyConstraint(["game_id"], ["games.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["player_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("game_id", "number", name="uq_move_game_number"),
        sa.UniqueConstraint("game_id", "row", "column", name="uq_move_game_cell"),
    )


def downgrade() -> None:
    op.drop_table("moves")
    op.drop_index("ix_games_status", table_name="games")
    op.drop_table("games")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
