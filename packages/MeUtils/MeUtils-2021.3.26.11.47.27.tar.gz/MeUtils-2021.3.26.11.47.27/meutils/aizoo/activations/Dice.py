#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : DeepNN.
# @File         : Dice
# @Time         : 2020/5/13 8:55 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import tensorflow as tf
from tensorflow.python.keras.initializers import Zeros


class Dice(tf.keras.layers.Layer):
    """The Data Adaptive Activation Function in DIN,which can be viewed as a generalization of PReLu and can adaptively adjust the rectified point according to distribution of input data.

      Input shape
        - Arbitrary. Use the keyword argument `input_shape` (tuple of integers, does not include the samples axis) when using this layer as the first layer in a model.

      Output shape
        - Same shape as the input.

      Arguments
        - **axis** : Integer, the axis that should be used to compute data distribution (typically the features axis).

        - **epsilon** : Small float added to variance to avoid dividing by zero.

      References
        - [Zhou G, Zhu X, Song C, et al. Deep interest network for click-through rate prediction[C]//Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining. ACM, 2018: 1059-1068.](https://arxiv.org/pdf/1706.06978.pdf)
    """

    def __init__(self, axis=-1, epsilon=1e-9, **kwargs):
        self.axis = axis
        self.epsilon = epsilon
        super(Dice, self).__init__(**kwargs)

    def build(self, input_shape):
        super(Dice, self).build(input_shape)  # Be sure to call this somewhere!

        self.uses_learning_phase = True  # 学习阶段

        self.bn = tf.keras.layers.BatchNormalization(
            xis=self.axis,
            epsilon=self.epsilon,
            center=False,
            scale=False)  # TODO:为啥是false

        self.alphas = self.add_weight(
            shape=(input_shape[-1],),
            initializer=Zeros(),
            dtype=tf.float32,
            name='dice_alpha')  # name='alpha_'+self.name

    def call(self, inputs, training=None, **kwargs):
        """
        有些Keras层,如BN,Dropout,在训练和测试过程中的行为不一致, 你可以通过打印layer.uses_learning_phase来确定当前层工作在训练模式还是测试模式
        if training is None:
            tf.keras.backend.learning_phase() # TODO:打印一下
        """
        inputs_normed = self.bn(inputs, training=training)
        x_p = tf.sigmoid(inputs_normed)
        return x_p * inputs + (1.0 - x_p) * self.alphas * inputs

    def compute_output_shape(self, input_shape):
        return input_shape

    def get_config(self):
        base_config = super().get_config()
        config = {'axis': self.axis, 'epsilon': self.epsilon}
        return {**base_config, **config}
