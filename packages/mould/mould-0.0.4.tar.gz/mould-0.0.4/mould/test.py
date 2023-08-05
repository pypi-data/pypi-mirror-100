import mould

print(mould._syntax_check("text"))
variables = {"text": "World !", "marker": "Macbook Pro",
             "name": "Python", "n": 1, "x": 6, "y": 6, "d": {"a": 1, "b": 2}, "l": [1, 2, 3, 4, 5], "t": ("q", "w", "e", "r", "t", "y")}
op = mould.it("/Users/raam/Desktop/PyWorkspace/test", variables)
print(op.strip())
# a = '''!@#$%^&*();:'"'/''''''',./<>?\|'''
# if "'" in a:
# print(a)
# var = {
#     "a": 1,˜
#     "b": 2
# }

# var1 = [1, 2, 3]

# print(type(var))
# print(type(var1))

# if type(var) == dict:
#     print("type check works")
# else:
#     print("type check did not work")


# def escape_quot(string):
#     string
# n = 4
# print(n+*44)
# def tempp():
#     a = "tttt   ppp"
#     b = 50
#     # try:
#     if a:
#         print(a)
#     # except:
#         # print("this is the error")


# tempp()
