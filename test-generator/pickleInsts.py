import click
import pickle

from utils.utils import bin2bytes


@click.command()
@click.argument("instsfile", type=click.File("r"))
@click.argument('strategy', type=str)
@click.argument('encoding', type=str)
def main(instsfile, strategy, encoding):
    insts = {}
    mode = 'thumb' if encoding == 'T16' or encoding == 'T32' else ''
    for i, line in enumerate(instsfile):
        if strategy == 'symbolic' and (encoding == 'T16' or encoding == 'A64'):
            name, _, inst = line.split(" ")
        else:
            name, inst = line.split(" ")
        insts[i] = (name, bin2bytes(inst, mode))
    
    filename = instsfile.name.split('/')[-1]
    print(f'pickled_{filename}')
    with open(f'pickled_{filename}', 'wb') as f:
        pickle.dump(insts, f)


if __name__ == '__main__':
    main()
