import click
import pickle

from utils.utils import bin2bytes


@click.command()
@click.argument("instsfile", type=click.File("r"))
@click.argument('strategy', type=str)
@click.option('--thumb', is_flag=True)
def main(instsfile, strategy, thumb):
    insts = {}
    mode = 'thumb' if thumb else ''
    for i, line in enumerate(instsfile):
        if strategy == 'random':
            name, inst = line.split(" ")
        else:
            name, _, inst = line.split(" ")
        insts[i] = (name, bin2bytes(inst, mode))
    with open(f'pickled_{instsfile.name}', 'wb') as f:
        pickle.dump(insts, f)


if __name__ == '__main__':
    main()
