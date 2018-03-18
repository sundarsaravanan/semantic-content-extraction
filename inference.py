def prediction(objectsCount,category,primaryObject):
    if category=="Sports":
        if objectsCount[primaryObject]==1:
            if "person" not in objectsCount:
                print("There is a",primaryObject)
                return
            if objectsCount["person"]>5:
                print("It is a",primaryObject,"match.")
                return
            if "person" in objectsCount:
                print("There is a",primaryObject,"and",objectsCount["person"],"person(s).Maybe Playing.")
                return
        elif objectsCount[primaryObject]==2:
            if "person" not in objectsCount:
                print("There are two",primaryObject)
                return
            if "person" in objectsCount:
                print("There are two",primaryObject,"and",objectsCount["person"],"person(s).Maybe practising.")
                return
        else:
            if "person" not in objectsCount:
                print("There are two or more",primaryObject,"s")
                return
            if "person" in objectsCount:
                print("There are two or more",primaryObject,"and",objectsCount["person"],"person(s).Maybe Practising.")
                return

    if category=="Transport":
        if objectsCount["airplane"]==1:
            print("An Aeroplane is Flying")
            return
        if objectsCount["airplane"]>1:
            print("There are",objectsCount["aeroplane"],"airplanes in an Airport")
            return

    if category=="Harbour":
        if "ship" and "boat" in objectsCount:
            print("It is an Harbour")
            return
        if "ship" in objectsCount:
            print("It is a Sea port")
            return
        if "boat" in objectsCount:
            print("It is a Fishing port")
            return

    if category=="Education":
        if "person" not in objectsCount:
            if "blackboard" or "greenboard" in objectsCount:
                print("It is an empty classroom")
                return
            if "computer" in objectsCount:
                print("It is an empty computer lab")
                return
            if "projector" in objectsCount:
                print("It is an empty hall")
                return
