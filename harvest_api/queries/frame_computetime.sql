-- ########################################
-- Returns the average time taken to render a frame for each project to each type of blade
-- ########################################

-- SUBQUERY : Get the computation time per frames per blades per project
SELECT
-- Select the average frametime for each computer, project group
computer, project, TRUNC(AVG(frametime)) AS frametime
FROM

    -- SUBQUERY : Get the blade that computed that task and the time per frames
    (SELECT
    -- Merge all the rows with the same combinason of jid, tid, project
    DISTINCT ON (metadata.jid, metadata.tid, metadata.project)
    metadata.project,
    -- Conform the name of the blades with simple regex (real regex : '(?<=-).*(?=-[\d]{4})' but not supported by tractor's psql version)
    substring(upper(blade.name) from 'MK\d') AS computer,
    -- Get the time taken for each job divided by the quantity of frames
    invocation.elapsedreal / metadata.frames AS frametime, invocation.elapsedreal, metadata.frames
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
        WHERE state = 'done' AND job_metadata->>'project' != 'TEST_PIPE' AND job_metadata->>'renderState' = 'final') AS metadata, invocation, blade

    -- Join the subquery to the invocation and the blade table
    WHERE metadata.jid = invocation.jid AND metadata.tid = invocation.tid AND blade.bladeid = invocation.bladeid) AS computationstat

-- Ignore the computer names that did not match the regex
WHERE computer != ''
GROUP BY computer, project
ORDER BY project, computer
