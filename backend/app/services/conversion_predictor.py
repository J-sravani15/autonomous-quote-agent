def predict_conversion(premium):

    if premium <= 500:
        return 80
    elif premium <= 800:
        return 60
    else:
        return 30