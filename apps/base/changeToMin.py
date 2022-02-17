# Changes the format of the time from a string type (e.g. 2hrs 30min) to minutes (150) 

def changeToMinute(str):
    try:
        total=0
        x=""
        if "day" in str:
            y = str.split("day")
            total+=1440*int(y[0])
            rest = y[1]
            if rest[0]=="s":
                rest = y[1][1:]
            x = rest.split("hr")
        else:
            x = str.split("hr")
        hour = 0
        min = 0
        if len(x) > 1:
            hour = x[0].strip()
        min_idx = x[-1].find("min")
        if min_idx!=-1:
            min = x[-1][:min_idx].strip()
            if min[0].isnumeric()==False:
                min = min[2:]
        total+=60*int(hour)+int(min)
        return total
    except:
        return 0
