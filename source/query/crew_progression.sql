-- Get only the most recent row for each date(it can be by week, days, or anything), for each teams
SELECT
DISTINCT ON (date, owner)
owner, date, row_number() OVER (PARTITION BY owner ORDER BY starttime, sequence, shot, title, frame) AS done
FROM
    -- Remove the frame that where rendered twice
    (SELECT
    DISTINCT ON (frame, shot, sequence, owner) 
    * 
    FROM
        -- Get the data joined between task and job, and create a row for each frames in the frame ranges
        (SELECT
        job.*, date_trunc('week', job.starttime) AS date, task.tid, task.title, generate_series(task.startframe, task.endframe) AS frame, task.state
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
        job.jid = task.jid AND task.state = 'done' AND type = 'final') AS output
    ORDER BY frame, shot, sequence, owner, starttime) AS output
ORDER BY date, owner, done DESC
