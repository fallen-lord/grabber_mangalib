# import asyncio
#
#
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
