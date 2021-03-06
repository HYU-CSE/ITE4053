import numpy as np
from tqdm import tqdm

from nnn import utils


def main(args) -> float:

    if args.mode == 'tf':
        import tensorflow.keras as nn
    else:
        import nnn as nn

    score = .0

    with tqdm(total=args.repeat) as t:
        for e in range(args.repeat):
            train = utils.Dataset(args.size, normal=args.normal)
            test = utils.Dataset(args.size, normal=args.normal)

            # Build Network
            # default network is two dense layer with sigmoid activation which have 2 hidden layer
            # 2 2 sigmoid
            # 2 1 sigmoid
            model = nn.Sequential([
                nn.layers.Dense(int(output_dim),
                                input_dim=int(input_dim),
                                activation=getattr(nn.activations, activation))
                for (input_dim, output_dim, activation) in args.layer or [
                    ['2', '2', 'sigmoid'],
                    ['2', '1', 'sigmoid'],
                ]
            ])

            # Create Optimizer
            optimizer = getattr(nn.optimizers, args.optimizer)(lr=args.lr)

            # Compile network
            model.compile(optimizer=optimizer,
                          loss=args.loss,
                          metrics=['accuracy'])

            # Train model with train dataset
            model.fit(train.X, train.Y, epochs=args.epoch, verbose=args.verbose)

            # Test model with test dataset
            loss, acc = model.evaluate(test.X, test.Y, verbose=args.verbose)
            score += acc

            t.set_postfix(loss=f'{loss:.4f}',
                          score=f'{acc*100:.2f}%',
                          mean=f'{score/(e+1)*100:.2f}%')
            t.update()

    if args.mode == 'np' and args.save:
        np.savez(args.save, **{
            str(i): p for i, p in enumerate(model.parameters)
        })

        print('\n\n== Parameters')
        for i, layer in enumerate(model.layers):
            print(f'{i}: {layer.__class__.__name__}', layer.parameters)

    return score / args.repeat


if __name__ == '__main__':
    main(utils.arguments)
