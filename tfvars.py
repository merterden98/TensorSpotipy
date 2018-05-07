import os
os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"

import numpy as np
import tensorflow as tf


def forwardprop(input_layer, w_1, w_2):

    hidden_l = tf.nn.sigmoid(tf.matmul(input_layer, w_1))
    output_l = tf.matmul(hidden_1, w_2)
    return  output_l

def main():

    input_size = int(input("Enter Input Size\n"))
    output_size = int(input("Enter Output Size\n"))

    hidden_size = int(input("Enter Hidden Layer Size\n"))

    input_layer = tf.placeholder(tf.float64, shape=[None, input_size])
    output_layer = tf.placeholder(tf.float64, shape = [None, output_size])

    w_1 = tf.Variable(np.random.random((input_size, hidden_size)))
    w_2 = tf.Variable(np.random.random((hidden_size, output_size)))

    guess = forwardprop(input_layer, w_1, w_2)
    predict = tf.argmax(guessm axis=1)

main()
