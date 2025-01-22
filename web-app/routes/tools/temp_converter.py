from fastapi import APIRouter, Query, HTTPException

router = APIRouter()

@router.get("",
        description=(
        "Convert temperatures between Celsius and Fahrenheit."
        "Provide the temperature in either Celsius (`c`) or Fahrenheit (`f`) as a query parameter. "
        "If both parameters are provided, the API will return an error."
        ),
    )
def convert_temperature(
    c: float = Query(None, description="Temperature in Celsius"),
    f: float = Query(None, description="Temperature in Fahrenheit")
):
    if c is not None and f is not None:
        raise HTTPException(status_code=400, detail="Provide either 'c' or 'f', not both.")
    elif c is not None:
        f = (c * 9 / 5) + 32
        return {"Celsius": c, "Fahrenheit": f}
    elif f is not None:
        c = (f - 32) * 5 / 9
        return {"Fahrenheit ": f, "Celsius": c}
    else:
        raise HTTPException(status_code=400, detail="You must provide either 'c' or 'f'.")
