import s3_worker

mys3_worker = s3_worker.s3_worker("../credentials.json")

mys3_worker.create_bucket()

mys3_worker.add_to_bucket('test_images/love_ctk.jpg')
