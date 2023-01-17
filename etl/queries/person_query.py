from settings import settings


QUERY = f"""
    SELECT 
        p.id,
        p.full_name,
        coalesce (
	        jsonb_agg(distinct fw.id) filter (where pfw.role = 'actor'),'[]') as film_id_actor,
        coalesce (
	        jsonb_agg(distinct fw.id) filter (where pfw.role = 'writer'),'[]') as film_id_writer,
        coalesce (
	        jsonb_agg(distinct fw.id) filter (where pfw.role = 'director'),'[]') as film_id_director 
    FROM content.person p 
    LEFT JOIN "content".person_film_work pfw  on pfw.person_id = p.id
    LEFT JOIN "content".film_work fw  on fw.id = pfw.film_work_id 
    WHERE GREATEST (fw.modified, p.modified) > (TIMESTAMP '%s')
    GROUP BY p.id 
    ORDER BY p.modified
    LIMIT {settings.batch_size}
    OFFSET {settings.batch_size} * %d;
"""
