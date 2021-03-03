-- Get only the most recent row for each date(it can be by week, days, or anything), for each teams
SELECT
DISTINCT ON (date, project)
project, date, row_number() OVER (PARTITION BY project ORDER BY starttime, sequence, shot, frame) AS done
FROM
    -- Remove the frame that where rendered twice
    (SELECT
    DISTINCT ON (frame, shot, sequence, project) 
    *
    FROM
        -- Get the parsed metadata content and expand the array of frames
        (SELECT 
        jid, tid, date_trunc('day', starttime) AS date, starttime, state,
        job_metadata->>'project' AS project, job_metadata->>'renderState' AS category, job_metadata->>'seq' AS sequence, job_metadata->>'shot' AS shot, 
        unnest(string_to_array(regexp_replace(task_metadata->>'frames', '[\[\]\s\.]', '', 'g'), ',', '')::int[]) AS frame
        FROM
            -- Get the parsed metadata
            (SELECT 
                task.jid, task.tid, job.starttime, job.metadata::json AS job_metadata, task.metadata::json AS task_metadata, task.state
                FROM job, task 
                WHERE is_valid_json(job.metadata) AND is_valid_json(task.metadata) AND task.jid = job.jid LIMIT 10000000) AS taskData 
        WHERE state = 'done') AS metadata
    WHERE project != 'TEST_PIPE' AND category = 'final' AND shot != '' AND sequence != '') AS metadata
ORDER BY date, project, done DESC
