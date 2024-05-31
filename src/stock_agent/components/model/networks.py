import tensorflow as tf
from tensorflow.keras import Model, Input # type: ignore
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv1D, Concatenate, Lambda # type: ignore

def wrapped_tf_fn(x):
    # Perform the transpose operation
    return tf.transpose(x, perm=[0, 2, 1])

def create_actor_model_3(input_shape, dropout_rate=0.2):
    state_input = Input(shape=input_shape)
    x = Dense(256)(state_input)
    x = Dense(128, activation='relu')(x)
    x = Dense(128, activation='relu')(x)
    x = Dense(128, activation='relu')(x)
    x = Dense(128, activation='relu')(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(dropout_rate)(x)
    x = Dense(64, activation='relu')(x)
    x = Dense(64, activation='relu')(x)
    x = Dropout(dropout_rate)(x)
    x = Dense(20, activation='relu')(x)
    x = Dense(20, activation='relu')(x)
    # out = tf.transpose(x,perm=[0,2,1])
    out = Lambda(wrapped_tf_fn)(x)
    out1 = Dense(3, activation='softmax')(out)
    # out2 = tf.transpose(out1,perm=[0,2,1])
    out2 = Lambda(wrapped_tf_fn)(out1)
    out2 = Dense(20,activation="softmax")(out2[:,:2])
    argmax = tf.math.argmax(out1,axis=-1)
    argmax = tf.cast(argmax,dtype=tf.float32)
    outputs = Concatenate(axis=1)([tf.expand_dims(argmax, -2),out2])
    model = Model(inputs=state_input, outputs=outputs)
    return model


def create_actor_model_1(input_shape, fc1_dims=128, fc2_dims=64, dropout_rate=0.2):
    state_input = Input(shape=input_shape)
    inp = tf.transpose(state_input,perm=[0,2,1])
    x = Conv1D(64,3,padding = "same")(inp[:,26:,:])
    x = Dense(128, activation='relu')(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(dropout_rate)(x)
    x = Conv1D(32,3,padding="same")(x)
    x = Dense(64, activation='relu')(x)
    x = Dense(64, activation='relu')(x)
    x = Dropout(dropout_rate)(x)
    x = Conv1D(32,3,padding="same")(x)
    x = Dense(20, activation='relu')(x)
    x = Dense(20, activation='relu')(x)
    x = tf.transpose(x,perm=[0,2,1])
    x1 = Dense(20,activation = "relu")(inp[:,:26,:])
    x1 = Dense(20,activation = "relu")(x1)
    x1 = tf.transpose(x1,perm=[0,2,1])
    out = Concatenate()([x,x1])
    out = Dense(32,activation="relu")(out)
    outputs = Dense(3, activation='softmax')(out)
    model = Model(inputs=state_input, outputs=outputs)
    return model

def create_actor_model_2(input_shape, dropout_rate=0.2):
    state_input = Input(shape=input_shape)
    inp = tf.transpose(state_input, perm=[0, 2, 1])  # Transpose input to (batch, features, timesteps)
    x = inp[:, 26:, :]  # Slice to get only the part after the first 26 features
    x = Conv1D(64, 3, padding="same")(x)
    x = Dense(128, activation='relu')(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(dropout_rate)(x)
    x = Conv1D(32, 3, padding="same")(x)
    x = Dense(64, activation='relu')(x)
    x = Dense(64, activation='relu')(x)
    x = Dropout(dropout_rate)(x)
    x = Conv1D(32, 3, padding="same")(x)
    x = Dense(20, activation='relu')(x)
    x = Dense(20, activation='relu')(x)
    x = tf.transpose(x, perm=[0, 2, 1])  # Transpose back to (batch, timesteps, features)
    x1 = Dense(20, activation="relu")(inp[:, :26, :])
    x1 = Dense(20, activation="relu")(x1)
    x1 = tf.transpose(x1, perm=[0, 2, 1])  # Transpose to (batch, timesteps, features)
    out = Concatenate()([x, x1])
    out1 = Dense(3, activation='softmax')(out)
    model = Model(inputs=state_input, outputs=out1)
    return model


def create_critic_model(input_shape,action_shape, fc1_dims=128, fc2_dims=64):
    state_input = Input(shape=input_shape)
    action_input = Input(shape=action_shape)
    x1 = Dense(fc1_dims, activation='relu')(state_input)
    x2 = Dense(fc1_dims, activation='relu')(action_input)
    x1 = Flatten()(x1)
    x2 = Flatten()(x2)
    out = Concatenate()([x2, x1])
    x = Dense(fc2_dims, activation='relu')(out)
    x = Dense(fc2_dims, activation='relu')(out)
    x = Dense(fc2_dims, activation='relu')(out)
    x = Dense(64, activation='relu')(x)
    q_output = Dense(1, activation=None)(x)
    model = Model(inputs=[state_input,action_input], outputs=q_output)
    return model