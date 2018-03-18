def prediction(videoObjects):
    videoCategory={}
    primaryObjects={
        "Sports":["football","basketball","volleyball"],
        "Education":["blackboard","whiteboard","computer","projector"],
        "Road":["car","bike","truck","auto"],
        "Harbour":["ship","boat"],
        "Airport":["aeroplane","helicopter"],
        "Crime":["gun","blood","knife"]
    }
    numberOfFrames=len(videoObjects)
    accuracy=numberOfFrames-int(numberOfFrames/3)
    for obj in videoObjects:
        objKey=list(obj.keys())[0]
        for pri in primaryObjects:
            if objKey in primaryObjects[pri]:
                if pri in videoCategory:
                    videoCategory[pri]+=1
                else:
                    videoCategory[pri]=1
    for obj in videoCategory:
        if videoCategory[obj]>=accuracy:
            print(obj,"Video")
            del videoCategory
            return
    print("Does not fall under any defined category...")
