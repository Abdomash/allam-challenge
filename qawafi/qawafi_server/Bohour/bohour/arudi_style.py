import random
import re
from pyarabic.araby import strip_tashkeel

harakat = ["\u0650", "\u064E", "\u064F"]  # [kasra, fatha, damma, ]
sukun = ["\u0652"]  # [sukun]
mostly_saken = [
    "\u0627",
    "\u0648",
    "\u0649",
    "\u064A",
]  # [alef, waw, alef maqsurah, ya'a]
tnween_chars = [
    "\u064c",
    "\u064d",
    "\u064b",
]  # damm tanween, kasra tanween, fatha tanween, maddah
shadda_chars = ["\u0651"]
all_chars = list("إةابتثجحخدذرزسشصضطظعغفقكلمنهويىأءئؤ ")
prem_chars = harakat + sukun + mostly_saken + tnween_chars + shadda_chars + all_chars
CHANGE_LST = {
    u"هذا": u"هَاذَا",
    u"هذه": u"هَاذِه",
    u"هذان": u"هَاذَان",
    u"هذين": u"هَاذَين",
    u"ذلك": u"ذَالِك",
    u"ذلكما": u"ذَالِكُمَا",
    u"ذلكم": u"ذَالِكُم",
    u"الله": u"اللَّاه",
    u"اللهم": u"اللَّاهُمّ",
    u"إله": u"إِلَاه",
    u"الإله": u"الإِلَاه",
    u"إلهي": u"إِلَاهي",
    u"إلهنا": u"إِلَاهنا",
    u"إلهكم": u"إِلَاهكم",
    u"إلههم": u"إِلَاههم",
    u"إلههن": u"إِلَاههن",
    u"رحمن": u"رَحمَان",
    u"طاوس": u"طَاوُوس",
    u"داود": u"دَاوُود",
    u"لكنه":u"لَاكِنّهُ",
  # u"لكن": u"ّلَاكِن",
    # u"لكنني": u"لَاكِنَّنِي",
    # u"لكنك": u"لَاكِنَّك",
    # u"لكنه": u"لَاكِنَّه",
    # u"لكنها": u"لَاكِنَّهَا",
    # u"لكنهما": u"لَاكِنَّهُمَا",
    # u"لكنهم": u"لَاكِنَّهُم",
    # u"لكنهن": u"لَاكِنَّهُن",
    u"أولئك": u"أُلَائِك",
    u"أولئكم": u"أُلَائِكُم",
}

def handle_space(plain_chars):
    if plain_chars[-1] == " ":
        return plain_chars[:-2]
    else:
        return plain_chars[:-1]


def remove_extra_harakat(pred): #WRONG, fixed
    out = ""
    i = 0
    while i < len(pred):
        if i < len(pred) - 1:
            if pred[i] in harakat and pred[i + 1] in harakat:
                i += 1
                continue
        out += pred[i]
        i += 1
    return out


