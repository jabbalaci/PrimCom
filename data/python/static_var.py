def name_generator():
    if not hasattr(name_generator, "cnt"):
        name_generator.cnt = 0    # it doesn't exist yet, so initialize it
    #
    result = "name-{cnt}".format(cnt=name_generator.cnt)
    name_generator.cnt += 1
    return result


for _ in range(3):
    print name_generator()
# name-0
# name-1
# name-2
