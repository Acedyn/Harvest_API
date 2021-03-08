-- ########################################
-- Returns the frames that has been rendered since last validation for the specified project
--
-- Parameters : :project :last_validation
-- ########################################


    -- SUBQUERY : Get the parsed metadata content and expand the array of frames
    SELECT 
    DISTINCT ON (job_metadata->>'project')
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
    WHERE state = 'done' AND starttime > '2021-01-01 00:00:00'
    AND job_metadata->>'renderState' = 'final' AND job_metadata->>'shot' != '' AND job_metadata->>'seq' != ''
    ORDER BY job_metadata->>'project', starttime, frame
