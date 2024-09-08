# SIH_Vegetable_Disease_Detection
Our project for the Smart India Hackathon 2024 on classifying and treating diseases in vegetables to help farmers.
14 different plants were used for this project. The datasets for the various plants were taken from Kaggle. Each plant has a specific set of diseases which our model can predict. Some of the plants have a binary classification of healthy or diseased while some have many different classes, healthy + set of diseases.
The datasets were downloaded to drive, imported, resized and augmented. Also, for recognizing OOD(Out Of Distribution) images, the CIFAR-10 dataset was used. Using this, if any image is uplaoded which isn't of any category of that given plant, our model classifies it as an OOD class.
Datasets were saved as a tensorflow dataset to make augmentation easier. Early Stoppage was used to make the training more efficient.
Finally, the accuracies of the various plants are listed below:

            1) Apple: 98.52%    (5 classes)
            2) Brinjal: 99.60%   (3 classes)
            3) Cauliflower: 95.28%  (5 classes)
            4) Cherry: 100%     (3 classes)
            5) Corn: 92.82%     (5 classes)
            6) Grape: 99.34%     (5 classes)
            7) Mango: 94.80%    (9 classes)
            8) Peach: 98.89%    (3 classes)
            9) PepperBell: 99.32% (3 classes)
            10) Potato: 96.49%   (4 classes)
            11) Rice: 91.37%   (7 classes)
            12) Tea: 95.39%  (5 classes)
            13) Tomato: 89.71% (11 classes)
            14) Wheat: 96.30%  (4 classes)

Along with the colab notebooks, the model weights are also uploaded as a .h5 file for each plant, which, when downloaded to local machine, can be used to predict the disease for that specific plant.
