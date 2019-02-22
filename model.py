import tensorflow as tf
from tensorflow import keras

def simple_nn(args):
    model = keras.Sequential([
        keras.layers.Flatten(
            data_format="channels_first", 
            input_shape=(len(args.channels), args.image_width, args.image_height)
        ),
        keras.layers.Dense(384, activation=tf.nn.relu),
        keras.layers.Dense(args.noc, activation="softmax")
    ])

    return model


def simple_nn_with_dropout(args):
    model = keras.Sequential([
        keras.layers.Flatten(
            data_format="channels_first", 
            input_shape=(len(args.channels), args.image_width, args.image_height)
        ),
        keras.layers.Dropout(args.dropout_visible),
        keras.layers.Dense(384, activation=tf.nn.relu),
        keras.layers.Dropout(args.dropout_hidden),
        keras.layers.Dense(args.noc, activation="softmax")
    ])

    return model
