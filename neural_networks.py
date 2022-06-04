import constants
import tensorflow as tf
from tensorflow.keras import layers
import numpy as np

from typing import List
from dataclasses import dataclass
import dataclasses

import json
import ast
import os

import random


@dataclass
class FFNHyperparams:
    """Feed-Forward Network Hyperparameters"""
    num_inputs: int
    num_outputs: int

    hidden_dims: List[int]
    activation_fcn: str  # ['relu', 'tanh', 'sigmoid', 'elu', 'selu', 'softplus']
    learning_rate: float


def build_model(hp: FFNHyperparams):

    model = tf.keras.Sequential()

    model.add(layers.Dense(hp.num_inputs, activation=hp.activation_fcn, input_shape=[hp.num_inputs], name='ukryta_1'))

    for i, hidden_dim in enumerate(hp.hidden_dims):
        model.add(layers.Dense(hidden_dim, activation=hp.activation_fcn, name='ukryta_'+str(i+2)))

    model.add(layers.Dense(hp.num_outputs, name='wyjsciowa'))  # model regresyjny, activation=None w warstwie wyjściowej

    optimizer = tf.keras.optimizers.Adam(learning_rate=hp.learning_rate)

    model.compile(optimizer=optimizer, loss=tf.keras.losses.mse,
                  metrics=[tf.keras.metrics.mean_absolute_error, 'mse'])

    return model


def train(model, train_data, valid_data=None, training_dir='exp_00/'):

    (x, y) = train_data

    # TODO define callbacks EarlyStopping, ModelCheckpoint, TensorBoard
    # my callbacks
    es_cbk = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=1000,
        restore_best_weights=True,
    )
    ckp_cbk = tf.keras.callbacks.ModelCheckpoint(
        training_dir + "model_best_weights",
        save_best_only=True,
        save_weights_only=True,
    )
    tb_cbk = tf.keras.callbacks.TensorBoard(training_dir)

    # tensorboard --logdir=.

    # training
    if valid_data is None:
        history = model.fit(x=x, y=y, batch_size=64, validation_split=0.2,
                            epochs=constants.training_epochs, verbose=1, callbacks=[es_cbk, ckp_cbk, tb_cbk])
    else:
        history = model.fit(x=x, y=y, batch_size=64, validation_data=valid_data,
                            epochs=constants.training_epochs, verbose=1, callbacks=[es_cbk, ckp_cbk, tb_cbk])

    return model, history


def single_run(hp, train_data, training_dir, valid_data=None, verbose=True):

    if verbose:
        print(f"Training model with hyperparams: {hp}")

    os.makedirs(training_dir, exist_ok=True)

    # save hyperparams
    with open(training_dir + 'hp.json', 'w') as f:
        json.dump(dataclasses.asdict(hp), f)

    # build model
    model = build_model(hp)

    try:
        model.load_weights(training_dir + "model_best_weights")
        print("Loaded model from " + training_dir)
    except tf.errors.NotFoundError:
        print(f"No model found in '{training_dir}'. Training new model.")

    if verbose:
        print(model.summary())

    # train model
    output = train(model, train_data, valid_data=valid_data, training_dir=training_dir)
    model.save_weights('./training/final_weights')
    return output


def load_training_data(training_dir):
    with open(training_dir + "evals_normalized.json", 'r') as file:
        jj = json.load(file)

    train_features = list(jj.keys())
    train_targets = list(jj.values())
    for i, key in enumerate(train_features):
        train_features[i] = ast.literal_eval(key)

    # randomly shuffling the training data
    to_shuffle = list(zip(train_features, train_targets))
    random.shuffle(to_shuffle)
    train_features, train_targets = zip(*to_shuffle)

    train_features = np.array(train_features)
    train_targets = np.array(train_targets)

    return train_features, train_targets


def start_training():
    training_dir = './training/'
    training_data = load_training_data(training_dir)

    # setup hyperparameters
    hp = constants.default_hyperparams

    # run training with them
    _, history = single_run(hp, training_data, training_dir)
