from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import overload

from sqlalchemy.orm import selectinload

from src.models import TestModel, QuestionModel, OptionModel
from src.schemas import TestCreateSchema, TestUpdateSchema


@overload
async def create_or_save_test(
    session: AsyncSession, test: TestCreateSchema, test_id: None
) -> TestModel: ...


@overload
async def create_or_save_test(
    session: AsyncSession, test: TestUpdateSchema, test_id: int
) -> TestModel: ...


async def create_or_save_test(
    session: AsyncSession,
    test: TestCreateSchema | TestUpdateSchema,
    test_id: int | None,
) -> TestModel:
    if test_id is None:
        questions = []
        for question in test.questions:
            options = [OptionModel(**opt.dict()) for opt in question.options]
            question_obj = QuestionModel(
                title=question.title,
                question_type=question.question_type,
                options=options,
                scores=question.scores,
            )
            questions.append(question_obj)
        new_test = TestModel(
            title=test.title,
            description=test.description,
            passing_score=test.passing_score,
            user_id=test.user_id,
            questions=questions,
        )

        session.add(new_test)
        await session.commit()
        await session.refresh(new_test)
        return new_test
    else:
        stmt = (
            select(TestModel)
            .where(TestModel.id == test_id)
            .options(selectinload(TestModel.questions))
        )
        result = await session.execute(stmt)
        existing_test = result.scalar_one_or_none()
        if existing_test is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Тест с таким id не найден",
            )
        existing_test.title = test.title
        existing_test.description = test.description
        existing_test.passing_score = test.passing_score
        existing_test.questions.clear()
        for question in test.questions:
            options = [OptionModel(**opt.dict()) for opt in question.options]
            question_obj = QuestionModel(
                title=question.title,
                question_type=question.question_type,
                options=options,
                scores=question.scores,
            )
            existing_test.questions.append(question_obj)

        await session.commit()
        await session.refresh(existing_test)
        return existing_test


async def get_test_by_id(session: AsyncSession, test_id: int) -> TestModel | None:
    stmt = (
        select(TestModel)
        .where(TestModel.id == test_id)
        .options(selectinload(TestModel.questions))
    )
    result = (await session.execute(stmt)).first()
    if not result:
        return None
    return result[0]


async def delete_test(session: AsyncSession, test_id: int) -> TestModel | None:
    test = await get_test_by_id(session, test_id)
    if not test:
        return None
    await session.delete(test)
    await session.commit()
    return test
