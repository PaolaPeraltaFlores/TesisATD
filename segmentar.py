from roboflow import Roboflow

rf = Roboflow(api_key="ezWoyGKUgHzvpZ7l34C3")
project = rf.workspace().project("tongue-segmentation")
model = project.version(1).model

# infer on a local image
#print(model.predict("lengua1.jpg").json())

# infer on an image hosted elsewhere
#print(model.predict("lengua1.jpg").json())

# save an image annotated with your predictions
model.predict("p.jpg").save("p1.jpg")