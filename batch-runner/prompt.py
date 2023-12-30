from services.google.spread_sheet.spread_sheet_facade import SpreadSheetFacade
from services.openai.gpt.model import GPTModelFacade


async def main():
    model = GPTModelFacade()
    spread_facade = SpreadSheetFacade("1mjk98TSpRJ2ixsYfJ5rp4Zw0Pr8EeDV_YNS5VdO4jnM", "write")
    values = spread_facade.get_values("SEO")
    result = []
    # for index, value in enumerate(values, 1):
    #     if len(value) == 3:
    #         continue
    #     answer = await model.listen_markdown_prompt(value[1])
    #     result.append([answer])
    #     sheet_range = f'SEO!B{index}'
    #     await spread_facade.write_sheet("SEO", result, sheet_range)
    #     print("done")
    print("aaa")
    index = 2
    answer = await model.listen_markdown_prompt(values[index][1])
    result.append([answer])
    sheet_range = f'SEO!B{index}'
    await spread_facade.write_sheet("SEO", result, sheet_range)
    print("done")

import asyncio
asyncio.run(main())
