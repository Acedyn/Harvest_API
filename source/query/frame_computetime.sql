-- Get the computation time per frames per blades per project
SELECT
computer, owner, AVG(frametime) AS frametime
FROM
    -- Get the blade that computed that task
    (SELECT 
    DISTINCT ON (task.jid, task.tid) substring(upper(blade.name) from '(?<=-MK).*(?=-[\d]{4})')::int AS index, substring(upper(blade.name) from '(?<=-).*(?=-[\d]{4})') AS computer, task.*, invocation.elapsedreal / task.frames AS frametime
    FROM
        -- Get the time it took to complete each tasks
        (SELECT
        job.jid, task.tid, job.owner, (task.endframe - task.startframe) + 1 AS frames
        FROM
            -- Get the parsed metadata content
            (SELECT
            jid, owner, starttime, metadata->>'renderState' AS type
            FROM 
                -- Get the parsed metadata
                (SELECT 
                jid, owner, starttime, metadata::json AS metadata, (metadata::json->>'scene')::json AS scene 
                FROM job 
                WHERE metadata != '') AS jobData 
            WHERE scene->>'project' != 'TEST_PIPE') AS job, task 
        WHERE 
        job.jid = task.jid AND task.state = 'done' AND type = 'final') AS task, invocation, blade
    WHERE task.jid = invocation.jid AND task.tid = invocation.tid AND blade.bladeid = invocation.bladeid
    ORDER BY task.jid, task.tid) AS computationstat
WHERE index >= 0
GROUP BY index, computer, owner
ORDER BY owner, index