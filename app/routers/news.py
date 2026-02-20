from fastapi import APIRouter, Depends, HTTPException, Query, status
from datetime import datetime, timezone
from typing import List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models import (
    User,
    Category,
    Post,
    Comment,
    Tag,
    Profession,
    Like,
    Devices,
    UserSearch,
    Media,
    PostTag,
    PostMedia,
)
from app.schemas.news import (
    PostCreate,
    CommentCreate,
    PostResponse,
    CategoryCreate,
    CategoryResponse,
    CommentUpdate,
    DeviceCreate,
    DeviceResponse,
    LikeCreate,
    MediaCreate,
    MediaResponse,
    ProfessionCreate,
    ProfessionResponse,
    SearchTrackRequest,
    SearchTrackResponse,
    TagCreate,
    TagResponse,
)
from app.schemas.user import UserResponse, UserCreate, UserUpdate
from app.dependencies import current_user_jwt_dep
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

    search_stmt = select(UserSearch).where(UserSearch.term == q)
    search_res = await session.execute(search_stmt)
    search = search_res.scalars().first()
    if search:
        search.count += 1
    else:
        search = UserSearch(term=q, count=1)
        session.add(search)
    await session.commit()

    return result.scalars().all()


@router.get("/trending", response_model=List[PostResponse])
async def news_trending(
    is_active: bool | None = None,
    session: AsyncSession = Depends(get_db),
):

    stmt = (
        select(Post)
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
    current_user: current_user_jwt_dep,
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
async def author_create(
    user_in: UserCreate,
    current_user: current_user_jwt_dep,
    session: AsyncSession = Depends(get_db),
):
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
    current_user: current_user_jwt_dep,
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


@router.get("/tags", response_model=list[TagResponse])
async def tag_list(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Tag))
    return result.scalars().all()


@router.post("/tags", response_model=TagResponse)
async def tag_create(
    tag_in: TagCreate,
    current_user: current_user_jwt_dep,
    session: AsyncSession = Depends(get_db),
):
    tag = Tag(name=tag_in.name, slug=generate_slug(tag_in.name))
    session.add(tag)
    await session.commit()
    await session.refresh(tag)
    return tag


@router.put("/tags/{tag_id}", response_model=TagResponse)
async def tag_update(
    tag_id: int,
    tag_in: TagCreate,
    current_user: current_user_jwt_dep,
    session: AsyncSession = Depends(get_db),
):
    tag = await session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(404, "Tag not found")

    tag.name = tag_in.name
    tag.slug = generate_slug(tag_in.name)
    await session.commit()
    await session.refresh(tag)
    return tag


@router.get("/professions", response_model=list[ProfessionResponse])
async def profession_list(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Profession))
    return result.scalars().all()


@router.post("/professions", response_model=ProfessionResponse)
async def profession_create(
    profession_in: ProfessionCreate,
    current_user: current_user_jwt_dep,
    session: AsyncSession = Depends(get_db),
):
    profession = Profession(name=profession_in.name)
    session.add(profession)
    await session.commit()
    await session.refresh(profession)
    return profession


@router.put("/professions/{profession_id}", response_model=ProfessionResponse)
async def profession_update(
    profession_id: int,
    profession_in: ProfessionCreate,
    current_user: current_user_jwt_dep,
    session: AsyncSession = Depends(get_db),
):
    profession = await session.get(Profession, profession_id)
    if not profession:
        raise HTTPException(404, "Profession not found")

    profession.name = profession_in.name
    await session.commit()
    await session.refresh(profession)
    return profession


@router.get("/media", response_model=list[MediaResponse])
async def media_list(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Media))
    return result.scalars().all()


@router.post("/media", response_model=MediaResponse)
async def media_create(
    media_in: MediaCreate,
    current_user: current_user_jwt_dep,
    session: AsyncSession = Depends(get_db),
):
    media = Media(url=media_in.url)
    session.add(media)
    await session.commit()
    await session.refresh(media)
    return media


