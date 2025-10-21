"""Initial schema

Revision ID: 20251021_initial_schema
Revises: 
Create Date: 2025-10-21 16:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20251021_initial_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Creating enum types
    riskcategory = postgresql.ENUM('cybersecurity', 'network', 'compliance', 'infrastructure', 'human', name='riskcategory')
    probability = postgresql.ENUM('low', 'medium', 'high', name='probability')
    impact = postgresql.ENUM('minor', 'significant', 'critical', name='impact')
    
    riskcategory.create(op.get_bind())
    probability.create(op.get_bind())
    impact.create(op.get_bind())

    # Creating risks table
    op.create_table('risks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('category', riskcategory, nullable=False),
        sa.Column('probability', probability, nullable=False),
        sa.Column('impact', impact, nullable=False),
        sa.Column('score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('potential_loss_usd', sa.Float(), nullable=True),
        sa.Column('mitigation_measures', sa.Text(), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('delegate_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('history', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['owner_id'], ['owners.id'], ),
        sa.ForeignKeyConstraint(['delegate_id'], ['owners.id'], ),
    )
    op.create_index(op.f('ix_risks_category'), 'risks', ['category'], unique=False)
    op.create_index(op.f('ix_risks_owner_id'), 'risks', ['owner_id'], unique=False)

    # Creating owners table
    op.create_table('owners',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_owners_email'), 'owners', ['email'], unique=True)

    # Creating audit_logs table
    op.create_table('audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('risk_id', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('details', sa.JSON(), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['risk_id'], ['risks.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['owners.id'], ),
    )
    op.create_index(op.f('ix_audit_logs_risk_id'), 'audit_logs', ['risk_id'], unique=False)
    op.create_index(op.f('ix_audit_logs_user_id'), 'audit_logs', ['user_id'], unique=False)

    # Creating business_impact_factors table
    op.create_table('business_impact_factors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('category', riskcategory, nullable=False),
        sa.Column('cost_per_hour_usd', sa.Float(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('category')
    )

def downgrade():
    op.drop_table('business_impact_factors')
    op.drop_table('audit_logs')
    op.drop_table('owners')
    op.drop_table('risks')
    op.execute('DROP TYPE riskcategory')
    op.execute('DROP TYPE probability')
    op.execute('DROP TYPE impact')