import json

data = {
    "topic": "qa4_lot_auction",
    "maxPartitions": 10,
    "event": {
        "@class": "com.copart.g2.acs.event.ycs.dto.SaleScheduleEventDTO",
        "id": "ASCH25",
        "correlationId": "G2-ASM-fac6b39e-62f7-43a4-b70b-fbd9734538ed",
        "eventType": "SaleScheduleModified",
        "eventCreateTime": 0,
        "countryGroupCode": "USPLUS",
        "userId": "aikamatapu",
        "eventStatus": "MESSAGE_PUSHED_TO_LOCAL_Q",
        "auctionHostId": 25
    },
    "gatewayMessagesSize": None,
    "solrInsertDocs": None,
    "solrUpdateDocs": None,
    "auctionBidSolrDocs": None,
    "bidHistorySolrDoc": None,
    "mdcMap": {
        "siteCode": None,
        "countryCode": "USA",
        "selectedSaleYardNumber": 25,
        "correlationId": "G2-ASM-fac6b39e-62f7-43a4-b70b-fbd9734538ed",
        "lang": "en",
        "userId": "aikamatapu",
        "countryGroupCode": "USPLUS",
        "skipAccessCheck": "N"
    }
}

json_string = json.dumps(data)
print(json_string)