@router.delete("/media/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
async def media_delete(
    media_id: int,
    current_user: current_user_jwt_dep,
    session: AsyncSession = Depends(get_db),
):
    media = await session.get(Media, media_id)
    if not media:
        raise HTTPException(404, "Media not found")

    await session.delete(media)
    await session.commit()


@router.post("/{news_id}/comments", response_model=None)
async def write_comment(
    news_id: int,
    comment_in: CommentCreate,
    current_user: current_user_jwt_dep,
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


@router.post("/{news_id}/tags/{tag_id}", status_code=status.HTTP_201_CREATED)
async def attach_tag(
    news_id: int,
    tag_id: int,
    current_user: current_user_jwt_dep,
    session: AsyncSession = Depends(get_db),
):
    post = await session.get(Post, news_id)
    if not post:
        raise HTTPException(404, "News not found")

    tag = await session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(404, "Tag not found")

    stmt = select(PostTag).where(
        PostTag.post_id == news_id, PostTag.tag_id == tag_id
    )
    existing = (await session.execute(stmt)).scalars().first()
    if existing:
        return {"message": "Already attached"}

    link = PostTag(post_id=news_id, tag_id=tag_id)
    session.add(link)
    await session.commit()
    return {"message": "Tag attached"}


@router.delete("/{news_id}/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def detach_tag(
    news_id: int,
    tag_id: int,
    current_user: current_user_jwt_dep,
    session: AsyncSession = Depends(get_db),
):
    stmt = select(PostTag).where(
        PostTag.post_id == news_id, PostTag.tag_id == tag_id
    )
    link = (await session.execute(stmt)).scalars().first()
    if not link:
        raise HTTPException(404, "Tag link not found")

    await session.delete(link)
    await session.commit()


@router.post("/{news_id}/media/{media_id}", status_code=status.HTTP_201_CREATED)
async def attach_media(
    news_id: int,
    media_id: int,
    current_user: current_user_jwt_dep,
    session: AsyncSession = Depends(get_db),
):
    post = await session.get(Post, news_id)
    if not post:
        raise HTTPException(404, "News not found")

    media = await session.get(Media, media_id)
    if not media:
        raise HTTPException(404, "Media not found")

    stmt = select(PostMedia).where(
        PostMedia.post_id == news_id, PostMedia.media_id == media_id
    )
    existing = (await session.execute(stmt)).scalars().first()
    if existing:
        return {"message": "Already attached"}

    link = PostMedia(post_id=news_id, media_id=media_id)
    session.add(link)
    await session.commit()
    return {"message": "Media attached"}


@router.delete(
    "/{news_id}/media/{media_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def detach_media(
    news_id: int,
    media_id: int,
    current_user: current_user_jwt_dep,
    session: AsyncSession = Depends(get_db),
):
    stmt = select(PostMedia).where(
        PostMedia.post_id == news_id, PostMedia.media_id == media_id
    )
    link = (await session.execute(stmt)).scalars().first()
    if not link:
        raise HTTPException(404, "Media link not found")

    await session.delete(link)
    await session.commit()


@router.post("/devices", response_model=DeviceResponse)
async def register_device(
    device_in: DeviceCreate,
    current_user: current_user_jwt_dep,
    session: AsyncSession = Depends(get_db),
):
    device = Devices(
        user_agent=device_in.user_agent,
        last_active=datetime.now(timezone.utc),
    )
    session.add(device)
    await session.commit()
    await session.refresh(device)
    return device


@router.post("/{news_id}/likes", status_code=status.HTTP_201_CREATED)
async def like_news(
    news_id: int,
    like_in: LikeCreate,
    current_user: current_user_jwt_dep,
    session: AsyncSession = Depends(get_db),
):
    post = await session.get(Post, news_id)
    if not post:
        raise HTTPException(404, "Post not found")

    device = await session.get(Devices, like_in.device_id)
    if not device:
        raise HTTPException(404, "Device not found")

    like = Like(post_id=news_id, device_id=like_in.device_id)
    device.last_active = datetime.now(timezone.utc)

    session.add(like)
    await session.commit()
    return {"message": "Liked"}


@router.post("/search/track", response_model=SearchTrackResponse)
async def track_search(
    data: SearchTrackRequest,
    current_user: current_user_jwt_dep,
    session: AsyncSession = Depends(get_db),
):
    stmt = select(UserSearch).where(UserSearch.term == data.term)
    res = await session.execute(stmt)
    search = res.scalars().first()

    if search:
        search.count += 1
    else:
        search = UserSearch(term=data.term, count=1)
        session.add(search)

    await session.commit()
    return {"term": search.term, "count": search.count}


@router.put("/authors/{author_id}", response_model=UserResponse)
async def update_author(
    author_id: int,
    user_in: UserUpdate,
    current_user: current_user_jwt_dep,
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
    current_user: current_user_jwt_dep,
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
    current_user: current_user_jwt_dep,
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
    current_user: current_user_jwt_dep,
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
async def news_delete(
    news_id: int,
    current_user: current_user_jwt_dep,
    session: AsyncSession = Depends(get_db),
):
    post = await session.get(Post, news_id)
    if not post:
        raise HTTPException(404, "News not found")

    await session.delete(post)
    await session.commit()
