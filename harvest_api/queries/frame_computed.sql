-- ########################################
-- Returns the amount of frame rendered on the farm
-- ########################################

SELECT
stats.project, SUM(stats.frames)
FROM
    -- SUBQUERY : Get the quantity of frame rendered for each project
    (SELECT
    -- Merge all the rows with the same combinason of jid, tid, project
    DISTINCT ON (metadata.jid, metadata.tid, metadata.project)
    metadata.project, metadata.frames
    FROM
        -- SUBQUERY : Get the parsed metadata content and compute the amount of frames in each task
        (SELECT 
        jid, tid, state,
        -- Select the metadata that we need
        job_metadata->>'project' AS project, job_metadata->>'renderState' AS category,
        -- Get the size of metadata's array of frames
        array_length(string_to_array(regexp_replace(task_metadata->>'frames', '[\[\]\s\.]', '', 'g'), ',', '')::int[], 1) AS frames
        -- Join the subquery to the invocation and the blade table
        FROM
            -- SUBQUERY : Get the parsed metadata
            (SELECT 
            -- Select the metadata from job and task and cast them from string to json
            task.jid, task.tid, job.metadata::json AS job_metadata, task.metadata::json AS task_metadata, task.state
            -- Join the job table and the task table
            FROM job, task 
            -- Ignore the jobs and the task where the metadata can't be converted to json
            -- TODO: Figure out why it doesn't work if we don't put a limit
            WHERE is_valid_json(job.metadata) AND is_valid_json(task.metadata) AND task.jid = job.jid LIMIT 999999999) AS taskData 
        
        -- Get only the task that are done and ignore the task that are from TEST_PIPE
        WHERE state = 'done' AND job_metadata->>'project' != 'TEST_PIPE') AS metadata) AS stats
GROUP BY stats.project
