"""init

Revision ID: 1abad4e6b368
Revises: 
Create Date: 2023-10-15 14:07:13.139180

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.schema import Sequence, CreateSequence

# revision identifiers, used by Alembic.
revision = '1abad4e6b368'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute(CreateSequence(Sequence('user_id_seq')))
    op.execute(CreateSequence(Sequence('post_id_seq')))

    op.create_table("users",
                    sa.Column("user_id", sa.Integer, primary_key=True),
                    sa.Column("name", sa.String),
                    sa.Column("email", sa.String),
                    sa.Column("password", sa.String),
                    )

    op.create_table("posts",
                    sa.Column("post_id", sa.Integer, primary_key=True),
                    sa.Column("user_id", sa.Integer),
                    sa.Column("price", sa.Integer),
                    sa.Column("title", sa.String),
                    sa.Column("desc", sa.String),
                    sa.Column("img", sa.String),
                    sa.Column("sold", sa.Boolean),
                    sa.Column("created_at", sa.DateTime),
                    )

    op.create_table("otp",
                    sa.Column("email", sa.String, primary_key=True),
                    sa.Column("otp", sa.Integer),
                    sa.Column("created_at", sa.DateTime),
                    sa.Column("attempts", sa.Integer),
                    )

    op.create_table("transactions",
                    sa.Column("post_id", sa.Integer),
                    sa.Column("from_user", sa.Integer),
                    sa.Column("to_user", sa.Integer),
                    )


def downgrade():
    op.drop_table("users")
    op.drop_table("posts")
    op.drop_table("transactions")
    op.drop_table("otp")
