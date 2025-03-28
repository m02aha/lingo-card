from gpytranslate import Translator
import asyncio

async def maintranslation(original_txt,dest_lang):
    t=Translator()
    translation=await t.translate(original_txt,targetlang=dest_lang)
    langauge=await t.detect(translation.text)
    return translation.text,langauge



