-- Get the final output ordered by starttime
SELECT * 
FROM
    -- Get the data joined between task and job
    (SELECT
    DISTINCT ON (task.title) job.*, task.tid, task.title, task.state
    FROM
        -- Get the parsed metadata content
        (SELECT 
        jid, owner, starttime, metadata->>'renderState' AS type, scene->>'seq' AS sequence, scene->>'shot' AS shot, metadata->>'dcc' AS dcc
        FROM 
            -- Get the parsed metadata
            (SELECT 
            jid, owner, starttime, metadata::json AS metadata, (metadata::json->>'scene')::json AS scene FROM job WHERE metadata != '') AS jobData 
        WHERE scene->>'project' != 'TEST_PIPE') AS job, task 
    WHERE 
    job.jid = task.jid AND task.state = 'done' AND type = 'final'
    ORDER BY
    task.title) AS output
ORDER BY starttime