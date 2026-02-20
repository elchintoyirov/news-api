from fastapi import APIRouter, Depends, HTTPException, Query, status
from datetime import datetime, timezone
from typing import List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models import User, Category, Post, Comment, Tag, Like
from app.schemas.news import (
    PostCreate,
    CommentCreate,
    PostResponse,
    CategoryCreate,
    CategoryResponse,
    CommentUpdate,
)
from app.schemas.user import UserResponse, UserCreate, UserUpdate
from app.services.utils import generate_slug

router = APIRouter()


@router.get("/", response_model=List[PostResponse])
async def news_list(
    is_active: bool | None = None,
    category_id: int | None = None,
    tag_id: int | None = None,
    session: AsyncSession = Depends(get_db),
):
    stmt = select(Post)

    if is_active is not None:
        stmt = stmt.where(Post.is_active == is_active)

    if category_id is not None:
        stmt = stmt.where(Post.category_id == category_id)

    if tag_id is not None:
        stmt = stmt.where(Post.tags.any(Tag.id == tag_id))

    stmt = stmt.order_by(Post.created_at.desc())

    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{news_id}", response_model=PostResponse)
async def news_by_id(news_id: int, session: AsyncSession = Depends(get_db)):
    stmt = select(Post).where(Post.id == news_id)
    result = await session.execute(stmt)
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="News not found")
    return post


@router.get("/category/{category_name}", response_model=List[PostResponse])
async def news_by_category(category_name: str, session: AsyncSession = Depends(get_db)):
    stmt = select(Post).join(Category).where(Category.name == category_name)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/author/{author_id}", response_model=List[PostResponse])
async def news_by_author(author_id: int, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Post).where(Post.user_id == author_id))
    return result.scalars().all()


@router.get("/search", response_model=List[PostResponse])
async def search_news(
    q: str = Query(..., min_length=1), session: AsyncSession = Depends(get_db)
):
    stmt = select(Post).where(Post.title.ilike(f"%{q}%"))
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/trending", response_model=List[PostResponse])
async def news_trending(
    is_active: bool | None = None,
    session: AsyncSession = Depends(get_db),
):

    stmt = (
        select(Like)
        .outerjoin(Like, Like.post_id == Post.id)
        .group_by(Post.id)
        .order_by(func.count(Like.id).desc())
    )

    if is_active is not None:
        stmt = stmt.where(Post.is_active == is_active)

    result = await session.execute(stmt)
    return result.scalars().all()


@router.post("/", response_model=PostResponse)
async def news_create(
    post_in: PostCreate,
    session: AsyncSession = Depends(get_db),
):
    slug = generate_slug(post_in.title)

    post = Post(
        title=post_in.title,
        slug=slug,
        body=post_in.body,
        category_id=post_in.category_id,
        user_id=post_in.user_id,
        is_active=post_in.is_active,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


@router.post("/authors", response_model=UserResponse)
async def author_create(user_in: UserCreate, session: AsyncSession = Depends(get_db)):
    user = User(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        email=user_in.email,
        password_hash=user_in.password_hash,
        bio=user_in.bio,
        profession_id=user_in.profession_id,
        is_active=user_in.is_active,
        is_staff=user_in.is_staff,
        is_superuser=user_in.is_superuser,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.post("/categories", response_model=CategoryResponse)
async def category_create(
    category_in: CategoryCreate,
    session: AsyncSession = Depends(get_db),
):
    category = Category(
        name=category_in.name,
        slug=generate_slug(category_in.name),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category


@router.post("/{news_id}/comments", response_model=None)
async def write_comment(
    news_id: int,
    comment_in: CommentCreate,
    session: AsyncSession = Depends(get_db),
):
    post = await session.get(Post, news_id)
    if not post:
        raise HTTPException(404, "Post not found")

    comment = Comment(
        post_id=news_id,
        user_id=comment_in.user_id,
        text=comment_in.text,
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    post.comments_count = (post.comments_count or 0) + 1
    session.add(comment)
    await session.commit()
    return comment


@router.put("/authors/{author_id}", response_model=UserResponse)
async def update_author(
    author_id: int,
    user_in: UserUpdate,
    session: AsyncSession = Depends(get_db),
):
    user = await session.get(User, author_id)
    if not user:
        raise HTTPException(404, "Author not found")

    for field, value in user_in.dict(exclude_unset=True).items():
        setattr(user, field, value)
    user.updated_at = datetime.now(timezone.utc)

    await session.commit()
    await session.refresh(user)
    return user


@router.put("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category_in: CategoryCreate,
    session: AsyncSession = Depends(get_db),
):
    category = await session.get(Category, category_id)
    if not category:
        raise HTTPException(404, "Category not found")

    category.name = category_in.name
    category.slug = generate_slug(category_in.name)
    category.updated_at = datetime.now(timezone.utc)

    await session.commit()
    return category


@router.put("/{news_id}", response_model=PostResponse)
async def update_news(
    news_id: int,
    post_in: PostCreate,
    session: AsyncSession = Depends(get_db),
):
    post = await session.get(Post, news_id)
    if not post:
        raise HTTPException(404, "News not found")

    post.title = post_in.title
    post.slug = generate_slug(post_in.title)
    post.body = post_in.body
    post.category_id = post_in.category_id
    post.is_active = post_in.is_active
    post.updated_at = datetime.now(timezone.utc)

    await session.commit()
    await session.refresh(post)
    return post


@router.patch("/{news_id}/comments/{comment_id}", response_model=None)
async def comment_edit(
    news_id: int,
    comment_id: int,
    comment_in: CommentUpdate,
    session: AsyncSession = Depends(get_db),
):
    comment = await session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(404, "Comment not found")

    comment.text = comment_in.text
    comment.updated_at = datetime.now(timezone.utc)
    await session.commit()
    return comment


@router.delete(
    "/{news_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def news_delete(news_id: int, session: AsyncSession = Depends(get_db)):
    post = await session.get(Post, news_id)
    if not post:
        raise HTTPException(404, "News not found")

    await session.delete(post)
    await session.commit()
