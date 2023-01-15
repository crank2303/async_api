from settings import settings
QUERY_PERSON = f"""
    SELECT 
        p.id,
        p.full_name,
        JSON_AGG(DISTINCT jsonb_build_object('id', fw.id, 'title', fw.title))
        FILTER(WHERE pfw.role = 'actor') AS actor_films,
        JSON_AGG(DISTINCT jsonb_build_object('id', fw.id, 'title', fw.title))
        FILTER(WHERE pfw.role = 'writer') AS writer_films, 
        JSON_AGG(DISTINCT jsonb_build_object('id', fw.id, 'title', fw.title))
        FILTER(WHERE pfw.role = 'director') AS director_films  
    FROM content.person p 
    LEFT JOIN content.person_film_work pfw  on pfw.person_id = p.id
    LEFT JOIN content.film_work fw  on fw.id = pfw.film_work_id 
    WHERE p.modified > (TIMESTAMP '%s')
    GROUP BY p.id
    ORDER BY p.modified
    LIMIT {settings.batch_size}
    OFFSET {settings.batch_size} * %d;
"""
