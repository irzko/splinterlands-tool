empty_line = "  │                                                                                                                  │"
end = "  └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘"
break_line = "  ├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤"
def header(tittle):
    t = " {0} ".format(tittle)
    p = t.center(114, '═')
    header = "\n  ╒" + p.format(tittle) + "╕"
    print(header)
    print(empty_line)
def make_empty_line(line):
    for i in range(0, line):
        print(empty_line)