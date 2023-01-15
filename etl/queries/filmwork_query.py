from settings import settings
QUERY_FILMWORK = f"""
    SELECT
        fw.id,
        fw.title,
        fw.description,
        fw.rating,
        fw.type,
        fw.created,
        fw.modified,
        fw.mpaa_rating,
        JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
        FILTER(WHERE pfw.role = 'director') AS director,
        JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
        FILTER(WHERE pfw.role = 'actor') AS actors,
        JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
        FILTER(WHERE pfw.role = 'writer') AS writers,
        JSON_AGG(DISTINCT jsonb_build_object('name', g.name, 'id', g.id)) AS genres
    FROM content.film_work fw
    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
    LEFT JOIN content.person p ON p.id = pfw.person_id
    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
    LEFT JOIN content.genre g ON g.id = gfw.genre_id
    WHERE GREATEST (fw.modified, p.modified, g.modified) > '%s'
    GROUP BY fw.id
    ORDER BY fw.modified
    LIMIT {settings.batch_size}
    OFFSET {settings.batch_size} * %d;
"""
