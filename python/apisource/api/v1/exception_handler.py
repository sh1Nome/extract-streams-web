from fastapi import Request
from fastapi.responses import JSONResponse

# 一般的な例外のハンドリング
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"Internal server error: {str(exc)}"}
    )
