SELECT 
    x.*,
    COUNT(*) OVER () AS total_count
FROM
(
    SELECT lpc.*
    FROM liceo_projects_coordinators lpc
    WHERE lpc.project_id = ANY(:ids)
) as x