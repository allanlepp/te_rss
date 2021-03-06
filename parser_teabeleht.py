#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Teabeleht RSS-voo sisendite parsimine
"""

import makereq
import parsers_common


def getArticleListsFromHtml(pageTree, domain, maxPageURLstoVisit):
    """
    Meetod uudistesaidi kõigi uudiste nimekirja loomiseks
    """

    articleDescriptions = pageTree.xpath('//div[@id="nsp-nsp-234"]//div[@class="nspArt nspCol1"]/div[@class="gkArtContentWrap"]/p[1]/text()')
    articleIds = []
    articleImages = pageTree.xpath('//div[@id="nsp-nsp-234"]//div[@class="nspArt nspCol1"]/a/img/@src')
    articlePubDates = []
    articleTitles = pageTree.xpath('//div[@id="nsp-nsp-234"]//div[@class="nspArt nspCol1"]/div[@class="gkArtContentWrap"]/h4/a/text()')
    articleUrls = pageTree.xpath('//div[@id="nsp-nsp-234"]//div[@class="nspArt nspCol1"]/div[@class="gkArtContentWrap"]/h4/a/@href')
    articleUrls = parsers_common.domainUrls(domain, articleUrls)

    # todo(reading times from articles is BROKEN and maybe useless too)
    get_article_bodies = False

    for i in range(0, len(articleUrls)):
        articleUrl = articleUrls[i]

        # generate unique id from articleUrl
        articleIds.append(parsers_common.urlToHash(articleUrl))

        if (get_article_bodies is True and i < maxPageURLstoVisit):
            # load article into tree
            articleTree = makereq.getArticleData(articleUrl)

            # timeformat magic from "Avaldatud: Neljapäev, 14 Detsember 2017 12:46" to datetime()
            # curArtPubDate = parsers_common.treeExtract(articleTree, '//div[@class="kakk-postheadericons kakk-metadata-icons"]/span/::before/text()')  # katki
            curArtPubDate = parsers_common.treeExtract(articleTree, '//span[@class="kakk-postdateicon"]//text()')
            curArtPubDate = parsers_common.longMonthsToNumber(curArtPubDate.split(',')[1])
            curArtPubDate = parsers_common.rawToDatetime(curArtPubDate, "%d %m %Y %H:%M")
            articlePubDates.append(curArtPubDate)

    return {"articleDescriptions": articleDescriptions,
            "articleIds": articleIds,
            "articleImages": articleImages,
            "articlePubDates": articlePubDates,
            "articleTitles": articleTitles,
            "articleUrls": articleUrls,
           }
