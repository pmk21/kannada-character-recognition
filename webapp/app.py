#Import required models
import os
from PIL import Image as Im
import io, base64
from flask import Flask, render_template, request, url_for, send_from_directory
from fastai.vision import *

#Load trained model and return the model for prediction
def load_model():
    sz = 64
    bs = 64
    data = ImageDataBunch.from_csv('../', folder='data/', size=sz, bs=bs, 
                               ds_tfms=get_transforms(do_flip=False, max_zoom=1.)).normalize(imagenet_stats)
    learn = create_cnn(data, models.resnet18, metrics=[error_rate]).load('4_resnet18_0.86')
    return learn


app = Flask(__name__, static_url_path="/templates/static")


@app.route("/", methods=["POST", "GET"])
def home(): 

    if request.method == "POST":
        
        img64 = request.form['my_hidden']
        
        #Check if an image is sent
        if img64:
            
            image = Im.open(io.BytesIO(base64.b64decode(img64.split(',')[1])))
            
            #Below code adds a white background to the png image
            pixel_data = image.load()
            if image.mode == "RGBA":
            # If the image has an alpha channel, convert it to white
            # Otherwise we'll get weird pixels
                for y in range(image.size[1]): # For each row ...
                    for x in range(image.size[0]): # Iterate through each column ...
                        # Check if it's opaque
                        if pixel_data[x, y][3] < 255:
                            # Replace the pixel data with the colour white
                            pixel_data[x, y] = (255, 255, 255, 255)

            # Resize the image thumbnail
            image.thumbnail([250, 250], Im.ANTIALIAS)
            IMG_PATH = 'templates/static/images/'
            #Store the image
            folders = os.listdir(IMG_PATH)
            img_name = '' 
            if 'appimgs' not in folders:
                os.mkdir(IMG_PATH + 'appimgs')
                img_name = '1'
            else:
                temp = os.listdir(IMG_PATH + 'appimgs/')
                img_name = str(len(temp) + 1)
            
            IMG_DEST_PATH = IMG_PATH + 'appimgs/'
            image.save(IMG_DEST_PATH + img_name + '.png')
            
            #Open the image using the open_image from the fastai library
            img = open_image(IMG_DEST_PATH + img_name + '.png')
            learn = load_model()
            
            app.logger.info("Model Loaded")
            
            #Get the prediction
            prediction = learn.predict(img)[0]
            top_preds = learn.predict(img)[2].numpy()
            top_classes = list(np.flip(np.argsort(top_preds)[-14:-2]))
            top_classes = list(map(str, top_classes))
            curr_img = img_name + '.png'

            #curr_img = "1.png"
            #prediction = 1
        else:
            
            pass
        
        #Pass all the parameters to test.html
        return render_template("show_prediction.html", top_classes=top_classes, curr_img=curr_img, prediction=str(int(prediction)+1))
    
    return render_template("home.html")

@app.route('/templates/static/images/appimgs/<filename>', methods=['GET'])
def send_image(filename):
    return send_from_directory("templates/static/images/appimgs", filename)

@app.route('/templates/static/images/classes/<filename>', methods=['GET'])
def send_class_image(filename):
    return send_from_directory("templates/static/images/classes", filename)

if __name__ == '__main__':
    app.run(debug=True)