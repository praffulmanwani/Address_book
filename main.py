from fastapi import FastAPI
from controller import Routes
from data import create_db_tables
app = FastAPI()
router = Routes(app)
router.include_routers()
create_db_tables()


@app.get("/")
def read_root():
    return {"Hello": "testing"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
