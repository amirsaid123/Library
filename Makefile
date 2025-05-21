# 1. Create a new revision (migration)
revise:
	alembic revision --autogenerate -m "Revised"

# 2. Apply latest migrations
head:
	alembic upgrade head

# 3. Downgrade to previous revision
down:
	alembic downgrade -1

# 4. Downgrade to base (initial state)
base:
	alembic downgrade base

# 5. View current revision in the database
current:
	alembic current

# 6. Show all migration history
history:
	alembic history

# 7. Show full details of a specific revision
show:
	alembic show <revision_id>


