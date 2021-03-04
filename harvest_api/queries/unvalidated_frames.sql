-- ########################################
-- Returns the frames that has been rendered since last validation for the specified project
--
-- Parameters : :project :last_validation
-- ########################################


-- SUBQUERY : Remove the frame that where rendered twice
SELECT
-- Merge all the rows with the same combinasion of frame, shot, sequence
DISTINCT ON (frame, shot, sequence) 
project, sequence, shot, frame
FROM

    -- SUBQUERY : Get the parsed metadata content and expand the array of frames
    (SELECT 
    starttime,
    -- Select the metadata that we need
    job_metadata->>'project' AS project, job_metadata->>'seq' AS sequence, job_metadata->>'shot' AS shot, 
    -- Create a raw for each element of the metadata's array of frames
    unnest(string_to_array(regexp_replace(task_metadata->>'frames', '[\[\]\s\.]', '', 'g'), ',', '')::int[]) AS frame
    FROM

        -- SUBQUERY : Get the parsed metadata
        (SELECT 
        -- Select the metadata from job and task and cast them from string to json
        job.starttime, job.metadata::json AS job_metadata, task.metadata::json AS task_metadata, task.state
        -- Join the job table and the task table
        FROM job, task 
        -- Ignore the jobs and the task where the metadata can't be converted to json
        -- TODO: Figure out why it doesn't work if we don't put a limit
        WHERE is_valid_json(job.metadata) AND is_valid_json(task.metadata) AND task.jid = job.jid LIMIT 999999999) AS taskData 

    -- Get only the task that are done and only the one that belong to the given project parameter
    WHERE state = 'done' AND job_metadata->>'project' = :project AND starttime > :last_validation
    -- Get only the jobs marked as 'final' and ignore the job that don't have shot name or sequence (probably simulations)
    AND job_metadata->>'renderState' = 'final' AND job_metadata->>'shot' != '' AND job_metadata->>'seq' != '') AS metadata

ORDER BY sequence, shot, frame