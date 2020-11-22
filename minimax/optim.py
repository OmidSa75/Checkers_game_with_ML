def criterion(v_train, v_b0):
    loss = v_train - v_b0
    return loss


def optimizer(weights, features, loss, lr):
    for i in range(len(weights)):
        weights[i] = weights[i] + lr * features[i] * loss

    return weights
