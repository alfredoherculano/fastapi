from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, oauth2, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",  # The prefix for the specified url of each path operation
    tags=["Posts"]    # The tag is used to organize the documentation file in groups
)

# @router.get("/", response_model=List[schemas.PostResponse])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""): # The "db" parameter (available in the FastAPI documentation)
                                                                           # needs to be used when we want to perform a database
                                                                           # operation with SQLAclhemy. The "limit" parameter will be
                                                                           # used whenever we want to specify a query parameter for
                                                                           # our routers/endpoints.

    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.posts_id).label("votes")).join(
        models.Vote, models.Vote.posts_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() 
        
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # The post argument is used to make sure the request comes with the schema we provided    
    
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
     
    # In the above code, we don't code with fstring here because that would make the code vunerable to SQL injection,
    # where the user could pass SQL statements into the code, which could potentially breach security.
    
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(owner_id=current_user.id, **post.dict()) # We call the dict() method (with ** to unpack it) instead of
                                                                    # mannualy calling each field (.title .content etc) so that
                                                                    # if the schema has many user provided fields we don't need
                                                                    # to hard code every one of them.
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # The refresh() method is the SQLAlchemy equivalent of RETURNING * in raw SQL
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # Checks and validates if id input can be converted to an integer
    
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))

    # A tuple with a single element is used because that's the psycopg3 syntax

    # post = cursor.fetchone()

    post = db.query(models.Post, func.count(models.Vote.posts_id).label("votes")).join(
        models.Vote, models.Vote.posts_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.id == id).first()      # Finds the 1st instance with that id
                                                                      # and returns it.

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found.")
    
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT) # The return statement is different because with a 204
                                                            # fastapi does not expect to send any data back to the client.


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()