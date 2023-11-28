import click
import logging
import time
from angr import run
from examiner.elf import get_template_locations, get_template_segments

logging.getLogger("angr").setLevel(100)
logging.getLogger("pyvex.lifting").setLevel(100)


@click.command()
@click.argument("instsfile", type=click.File("r"))
@click.option(
    "--mode",
    required=True,
    type=click.Choice(["arm", "thumb", "arm64"]),
)
@click.option("--outfile", default="status_angr.json")
def main(instsfile, mode, outfile):
    (data1, data2) = get_template_segments(mode)
    if mode == "arm64":
        segments = [
            (0x400000, 0x7000, "rx", data1),
            (0x416000, 0x5000, "rw", data2),
        ]
    else:
        segments = [
            (0x10000, 0x6000, "rx", data1),
            (0x25000, 0x4000, "rw", data2),
        ]
    insts = []
    for i, line in enumerate(instsfile):
        name, code = line.strip().split()
        insts.append((i, name, code))
    entry, _, _ = get_template_locations(mode)
    start_time = time.process_time()
    run(insts, mode, segments, entry, outfile)
    end_time = time.process_time()
    print('time: ', end_time - start_time)


if __name__ == "__main__":
    main()
