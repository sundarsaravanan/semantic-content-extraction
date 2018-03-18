import os
import sys
import json
import time
import glob
import datetime
from threading import Thread
import numpy as np
from PIL import Image
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def inferencePrediction(objectsCount,category,primaryObject):
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

def categoryPrediction(objectsCount):
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

def fetchCategories(path):
  with open(path, 'r') as inputFile:
    labels=[]
    categoryString = inputFile.read()
    cat=categoryString.replace(" ","")
    cat=cat.replace("item","{\"item\":")
    cat=cat.replace("}","}} ")
    cat=cat.replace("id","\"id\"")
    cat=cat.replace("name",",\"name\"")
    cat=cat.replace("\n","")
    categoriesString=cat.split(" ")
    categories=[]
    for cat in categoriesString:
        if not cat=="":
            catJSON=json.loads(cat)
            categories.append({'id':catJSON["item"]["id"],'name':catJSON["item"]["name"]})
  return categories

def categoriesList(labelDictionary):
    categories = fetchCategories(labelDictionary)
    categoryIndex ={}
    acceptedIndex=[]
    for category in categories:
      categoryIndex[category['id']] = category
      acceptedIndex.append(category['id'])
    return categoryIndex,acceptedIndex

def imageToNumpyArray(image):
  width,height = image.size
  npArray=np.array(image.getdata())
  tranformShape=npArray.reshape(height,width,3)
  return tranformShape.astype(np.uint8)

def threadProcess():
    thread1=Thread(target=run,args=("frozen_ball_inference_graph.pb","ball-detection.pbtxt"))
    thread2=Thread(target=run,args=("frozen_person_inference_graph.pb","person-detection.pbtxt"))
    thread2.start()
    thread1.start()
    thread1.join()
    thread2.join()
    draw_box(boxValues)
    del boxValues[:]

def run(inferenceGraph,labelDictionary):
    categoryIndex,acceptedIndex=categoriesList('label_map/'+labelDictionary)
    classes,scores,boxes=detect('inference_graph/'+inferenceGraph,categoryIndex)
    output(classes,scores,boxes,categoryIndex,acceptedIndex)

def detect(inferenceGraph,categoryIndex):
    global image_np,testingImage
    detectionGraph = tf.Graph()
    with detectionGraph.as_default():
      od_graph_def = tf.GraphDef()
      with open(inferenceGraph, 'rb') as inferenceFile:
        serialized_graph = inferenceFile.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
      with tf.Session(graph=detectionGraph) as sess:
        image_tensor = detectionGraph.get_tensor_by_name('image_tensor:0')
        detection_boxes = detectionGraph.get_tensor_by_name('detection_boxes:0')
        detection_scores = detectionGraph.get_tensor_by_name('detection_scores:0')
        detection_classes = detectionGraph.get_tensor_by_name('detection_classes:0')
        num_detections = detectionGraph.get_tensor_by_name('num_detections:0')
        image = Image.open(testingImage)
        image_np = imageToNumpyArray(image)
        image_np_expanded = np.expand_dims(image_np, axis=0)
        (boxes, scores, classes, num) = sess.run(
              [detection_boxes, detection_scores, detection_classes, num_detections],
              feed_dict={image_tensor: image_np_expanded})
        return classes,scores,boxes

def output(classes,scores,boxes,categoryIndex,acceptedIndex):
    global boxValues,objects
    for index, value in enumerate(classes[0]):
        if value in acceptedIndex:
            if scores[0, index] > 0.6:
              objects.append({categoryIndex[value]['name']:scores[0][index]})
              boxValues.append(boxes[0][index])

def draw_box(boxValues):
    global image_np
    figure = plt.figure()
    axes = plt.Axes(figure, [0., 0., 1., 1.])
    plt.axis('off')
    figure.add_axes(axes)
    for box in boxValues:
        x1=box[1]*image_np.shape[1]
        x2=box[3]*image_np.shape[1]
        y1=box[0]*image_np.shape[0]
        y2=box[2]*image_np.shape[0]
        axes.add_patch(patches.Rectangle((x1,y1),x2-x1,y2-y1,linewidth=3,edgecolor='b',facecolor='none'))
    axes.imshow(image_np)
    extent = axes.get_window_extent().transformed(figure.dpi_scale_trans.inverted())
    outputPath=os.getcwd()+"/output/result"+str(int(time.time()))+".jpg"
    plt.savefig(outputPath,bbox_inches=extent)
    plt.close(figure)

def objectsCount(mode):
    countObjects={}
    global videoObjects
    for obj in objects:
        objKey=list(obj.keys())[0]
        if objKey in countObjects:
            countObjects[objKey]+=1
        else:
            countObjects[objKey]=1
    del objects[:]
    if mode=="1" or mode=="2":
        category,primaryObject=categoryPrediction(countObjects)
        if category:
            inferencePrediction(countObjects,category,primaryObject)
    if mode=="3":
        videoObjects.append(countObjects)
    del countObjects

def videoPrediction():
    global videoObjects
    videoCategory={}
    primaryObjects={
        "Sports":["football","basketball","volleyball"],
        "Education":["blackboard","whiteboard","computer","projector"],
        "Transport":["car","bike","truck","auto","ship","boat","airplane"],
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

# main
boxValues=[]
objects=[]
videoObjects=[]
image_np=0

print("<----------Semantic Content Extraction---------->")
while(1):
    confirm=""
    option=""
    imageName=""
    count=0
    print("Options:\n1.Extraction in Single Image\n2.Extraction in Multiple Images\n3.Scene Prediction\n4.Quit")
    option=input("Enter Option:")
    if option=="1":
        print("Place the image in \"./input/single\" folder")
        imageName=input("Name of image:")
        testingImage="input/single/"+imageName
        threadProcess()
        objectsCount(option)
        print("Completed detecting the objects in the image, categorised and predicted an inference.")

    elif option=="2":
        print("Place the images in \"./input/multiple\" folder")
        confirm=input("Enter 1 to continue :")
        if(confirm=="1"):
            for testingImage in glob.iglob("input/multiple/*"):
                threadProcess()
                objectsCount(option)
                count=count+1
            print("Completed detecting the objects in",count,"images... Categorised and predicted an inference.")
        else:
            print("Retry...")

    elif option=="3":
        print("Place the frames in \"./input/scene\" folder")
        confirm=input("Enter 1 to continue :")
        if(confirm=="1"):
            for testingImage in glob.iglob("input/scene/*"):
                threadProcess()
                objectsCount(option)
            videoPrediction()
            del videoObjects
        else:
            print("Retry...")

    elif option=="4":
        print("Quitting...")
        break

    else:
        print("Invalid Option...Retry...")
