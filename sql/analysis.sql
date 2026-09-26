-- ============================================
-- JobPulse SQL Analytics
-- ============================================


-- 1. Total number of jobs
SELECT
    COUNT(*) AS total_jobs
FROM jobs;


-- 2. Top 10 job locations
SELECT
    location,
    COUNT(*) AS job_count
FROM jobs
WHERE location IS NOT NULL
GROUP BY location
ORDER BY job_count DESC
LIMIT 10;

-- 3. Top 10 companies by number of job postings
SELECT
    company_name,
    COUNT(*) AS job_count
FROM jobs
WHERE company_name IS NOT NULL
GROUP BY company_name
ORDER BY job_count DESC
LIMIT 10;

-- 4. Most common experience requirements
SELECT
    experience,
    COUNT(*) AS job_count
FROM jobs
WHERE experience IS NOT NULL
GROUP BY experience
ORDER BY job_count DESC
LIMIT 10;

-- 5. Average salary by location
SELECT
    location,
    ROUND(AVG(average_salary), 2) AS average_salary,
    COUNT(*) AS job_count
FROM jobs
WHERE average_salary IS NOT NULL
GROUP BY location
HAVING COUNT(*) >= 50
ORDER BY average_salary DESC
LIMIT 10;

-- 6. Remote vs non-remote jobs
SELECT
    CASE
        WHEN LOWER(location) LIKE '%remote%' THEN 'Remote'
        ELSE 'Non-Remote'
    END AS work_type,
    COUNT(*) AS job_count
FROM jobs
GROUP BY work_type
ORDER BY job_count DESC;

-- 7. Job posting status
SELECT
    posting_status,
    COUNT(*) AS job_count
FROM jobs
GROUP BY posting_status
ORDER BY job_count DESC;

-- 8. Jobs by posting age
SELECT
    days_since_posted,
    COUNT(*) AS job_count
FROM jobs
WHERE days_since_posted IS NOT NULL
GROUP BY days_since_posted
ORDER BY days_since_posted
LIMIT 15;