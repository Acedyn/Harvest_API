-- Get the computation time per frames per blades per project
SELECT
computer, project, TRUNC(AVG(frametime)) AS frametime
FROM
    -- Get the blade that computed that task and the time per frames
    (SELECT
    DISTINCT ON (metadata.jid, metadata.tid, metadata.project)
    metadata.project,
    substring(upper(blade.name) from 'MK\d') AS computer,
    invocation.elapsedreal / metadata.frames AS frametime, invocation.elapsedreal, metadata.frames
    FROM
        -- Get the parsed metadata content and compute the amount of frames in each task
        (SELECT 
        jid, tid, state,
        job_metadata->>'project' AS project, job_metadata->>'renderState' AS category,
        array_length(string_to_array(regexp_replace(task_metadata->>'frames', '[\[\]\s\.]', '', 'g'), ',', '')::int[], 1) AS frames
        FROM
            -- Get the parsed metadata
            (SELECT 
                task.jid, task.tid, job.metadata::json AS job_metadata, task.metadata::json AS task_metadata, task.state
                FROM job, task 
                WHERE is_valid_json(job.metadata) AND is_valid_json(task.metadata) AND task.jid = job.jid LIMIT 10000000) AS taskData 
        WHERE state = 'done' AND job_metadata->>'project' != 'TEST_PIPE' AND job_metadata->>'renderState' = 'final') AS metadata, invocation, blade
    WHERE metadata.jid = invocation.jid AND metadata.tid = invocation.tid AND blade.bladeid = invocation.bladeid) AS computationstat
GROUP BY computer, project
ORDER BY project, computer