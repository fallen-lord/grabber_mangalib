# import asyncio
#   10  => yuklab olsih uchun ketgan vaqt: 51.143468379974365 s
#   20 => 105.99165773391724 s

"""

tmie for single chapter: 4.980313301086426 s
tmie for single chapter: 3.2176032066345215 s
tmie for single chapter: 2.623701333999634 s
tmie for single chapter: 2.1192424297332764 s
tmie for single chapter: 2.5919671058654785 s
tmie for single chapter: 1.9533445835113525 s
tmie for single chapter: 2.000525712966919 s
tmie for single chapter: 2.020423412322998 s
tmie for single chapter: 1.8965320587158203 s
tmie for single chapter: 2.1831674575805664 s



10 yuklab olsih uchun ketgan vaqt: 46.61993098258972 s

tmie for single chapter: 5.377012014389038 s
tmie for single chapter: 2.2289700508117676 s
tmie for single chapter: 2.91770601272583 s
tmie for single chapter: 3.905614137649536 s
tmie for single chapter: 3.126905679702759 s
tmie for single chapter: 3.2988009452819824 s
tmie for single chapter: 2.5159502029418945 s
tmie for single chapter: 3.781144618988037 s
tmie for single chapter: 3.681570291519165 s
tmie for single chapter: 3.0310542583465576 s
tmie for single chapter: 3.0180652141571045 s
tmie for single chapter: 2.4574151039123535 s
tmie for single chapter: 2.854382038116455 s
tmie for single chapter: 3.8605422973632812 s
tmie for single chapter: 2.102545976638794 s
tmie for single chapter: 2.651311159133911 s
tmie for single chapter: 3.6903011798858643 s
tmie for single chapter: 3.683382987976074 s
tmie for single chapter: 3.6316301822662354 s
tmie for single chapter: 3.003983736038208 s



20  yuklab olsih uchun ketgan vaqt: 91.84443020820618 s


"""

"""
tmie for single chapter: 0.40129542350769043 s
tmie for single chapter: 0.4236726760864258 s
tmie for single chapter: 0.3677046298980713 s
tmie for single chapter: 0.35373973846435547 s
tmie for single chapter: 0.45003223419189453 s
tmie for single chapter: 0.4611630439758301 s
tmie for single chapter: 0.43270015716552734 s
tmie for single chapter: 0.31888628005981445 s
tmie for single chapter: 0.3696479797363281 s
tmie for single chapter: 0.4507136344909668 s



 yuklab olsih uchun ketgan vaqt: 17.616514444351196 s


tmie for single chapter: 0.3426392078399658 s
tmie for single chapter: 0.3228161334991455 s
tmie for single chapter: 0.38466429710388184 s
tmie for single chapter: 0.32068586349487305 s
tmie for single chapter: 0.3617687225341797 s
tmie for single chapter: 0.38225388526916504 s
tmie for single chapter: 0.29486656188964844 s
tmie for single chapter: 0.3463020324707031 s
tmie for single chapter: 0.33924293518066406 s
tmie for single chapter: 0.4333171844482422 s
tmie for single chapter: 0.4487600326538086 s
tmie for single chapter: 0.345794677734375 s
tmie for single chapter: 0.3958733081817627 s
tmie for single chapter: 0.47464537620544434 s
tmie for single chapter: 0.38655900955200195 s
tmie for single chapter: 0.3188025951385498 s
tmie for single chapter: 0.43103718757629395 s
tmie for single chapter: 0.46325135231018066 s
tmie for single chapter: 0.335024356842041 s
tmie for single chapter: 0.43378615379333496 s



 yuklab olsih uchun ketgan vaqt: 23.059311389923096 s


"""

# async def funck3():
# 	from requests_html import AsyncHTMLSession
# 	ass = AsyncHTMLSession()
# 	ass.headers['Content-Type'] = 'image/jpeg'
# 	ass.headers['Accept-Ranges'] = 'bytes'
# 	print(ass.headers)
# 	response = await ass.get("https://img33.imgslib.link//manga/doupo-cangqiong-dou-po-cang-qiong/chapters/2-226/20.jpg")
# 	# await asyncio.sleep(1)
# 	print(response)
# 	print(type(response))
# 	print(response.headers)
#
# def funck2(par1, par2):
# 	print(par1, par2)
#
# async def main(par1, par2):
# 	funck2(par1, par2)
# 	await funck3()
#
#
# asyncio.run(main('sss', 111111))
#
# import asyncio
#
# async def recursive_async_function(count):
#     if count <= 0:
#         return
#     print(f"Count: {count}")
#     await asyncio.sleep(1)  # Simulate an asynchronous operation
#     await recursive_async_function(count - 1)
#
# async def main():
#     await recursive_async_function(5)
#
# if __name__ == "__main__":
#     asyncio.run(main())
#
#     lis = []
#
#     print(lis == [])
#
# import asyncio
#
# from requests_html import AsyncHTMLSession
#
# def send_file(chapter):
#
# 	async def asend_file():
#
# 		session = AsyncHTMLSession()
#
# 		url = BOT_URL + "sendDocument"
# 		data = {"chat_id": SOURCE_CHANEL}
# 		files = {"document": (f"Chapter {chapter[3]}.pdf", chapter[-1])}
#
# 		response = await session.post(url,
# 		# response = post(url,
# 			data=data,
# 			files=files)
#
# 		file_id = response.json()['result']['document']['file_id']
#
# 		await session.post(url,
# 		# post(url,
# 			data={"chat_id": MAIN_CHANEL, "document": file_id})
#
# 	asyncio.run(asend_file())

a = None

for i in a:
    print(i)
