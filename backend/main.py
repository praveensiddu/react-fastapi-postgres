from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.fastapi_postgres import models, schemas
from backend.fastapi_postgres.database import engine, get_db
import uvicorn
import os
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# ----------------------
# Serving React Static files from /static folder
# ----------------------
static_build_outdir = os.path.join(os.path.dirname(__file__), "build_outdir")
static_dir = f'{static_build_outdir}{os.sep}static'
app.mount("/static", StaticFiles(directory=static_dir), name="static")


# This function loads the index.html
@app.get("/")
async def serve_spa():
    index_file = os.path.join(static_build_outdir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": "Frontend not built. Run npm run build in frontend/"}


@app.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    try:
        db.commit()
    except Exception as e:
        print(e)
        # TODO return http error code for incorrect data
        raise HTTPException(
            status_code=400,
            detail=f"Bad request: {str(e)}"  # Optionally include the error message
        )
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/", response_model=list[schemas.UserOut])
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.put("/users/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in user.dict().items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.patch("/users/{user_id}", response_model=schemas.UserOut)
def patch_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in user.dict(exclude_unset=True).items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}



# code starts executing from the main function
if __name__ == "__main__":
    # uvicorn provides the webserver functionality like apache server
    # reload=True tells unicorm to reload the python script if it changes.
    if os.getenv("DATABASE_URL") == None:
        print("Environment variable DATABASE_URL must be set")
        print("example postgresql://fastapi_user:fastapi_pass@localhost/fastapi_db")
        exit(-1)

    uvicorn.run("main:app", port=8000, reload=True)