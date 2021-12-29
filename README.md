# chinese-ocr-flask-deploy
 
 Caffe Chinese-ocr Model Deployment Based on Docker and Flask!

Model coverted from [chinese-ocr](https://github.com/chineseocr/chineseocr)

Read full tutorial at my blog ==here== !
 
 ![](README_md_files%5Cimage.png?v=1&type=image)
 
 

 **1. Step  1  Build Image**
	
`docker  build -t my_app .`
 
 **2. Step  2  Run App**

`docker run -it --rm -p 5002:5002 my_app`
 
 **3. Step  3 Check Result**
 Open [this](http://localhost:5002/) link, upload local chinese text image or input an image url and see result.
