def text_to_block(rest):
    text_blocks = []
    while (len(rest) > 1100):
        begin = 0
        end = rest.find(".", 1000)

        if (end == -1):
            end = rest.find(" ", 1000)

        text_blocks = rest[begin:end]
        rest = rest[end:]
        text_blocks.append(text_blocks)
    
    text_blocks.append(rest)
    return text_blocks