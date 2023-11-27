import os
import pickle

import click
from tqdm import tqdm

from utils.elf import parse_template


def generate(binary: bytes, offset: int, insts: dict, outdir: str):
    for id, (name, inst) in tqdm(insts.items()):
        binary = binary[:offset] + inst + binary[offset + len(inst) :]
        outpath = os.path.join(outdir, str(id))
        with open(os.open(outpath, os.O_CREAT | os.O_WRONLY, 0o777), "wb") as f:
            f.write(binary)


@click.command()
@click.argument("instsfile", type=click.File("rb"))
@click.option(
    "--outdir",
    default="testcases",
    type=click.Path(resolve_path=True),
)
@click.option(
    "--mode",
    required=True,
    type=click.Choice(["arm", "thumb", "arm64"]),
)
def main(instsfile, outdir, mode):

    insts = pickle.load(instsfile)

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    binary, offset = parse_template(mode)
    generate(binary, offset, insts, outdir)


if __name__ == "__main__":
    main()
