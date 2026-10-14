"""1.1 Logo parkingyou (p6) plus beeldmerk and wordmark splits."""
from pyassets.registry import element, crop

# (id suffix, mark bbox, wordmark bbox) per variant on page 6
LOGO = {
    "horizontal-color": ((394, 192, 458, 268), (471, 201, 660, 243)),
    "stacked-color": ((185, 162, 248, 237), (122, 242, 311, 284)),
    "horizontal-black": ((395, 395, 459, 472), (472, 405, 661, 447)),
    "stacked-black": ((185, 365, 249, 441), (122, 445, 311, 488)),
    "horizontal-white": ((387, 580, 459, 666), (475, 590, 689, 638)),
    "stacked-white": ((194, 545, 267, 632), (124, 637, 338, 684)),
}
NAMES = {
    "horizontal-color": "Logo liggend, kleur",
    "stacked-color": "Logo staand, kleur",
    "horizontal-black": "Logo liggend, zwart",
    "stacked-black": "Logo staand, zwart",
    "horizontal-white": "Logo liggend, diapositief",
    "stacked-white": "Logo staand, diapositief",
}
for key, (mark, word) in LOGO.items():
    full = (min(mark[0], word[0]), min(mark[1], word[1]), max(mark[2], word[2]), max(mark[3], word[3]))

    def mk(full=full):
        return lambda src: crop(src, 6, full, texts=False)

    element(f"py-atom-logo-{key}", NAMES[key], "atom", "logo", 6, built_from=("py-atom-logo-beeldmerk-" + key.split("-")[1], "py-atom-logo-wordmark-" + key.split("-")[1]))(mk())
    variant = key.split("-")[1]
    shape = key.split("-")[0]
    if shape == "horizontal":  # beeldmerk and wordmark atoms are split once per colour from the horizontal logo
        def mk_mark(mark=mark):
            return lambda src: crop(src, 6, mark, texts=False)

        def mk_word(word=word):
            return lambda src: crop(src, 6, word, texts=False)

        if variant != "color":  # colour beeldmerk comes from p9 (real hole instead of a white fill)
            element(f"py-atom-logo-beeldmerk-{variant}", f"Beeldmerk {variant}", "atom", "logo", 6)(mk_mark())
        element(f"py-atom-logo-wordmark-{variant}", f"Woordmerk {variant} (contouren)", "atom", "logo", 6)(mk_word())
