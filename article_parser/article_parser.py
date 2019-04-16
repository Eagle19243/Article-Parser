import json
from html.parser import HTMLParser


class ImageParser(HTMLParser):
    def __init__(self, body):
        self.body = body
        self.result = ""
        self.looking_for_caption = False
        self.open_caption = False
        self.last_pos = 0
        self.depth = 0
        self.line_offset = [0, 0]
        for i, c in enumerate(self.body):
            if c == '\n':
                self.line_offset.append(i + 1)  # + 1 to skip the '\n' char
        super().__init__()

    def run(self):
        self.feed(self.body)
        self.result = self.result.format(caption='')
        self.result += self.body[self.last_pos:]

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self.looking_for_caption = True
            self.open_caption = False
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
        elif self.looking_for_caption:
            self.looking_for_caption = False
            self.open_caption = True
            self.depth = 1
        elif self.open_caption:
            self.depth += 1

    def handle_endtag(self, tag):
        if self.looking_for_caption:
            self.result += '</{}>'.format(tag)
            self.last_pos += len(tag) + 3
        if self.open_caption:
            self.depth -= 1
            if self.depth == 0:
                line, offset = self.getpos()
                current_pos = self.line_offset[line] + offset
                self.last_pos = current_pos + len(tag) + 3
                self.open_caption = False

    def handle_data(self, data):
        if self.open_caption:
            caption = '<p class="caption">{}</p>'.format(data)
            self.result = self.result.format(caption=caption)


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
        json.dump(data, foutput, indent=4, sort_keys=True)


if __name__ == '__main__':
    transform('tests/input.json', 'tests/output.json')
