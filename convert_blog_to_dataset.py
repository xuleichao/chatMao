import json
import os
import fitz

# 输入博客文件路径、输出目录路径、对话者名称和最大文本长度
def convert_blog_to_dialogue(filename, output_dir, speaker_name, max_length):
    # 读取博客文件内容
    blog_text = ''
    f = fitz.open(filename)
    for page in f:
        text = page.get_text()
        blog_text += text

    # 将博客内容分解为多个段落部分
    blog_segments = blog_text.split('。')

    # 将博客转换为对话记录
    dialogue = []
    for segment in blog_segments:
        # 将每个段落分解为多个句子
        sentences = segment.split('。')
        for sentence in sentences:
            # 将每个句子加入对话记录
            sentence = clean_text(sentence)
            if sentence:
                dialogue.append((speaker_name, sentence))

    # 将对话记录分割成多个对话长度最大为"max_length"的段落
    dialogue_segments = split_dialogue_into_segments(dialogue, max_length)

    # 对于每个对话段落，创建一个文本文件
    f=  open('mao_xuanji.json', 'w', encoding='utf-8')
    res = []
    for i, segment in enumerate(dialogue_segments):
        segment_filename = os.path.join(output_dir, '{}.txt'.format(i))


        last = "主席您好，我们来探讨一下中国革命史"
        for speaker, sentence in segment:
            # f.write('<{}> {}\n'.format(speaker, sentence))

            info = {
                "instruction": last,
                "input": "",
                "output": sentence
            }
            last = sentence
            res.append(info)
    f.write(json.dumps(res, ensure_ascii=False, indent=3))

# 去除HTML标签和特殊字符
def clean_text(text):
    # 暂时省略实现
    text = text.replace("\n", "")
    return text

# 将对话记录按照"max_length"的长度分割成多个段落，保留段落结构
def split_dialogue_into_segments(dialogue, max_length):
    segments = []
    current_segment = []
    current_length = 0

    for speaker, sentence in dialogue:
        # 如果当前对话段落中的文本长度超过了 max_length，就将其保存并开始新的段落
        if current_length + len(sentence) > max_length:
            segments.append(current_segment)
            current_segment = []
            current_length = 0

        current_segment.append((speaker, sentence))
        current_length += len(sentence)

    # 如果还有剩余的对话记录没有保存，就将其作为最后一个段落保存
    if current_segment:
        segments.append(current_segment)

    return segments


# 指定输入文件路径、输出目录路径、对话者名称和最大文本长度
filename = r"F:\xlcFiles\Read\毛选\毛泽东选集.mobi"
output_dir = './output/'
speaker_name = '毛泽东'
max_length = 512

# 转化为对话记录
convert_blog_to_dialogue(filename, output_dir, speaker_name, max_length)
