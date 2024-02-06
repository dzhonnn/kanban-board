import aiofiles
from dict2xml import dict2xml
from collections import OrderedDict


async def make_xml(data: dict):
    async with aiofiles.open(f"board{data['id']}.xml", "w") as f:
        await f.close()
    async with aiofiles.open(f"board{data['id']}.xml", "a") as f:
        for section in data["section"]:
            section = OrderedDict(section)
            del section["id"]
            notes = list()
            for note in section["note"]:
                note = OrderedDict(note)
                del note["id"]
                notes.append(note)
            section["note"] = notes
            await f.write(dict2xml(section, indent="  ", wrap=section["title"]))
        await f.close()
