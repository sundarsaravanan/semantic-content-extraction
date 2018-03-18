def prediction(objectsCount):
    primaryObjects={
        "Sports":["football","basketball","volleyball"],
        "Education":["blackboard","whiteboard","computer","projector"],
        "Transport":["car","bike","truck","auto","ship","boat","airplane"],
        "Crime":["gun","blood","knife"]
    }
    for primary in primaryObjects:
        for objCount in objectsCount:
            if objCount in primaryObjects[primary]:
                print("Category :",primary)
                return primary,objCount
    print("Does not fall under any defined categories...")
    return False,{}
