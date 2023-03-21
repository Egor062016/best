import logging
import openai
from gpytranslate import Translator

from aiogram import Bot, Dispatcher, executor, types

# log
logging.basicConfig(level=logging.INFO)

# init translator
t = Translator()

# init openai
openai.api_key = "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"

# init aiogram
bot = Bot("5985844276:AAHVRP7ofOfoFWPIMtnU5g6gWf0u-kXblgI")
dp = Dispatcher(bot)


@dp.message_handler()
async def gpt_answer(message: types.Message):
    # await message.answer(message.text)

    model_engine = "text-davinci-003"
    max_tokens = 128  # default 1024
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=message.text,
        max_tokens=max_tokens,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    await message.answer("ChatGPT: Генерирую ответ ...")
    await message.answer(completion.choices[0].text)

# run long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
