def try_convert_to_float(str):
    try:
        flt = float(str)
        return flt
    except Exception as e:
        return None
