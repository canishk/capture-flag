from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.categories.domain.entities import Category
from app.modules.categories.domain.enums import CategoryStatus
from app.modules.categories.infrastructure.models import CategoryModel


class CategoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        name: str,
        description: str | None,
        icon: str,
        display_order: int,
        status: CategoryStatus,
    ) -> Category:
        model = CategoryModel(
            name=name,
            description=description,
            icon=icon,
            display_order=display_order,
            status=status,
        )
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, category_id: UUID) -> Category | None:
        result = await self._session.execute(
            select(CategoryModel).where(CategoryModel.id == category_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_name(self, name: str) -> Category | None:
        result = await self._session.execute(
            select(CategoryModel).where(CategoryModel.name == name)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def list_categories(
        self,
        *,
        page: int,
        page_size: int,
        status: CategoryStatus | None = None,
        search: str | None = None,
    ) -> tuple[list[Category], int]:
        stmt = select(CategoryModel)
        count_stmt = select(func.count()).select_from(CategoryModel)
        if status is not None:
            stmt = stmt.where(CategoryModel.status == status)
            count_stmt = count_stmt.where(CategoryModel.status == status)
        if search:
            pattern = f"%{search}%"
            stmt = stmt.where(CategoryModel.name.ilike(pattern))
            count_stmt = count_stmt.where(CategoryModel.name.ilike(pattern))
        total = int(await self._session.scalar(count_stmt) or 0)
        stmt = (
            stmt.order_by(CategoryModel.display_order.asc(), CategoryModel.name.asc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars().all()], total

    async def update(
        self,
        category_id: UUID,
        *,
        name: str | None = None,
        description: str | None = None,
        icon: str | None = None,
        status: CategoryStatus | None = None,
    ) -> Category | None:
        model = await self._get_model(category_id)
        if model is None:
            return None
        if name is not None:
            model.name = name
        if description is not None:
            model.description = description
        if icon is not None:
            model.icon = icon
        if status is not None:
            model.status = status
        await self._session.flush()
        return self._to_entity(model)

    async def update_display_order(self, category_id: UUID, display_order: int) -> Category | None:
        model = await self._get_model(category_id)
        if model is None:
            return None
        model.display_order = display_order
        await self._session.flush()
        return self._to_entity(model)

    async def get_max_display_order(self) -> int:
        result = await self._session.scalar(select(func.max(CategoryModel.display_order)))
        return int(result or 0)

    async def _get_model(self, category_id: UUID) -> CategoryModel | None:
        result = await self._session.execute(
            select(CategoryModel).where(CategoryModel.id == category_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    def _to_entity(model: CategoryModel) -> Category:
        return Category(
            id=model.id,
            name=model.name,
            description=model.description,
            icon=model.icon,
            display_order=model.display_order,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
