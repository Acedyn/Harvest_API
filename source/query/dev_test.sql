-- Get the time it took to complete each tasks
SELECT
job.jid, task.tid, job.owner, date_trunc('week', job.starttime) AS date, (task.endframe - task.startframe) + 1 AS frames, task.statetime - task.activetime AS totaltime
FROM
    -- Get the parsed metadata content
    (SELECT
    jid, owner, starttime, metadata->>'renderState' AS type, scene->>'seq' AS sequence, scene->>'shot' AS shot, metadata->>'dcc' AS dcc
    FROM 
        -- Get the parsed metadata
        (SELECT 
        jid, owner, starttime, metadata::json AS metadata, (metadata::json->>'scene')::json AS scene 
        FROM job 
        WHERE metadata != '') AS jobData 
    WHERE scene->>'project' != 'TEST_PIPE') AS job, task 
WHERE 
job.jid = task.jid AND task.state = 'done' AND job.owner = 'FROM_ABOVE'
