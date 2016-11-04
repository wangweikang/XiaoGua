def f1(arg1, arg2, arg3=1, arg4=2, *args, **kwargs):
    print(arg1, arg2)
    print(args)
    print(arg3, arg4)

    print(kwargs)


f1(1, 2, 3, 4, 5, 6, 7, 8, a=9)
