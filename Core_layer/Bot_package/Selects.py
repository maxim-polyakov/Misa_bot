class Select:
    SELECT_TH = str('(select text, thanks FROM train_sets.all_set_thanks WHERE (thanks=1) ORDER BY random() LIMIT 3000) ' +
             'union all'
             '(select text, thanks FROM train_sets.all_set_none WHERE (thanks=0) ORDER BY random() LIMIT 2000)' +
             'union all' +
             '(select text, thanks FROM train_sets.all_set_hi WHERE (thanks=0) ORDER BY random() LIMIT 500)' +
             'union all' +
             '(select text, thanks FROM train_sets.all_set_business WHERE (thanks=0) ORDER BY random() LIMIT 500)' +
             'union all' +
             '(select text, thanks FROM train_sets.all_set_weather WHERE (thanks=0) ORDER BY random() LIMIT 500)' +
             'union all' +
             '(select text, thanks FROM train_sets.all_set_trash WHERE (thanks=0) ORDER BY random() LIMIT 500)')

    SELECT_TRASH = str('(select text, trash FROM train_sets.all_set_trash WHERE (trash=1) ORDER BY random() LIMIT 366) ' +
             'union all'
             '(select text, trash FROM train_sets.all_set_none WHERE (trash=0) ORDER BY random() LIMIT 200)' +
             'union all' +
             '(select text, trash FROM train_sets.all_set_hi WHERE (trash=0) ORDER BY random() LIMIT 50)' +
             'union all' +
             '(select text, trash FROM train_sets.all_set_business WHERE (trash=0) ORDER BY random() LIMIT 50)' +
             'union all' +
             '(select text, trash FROM train_sets.all_set_weather WHERE (trash=0) ORDER BY random() LIMIT 50)' +
             'union all' +
             '(select text, trash FROM train_sets.all_set_thanks WHERE (trash=0) ORDER BY random() LIMIT 50)')

    SELECT_HI = str('(select text, hi FROM train_sets.all_set_hi WHERE (hi=1) ORDER BY random() LIMIT 3000)' +
            'union all' +
            '(select text, hi FROM train_sets.all_set_none WHERE (hi=0) ORDER BY random() LIMIT 2000)' +
            'union all' +
            '(select text, hi FROM train_sets.all_set_thanks WHERE (hi=0) ORDER BY random() LIMIT 500)' +
            'union all' +
            '(select text, hi FROM train_sets.all_set_business WHERE (hi=0) ORDER BY random() LIMIT 500)' +
            'union all' +
            '(select text, hi FROM train_sets.all_set_weather WHERE (hi=0) ORDER BY random() LIMIT 500)'
            'union all' +
            '(select text, hi FROM train_sets.all_set_trash WHERE (hi=0) ORDER BY random() LIMIT 500)')

    SELECT_BUSINESS = str('(select text, business FROM train_sets.all_set_business WHERE (business=1) ORDER BY random() LIMIT 3000)'+
                   'union all' +
                   '(select text, business FROM train_sets.all_set_none WHERE (business=0) ORDER BY random() LIMIT 2000)' +
                   'union all' +
                   '(select text, business FROM train_sets.all_set_thanks WHERE (business=0) ORDER BY random() LIMIT 500)' +
                   'union all' +
                   '(select text, business FROM train_sets.all_set_hi WHERE (business=0) ORDER BY random() LIMIT 500)' +
                   'union all' +
                   '(select text, business FROM train_sets.all_set_weather WHERE (business=0) ORDER BY random() LIMIT 500)'
                   'union all' +
                   '(select text, business FROM train_sets.all_set_trash WHERE (business=0) ORDER BY random() LIMIT 500)')

    SELECT_WEATHER = str('(select text, weather  FROM train_sets.all_set_weather WHERE (weather =1) ORDER BY random() LIMIT 3000)' +
                  'union all' +
                  '(select text, weather FROM train_sets.all_set_none WHERE (weather=0) ORDER BY random() LIMIT 2000)' +
                  'union all' +
                  '(select text, weather FROM train_sets.all_set_thanks WHERE (weather=0) ORDER BY random() LIMIT 500)' +
                  'union all' +
                  '(select text, weather FROM train_sets.all_set_hi WHERE (weather=0) ORDER BY random() LIMIT 500)' +
                  'union all' +
                  '(select text, weather FROM train_sets.all_set_business WHERE (weather=0) ORDER BY random() LIMIT 500)'
                  'union all' +
                  '(select text, weather FROM train_sets.all_set_trash WHERE (weather=0) ORDER BY random() LIMIT 500)')

    SELECT_EMOTIONS = str('(select text, emotionid  FROM train_sets.all_set_weather ORDER BY random() LIMIT 3000)' +
                          'union all' +
                          '(select text, emotionid FROM train_sets.all_set_none ORDER BY random() limit 500)' +
                          'union all' +
                          '(select text, emotionid FROM train_sets.all_set_thanks order by random() LIMIT 500)' +
                          'union all' +
                          '(select text, emotionid FROM train_sets.all_set_hi order by random() limit 500)' +
                          'union all' +
                          '(select text, emotionid  FROM train_sets.all_set_business order by random() limit 500)' +
                          'union all' +
                          '(select text, emotionid  FROM train_sets.all_set_trash order by random() limit 500)')
