SELECT job.owner, count(*)
FROM task, job
WHERE task.jid = job.jid AND task.state = 'active'
GROUP BY job.owner