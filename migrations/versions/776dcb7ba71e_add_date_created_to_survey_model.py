"""Add date_created to Survey model

Revision ID: 776dcb7ba71e
Revises: 
Create Date: 2024-11-03 17:11:37.025647

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '776dcb7ba71e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('surveys',
    sa.Column('survey_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('survey_id')
    )
    op.drop_table('template')
    op.drop_table('permission')
    op.drop_table('dashboard')
    op.drop_table('api')
    op.drop_table('report')
    with op.batch_alter_table('answer', schema=None) as batch_op:
        batch_op.drop_constraint('fk_answer_response', type_='foreignkey')
        batch_op.drop_constraint('fk_answer_question', type_='foreignkey')
        batch_op.create_foreign_key(None, 'response', ['response_id'], ['response_id'])
        batch_op.create_foreign_key(None, 'question', ['question_id'], ['question_id'])

    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.drop_constraint('fk_survey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'survey', ['survey_id'], ['survey_id'])

    with op.batch_alter_table('questionoption', schema=None) as batch_op:
        batch_op.alter_column('option_text',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=255),
               type_=sa.Text(),
               existing_nullable=False)
        batch_op.drop_constraint('fk_question', type_='foreignkey')
        batch_op.create_foreign_key(None, 'question', ['question_id'], ['question_id'])

    with op.batch_alter_table('response', schema=None) as batch_op:
        batch_op.alter_column('submitted_at',
               existing_type=mysql.TIMESTAMP(),
               type_=sa.DateTime(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
        batch_op.drop_constraint('fk_respondent', type_='foreignkey')
        batch_op.drop_constraint('fk_response_survey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'survey', ['survey_id'], ['survey_id'])
        batch_op.create_foreign_key(None, 'users', ['respondent_id'], ['id'])

    with op.batch_alter_table('survey', schema=None) as batch_op:
        batch_op.alter_column('created_at',
               existing_type=mysql.TIMESTAMP(),
               type_=sa.DateTime(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
        batch_op.drop_constraint('fk_creator', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['creator_id'], ['id'])

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('finance_no',
               existing_type=mysql.INTEGER(),
               type_=sa.String(length=20),
               nullable=False)
        batch_op.alter_column('name_ar',
               existing_type=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_unicode_ci', length=255),
               type_=sa.String(length=100),
               nullable=False)
        batch_op.alter_column('name_en',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=255),
               type_=sa.String(length=100),
               nullable=False)
        batch_op.alter_column('mobile_no',
               existing_type=mysql.BIGINT(),
               type_=sa.String(length=20),
               nullable=False)
        batch_op.alter_column('email_id',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=255),
               type_=sa.String(length=100),
               nullable=False)
        batch_op.alter_column('hashed_password',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=255),
               nullable=False)
        batch_op.alter_column('section',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=255),
               type_=sa.String(length=100),
               existing_nullable=True)
        batch_op.create_unique_constraint(None, ['email_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('section',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=255),
               existing_nullable=True)
        batch_op.alter_column('hashed_password',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=255),
               nullable=True)
        batch_op.alter_column('email_id',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=255),
               nullable=True)
        batch_op.alter_column('mobile_no',
               existing_type=sa.String(length=20),
               type_=mysql.BIGINT(),
               nullable=True)
        batch_op.alter_column('name_en',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=255),
               nullable=True)
        batch_op.alter_column('name_ar',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_unicode_ci', length=255),
               nullable=True)
        batch_op.alter_column('finance_no',
               existing_type=sa.String(length=20),
               type_=mysql.INTEGER(),
               nullable=True)

    with op.batch_alter_table('survey', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('fk_creator', 'users', ['creator_id'], ['id'], ondelete='CASCADE')
        batch_op.alter_column('created_at',
               existing_type=sa.DateTime(),
               type_=mysql.TIMESTAMP(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))

    with op.batch_alter_table('response', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('fk_response_survey', 'survey', ['survey_id'], ['survey_id'], ondelete='CASCADE')
        batch_op.create_foreign_key('fk_respondent', 'users', ['respondent_id'], ['id'], ondelete='CASCADE')
        batch_op.alter_column('submitted_at',
               existing_type=sa.DateTime(),
               type_=mysql.TIMESTAMP(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))

    with op.batch_alter_table('questionoption', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('fk_question', 'question', ['question_id'], ['question_id'], ondelete='CASCADE')
        batch_op.alter_column('option_text',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=255),
               existing_nullable=False)

    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('fk_survey', 'survey', ['survey_id'], ['survey_id'], ondelete='CASCADE')

    with op.batch_alter_table('answer', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('fk_answer_question', 'question', ['question_id'], ['question_id'], ondelete='CASCADE')
        batch_op.create_foreign_key('fk_answer_response', 'response', ['response_id'], ['response_id'], ondelete='CASCADE')

    op.create_table('report',
    sa.Column('ReportID', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('SurveyID', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('GeneratedDate', mysql.DATETIME(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('Content', mysql.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('ReportID'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('api',
    sa.Column('APIID', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('Endpoint', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('Description', mysql.TEXT(), nullable=True),
    sa.Column('Method', mysql.ENUM('GET', 'POST', 'PUT', 'DELETE'), nullable=False),
    sa.PrimaryKeyConstraint('APIID'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('dashboard',
    sa.Column('DashboardID', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Widget', mysql.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['users.id'], name='fk_dashboard_users', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('DashboardID'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('permission',
    sa.Column('PermissionID', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('PermissionName', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('Description', mysql.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('PermissionID'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('template',
    sa.Column('TemplateID', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('Title', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=255), nullable=False),
    sa.Column('Description', mysql.TEXT(collation='utf8mb4_unicode_ci'), nullable=True),
    sa.Column('Content', mysql.TEXT(collation='utf8mb4_unicode_ci'), nullable=True),
    sa.Column('CreatedBy', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['CreatedBy'], ['users.id'], name='template_ibfk_1'),
    sa.PrimaryKeyConstraint('TemplateID'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('surveys')
    # ### end Alembic commands ###
