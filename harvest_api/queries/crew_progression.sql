-- ########################################
-- Returns the number of frames computed for each project every n times (can be days, week...)
-- ########################################

-- SUBQUERY : Get only the most recent row for each date(it can be by week, days, or anything), for each teams
SELECT
-- Merge all the rows with the same combinasion of date and project
DISTINCT ON (date, project)
project, date, row_number() OVER (PARTITION BY project ORDER BY starttime, sequence, shot, frame) AS frames_done
FROM

    -- SUBQUERY : Remove the frame that where rendered twice
    (SELECT
    -- Merge all the rows with the same combinasion of frame, shot, sequence, and project
    DISTINCT ON (frame, shot, sequence, project) 
    *
    FROM

        -- SUBQUERY : Get the parsed metadata content and expand the array of frames
        (SELECT 
        -- Truncate the date to DISTINCT ON date later
        date_trunc('day', starttime) AS date, starttime, state,
        -- Select the metadata that we need
        job_metadata->>'project' AS project, job_metadata->>'renderState' AS category, job_metadata->>'seq' AS sequence, job_metadata->>'shot' AS shot, 
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

        -- Get only the task that are done and ignore the task that are from TEST_PIPE
        WHERE state = 'done' AND job_metadata->>'project' != 'TEST_PIPE') AS metadata

    -- Get only the jobs marked as 'final' and ignore the job that don't have shot name or sequence (probably simulations)
    WHERE category = 'final' AND shot != '' AND sequence != '') AS metadata

-- The order is important because we will walk through the result in the given order later in python
ORDER BY date, project, frames_done DESC
