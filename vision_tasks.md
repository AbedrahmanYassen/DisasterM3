## Image classification, detection and segmentation in natural disasters analysis 

 I will try to explain image classification, detection and  segmentation in the context of natural disasters, but I will use the the terminology used in the DisasterM3 paper, like the name of the task. 

 now Classification in computer vision, you basically try to classify entire image as one of the classes, for example is this a dog or not in an image.  in the context of natural disasters, we have Disaster Type Recognition, "What disaster happened?" , predicts one label from a fixed set (explosion, flood, earthquake, etc.). 

  If you have multiple objects in your image such as Trees and houses, you might want to find their location and you can try drawing  boxes or rectangles specifying the location of these classes. This is called object detection. In the context of natural disasters, we might include the Damaged Building Counting task. 

 You can go one more level up and classify each pixel as one of the classes. where you're exactly specifying each pixel belonging to each class. we have a very clear example in the context of natural disasters,Damage Segmentation, which produces pixel-level masks over damaged regions (flooded roads, destroyed buildings). 

 So just to summarize when you classify the entire image as one of the classes is called Image Classification. When you detect the objects within an image with rectangular boxes, it's called Object Detection; and when you classify each of the pixels as one of the classes it is called Image Segmentation. 