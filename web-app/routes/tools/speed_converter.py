from fastapi import APIRouter, Query, HTTPException

router = APIRouter()

@router.get("")
def convert_speed(
    knots: float = Query(None, description="Speed in knots"),
    mach: float = Query(None, description="Speed in Mach"),
    mph: float = Query(None, description="Speed in miles per hour")
):
    if sum(map(lambda x: x is not None, [knots, mach, mph])) > 1:
        raise HTTPException(status_code=400, detail="Provide only one speed unit at a time.")
    elif knots is not None:
        mach = knots / 661.49
        mph = knots * 1.15078
        return {"knots": knots, "mach": mach, "mph": mph}
    elif mach is not None:
        knots = mach * 661.49
        mph = knots * 1.15078
        return {"knots": knots, "mach": mach, "mph": mph}
    elif mph is not None:
        knots = mph / 1.15078
        mach = knots / 661.49
        return {"knots": knots, "mach": mach, "mph": mph}
    else:
        raise HTTPException(status_code=400, detail="You must provide a speed in knots, mach, or mph.")
