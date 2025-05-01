from typing import overload
from uuid import UUID

from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.api.utils import CheckAnswers
from src.models import (
    TestModel,
    QuestionModel,
    OptionModel,
    ResultModel,
    TestedUserModel,
)
from src.schemas import (
    TestCreateSchema,
    TestUpdateSchema,
    TestSendSchema,
    TestedUserCreateSchema,
    QuestionSendSchema,
)


@overload
async def create_or_save_test(
    session: AsyncSession, test: TestCreateSchema, test_id: None
) -> TestModel: ...


@overload
async def create_or_save_test(
    session: AsyncSession, test: TestUpdateSchema, test_id: int
) -> TestModel: ...


async def create_test(
    session: AsyncSession,
    test: TestCreateSchema | TestUpdateSchema,
) -> TestModel:
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
        duration=test.duration,
        questions=questions,
    )

    session.add(new_test)
    await session.commit()
    await session.refresh(new_test)
    return new_test


async def save_test(
    session: AsyncSession,
    test: TestCreateSchema | TestUpdateSchema,
    test_id: int | None,
) -> TestModel:
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


async def create_or_save_test(
    session: AsyncSession,
    test: TestCreateSchema | TestUpdateSchema,
    test_id: int | None,
) -> TestModel:
    print(test_id)
    if test_id is None:
        return await create_test(session, test)
    else:
        return await save_test(session, test, test_id)


async def get_test_by_id(session: AsyncSession, test_id: int) -> TestModel | None:
    stmt = (
        select(TestModel)
        .where(TestModel.id == test_id)
        .options(selectinload(TestModel.questions).selectinload(QuestionModel.options))
    )
    result = (await session.execute(stmt)).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тест с таким id не найден",
        )
    return result[0]


async def get_user_tests(session: AsyncSession, user_id: UUID):
    stmt = select(TestModel).where(TestModel.user_id == user_id)
    tests = (await session.scalars(stmt)).all()
    return tests


async def delete_test(session: AsyncSession, test_id: int):
    test = await get_test_by_id(session, test_id)
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тест с таким id не найден",
        )
    await session.delete(test)
    await session.commit()
    return {"message": f"Test {test_id} successfully deleted", "ok": True}


async def get_right_test(
    ans: list[QuestionSendSchema],
    test: TestModel | None,
):
    answers = [
        {
            "title": a.title,
            "question_type": a.question_type,
            "options": [
                {"text": o.text, "is_correct": o.is_correct} for o in a.options
            ],
        }
        for a in ans
    ]

    right_test = []
    for question in test.questions:
        question_data = {
            "title": question.title,
            "scores": question.scores,
            "question_type": question.question_type,
            "options": [],
        }
        for option in question.options:
            question_data["options"].append(
                {"text": option.text, "is_correct": option.is_correct}
            )
        right_test.append(question_data)
    return answers, right_test


async def send_test(
    session: AsyncSession,
    test_id: int,
    sent_test: TestSendSchema,
    tested_user_data: TestedUserCreateSchema,
):
    test = await get_test_by_id(session, test_id)

    tested_user = tested_user_data.model_dump()
    tested_user_model = TestedUserModel(**tested_user)
    session.add(tested_user_model)
    stmt = select(TestedUserModel).where(
        TestedUserModel.email == tested_user_model.email
    )
    tested_user_model = (await session.execute(stmt)).first()[0]

    ans = sent_test.questions
    answers, right_test = await get_right_test(ans, test)

    score = 0
    passing_score = test.passing_score
    for right_q, user_q in zip(right_test, answers):
        if right_q["title"] != user_q["title"]:
            continue

        check_answers = CheckAnswers(
            score,
            current_question_score=right_q["scores"],
            question_type=right_q["question_type"],
            right_options=right_q["options"],
            user_options=user_q.get("options", []),
            user_answer_text=user_q.get("answer_text", "").strip(),
        )
        await check_answers.check_answer()
        score = check_answers.score

    if score >= passing_score:
        score_passed = True
    else:
        score_passed = False

    result = {
        "score": score,
        "test_id": test.id,
        "score_passed": score_passed,
        "tested_user_id": tested_user_model.id,
    }
    tested_user_model.score = score
    result_model = ResultModel(**result)
    session.add(result_model)

    await session.commit()
    return {"detail": "test successfully sent", "ok": True}


# {
#   "test": {
#     "title": "Новый тест123",
#     "description": "Описание123",
#     "passing_score": 20,
#     "duration": "17:10:16.572Z",
#     "questions": [
#       {
#         "title": "Новый вопрос 1",
#         "question_type": "single",
#         "scores": 10,
#         "options": [
#           { "text": "Вариант ответа 1", "is_correct": false },
#           { "text": "Вариант ответа 2", "is_correct": true },
#           { "text": "Вариант ответа 3", "is_correct": false },
#           { "text": "Вариант ответа 4", "is_correct": false },
#           { "text": "Вариант ответа 5", "is_correct": false }
#         ]
#       },
#       {
#         "title": "Новый вопрос 2",
#         "question_type": "single",
#         "scores": 10,
#         "options": [
#           { "text": "Вариант ответа 1", "is_correct": false },
#           { "text": "Вариант ответа 2", "is_correct": false },
#           { "text": "Вариант ответа 3", "is_correct": false },
#           { "text": "Вариант ответа 4", "is_correct": true },
#           { "text": "Вариант ответа 5", "is_correct": false }
#         ]
#       },
#       {
#         "title": "Новый вопрос 3",
#         "question_type": "multiple",
#         "scores": 10,
#         "options": [
#           { "text": "Вариант ответа 1", "is_correct": false },
#           { "text": "Вариант ответа 2", "is_correct": true },
#           { "text": "Вариант ответа 3", "is_correct": true },
#           { "text": "Вариант ответа 4", "is_correct": false }
#         ]
#       }
#     ]
#   },
#   "tested_user": {
#     "email": "user5@example.com",
#     "first_name": "string",
#     "last_name": "string"
#   }
# }

# {
#   "title": "Новый тест",
#   "description": "Описание123",
#   "user_id": "2ac5e036-f3c0-41e3-a1f9-348e62fed134",
#   "passing_score": 20,
#   "duration": "17:10:16",
#   "questions": [
#     {
#       "title": "Новый вопрос 1",
#       "question_type": "single",
#       "scores": 10,
#       "options": [
#         { "text": "Вариант ответа 1", "is_correct": false },
#         { "text": "Вариант ответа 2", "is_correct": true },
#         { "text": "Вариант ответа 3", "is_correct": false },
#         { "text": "Вариант ответа 4", "is_correct": false },
#         { "text": "Вариант ответа 5", "is_correct": false }
#       ]
#     },
#     {
#       "title": "Новый вопрос 2",
#       "question_type": "single",
#       "scores": 10,
#       "options": [
#         { "text": "Вариант ответа 1", "is_correct": false },
#         { "text": "Вариант ответа 2", "is_correct": false },
#         { "text": "Вариант ответа 3", "is_correct": false },
#         { "text": "Вариант ответа 4", "is_correct": true },
#         { "text": "Вариант ответа 5", "is_correct": false }
#       ]
#     },
#     {
#       "title": "Новый вопрос 3",
#       "question_type": "multiple",
#       "scores": 10,
#       "options": [
#         { "text": "Вариант ответа 1", "is_correct": false },
#         { "text": "Вариант ответа 2", "is_correct": true },
#         { "text": "Вариант ответа 3", "is_correct": true },
#         { "text": "Вариант ответа 4", "is_correct": false }
#       ]
#     }
#   ]
# }
