@ECHO OFF
IF EXIST backup.sql DEL backup.sql
SET PGPASSWORD=adriana
ECHO Backup Cofetarie
(
    FOR %%t IN (
        "\"django\".\"Cofetarie_ingrediente\""
        "\"django\".\"Cofetarie_locatie\""
        "\"django\".\"Cofetarie_optiuni_decoratiune\""
        "\"django\".\"Cofetarie_optiuni_blat\""
        "\"django\".\"Cofetarie_optiuni_crema\""
        "\"django\".\"Cofetarie_organizator\""
        "\"django\".\"Cofetarie_prajitura\""
        "\"django\".\"Cofetarie_prajitura_ingrediente\""
        "\"django\".\"Cofetarie_tort\""
        "\"django\".\"Cofetarie_tort_ingrediente\""
    ) DO (
        ECHO Backing up %%t ...
        pg_dump --column-inserts --data-only --inserts ^
            -h localhost -U adriana -p 5432 -d cofetarie -t %%t >> backup.sql
    )
)
SET PGPASSWORD=
ECHO Backup finalizat
PAUSE