-- Create login (if not exists)
IF NOT EXISTS (SELECT name FROM sys.server_principals WHERE name = N'oteluser')
BEGIN
    CREATE LOGIN oteluser WITH PASSWORD = 'YourStrong!OtelUserPassw0rd';
END
-- Grant required permissions
GRANT VIEW SERVER STATE TO oteluser;
GRANT VIEW ANY DATABASE TO oteluser;
-- For SQL Server 2022+ only, also:
-- GRANT VIEW SERVER PERFORMANCE STATE TO oteluser;