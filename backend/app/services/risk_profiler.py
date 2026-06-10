def calculate_risk(data):

    score = data.Prev_Accidents * 3 + data.Prev_Citations * 2

    if score < 3:
        return "LOW"
    elif score < 6:
        return "MEDIUM"
    else:
        return "HIGH"