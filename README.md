# emotion-detector
Detect user emotion based on facial expression with CNN.

# Class
Predict 7 type of human emotion : angry, happy, sad, suprise, neutral, disgust, fear

# Model
Using MobileNetV3 with transfer learning

# Dataset
Using FER-2013

# Model Performance
## Train Data
Accuracy : 0.85, Recall : 0.84, Precision : 0.84, Loss : 0.48
## Test Data
Accuracy : 0.68, Recall : 0.65, Precision : 0.68, Loss : 1.12

# Limitation
The FER-2013 dataset contains high similarity between several emotion classes, making certain expressions difficult for the model to distinguish accurately.

