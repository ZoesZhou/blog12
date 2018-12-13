
# from wsgiref.simple_server import make_server, demo_app
#
# ip = '127.0.01'
# port =9999
#
# server = make_server(ip, port, demo_app)
# server.serve_forever()

#
# from wsgiref.simple_server import make_server
#
# res_str = b"Zoes surface"
# ip = '127.0.0.1'
# port = 9999
#
#
# #  函数实现
# def application(envirno, start_response):
#     start_response("200 Ok", [("Content-Type", "text/plain; charset=utf-8")])
#     return [res_str]
#
#
# server = make_server(ip, port, application())
# server.serve_forever()


# # 可迭代对象
# class Application:
#     def __init__(self, envirno, start_response):
#         self.envirno = envirno
#         self.start_response = start_response
#
#     def __iter__(self):
#         self.start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8")])
#         yield res_str
#
#
# server = make_server(ip, port, Application)
# print(callable(Application))  # =>A(e, s)，实例用for迭代
# server.serve_forever()
#
#
# # 把类的实例当作可调用对象实现
# class Application:
#     def __call__(self, envirno, start_response):
#         print(envirno, type(envirno))
#         start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8")])
#         return [res_str]
#
#
# server = make_server(ip, port, Application())
# server.serve_forever()



