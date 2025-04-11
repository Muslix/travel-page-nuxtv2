"""Initial migration

Revision ID: b3601c5e9712
Revises: 
Create Date: 2025-04-11 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3601c5e9712'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Erstelle die Tabelle für Tags
    op.create_table('tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('slug')
    )
    op.create_index(op.f('ix_tags_id'), 'tags', ['id'], unique=False)
    op.create_index(op.f('ix_tags_name'), 'tags', ['name'], unique=True)
    op.create_index(op.f('ix_tags_slug'), 'tags', ['slug'], unique=True)
    
    # Erstelle die Tabelle für Profile
    op.create_table('profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('avatar', sa.String(length=255), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('social_links', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_profiles_id'), 'profiles', ['id'], unique=False)
    
    # Erstelle die Tabelle für Ausrüstung
    op.create_table('equipment',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('weight_g', sa.Integer(), nullable=True),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('purchase_link', sa.String(length=255), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_equipment_id'), 'equipment', ['id'], unique=False)
    
    # Erstelle die Tabelle für Abenteuer
    op.create_table('adventures',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('duration_days', sa.Integer(), nullable=True),
        sa.Column('distance_km', sa.Float(), nullable=True),
        sa.Column('elevation_m', sa.Integer(), nullable=True),
        sa.Column('difficulty', sa.String(length=50), nullable=True),
        sa.Column('surface', sa.String(length=50), nullable=True),
        sa.Column('gpx_file_path', sa.String(length=255), nullable=True),
        sa.Column('start_coordinates', sa.String(length=100), nullable=True),
        sa.Column('equipment', sa.Text(), nullable=True),
        sa.Column('tips', sa.Text(), nullable=True),
        sa.Column('cover_image', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.Date(), nullable=True),
        sa.Column('updated_at', sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )
    op.create_index(op.f('ix_adventures_id'), 'adventures', ['id'], unique=False)
    op.create_index(op.f('ix_adventures_slug'), 'adventures', ['slug'], unique=True)
    
    # Erstelle die Tabelle für Bilder
    op.create_table('images',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('file_path', sa.String(length=255), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_cover', sa.Boolean(), nullable=True),
        sa.Column('adventure_id', sa.Integer(), nullable=True),
        sa.Column('equipment_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['adventure_id'], ['adventures.id'], ),
        sa.ForeignKeyConstraint(['equipment_id'], ['equipment.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_images_id'), 'images', ['id'], unique=False)
    
    # Erstelle die Verknüpfungstabelle für Abenteuer und Tags
    op.create_table('adventure_tag',
        sa.Column('adventure_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['adventure_id'], ['adventures.id'], ),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
        sa.PrimaryKeyConstraint('adventure_id', 'tag_id')
    )


def downgrade():
    # Drop the tables in reverse order
    op.drop_table('adventure_tag')
    op.drop_index(op.f('ix_images_id'), table_name='images')
    op.drop_table('images')
    op.drop_index(op.f('ix_adventures_slug'), table_name='adventures')
    op.drop_index(op.f('ix_adventures_id'), table_name='adventures')
    op.drop_table('adventures')
    op.drop_index(op.f('ix_equipment_id'), table_name='equipment')
    op.drop_table('equipment')
    op.drop_index(op.f('ix_profiles_id'), table_name='profiles')
    op.drop_table('profiles')
    op.drop_index(op.f('ix_tags_slug'), table_name='tags')
    op.drop_index(op.f('ix_tags_name'), table_name='tags')
    op.drop_index(op.f('ix_tags_id'), table_name='tags')
    op.drop_table('tags')
