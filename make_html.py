import os

template_start = """                        
<h2 align='right' class='rh'>{header}&nbsp;&nbsp;{date_formated}</h2>
<div style="float:left;margin:0 10px;">
<a href="images/{date}/{pict_main}" rel='iLoad|{header}' title=""><img src="images/{date}/{pict_main}" width='150' vspace="5" hspace='5'></a>
</div>
<p align='justify' valign='top' style="font-size:1.1em;">
{text}
</p>
<p align='right'><a href="#" onclick="$('#{date}').toggleClass('hide');return false;" align='center'>Фотоотчет</a></p>
<div class="hide" id="{date}">
"""
template_list = """<a href="images/{date}/{pict}" rel='iLoad|{header}' title=""><img src="images/{date}/{pict}" width='100' vspace="5" hspace='5'></a>
"""
template_video = """<video controls="controls"><source src="images/{date}/{pict}"></video>
"""
video_ext = ('.mp4', '.ogg', '.webm')
template_end = """</div>
<hr>
"""
path_list = ('taxi', 'othere')
images = 'images'

for path in path_list:
    for file in os.listdir(path):
        with open(os.path.join(path, file), 'r', encoding='utf8') as file_r:
            text = ''
            for i, line in enumerate(file_r.readlines()):
                if i == 0:
                    header = line.rstrip()
                else:
                    text += f'{line}<br>'
        date = file
        date_formated = f'{date[:2]}/{date[2:4]}/{date[4:]}'
        pict_list = os.listdir(os.path.join(images, date))
        if len(pict_list) == 0:
            raise Exception
        html = template_start.format(
            header=header, date_formated=date_formated, date=date, pict_main=pict_list[0], text=text)
        for pict in pict_list[1:]:
            if pict[pict.rfind('.'):] in video_ext:
                html += template_video.format(pict=pict, date=date)
            else:
                html += template_list.format(pict=pict, date=date, header=header)
        html += template_end
        with open(f'{path}_new.html', 'a', encoding='utf8') as file_w:
            print(html, file=file_w)
