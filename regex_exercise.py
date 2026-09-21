import re

log_lines = [
    "2024-01-15 10:02:11 INFO Server started on port 8080",
    "2024-01-15 10:03:47 ERROR Failed to connect to database",
    "2024-01-16 08:15:00 WARNING Disk usage at 85%",
    "2024-01-16 14:22:39 ERROR Timeout while fetching https://example.com/api",
    "2024-01-17 09:00:05 INFO User admin logged in from 192.168.1.10",
    "2024-01-17 11:41:18 DEBUG Cache cleared successfully",
    "2024-01-18 03:12:56 ERROR Connection refused from 192.168.1.55",
    "2024-01-18 23:59:02 INFO Backup completed in 42s",
]

print([line for line in log_lines if re.search("2024-01-16", line)])
print([line for line in log_lines if re.search("WARNING|ERROR", line)])
print([line for line in log_lines if re.search("(\d{1,3}\.){3}\d{1,3}", line)])
print([line for line in log_lines if re.search("\d+s$", line)])
print([line for line in log_lines if re.search("http://|https://", line)])


