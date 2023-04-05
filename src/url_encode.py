def url_encode(s):
    """
    URL-encodes a string.
    """
    HEX_MAP = '0123456789ABCDEF'
    encoded_str = ''
    for char in s:
        if char.isalpha() or char.isdigit():
            encoded_str += char
        elif char == ' ':
            encoded_str += '+'
        elif ord(char) < 128: # ASCII character
            encoded_str += '%' + HEX_MAP[ord(char) // 16] + HEX_MAP[ord(char) % 16]
        else:
            # Non-ASCII character - encode as UTF-8 then convert to URL-encoded string
            utf8_bytes = char.encode('utf-8')
            for byte in utf8_bytes:
                encoded_str += '%' + HEX_MAP[byte // 16] + HEX_MAP[byte % 16]
    return encoded_str
