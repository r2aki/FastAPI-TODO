from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.db import get_db
from app.models import User, Project
from app.schemas import ProjectCreate, ProjectRead

project_router = APIRouter(prefix="/projects", tags=["projects"])


@project_router.get("/", response_model=list[ProjectRead])
async def get_projects(
        limit: int = 20,
        offset: int = 0,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    query = (
        select(Project)
        .where(Project.owner_id == current_user.id)
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(query)
    projects = result.scalars().all()
    return [ProjectRead.model_validate(p) for p in projects]


@project_router.post("/", response_model=ProjectRead, status_code=201)
async def create_project(project_in: ProjectCreate, db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(get_current_user)) -> ProjectRead:
    new_project = Project(
        **project_in.model_dump(),
        owner_id=current_user.id,
    )
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return ProjectRead.model_validate(new_project)


@project_router.get("/{project_id}", response_model=ProjectRead)
async def get_project(
        project_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Project).where(and_(Project.id == project_id, Project.owner_id == current_user.id))
    )
    project = result.scalars().first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectRead.model_validate(project)


@project_router.delete("/{project_id}", status_code=204)
async def delete_project(
        project_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Project).where(
            and_(Project.id == project_id, Project.owner_id == current_user.id)
        )
    )
    project = result.scalars().first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    await db.delete(project)
    await db.commit()
