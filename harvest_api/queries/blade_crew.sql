SELECT job.owner, count(*)
FROM task, blade, job, invocation
WHERE task.jid = invocation.jid AND task.tid = invocation.tid AND task.jid = job.jid AND blade.bladeid = invocation.bladeid AND blade.status = 'no free slots (1)' AND task.state = 'active'
GROUP BY job.owner