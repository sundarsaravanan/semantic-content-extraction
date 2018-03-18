import numpy as np
import json

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
