import tensorflow as tf

def weight_variable(shape, name):
    initial = tf.truncated_normal(shape)
    return tf.Variable(initial, name=name)

def bias_variable(shape, name):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial, name=name)

def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='VALID')

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                          strides=[1, 2, 2, 1], padding='SAME')


def tf_weight_variable(shape):
    # print(shape, "weight variable shape")
    weight = tf.Variable(tf.truncated_normal(shape=shape, stddev=0.1))
    return weight

def tf_bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def tf_conv2d(x, previous_layer):
    # print(weight)
    # return tf.nn.conv2d(x, weight, strides=[1, 2, 2, 1], padding='VALID')
    return tf.layers.conv2d(
        inputs=previous_layer,
        filters=32,
        kernel_size=[5, 5],
        padding="same",
        activation=tf.nn.relu)

input = tf.placeholder(tf.float32, shape=[None, 9, 9], name="input")
output = tf.placeholder(tf.float32, shape=[None, 3], name="output")

weights1 = weight_variable([3, 3, 1, 64], "weights1")
biases1 = bias_variable([64], "biases1")

reshaped_input = tf.reshape(input, [-1, 9, 9, 1])

conv1 = tf.nn.relu(tf.add(conv2d(reshaped_input, weights1), biases1))
# pool1 = max_pool_2x2(conv1)

weights2 = weight_variable([3, 3, 64, 128], "weights2")
biases2 = bias_variable([128], "biases2")

conv2 = tf.nn.relu(tf.add(conv2d(conv1, weights2), biases2))
# pool2 = max_pool_2x2(conv2)

weights3 = weight_variable([3, 3, 128, 256], "weights2")
biases3 = bias_variable([256], "biases2")

conv3 = tf.nn.relu(tf.add(conv2d(conv2, weights3), biases3))
# pool2 = max_pool_2x2(conv2)

fc_weights1 = weight_variable([3 * 3 * 256, 256], "fc_weights1")
fc_biases1 = bias_variable([256], "fc_biases1")

conv3_flat = tf.reshape(conv3, [-1, 3 * 3 * 256])
fc1 = tf.nn.relu(tf.add(tf.matmul(conv3_flat, fc_weights1), fc_biases1))

keep_prob = tf.placeholder(tf.float32, name="keep_prob")
fc1_drop = tf.nn.dropout(fc1, keep_prob)

fc_weights2 = weight_variable([256, 3], "fc_weights2")
fc_biases2 = bias_variable([3], "fc_biases2")

model = tf.add(tf.matmul(fc1_drop, fc_weights2), fc_biases2, name="model")

loss = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=output, logits=model))
train_model = tf.train.AdamOptimizer(1e-4).minimize(loss, name="train_model")

correct_prediction = tf.equal(tf.argmax(model, 1), tf.argmax(output, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name="accuracy")

def valuate(output):
    return abs(output[0][0])/(abs(output[0][0])+abs(output[0][1])) + \
           abs(output[0][2])/(abs(output[0][0])+abs(output[0][1])+abs(output[0][2]))