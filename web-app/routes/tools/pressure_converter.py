from fastapi import APIRouter, Query, HTTPException

router = APIRouter()

@router.get("")
def convert_pressure(
    inhg: float = Query(None, description="Pressure in inches of mercury (inhg)"),
    hpa: float = Query(None, description="Pressure in hectopascals (hpa)"),
    pa: float = Query(None, description="Pressure in Pascals (pa)"),
    atm: float = Query(None, description="Pressure in Atmospheres (atm)"),
    bar: float = Query(None, description="Pressure in Bar (bar)"),
    psi: float = Query(None, description="Pressure in PSI (psi)")
):
    if sum(map(lambda x: x is not None, [inhg, hpa, pa, atm, bar, psi])) > 1:
        raise HTTPException(status_code=400, detail="Provide only one pressure unit at a time.")
    elif inhg is not None:
        hpa = inhg * 33.8639
        pa = hpa * 100
        atm = pa / 101325
        bar = pa / 100000
        psi = pa / 6894.76
        return {"inhg": inhg, "hpa": hpa, "pa": pa, "atm": atm, "bar": bar, "psi": psi}
    elif hpa is not None:
        inhg = hpa / 33.8639
        pa = hpa * 100
        atm = pa / 101325
        bar = pa / 100000
        psi = pa / 6894.76
        return {"inhg": inhg, "hpa": hpa, "pa": pa, "atm": atm, "bar": bar, "psi": psi}
    elif pa is not None:
        hpa = pa / 100
        inhg = hpa / 33.8639
        atm = pa / 101325
        bar = pa / 100000
        psi = pa / 6894.76
        return {"inhg": inhg, "hpa": hpa, "pa": pa, "atm": atm, "bar": bar, "psi": psi}
    elif atm is not None:
        pa = atm * 101325
        hpa = pa / 100
        inhg = hpa / 33.8639
        bar = pa / 100000
        psi = pa / 6894.76
        return {"inhg": inhg, "hpa": hpa, "pa": pa, "atm": atm, "bar": bar, "psi": psi}
    elif bar is not None:
        pa = bar * 100000
        hpa = pa / 100
        inhg = hpa / 33.8639
        atm = pa / 101325
        psi = pa / 6894.76
        return {"inhg": inhg, "hpa": hpa, "pa": pa, "atm": atm, "bar": bar, "psi": psi}
    elif psi is not None:
        pa = psi * 6894.76
        hpa = pa / 100
        inhg = hpa / 33.8639
        atm = pa / 101325
        bar = pa / 100000
        return {"inhg": inhg, "hpa": hpa, "pa": pa, "atm": atm, "bar": bar, "psi": psi}
    else:
        raise HTTPException(status_code=400, detail="You must provide a pressure in inhg, hpa, pa, atm, bar, or psi.")
