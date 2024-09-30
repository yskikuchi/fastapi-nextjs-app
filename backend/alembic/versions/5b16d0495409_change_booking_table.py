"""change booking table

Revision ID: 5b16d0495409
Revises: f07c80efa713
Create Date: 2024-09-30 06:26:18.535067

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5b16d0495409'
down_revision: Union[str, None] = 'f07c80efa713'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookings', sa.Column('status', sa.String(length=1024), server_default='unconfirmed', nullable=False))
    op.alter_column('bookings', 'reference_number',
               existing_type=sa.VARCHAR(length=1024),
               nullable=False)
    op.alter_column('bookings', 'start_time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('bookings', 'end_time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('bookings', 'amount',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('bookings', 'user_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('bookings', 'car_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.create_unique_constraint(None, 'bookings', ['reference_number'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'bookings', type_='unique')
    op.alter_column('bookings', 'car_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('bookings', 'user_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('bookings', 'amount',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('bookings', 'end_time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('bookings', 'start_time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('bookings', 'reference_number',
               existing_type=sa.VARCHAR(length=1024),
               nullable=True)
    op.drop_column('bookings', 'status')
    # ### end Alembic commands ###