def extract_tf3eelav3(pred, verbose=False, return_indices=False):
    indices = []
    pred = remove_extra_harakat(pred)
    chars = list(pred.replace("\u0622", "ءَا").strip())
    chars = [c for c in chars if c in prem_chars]
    chars = list(re.sub(" +", " ", "".join(chars).strip()))
    out = ""
    i = 0
    plain_chars = ""
    j = 0
    flag = True
    while i < len(chars) - 1 and flag:
        j += 1
        char = chars[i]
        if verbose:
            print(char)
        # plain_chars += char
        if char in all_chars:
            if char == " ":
                plain_chars += char
                i += 1
                continue
            # set up some vars
            next_char = chars[i + 1]
            if next_char == " ":
                next_char = chars[i + 2]
            if i < len(chars) - 2:
                next_next_char = chars[i + 2]
            if len(out) > 0:
                prev_char = out[-1]
            else:
                prev_char = ""
            # ----------------------
            if next_char in harakat:
                out += "1"
                indices.append(i)
                plain_chars += char
            elif next_char in sukun:
                if prev_char != "0":
                    out += "0"
                    indices.append(i)
                    plain_chars += char
                elif (i + 1) == len(chars) - 1:
                    out = out[:-1] + "10" #replace sukun (0) with 10 to avoid 100
                    indices.append(i) #adding 1 only
                    plain_chars += char
                else:
                    plain_chars = handle_space(plain_chars) + char
            elif next_char in tnween_chars:
                if char != "ا":
                    plain_chars += char
                plain_chars += "ن"
                out += "10"
                indices.append(i)
                indices.append(i) #add twice
            elif next_char in shadda_chars:
                """added characters"""
                # 1
                if prev_char != "0":
                    plain_chars += char
                    plain_chars += char
                    out += "01"
                    indices.append(i)
                    indices.append(i)
                else:
                    plain_chars = handle_space(plain_chars) + char + char
                    out += "1"
                    indices.append(i)
                if i + 2 < len(chars):  # need to recheck this
                    if (
                        chars[i + 2] in harakat
                    ):  # in case shaddah not followed by harakah
                        i += 1
                    elif (
                        chars[i + 2] in tnween_chars
                    ):  # in case shaddah is followed by tanween
                        i += 1
                        # plain_chars += char
                        plain_chars += "ن"
                        # out += '10'
                        out += "0"
                        indices.append(i)
            elif next_char in all_chars:
                if prev_char != "0":
                    out += "0"
                    indices.append(i)
                    plain_chars += char
                #removed prev_char == "0" from elif 
                elif chars[i + 1] in [" ", "ا", "و", "ي"] and (i+2 < len(chars)) and (i+4 > len(chars) or chars[i+1:i+4] != " ال"): #changed: allowed letter-vowel to be represented as 10, no need for harakat too
                    out += "1"
                    indices.append(i)
                    plain_chars += char
                else:
                    plain_chars = handle_space(plain_chars) + char
                    #plain_chars += char
                i -= 1
            if next_next_char == " ":
                #IGNORED mim to the edge case (adding vowel in hashw)
                #mim edge case only applies in jam3 (kaf mim, hah mim)
                if char == "ه" and prev_char != "0": #Fixed edge case with vowel-ha, dont add another vowel
                    if next_char == harakat[0]:
                        plain_chars += "ي"
                        out += "0"
                        indices.append(i)
                    if next_char == harakat[2]:
                        plain_chars += "و"
                        out += "0"
                        indices.append(i)
            i += 2
        if j > 2 * len(chars):
            print(out, plain_chars)
            flag = False
            raise Exception("error")

    if out[-1] != "0":
        out += "0"  # always add sukun to the end of baits if mutaharek
        indices.append(i)
    if chars[-1] == harakat[0]:
        plain_chars += "ي"
    elif chars[-1] == tnween_chars[1]:
        plain_chars = plain_chars[:-1] + "ي"
    elif chars[-1] == harakat[1]:
        plain_chars += "ا"
    elif chars[-1] == harakat[2]:
        plain_chars += "و"
    elif chars[-1] == tnween_chars[0]:
        plain_chars = plain_chars[:-1] + "و"
    elif chars[-1] in "ىاوي" and chars[-2] not in tnween_chars:
        plain_chars += chars[-1]
    plain_chars_no_space = plain_chars.replace(" ", "")
    if return_indices:
        return plain_chars, out, indices
    return plain_chars, out


def process_specials_before(bait):
    if bait[0] == "ا":
        bait = random.choice(["أَ", "إِ"]) + bait[1:]
    bait = bait.replace("وا ", "و ")
    if bait.find("وا") == len(bait) - 2:
        bait = bait[:-1]
    bait = bait.replace("وْا", "و")
    if bait.find("وْا") == len(bait) - 2:
        bait = bait[:-2] + "و"
    bait = bait.replace("الله", "اللاه")
    bait = bait.replace("اللّه", "الله")
    bait = bait.replace("إلَّا", "إِلّا")
    bait = bait.replace("نْ ال", "نَ ال")
    bait = bait.replace("لْ ال", "لِ ال")
    bait = bait.replace("إلَى", "إِلَى")
    bait = bait.replace("إذَا", "إِذَا")
    bait = bait.replace("ك ", "كَ ")
    #added al, vowel-alif combs
    bait = bait.replace("ْ ال", "ِ لْ")
    bait = bait.replace("ُ ال", "ِ لْ")
    bait = bait.replace("ِ ال", "ِ لْ")
    bait = bait.replace("َ ال", "ِ لْ")
    bait = bait.replace(" ال", " الْ")
    bait = bait.replace("لا", "لَا")
    bait = bait.replace("َاَ", "َا")
    bait = bait.replace("ْْ", "ْ") #added, to help fix al t3rif problem
    bait = bait.replace("ّْ", "ّ")
    print(bait)

    out = []
    for word in bait.split(" "):
      cleaned_word = strip_tashkeel(word)
      for key in CHANGE_LST:
        if key in cleaned_word:
          cleaned_word = cleaned_word.replace(key, CHANGE_LST[key])
          out.append(cleaned_word)
          break
      else:
        out.append(word)

    bait = ' '.join(out)

    if bait[1] in all_chars:
        bait = bait[0] + harakat[1] + bait[1:]
    out = ""
    i = 0
    while i < len(bait):
        if bait[i] == "ا" and bait[i - 1] in tnween_chars:
            i += 1
            if i < len(bait) and bait[i] in harakat + sukun + tnween_chars + shadda_chars:
                """
                remove the case when we have any tashkeel comes after tnween chars
                """
                i += 1
            continue
        out += bait[i]
        i += 1

    return out


def process_specials_after(bait):
    bait = bait.replace("ةن", "تن")
    # bait = bait.replace('ةي','تن')
    return bait


def get_arudi_style(bait, verbose=False):
    results = []
    indices = []
    bait = bait.strip()
    if len(bait) > 0:
        preprocessed = process_specials_before(bait)
        arudi_style, pattern, indices = extract_tf3eelav3(preprocessed, verbose=verbose, return_indices=True)
        results.append([process_specials_after(arudi_style), pattern, indices])
    else:
        results.append(["", ""])
    return results
