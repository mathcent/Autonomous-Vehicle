
from controller import Camera
from vehicle import Driver
from sklearn.linear_model import HuberRegressor, Ridge
from matplotlib import pyplot as plt
import cv2
import numpy as np


# Constants.
INPUT_WIDTH = 640
INPUT_HEIGHT = 640
SCORE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.45
CONFIDENCE_THRESHOLD = 0.45

# Text parameters.
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.7
THICKNESS = 1

# Colors
BLACK  = (0,0,0)
BLUE   = (255,178,50)
YELLOW = (0,255,255)
RED = (0,0,255)




def draw_label(input_image, label, left, top):
    """Draw text onto image at location."""
    
    # Get text size.
    text_size = cv2.getTextSize(label, FONT_FACE, FONT_SCALE, THICKNESS)
    dim, baseline = text_size[0], text_size[1]
    # Use text size to create a BLACK rectangle. 
    cv2.rectangle(input_image, (left, top), (left + dim[0], top + dim[1] + baseline), BLACK, cv2.FILLED);
    # Display text inside the rectangle.
    cv2.putText(input_image, label, (left, top + dim[1]), FONT_FACE, FONT_SCALE, YELLOW, THICKNESS, cv2.LINE_AA)


def pre_process(input_image, net):
	# Create a 4D blob from a frame.
	blob = cv2.dnn.blobFromImage(input_image, 1/255,  (INPUT_WIDTH, INPUT_HEIGHT), [0,0,0], 1, crop=False)

	# Sets the input to the network.
	net.setInput(blob)

	# Runs the forward pass to get output of the output layers.
	output_layers = net.getUnconnectedOutLayersNames()
	outputs = net.forward(output_layers)
	# print(outputs[0].shape)

	return outputs


def post_process(input_image, outputs):
	# Lists to hold respective values while unwrapping.
	class_ids = []
	confidences = []
	boxes = []

	# Rows.
	rows = outputs[0].shape[1]

	image_height, image_width = input_image.shape[:2]

	# Resizing factor.
	x_factor = image_width / INPUT_WIDTH
	y_factor =  image_height / INPUT_HEIGHT

	# Iterate through 25200 detections.
	for r in range(rows):
		row = outputs[0][0][r]
		confidence = row[4]

		# Discard bad detections and continue.
		if confidence >= CONFIDENCE_THRESHOLD:
			classes_scores = row[5:]

			# Get the index of max class score.
			class_id = np.argmax(classes_scores)

			#  Continue if the class score is above threshold.
			if (classes_scores[class_id] > SCORE_THRESHOLD):
				confidences.append(confidence)
				class_ids.append(class_id)

				cx, cy, w, h = row[0], row[1], row[2], row[3]

				left = int((cx - w/2) * x_factor)
				top = int((cy - h/2) * y_factor)
				width = int(w * x_factor)
				height = int(h * y_factor)
				
				box = np.array([left, top, width, height])
				boxes.append(box)

	# Perform non maximum suppression to eliminate redundant overlapping boxes with
	# lower confidences.
	indices = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
	for i in indices:
		box = boxes[i]
		left = box[0]
		top = box[1]
		width = box[2]
		height = box[3]
		
		right = left + width
		bottom = top + height
		cropped_image = input_image[top:bottom, left:right] # Slicing to crop the image
		cv2.imshow("cropped", cropped_image)
		cv2.waitKey(1)
		
		cv2.rectangle(input_image, (left, top), (left + width, top + height), BLUE, 2*THICKNESS)
				
		label = "{}:{:.2f}".format(classes[class_ids[i]], confidences[i])
		draw_label(input_image, label, left, top)
		
		if (classes[class_ids[i]]) == "traffic light":
			print(classes[class_ids[i]], confidences[i])
			print((right-left)*(bottom-top))
			color = ('b','g','r')
			ax.clear()
			for i,col in enumerate(color):
            			histr = cv2.calcHist([cropped_image],[i],None,[256],[0,256])
            			ax.plot(histr,color = col)
            			plt.xlim([0,256])
			plt.pause(0.1)

		if (classes[class_ids[i]]) == "stop sign":
			print(classes[class_ids[i]], confidences[i])
			print((right-left)*(bottom-top))

		if (classes[class_ids[i]]) == "car":
			print(classes[class_ids[i]], confidences[i])
			print((right-left)*(bottom-top))
		if (classes[class_ids[i]]) == "person":
			print(classes[class_ids[i]], confidences[i])
			print((right-left)*(bottom-top))
	return input_image


if __name__ == '__main__':
	# Load class names.
	i = 0
	fig, ax = plt.subplots()
	driver = Driver()
	camera = Camera("camera")
	timestep = int(driver.getBasicTimeStep())
	camera.enable(timestep)
	image = camera.getImage()
	classesFile = "coco.names"
	classes = None
	#print(timestep)
	
	with open(classesFile, 'rt') as f:
		classes = f.read().rstrip('\n').split('\n')
		
	# Give the weight files to the model and load the network using them.
	modelWeights = "models/yolov5m.onnx"
	net = cv2.dnn.readNet(modelWeights)

	# Load image.
	frame = cv2.imread(image)
	driver.setCruisingSpeed(50)
	print(driver.step())
	
	while (driver.step() != -1):
                i += 1
                if i % 10 == 0:
                    cameraData = camera.getImage();
                #imageRGB = [cameraData[i] for i in range(0, camera.getHeight()*camera.getWidth()*3)]
                #imageRGB = bytes(imageRGB)
                
                #convertendo bytes para np array
                    image = np.frombuffer(cameraData, np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4))
                    print(image.shape)
                    
                    #Elimina o quarto canal da imagem
                    image = image[:, :, :3]
                    
                    #print(image.shape)
                	
                    cv2.imwrite("frame.png", image)
                    
                    # Load video.
                    #frame = cv2.VideoCapture('video_teste.mp4')
                    
                    # Process image.
                    detections = pre_process(image, net)
                    img = post_process(image.copy(), detections)
                    
                    # Put efficiency information. The function getPerfProfile returns the overall time for inference(t) and the timings for each of the layers(in layersTimes)
                    t, _ = net.getPerfProfile()
                    label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
                    print(label)
                    cv2.putText(img, label, (20, 40), FONT_FACE, FONT_SCALE, RED, THICKNESS, cv2.LINE_AA)
                    
                    cv2.imshow('Output', img)
                    cv2.waitKey(1)