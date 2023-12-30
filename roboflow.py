def robofloww():
    rf = Roboflow(api_key="5nanhYltFBEGkcZ15ekd")
    project = rf.workspace().project("albiongathering")
    model = project.version(3).model

    # infer on a local image
    print(model.predict("output/dataset/screenshot_25.png", confidence=40, overlap=30).json())

    model.predict("output/dataset/screenshot_25.png", confidence=40, overlap=30).save("prediction.jpg")


def deploy_roboflow():
    rf = Roboflow(api_key="5nanhYltFBEGkcZ15ekd")
    project = rf.workspace().project("albiongathering")
    version = project.version(4)
    version.deploy("yolov5", "yolov5")