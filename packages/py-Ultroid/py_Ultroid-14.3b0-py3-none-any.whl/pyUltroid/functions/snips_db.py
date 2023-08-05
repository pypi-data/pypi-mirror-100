from . import udB


def list_to_str(list):  # Returns String
    str = ""
    for x in list:
        str += f"{x} "
    return str.strip()


def str_to_list(text):  # Returns List
    return text.split(" ")


def ls(list):
    str = ""
    for x in list:
        str += f"{x} |||"
    return str.strip()


def get_all_stuff():  # Returns List
    fills = udB.get("SNIPS")
    if fills is None or fills == "":
        return [""]
    else:
        return str_to_list(fills)


def get_reply(word):
    masala = udB.get("SNIPS")
    if not masala:
        return
    x = masala.split("|||")
    for i in x:
        x = i.split(":|")
        try:
            if str(x[0]).lower() == str(word).lower():
                return x[1]
        except:
            pass
    return None


def list_snip():
    fl = udB.get("SNIPS")
    if not fl:
        return None
    rt = fl.split("|||")
    tata = ""
    tar = 0
    for on in rt:
        er = on.split(":|")
        tata += f"👉 `${er[0]}`\n"
        tar += 1
    if tar == 0:
        return None
    return tata


def get_snips():
    fl = udB.get("SNIPS")
    if not fl:
        return None
    rt = fl.split("|||")
    tata = ""
    tar = 0
    for on in rt:
        er = on.split(":|")
        tata += f"{er[0]} "
        tar += 1
    if tar == 0:
        return None
    return tata


def add_snip(word, reply):
    try:
        dumb_masala = get_all_stuff()
        the_thing = f"|||{word}:|{reply}"
        rt = udB.get("SNIPS")
        if not rt:
            the_thing = f"{word}:|{reply}"
        dumb_masala.append(the_thing)
        udB.set("SNIPS", list_to_str(dumb_masala))
        return True
    except Exception as e:
        print(e)
        return False


def rem_snip(word):
    try:
        d = list_to_str(get_all_stuff())
        x = d.split("|||")
        reply = get_reply(word)
        the_thing = f"{word}:|{reply} "
        the_thing2 = f"{word}:|{reply}"
        try:
            x.remove(the_thing)
            x.remove(the_thing2)
        except BaseException:
            pass
        if len(x) < 2:
            udB.set("SNIPS", list_to_str(x))
        else:
            udB.set("SNIPS", ls(x))
        return True
    except Exception as e:
        print(e)
        return False
