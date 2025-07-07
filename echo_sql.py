from app.models import Base
print(str(Base.metadata.tables["users"].create()))
