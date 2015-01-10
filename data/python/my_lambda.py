def my_func(s):
    return s.lower()


def main():
    li = ['aladar', 'ALMA', 'akarki', 'AhA']
    print sorted(li)                             # ['ALMA', 'AhA', 'akarki', 'aladar']
    print sorted(li, key=my_func)                # ['AhA', 'akarki', 'aladar', 'ALMA']
    print sorted(li, key=lambda s: s.lower())    # ['AhA', 'akarki', 'aladar', 'ALMA']
