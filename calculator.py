import math
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field


app = FastAPI(title="Calculator Web Service", version="1.0.0")


class CalculationRequest(BaseModel):
    operation: Literal["add", "subtract", "multiply", "divide"]
    left: float = Field(allow_inf_nan=False)
    right: float = Field(allow_inf_nan=False)


@app.get("/", include_in_schema=False)
def calculator_page() -> FileResponse:
    return FileResponse(Path(__file__).with_name("index.html"))


@app.post("/calculate")
def calculate(request: CalculationRequest) -> dict[str, str | float]:
    if request.operation == "add":
        result = request.left + request.right
    elif request.operation == "subtract":
        result = request.left - request.right
    elif request.operation == "multiply":
        result = request.left * request.right
    else:
        if request.right == 0:
            raise HTTPException(status_code=400, detail="Division by zero is not allowed.")
        result = request.left / request.right

    if not math.isfinite(result):
        raise HTTPException(status_code=400, detail="The result is not a finite number.")

    return {
        "operation": request.operation,
        "left": request.left,
        "right": request.right,
        "result": result,
    }
