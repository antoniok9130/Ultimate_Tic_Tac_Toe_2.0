
from keras.layers import Dense, Conv2D, Dropout, Flatten, BatchNormalization, Activation
from keras.models import Sequential


def create_model():
    policy = Sequential()
    value = Sequential()

    layers = [
        Conv2D(64, (3, 3), padding='same', input_shape=(9, 9, 16)),
        BatchNormalization(),
        Activation("relu"),
        Conv2D(64, (3, 3)),
        BatchNormalization(),
        Activation("relu"),
        Dropout(0.25),
        Conv2D(64, (3, 3), padding='same'),
        BatchNormalization(),
        Activation("relu"),
        Conv2D(64, (3, 3)),
        BatchNormalization(),
        Activation("relu"),
        Dropout(0.25),
    ]
    for layer in layers:
        policy.add(layer)
        value.add(layer)

    policy.add(Conv2D(2, (1, 1)))
    policy.add(BatchNormalization())
    policy.add(Activation("relu"))
    policy.add(Flatten())
    policy.add(Dense(81))

    value.add(Conv2D(1, (1, 1)))
    value.add(BatchNormalization())
    value.add(Activation("relu"))
    value.add(Flatten())
    value.add(Dense(128))
    value.add(Activation("relu"))
    value.add(Dropout(0.5))
    value.add(Dense(1))
    value.add(Activation("tanh"))

    return policy, value

if __name__ == "__main__":
    policy, value = create_model()

    print(policy.summary())
    print(value.summary())