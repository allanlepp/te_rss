#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Kuma RSS-voo sisendite parsimine
"""

from lxml import html
import parsers_common


def getArticleListsFromHtml(htmlPage, domain, maxPageURLstoVisit):
    """
    Meetod uudistesaidi kõigi uudiste nimekirja loomiseks
    """
    # parandame untsuläinud tähtede kodeerimise
    htmlPage = parsers_common.fixBrokenUTF8asEncoding(htmlPage, 'iso8859_15')

    tree = html.fromstring(htmlPage)

    articleDescriptions = tree.xpath('//div[@class="news-list-item-wrapper"]/div[@class="news-list-item-excerpt"]/p/text()')
    articleIds = []
    articleImages = tree.xpath('//div[@class="news-list-media"]/img/@src')
    articleImages = [domain + elem for elem in articleImages]
    articlePubDates = []
    articleTitles = tree.xpath('//div[@class="news-list-item-wrapper"]/h3/a/text()')
    articleUrls = tree.xpath('//div[@class="news-list-item-wrapper"]/h3/a/@href')
    articleUrls = [domain + elem for elem in articleUrls]

    articlePubDay = tree.xpath('//div[@class="news-list-item-wrapper"]/div[@class="news-list-item-date"]/text()[1]')
    articlePubMonth = tree.xpath('//div[@class="news-list-item-wrapper"]/div[@class="news-list-item-date"]/span[@class="month"]/text()')
    articlePubYear = tree.xpath('//div[@class="news-list-item-wrapper"]/div[@class="news-list-item-date"]/text()[2]')

    get_article_bodies = True

    for i in range(0, len(articleUrls)):
        articleUrl = articleUrls[i]

        # generate unical id from ArticleUrl
        articleIds.append(parsers_common.urlToHash(articleUrl))

        if (get_article_bodies is True and i < maxPageURLstoVisit):
            # load article into tree
            articleTree = parsers_common.getArticleData(articleUrl)

            # descriptions
            articleDescriptionsParent = parsers_common.treeExtract(articleTree, '//div[@class="news-single-item"]/div[@class="news-single-content"]')  # as a parent
            articleDescriptionsChilds = parsers_common.stringify_children(articleDescriptionsParent)
            articleDescriptions[i] = articleDescriptionsChilds

            # timeformat magic from "13 dets  17" to datetime()
            curArtPubDate = parsers_common.treeExtract(articleTree, '//div[@class="news-single-timedata"]/text()')
            curArtPubDate = parsers_common.shortMonthsToNumber(curArtPubDate)
            curArtPubDate = parsers_common.rawToDatetime(curArtPubDate, "%d %m %y")
            articlePubDates.append(curArtPubDate)
        else:
            if i < len(articlePubYear) and (int(articlePubYear[i].strip()) > 2016):
                curYear = articlePubYear[i].strip()
            curArtPubDate = articlePubDay[i].strip() + " " + articlePubMonth[i].strip() + " " + curYear
            curArtPubDate = parsers_common.rawToDatetime(curArtPubDate, "%d %m %Y")
            articlePubDates.append(curArtPubDate)

    return {"articleDescriptions": articleDescriptions,
            "articleImages": articleImages,
            "articleIds": articleIds,
            "articlePubDates": articlePubDates,
            "articleTitles": articleTitles,
            "articleUrls": articleUrls,
           }