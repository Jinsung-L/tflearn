# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import tensorflow as tf
import tflearn


@tf.contrib.framework.add_arg_scope
def variable(name, shape=None, dtype=tf.float32, initializer=None,
             regularizer=None, trainable=True, collections=None, device='',
             restore=True):
    """ variable.

    Instantiate a new variable.

    Arguments:
        name: `str`. A name for this variable.
        shape: list of `int`. The variable shape (optional).
        dtype: `type`. The variable data type.
        initializer: `str` or `Tensor`. The variable initialization. (See
            tflearn.initializations for references).
        regularizer: `str` or `Tensor`. The variable regularizer. (See
            tflearn.losses for references).
        trainable: `bool`. If True, this variable weights will be trained.
        collections: `str`. A collection to add the new variable to (optional).
        device: `str`. Device ID to store the variable. Default: '/cpu:0'.
        restore: `bool`. Restore or not this variable when loading a
            pre-trained model (Only compatible with tflearn pre-built
            training functions).

    Returns:
        A Variable.

    """

    if isinstance(initializer, str):
        initializer = tflearn.initializations.get(initializer)()
    # Remove shape param if initializer is a Tensor
    if not callable(initializer) and isinstance(initializer, tf.Tensor):
        shape = None

    if isinstance(regularizer, str):
        regularizer = tflearn.losses.get(regularizer)

    with tf.device(device):

        try:
            var = tf.get_variable(name, shape=shape, dtype=dtype,
                                  initializer=initializer,
                                  regularizer=regularizer,
                                  trainable=trainable,
                                  collections=collections)
        # Fix for old TF versions
        except Exception as e:
            var = tf.get_variable(name, shape=shape, dtype=dtype,
                                  initializer=initializer,
                                  trainable=trainable,
                                  collections=collections)
            if regularizer is not None:
                tflearn.add_weights_regularizer(var, regularizer)

        if not restore:
            tf.add_to_collection(tf.GraphKeys.EXCL_RESTORE_VARS, var)

        return var


def get_all_variables():
    """ get_all_variables.

    Get all Graph variables.

    Returns:
        A list of Variables.

    """
    return tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)


def get_all_trainable_variable():
    """ get_all_variables.

    Get all Graph trainable variables.

    Returns:
        A list of Variables.

    """
    return tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES)


def get_layer_variables_by_name(name):
    """ get_layer_variables_by_name.

    Retrieve a layer's variables, given its name.

    Arguments:
        name: `str`. The layer name.

    Returns:
        A list of Variables.

    """
    return tf.get_collection(tf.GraphKeys.LAYER_VARIABLES + '/' + name)

# Shortcut
get_layer_variables = get_layer_variables_by_name


def get_value(var, session=None):
    """ get_value.

    Get a variable's value. If no session provided, use default one.

    Arguments:
        var: `Variable`. The variable to get value from.
        session: `Session`. The session to run the op. Default: the default
            session.

    Returns:
        The variable's value.

    """
    if not session:
        session = tf.get_default_session()
    return var.eval(session)


def set_value(var, value, session=None):
    """ set_value.

    Set a variable's value. If no session provided, use default one.

    Arguments:
        var: `Variable`. The variable to assign a value.
        value: The value to assign. Must be compatible with variable dtype.
        session: `Session`. The session to perform the assignation.
            Default: the default session.

    """
    op = tf.assign(var, value=value)
    if not session:
        session = tf.get_default_session()
    return op.eval(session=session)


def get_inputs_placeholder_by_name(name):
    vars = tf.get_collection(tf.GraphKeys.INPUTS)
    tflearn_name = name + '/X:0'
    if len(vars) == 0:
        raise Exception("The collection `tf.GraphKeys.INPUTS` is empty! "
                        "Cannot retrieve placeholder. In case placeholder was "
                        "defined outside TFLearn `input_data` layer, please "
                        "add it to that collection.")
    for e in vars:
        if e.name == tflearn_name:
            return e
    # Search again, in case defined outside TFLearn wrappers.
    for e in vars:
        if e.name == name:
            return e

    return None


def get_targets_placeholder_by_name(name):
    vars = tf.get_collection(tf.GraphKeys.TARGETS)
    tflearn_name = name + '/Y:0'
    if len(vars) == 0:
        raise Exception("The collection `tf.GraphKeys.INPUTS` is empty! "
                        "Cannot retrieve placeholder. In case placeholder was "
                        "defined outside TFLearn `input_data` layer, please "
                        "add it to that collection.")
    for e in vars:
        if e.name == tflearn_name:
            return e
    # Search again, in case defined outside TFLearn wrappers.
    for e in vars:
        if e.name == name:
            return e

    return None
