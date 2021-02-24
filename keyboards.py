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
fgbKB =  {
    'one_time': True,
    'buttons':
    [
        [
            {
                "action":
                    {
                        "type":"text",
                        "payload": "{\"mainMenu\":\"fuck_go_back\"}",
                        "label": "Назад"
                    },
                "color": "secondary"
            }
        ] 
    ]
}
undKB =  {
    'one_time': True,
    'buttons':
    [
        [
            {
                "action":
                    {
                        "type":"text",
                        "payload": "{\"mainMenu\":\"undo\"}",
                        "label": "Отменить запись"
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
                        "label": "Записаться"
                    },
                "color": "positive"
            }
        ]  
    ]
}
undoKB = json.dumps(undKB)
fuck_go_backKB = json.dumps(fgbKB)
beginKb = json.dumps(bKb)
confKB = json.dumps(mKB)