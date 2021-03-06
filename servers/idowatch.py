# -*- coding: utf-8 -*-
#------------------------------------------------------------
# streamondemand - XBMC Plugin
# Conector para idowatch
# http://www.mimediacenter.info/foro/viewforum.php?f=36
#------------------------------------------------------------

import re

from core import logger
from core import scrapertools
from lib import jsunpack


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    data = scrapertools.cache_page(page_url)
    if "File Not Found" in data:
        return False, "[Idowatch] Video non trovato"
    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)

    mediaurl = scrapertools.find_single_match(data, ',{file:(?:\s+|)"([^"]+)"')
    if not mediaurl:
        matches = scrapertools.find_single_match(data,
                                                 "<script type='text/javascript'>(eval\(function\(p,a,c,k,e,d.*?)</script>")
        matchjs = jsunpack.unpack(matches).replace("\\", "")
        mediaurl = scrapertools.find_single_match(matchjs, ',{file:(?:\s+|)"([^"]+)"')
    video_urls = []
    video_urls.append([scrapertools.get_filename_from_url(mediaurl)[-4:] + " [idowatch]", mediaurl])

    for video_url in video_urls:
        logger.info("pelisalacarta.servers.idowatch %s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://idowatch.net/m5k9s1g7il01.html
    patronvideos = 'idowatch.net/(?:embed-|)([a-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[idowatch]"
        url = "http://idowatch.net/%s.html" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'idowatch'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
