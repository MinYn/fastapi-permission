# 🚀 FastAPI Permission Usage (FastAPI 권한 사용 방법)
```python
@router.get("/", response_model=List[SummarySchema])
async def read_all_summaries(
        user_data = Depends(Permission([
            RoleType.OWNER,
            RoleType.EDITOR,
            RoleType.VIEWER
        ])
    )) -> List[SummarySchema]:
    return await crud.get_all()
```

# Test-Driven Development with FastAPI and Docker

![Continuous Integration and Delivery](https://github.com/testdrivenio/fastapi-tdd-docker/workflows/Continuous%20Integration%20and%20Delivery/badge.svg?branch=main)

https://testdriven.io/courses/tdd-fastapi/
