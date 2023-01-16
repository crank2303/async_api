from settings import settings
QUERY_PERSON = f"""
    SELECT 
        p.id,
        p.full_name,
        pfw.role,
        JSON_AGG(DISTINCT fw.id) 
    FROM content.person p 
    LEFT JOIN content.person_film_work pfw  on pfw.person_id = p.id
    LEFT JOIN content.film_work fw  on fw.id = pfw.film_work_id 
    WHERE p.modified > (TIMESTAMP '%s')
    GROUP BY p.id, pfw.role
    ORDER BY p.modified
    LIMIT {settings.batch_size}
    OFFSET {settings.batch_size} * %d;
"""
