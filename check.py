def detected_text_to_data(response_text=""):
    match = re.search( r'([0O]|\d+)km/h\s*[,.\s]*([NS]\d+\.\d+)[,.\s]*([EW]\d+\.\d+)' , response_text)
    if match:
        speed = match.group(1)
        if speed == 'O':
            speed = 0
        else:
            speed = int(speed)
        latitude = float(match.group(2).replace("N", ""))
        longitude = float(match.group(3).replace("E", ""))
        print(speed, latitude, longitude)


        return speed, latitude, longitude
        
    else:
        return None
