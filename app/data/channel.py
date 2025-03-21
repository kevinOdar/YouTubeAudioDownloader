import os
import sys

from model.channel import Channel
from model.video import Video

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
parent_dir = os.path.join(parent_dir, "..")
sys.path.insert(0, parent_dir)

from downloader import (
    get_videos_from_channel,
    download_audio_as_mp3,
    check_for_more_videos,
    set_driver,
    get_videos_from_channel_2,
    get_new_videos,
)

import iterator


class ChannelData:
    def __init__(self) -> None:
        self.videos_to_download = []
        self.i = 0

    def get_videos(self, channel: Channel):
        search = {
            "specific_word": "",
            "search_title": "",
            "channel_url": f"https://www.youtube.com/@{channel.channel_name}/videos",
        }
        return get_videos_from_channel(search)

    def download_videos(self, output_directory, show_message):
        for video in self.videos_to_download:
            try:
                download_audio_as_mp3(video, output_directory)
                show_message(f'"{video.title}" downloaded successfully')
            except Exception as e:
                show_message(str(e))

            print("-" * 50)

    def check_if_for_more_videos(self):
        return check_for_more_videos(self.i)

    def set_driver(self, channel: Channel):
        set_driver(f"https://www.youtube.com/@{channel.channel_name}/videos", 10)

    def get_videos2(self, channel: Channel):
        if self.i == 0:
            self.set_driver(channel)
        search = {
            "specific_word": "",
            "search_title": "",
            "channel_url": f"https://www.youtube.com/@{channel.channel_name}/videos",
        }

        video_element_list = get_new_videos(self.i)
        self.i += 1
        # for element in video_element_list:
        #     print(
        #         'Video("'
        #         + element.title
        #         + '", "'
        #         + element.url
        #         + '", "'
        #         + element.thumbnail_url
        #         + '"), '
        #     )

        # iteracion1 = [
        #     Video(
        #         "Meditation (Meditação) jazz version, Penelope Radsma & Bossa Nova Guitar",
        #         "https://www.youtube.com/watch?v=IK-JWV1wXKI",
        #         "https://i.ytimg.com/vi/IK-JWV1wXKI/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Samba do Avião - Bossa Nova Guitar Lesson #41: Bossa Nova Intro Phrase 4131",
        #         "https://www.youtube.com/watch?v=cipv3BTDjYU",
        #         "https://i.ytimg.com/vi/cipv3BTDjYU/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Carinhoso - Lúcia Helena Weiss & Bossa Nova Guitar",
        #         "https://www.youtube.com/watch?v=EbIeNd6nkwc",
        #         "https://i.ytimg.com/vi/EbIeNd6nkwc/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Este seu olhar - Marcele Berger & Bossa Nova Guitar",
        #         "https://www.youtube.com/watch?v=IPifSKy8xdk",
        #         "https://i.ytimg.com/vi/IPifSKy8xdk/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Caminhos Cruzados - Marcele Berger & Bossa Nova Guitar (w. English subtitles)",
        #         "https://www.youtube.com/watch?v=_6w1GTX0bns",
        #         "https://i.ytimg.com/vi/_6w1GTX0bns/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Bahia Com H - Bossa Nova Guitar Lesson #40: Intro Rhythmic Phrase 1113",
        #         "https://www.youtube.com/watch?v=lBJUcPx5LyY",
        #         "https://i.ytimg.com/vi/lBJUcPx5LyY/hqdefault.jpg",
        #     ),
        #     Video(
        #         "É Luxo Só - Bossa Nova Guitar Lesson #39: Fourth Basic Bossa Nova Phrase - 1321 (Partido Alto)",
        #         "https://www.youtube.com/watch?v=ftHIBM7hG_k",
        #         "https://i.ytimg.com/vi/ftHIBM7hG_k/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Eclipse -  Bossa Nova Guitar Lesson #38: Advanced Bossa Nova Rhythmic Phrase (1211)",
        #         "https://www.youtube.com/watch?v=CkViAYKXNCU",
        #         "https://i.ytimg.com/vi/CkViAYKXNCU/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Estate - Bossa Nova Guitar Lesson #37: Fourth Basic Bossa Nova Phrase Reversed Variation (2112)",
        #         "https://www.youtube.com/watch?v=mOz7KXiSMMw",
        #         "https://i.ytimg.com/vi/mOz7KXiSMMw/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Retrato em Branco e Preto - Bossa Nova Guitar Lesson #36: Bossa Nova Intro Phrases (0010 and 0112)",
        #         "https://www.youtube.com/watch?v=V_WNjtF06sI",
        #         "https://i.ytimg.com/vi/V_WNjtF06sI/hqdefault.jpg",
        #     ),
        #     Video(
        #         "S Wonderful - Bossa Nova Guitar Lesson #4: Basic Phrase Fully Syncopated (1313)",
        #         "https://www.youtube.com/watch?v=OjME5yYDAaA",
        #         "https://i.ytimg.com/vi/OjME5yYDAaA/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Chovendo na Roseira - Bossa Nova Guitar Lesson #35: Bossa Nova Swing",
        #         "https://www.youtube.com/watch?v=vV0MEheov0g",
        #         "https://i.ytimg.com/vi/vV0MEheov0g/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Sandália de Prata - Bossa Nova Guitar Lesson #34: Advanced Bossa Nova Rhythmic Phrase 0013",
        #         "https://www.youtube.com/watch?v=FOu5bdX9vJM",
        #         "https://i.ytimg.com/vi/FOu5bdX9vJM/hqdefault.jpg",
        #     ),
        #     Video(
        #         "De Conversa em Conversa - Bossa Nova Guitar Lesson #33: Second Basic Phrase Syncopated Reversed 3313",
        #         "https://www.youtube.com/watch?v=k-8LZ9VV8t4",
        #         "https://i.ytimg.com/vi/k-8LZ9VV8t4/hqdefault.jpg",
        #     ),
        #     Video(
        #         "A Primeira Vez - Bossa Nova Guitar Lesson #32: Advanced Rhythmic Phrase 4214",
        #         "https://www.youtube.com/watch?v=teyVZ6raN_Q",
        #         "https://i.ytimg.com/vi/teyVZ6raN_Q/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Pra Dizer Adeus - Bossa Nova Guitar Lesson #31: Advanced Rhythmic Phrase 1200",
        #         "https://www.youtube.com/watch?v=Ku9jHIOqbwg",
        #         "https://i.ytimg.com/vi/Ku9jHIOqbwg/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Ave Maria no Morro - Bossa Nova Guitar Lesson #30: Advanced Rhythmic Phrase 4413",
        #         "https://www.youtube.com/watch?v=AV5pPQaPpPE",
        #         "https://i.ytimg.com/vi/AV5pPQaPpPE/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Pra Que Discutir com Madame - Bossa Nova Guitar Lesson #29: Fourth Basic Phrase Variation 1331",
        #         "https://www.youtube.com/watch?v=0OUMHGOQMnA",
        #         "https://i.ytimg.com/vi/0OUMHGOQMnA/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Só Tinha de Ser Com Você - Bossa Nova Guitar Lesson #28: Advanced Rhythmic Phrase 1318",
        #         "https://www.youtube.com/watch?v=q5qi5EMDEXU",
        #         "https://i.ytimg.com/vi/q5qi5EMDEXU/hqdefault.jpg",
        #     ),
        #     Video(
        #         "'S Wonderful - Hannah Montenegro & Bossa Nova Guitar",
        #         "https://www.youtube.com/watch?v=KvQrznJE18c",
        #         "https://i.ytimg.com/vi/KvQrznJE18c/hqdefault.jpg",
        #     ),
        #     Video(
        #         "O Barquinho - Bossa Nova Guitar Lesson #27: Advanced Rhythmic Phrase 7333",
        #         "https://www.youtube.com/watch?v=FHzbikl-0hU",
        #         "https://i.ytimg.com/vi/FHzbikl-0hU/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Vivo Sonhando - Bossa Nova Guitar Lesson #26: Second Basic Rhythmic Phrase Syncopated and Reversed",
        #         "https://www.youtube.com/watch?v=ZWg6eUjL0Jc",
        #         "https://i.ytimg.com/vi/ZWg6eUjL0Jc/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Linda Flor - Bossa Nova Guitar Lesson #25: Advanced Phrase 0000",
        #         "https://www.youtube.com/watch?v=H-QNBbAaSBo",
        #         "https://i.ytimg.com/vi/H-QNBbAaSBo/hqdefault.jpg",
        #     ),
        #     Video(
        #         "O Amor Em Paz -  Bossa Nova Guitar Lesson #24: Third Basic Phrase Variation Fully Syncopated",
        #         "https://www.youtube.com/watch?v=KscK06Tkyd0",
        #         "https://i.ytimg.com/vi/KscK06Tkyd0/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Besame Mucho - Bossa Nova Guitar Lesson #23: Advanced Phrase 1222",
        #         "https://www.youtube.com/watch?v=cFMxl0rnC74",
        #         "https://i.ytimg.com/vi/cFMxl0rnC74/hqdefault.jpg",
        #     ),
        #     Video(
        #         "O Grande Amor - Bossa Nova Guitar Lesson #3: Basic Phrase Syncopated Reversed 1312",
        #         "https://www.youtube.com/watch?v=BtkT2oPrRAw",
        #         "https://i.ytimg.com/vi/BtkT2oPrRAw/hqdefault.jpg",
        #     ),
        #     Video(
        #         "O Pato - Bossa Nova Guitar Lesson #22: Advanced Phrase 7xxx",
        #         "https://www.youtube.com/watch?v=j9CClyBEkeI",
        #         "https://i.ytimg.com/vi/j9CClyBEkeI/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Outra Vez - Bossa Nova Guitar Lesson #21: Ghost Notes",
        #         "https://www.youtube.com/watch?v=NvzNxodR5ts",
        #         "https://i.ytimg.com/vi/NvzNxodR5ts/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Meditação (Meditation) - Bossa Nova Guitar Lesson #9: Third Basic Phrase Syncopated",
        #         "https://www.youtube.com/watch?v=qV08ny7HWQE",
        #         "https://i.ytimg.com/vi/qV08ny7HWQE/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Doralice - Bossa Nova Guitar Lesson #20: Advanced Phrase 1232",
        #         "https://www.youtube.com/watch?v=Al08qcJ9AVw",
        #         "https://i.ytimg.com/vi/Al08qcJ9AVw/hqdefault.jpg",
        #     ),
        # ]
        # iteracion2 = [
        #     Video(
        #         "Águas de Março (Waters of March) - Bossa Nova Guitar Lesson #19: Advanced Phrase 3333",
        #         "https://www.youtube.com/watch?v=TC4rTK5h6O8",
        #         "https://i.ytimg.com/vi/TC4rTK5h6O8/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Água de Beber (Water to Drink) - Bossa Nova Guitar Lesson #17: Advanced Phrase 3233",
        #         "https://www.youtube.com/watch?v=fZHnBkqgoHU",
        #         "https://i.ytimg.com/vi/fZHnBkqgoHU/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Aquarela do Brasil (Brazil) - Bossa Nova Guitar Lesson #16: Partido Alto Phrase Variation",
        #         "https://www.youtube.com/watch?v=VNFr9yau_4Y",
        #         "https://i.ytimg.com/vi/VNFr9yau_4Y/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Desafinado (Off Key) - Bossa Nova Guitar Lesson #12: Advanced Phrase 4444",
        #         "https://www.youtube.com/watch?v=Ky6eHa2jrOU",
        #         "https://i.ytimg.com/vi/Ky6eHa2jrOU/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Wave - Bossa Nova Guitar Lesson #18: Advanced Phrase 137x",
        #         "https://www.youtube.com/watch?v=-KvhDcZu0FI",
        #         "https://i.ytimg.com/vi/-KvhDcZu0FI/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Triste - Bossa Nova Guitar Lesson #15: Advanced Phrase 4x3x/3x4x",
        #         "https://www.youtube.com/watch?v=RshWioRtqCc",
        #         "https://i.ytimg.com/vi/RshWioRtqCc/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Samba de Uma Nota So (One Note Samba) - Bossa Nova Guitar Lesson #14: Advanced Phrase 4x44/444x",
        #         "https://www.youtube.com/watch?v=aiOPYXW8iA8",
        #         "https://i.ytimg.com/vi/aiOPYXW8iA8/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Chega de Saudade - Bossa Nova Guitar Lesson #11: Partido Alto Phrase",
        #         "https://www.youtube.com/watch?v=9lTOz3GuMeQ",
        #         "https://i.ytimg.com/vi/9lTOz3GuMeQ/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Garota de Ipanema (The Girl From Ipanema) - Bossa Nova Guitar Lesson #13: Musical Articulation",
        #         "https://www.youtube.com/watch?v=-e784DvyRMs",
        #         "https://i.ytimg.com/vi/-e784DvyRMs/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Aos Pés Da Cruz - Bossa Nova Guitar Lesson #9: Third Basic Phrase Syncopated",
        #         "https://www.youtube.com/watch?v=-OMH1dzrzng",
        #         "https://i.ytimg.com/vi/-OMH1dzrzng/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Insensatez (How Insensitive) - Bossa Nova Guitar Lesson #1: Basic Phrase",
        #         "https://www.youtube.com/watch?v=m1KZ5ElJLAg",
        #         "https://i.ytimg.com/vi/m1KZ5ElJLAg/hqdefault.jpg",
        #     ),
        #     Video(
        #         "A Felicidade - Bossa Nova Guitar Lessons #7 and #8: Third Basic Phrase",
        #         "https://www.youtube.com/watch?v=v1oxAdZmyHY",
        #         "https://i.ytimg.com/vi/v1oxAdZmyHY/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Samba da Minha Terra - Bossa Nova Guitar Lesson #6: Second Basic Phrase Variation",
        #         "https://www.youtube.com/watch?v=aW2hJ9ZUQjQ",
        #         "https://i.ytimg.com/vi/aW2hJ9ZUQjQ/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Este Seu Olhar - Bossa Nova Guitar Lesson #10: Third Basic Phrase Variation Syncopated",
        #         "https://www.youtube.com/watch?v=1WAMsfiJh1k",
        #         "https://i.ytimg.com/vi/1WAMsfiJh1k/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Corcovado (Quiet Nights of Quiet Stars) - Bossa Nova Guitar Lesson #2: Basic Phrase Syncopated",
        #         "https://www.youtube.com/watch?v=9fEUpmLf7TM",
        #         "https://i.ytimg.com/vi/9fEUpmLf7TM/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Pra Machucar Meu Coração - Bossa Nova Guitar Lesson #3: Basic Phrase Syncopated Reversed",
        #         "https://www.youtube.com/watch?v=BhFmyca_dxY",
        #         "https://i.ytimg.com/vi/BhFmyca_dxY/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Só Danço Samba - Bossa Nova Guitar Lesson #4: Basic Phrase Fully Syncopated",
        #         "https://www.youtube.com/watch?v=boCI-NHYAHA",
        #         "https://i.ytimg.com/vi/boCI-NHYAHA/hqdefault.jpg",
        #     ),
        #     Video(
        #         "Bim Bom - Bossa Nova Guitar Lesson #5: Second Basic Phrase",
        #         "https://www.youtube.com/watch?v=At1SdglKLbs",
        #         "https://i.ytimg.com/vi/At1SdglKLbs/hqdefault.jpg",
        #     ),
        # ]

        # if self.i == 1:
        #     return iteracion1
        # else:
        #     return iteracion2
        return video_element_list
