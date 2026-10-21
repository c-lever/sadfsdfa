project_root := justfile_directory()
ip := "127.0.0.1"
port := "5432"

run_db:
    postgres \
        -D "{{project_root}}/.postgres" \
        -k "{{project_root}}/.postgres" \
        -h {{ip}} \
        -p {{port}}

run_app:
    uvicorn app.main:app --reload
