import click
import time
from examiner.unicorn import run
from examiner.elf import get_template_locations, get_template_segments


@click.command()
@click.argument("instsfile", type=click.File("r"))
@click.option(
    "--mode",
    required=True,
    type=click.Choice(["arm", "thumb", "arm64"]),
)
@click.option("--outfile", default="status_unicorn.json")
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
    entry, _, _ = get_template_locations(mode)
    insts = []
    for i, line in enumerate(instsfile):
        name, code = line.strip().split()
        insts.append((i, name, code))
    start_time = time.process_time()
    run(insts, mode, segments, entry, outfile)
    end_time = time.process_time()
    print('time: ', start_time - end_time)


if __name__ == "__main__":
    main()
