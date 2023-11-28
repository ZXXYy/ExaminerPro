from os.path import dirname, abspath, join
from elftools.elf.elffile import ELFFile


class ELFParseException(Exception):
    pass


def get_segments(elfpath):
    with open(elfpath, "rb") as f:
        elffile = ELFFile(f)
        data = []
        for segment in elffile.iter_segments():
            p_type = segment.header["p_type"]
            if p_type == "PT_LOAD":
                data.append(segment.data())
    return data


def get_template_segments(mode):
    root_path = dirname(dirname(abspath(__file__)))
    template_path = join(root_path, "test_template/template_{}".format(mode))
    return get_segments(template_path)


def parse_template(mode, level):
    root_path = dirname(dirname(abspath(__file__)))
    if level == "user":
        template_path = join(root_path, "test_template/user-level/template_{}".format(mode))
        with open(template_path, "rb") as f:
            elffile = ELFFile(f)
            symtab = elffile.get_section_by_name(".symtab")
            inst_location = symtab.get_symbol_by_name("inst_location")[0]
            inst_location = inst_location.entry["st_value"]
            for segment in elffile.iter_segments():
                if segment.header["p_type"] == "PT_LOAD":
                    base_location = segment.header["p_vaddr"]
                    break
            else:
                raise ELFParseException("no load segment")
            offset = inst_location - base_location
            f.seek(0)
            binary = f.read()
        return binary, offset, None
    
    elif level == "system":
        template_path = join(root_path, "test_template/system-level/ktemplate_{}.ko".format(mode))
        with open(template_path, "rb") as f:
            elffile = ELFFile(f)
            symtab = elffile.get_section_by_name(".symtab")
            inst_location = symtab.get_symbol_by_name("inst_location")[0]
            inst_location = inst_location.entry["st_value"]
            # dump_mem_location = symtab.get_symbol_by_name("dump_memory")[0]
            # dump_mem_location = dump_mem_location.entry["st_value"]

            text_section = elffile.get_section_by_name(".text")
            text_section = text_section.header['sh_offset']
            
            # for segment in elffile.iter_segments():
            #     if segment.header["p_type"] == "PT_LOAD":
            #         base_location = segment.header["p_vaddr"]
            #         break
            # else:
            #     raise ELFParseException("no load segment")
            # offset = inst_location - base_location
            offset = inst_location + text_section #if mode=='arm' else inst_location
            # offset_mem = dump_mem_location + text_section #if mode=='arm' else dump_mem_location
            offset_mem = None
            f.seek(0)
            binary = f.read()
        return binary, offset, offset_mem
        
    else:
        raise ELFParseException("unknown level")
    
    


def get_locations(elfpath):
    with open(elfpath, "rb") as f:
        elffile = ELFFile(f)
        symtab = elffile.get_section_by_name(".symtab")
        inst_location = symtab.get_symbol_by_name("inst_location")[0]
        inst_location = inst_location.entry["st_value"]
        bkpt_location = symtab.get_symbol_by_name("bkpt_location")[0]
        bkpt_location = bkpt_location.entry["st_value"]
        for segment in elffile.iter_segments():
            if segment.header["p_type"] == "PT_LOAD":
                base_location = segment.header["p_vaddr"]
                break
        else:
            raise ELFParseException("no load segment")
    return (inst_location, bkpt_location, base_location)


def get_template_locations(mode):
    root_path = dirname(dirname(abspath(__file__)))
    template_path = join(root_path, "test_template/template_{}".format(mode))
    return get_locations(template_path)
