from app.models import Base
print(Base.metadata.tables["users"].columns.keys())
