#Python threadin on Neural Net from tensorflow
#Will train model from MNIST dataset

import tensorflow as tf
import threading

print(tf.__version__)

# Load the Fashion MNIST dataset
#fmnist = tf.keras.datasets.fashion_mnist
fmnist = tf.keras.datasets.cifar10

# Load the training and test split of the Fashion MNIST dataset
(training_images, training_labels), (test_images, test_labels) = fmnist.load_data()

# Build the classification model
model = tf.keras.models.Sequential([tf.keras.layers.Flatten(), 
                                    tf.keras.layers.Dense(128, activation=tf.nn.relu), 
                                    tf.keras.layers.Dense(10, activation=tf.nn.softmax)])

model.compile(optimizer = tf.optimizers.Adam(),
              loss = 'sparse_categorical_crossentropy',
              metrics=['accuracy'])

#Divided the training set into a list
def Div_data():
    list_train_img = [training_images[i:i+len(training_images)//5] for i in range(0, len(training_images), len(training_images)//5)]
    list_train_labels = [training_labels[i:i+len(training_labels)//5] for i in range(0, len(training_labels), len(training_labels)//5)]
    return list_train_img,list_train_labels

# Trains the model from the new list
def Train(lock, index, list_train_img, list_train_labels):
    lock.acquire()
    model.fit(list_train_img[index], list_train_labels[index], epochs=15)
    lock.release()

#Making Threads for Training
list_train_img ,list_train_labels = Div_data()
lock = threading.Lock()

print("Starting Training of the models\n")

threads = []
for i in range(5):
    t = threading.Thread(target=Train, args=(lock, i, list_train_img, list_train_labels))
    threads.append(t)
    print("Starting thread "+str(i))
    t.start()

for t in threads:
    t.join()

# Evaluate the model on unseen data
print("Starting Evaluation of the Model\n")
lost_and_accuracy = model.evaluate(test_images, test_labels)
print("Loss: "+str(lost_and_accuracy[0])+"\n")
print("Accuracy: "+str(lost_and_accuracy[1])+"\n")
