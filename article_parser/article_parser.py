import json
from html.parser import HTMLParser


class ImageParser(HTMLParser):
    def __init__(self, body):
        self.body = body
        self.result = ""
        self.looking_for_caption = False
        self.open_caption = False
        self.caption_data = ""
        self.last_pos = 0
        self.line_offset = [0, 0]
        for i, c in enumerate(self.body):
            if c == '\n':
                self.line_offset.append(i)
        super().__init__()

    def run(self):
        self.feed(self.body)
        self.result = self.result.format(caption='')
        self.result += self.body[self.last_pos:]

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self.looking_for_caption = True
            self.open_caption = False
            self.caption_data = ""
            alt = None
            line, offset = self.getpos()
            current_pos = self.line_offset[line] + offset
            self.result.format(caption='')
            self.result += self.body[self.last_pos: current_pos]
            self.last_pos = current_pos + len(self.get_starttag_text())
            for key, value in attrs:
                if key == 'alt':
                    alt = value
                if key == 'src':
                    src = value
            self.result += (
                '<div class="image">'
                '<img alt="{}" src="{}"/>{{caption}}'
                '</div>'.format(
                    alt, src
                )
            )
        elif tag == 'p':
            if self.looking_for_caption:
                self.looking_for_caption = False
                self.open_caption = True
        else:
            if self.looking_for_caption and not self.open_caption:
                self.looking_for_caption = False

    def handle_endtag(self, tag):
        if tag == 'p':
            if self.open_caption:
                line, offset = self.getpos()
                current_pos = self.line_offset[line] + offset
                self.last_pos = current_pos + 4 + 1  # len('</p>') == 4
                caption = '<p class="caption">{}</p>'.format(self.caption_data)
                self.result = self.result.format(caption=caption)
                self.open_caption = False

    def handle_data(self, data):
        if self.open_caption:
            self.caption_data += data


def parse_one(body):
    parser = ImageParser(body)
    parser.run()
    return parser.result


def parse(file_path):
    with open(file_path, 'r') as finput:
        data = json.load(finput)
        for item in data['objects']:
            item['post_body'] = parse_one(item['post_body'])
    return data


def transform(input_file_path, output_file_path):
    with open(output_file_path, 'w') as foutput:
        data = parse(input_file_path)
        json.dump(data, foutput, indent=4)


if __name__ == '__main__':
    transform('tests/input.json', 'tests/output.json')
