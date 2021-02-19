import json


mKB = {
    'one_time': True,
    'buttons':
    [
        [
            {
                "action":
                    {
                        "type":"text",
                        "payload": "{\"mainMenu\":\"new_date\"}",
                        "label": "Нужной даты нет в списке"
                    },
                "color": "secondary"
            }
        ] 
    ]
}
bKb = {
   'one_time': True,
    'buttons':
    [
        [
            {
                "action":
                    {
                        "type":"text",
                        "payload": "{\"command\":\"start\"}",
                        "label": "Начать"
                    },
                "color": "positive"
            }
        ]  
    ]
}
beginKb = json.dumps(bKb)
confKB = json.dumps(mKB)